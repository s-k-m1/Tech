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
        return False

    def _check_geo_anomaly(self, user, ip):
        return False
