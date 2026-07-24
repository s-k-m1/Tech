from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from apps.core.models import Device, Session, AuditLog
from apps.core.services.security_ai_service import SecurityAIService
from apps.core.ai.login_risk_analyzer import LoginRiskAnalyzer
import pyotp
import random


class AuthService:
    def login(self, user, request, device_data):
        risk_analyzer = LoginRiskAnalyzer()
        risk_score = risk_analyzer.analyze(user, request)

        if risk_score > 0.7:
            AuditLog.objects.create(
                tenant=user.tenant,
                user=user,
                action="login_blocked_high_risk",
                resource="auth",
                details={"risk_score": risk_score, "ip": request.META.get("REMOTE_ADDR")},
                risk_level="critical",
            )
            return {"error": "Login blocked due to security risk", "blocked": True}

        device, _ = Device.objects.get_or_create(
            user=user,
            device_name=device_data.get("device_name", "Unknown"),
            defaults={
                "device_type": device_data.get("device_type", "web"),
                "ip_address": device_data.get("ip_address", ""),
                "user_agent": device_data.get("user_agent", ""),
            },
        )

        if user.is_2fa_enabled or risk_score > 0.4:
            otp_secret = pyotp.random_base32()
            otp = pyotp.TOTP(otp_secret).now()
            request.session["otp_secret"] = otp_secret
            request.session["pending_user_id"] = str(user.id)
            request.session["pending_device_id"] = str(device.id)

            from apps.core.tasks.notification_tasks import send_otp_email
            send_otp_email.delay(user.email, otp)

            return {
                "requires_2fa": True,
                "token": request.session.session_key,
                "message": "OTP sent to your email",
            }

        return self._complete_login(user, device, request)

    def verify_otp(self, token, otp, request):
        stored_secret = request.session.get("otp_secret")
        if not stored_secret:
            return {"error": "OTP session expired"}, 400

        totp = pyotp.TOTP(stored_secret)
        if not totp.verify(otp):
            return {"error": "Invalid OTP"}, 400

        user_id = request.session.get("pending_user_id")
        device_id = request.session.get("pending_device_id")

        from apps.core.models import User, Device
        user = User.objects.get(id=user_id)
        device = Device.objects.get(id=device_id)

        del request.session["otp_secret"]
        del request.session["pending_user_id"]
        del request.session["pending_device_id"]

        return self._complete_login(user, device, request)

    def _complete_login(self, user, device, request):
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        session = Session.objects.create(
            user=user,
            device=device,
            token=access_token,
            refresh_token=refresh_token,
            ip_address=request.META.get("REMOTE_ADDR", ""),
            expires_at=timezone.now() + timezone.timedelta(days=7),
        )

        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])

        AuditLog.objects.create(
            tenant=user.tenant,
            user=user,
            action="login_success",
            resource="auth",
            details={"device": device.device_name, "ip": request.META.get("REMOTE_ADDR")},
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "id": str(user.id),
                "email": user.email,
                "username": user.username,
                "user_type": user.user_type,
                "tenant_id": str(user.tenant.id) if user.tenant else None,
            },
        }

    def logout(self, user, request):
        Session.objects.filter(user=user, is_active=True).update(is_active=False)
        AuditLog.objects.create(
            tenant=user.tenant,
            user=user,
            action="logout",
            resource="auth",
        )
