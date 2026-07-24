import hashlib
from datetime import timedelta
from django.utils import timezone
from apps.core.models import AuditLog


class LoginRiskAnalyzer:
    def analyze(self, user, request):
        score = 0.0

        ip = request.META.get("REMOTE_ADDR", "")
        user_agent = request.META.get("HTTP_USER_AGENT", "")

        if user.last_login_ip and user.last_login_ip != ip:
            score += 0.2

        now = timezone.now()
        recent_failures = AuditLog.objects.filter(
            user=user,
            action__contains="login_failed",
            created_at__gte=now - timedelta(hours=1),
        ).count()
        score += min(recent_failures * 0.1, 0.3)

        if not user_agent:
            score += 0.1

        suspicious_ips = self._check_suspicious_ip(ip)
        if suspicious_ips:
            score += 0.2

        geo_mismatch = self._check_geo_anomaly(user, ip)
        if geo_mismatch:
            score += 0.2

        return min(score, 1.0)

    def _check_suspicious_ip(self, ip):
        if not ip or ip.startswith("10.") or ip.startswith("192.168.") or ip == "127.0.0.1":
            return False
        high_risk_providers = ["tor-exit", "vpn", "proxy", "datacenter"]
        recent = AuditLog.objects.filter(
            action__contains="login_failed",
            ip_address=ip,
            created_at__gte=timezone.now() - timedelta(hours=24),
        ).count()
        return recent >= 5

    def _check_geo_anomaly(self, user, ip):
        if not user.last_login_ip or not ip:
            return False
        recent_ips = AuditLog.objects.filter(
            user=user,
            action__in=["login_success", "login_failed"],
        ).values_list("ip_address", flat=True).distinct()[:5]
        if recent_ips and ip not in recent_ips:
            return True
        return False
