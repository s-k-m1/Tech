from celery import shared_task
from apps.core.ai.anomaly_detector import AnomalyDetector
from apps.core.models import Tenant
from apps.core.services.notification_service import NotificationService


@shared_task
def run_security_scan():
    detector = AnomalyDetector()
    notifier = NotificationService()

    for tenant in Tenant.objects.filter(is_active=True):
        anomalies = detector.detect(tenant)
        if anomalies:
            for admin in tenant.users.filter(user_type="tenant_admin"):
                notifier.send(
                    tenant=tenant,
                    recipient=admin,
                    notification_type="email",
                    title="Security Alert",
                    message=f"Security anomalies detected: {len(anomalies)} issues found.",
                    data={"anomalies": anomalies},
                )


@shared_task
def analyze_login_attempt(user_id, request_data):
    from apps.core.ai.login_risk_analyzer import LoginRiskAnalyzer
    from apps.core.models import User

    user = User.objects.get(id=user_id)
    analyzer = LoginRiskAnalyzer()
    risk_score = analyzer.analyze(user, request_data)

    user.risk_score = risk_score
    user.save(update_fields=["risk_score"])

    return risk_score
