from apps.core.models import AuditLog
from django.utils import timezone
from datetime import timedelta


class SecurityAIService:
    def get_dashboard_data(self, tenant):
        now = timezone.now()
        last_24h = now - timedelta(hours=24)

        logs = AuditLog.objects.filter(tenant=tenant, created_at__gte=last_24h)

        return {
            "total_events": logs.count(),
            "critical_events": logs.filter(risk_level="critical").count(),
            "high_risk_events": logs.filter(risk_level="high").count(),
            "events_by_action": self._count_by_field(logs, "action"),
            "events_by_hour": self._events_by_hour(logs),
        }

    def generate_report(self, tenant):
        now = timezone.now()
        last_7d = now - timedelta(days=7)

        logs = AuditLog.objects.filter(tenant=tenant, created_at__gte=last_7d)

        return {
            "period": "7d",
            "total_events": logs.count(),
            "risk_breakdown": self._count_by_field(logs, "risk_level"),
            "action_breakdown": self._count_by_field(logs, "action"),
            "recommendations": self._generate_recommendations(logs),
        }

    def _count_by_field(self, queryset, field):
        counts = {}
        for item in queryset.values(field).distinct():
            counts[item[field]] = queryset.filter(**{field: item[field]}).count()
        return counts

    def _events_by_hour(self, queryset):
        from django.db.models import Count
        from django.db.models.functions import TruncHour

        return list(
            queryset.annotate(hour=TruncHour("created_at"))
            .values("hour")
            .annotate(count=Count("id"))
            .order_by("hour")
        )

    def _generate_recommendations(self, logs):
        recommendations = []
        critical_count = logs.filter(risk_level="critical").count()
        if critical_count > 10:
            recommendations.append(
                "Critical security events detected. Review and strengthen firewall rules."
            )
        failed_logins = logs.filter(action__contains="login_failed").count()
        if failed_logins > 20:
            recommendations.append(
                "Multiple failed login attempts detected. Consider implementing additional rate limiting."
            )
        return recommendations
