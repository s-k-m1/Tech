from datetime import timedelta
from django.utils import timezone
from apps.core.models import AuditLog


class AnomalyDetector:
    def detect(self, tenant):
        now = timezone.now()
        last_1h = now - timedelta(hours=1)

        anomalies = []

        rapid_requests = AuditLog.objects.filter(
            tenant=tenant,
            created_at__gte=last_1h,
        ).count()

        if rapid_requests > 1000:
            anomalies.append({
                "type": "traffic_spike",
                "severity": "high",
                "message": f"Rapid request rate detected: {rapid_requests} requests in last hour",
            })

        failed_logins = AuditLog.objects.filter(
            tenant=tenant,
            action__contains="login_failed",
            created_at__gte=last_1h,
        ).count()

        if failed_logins > 10:
            anomalies.append({
                "type": "brute_force",
                "severity": "critical",
                "message": f"Possible brute force attack: {failed_logins} failed logins",
            })

        return anomalies
