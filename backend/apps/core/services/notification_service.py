from apps.core.models.notification import Notification
from django.utils import timezone


class NotificationService:
    def send(self, tenant, recipient, notification_type, title, message, data=None):
        notification = Notification.objects.create(
            tenant=tenant,
            recipient=recipient,
            notification_type=notification_type,
            title=title,
            message=message,
            data=data or {},
        )

        if notification_type == "email":
            from apps.core.tasks.notification_tasks import send_email
            send_email.delay(
                recipient.email,
                title,
                message,
            )

        return notification

    def send_bulk(self, tenant, recipients, notification_type, title, message, data=None):
        notifications = []
        for recipient in recipients:
            notifications.append(
                Notification(
                    tenant=tenant,
                    recipient=recipient,
                    notification_type=notification_type,
                    title=title,
                    message=message,
                    data=data or {},
                )
            )
        Notification.objects.bulk_create(notifications)

        if notification_type == "email":
            from apps.core.tasks.notification_tasks import send_bulk_email
            emails = [(r.email, title, message) for r in recipients]
            send_bulk_email.delay(emails)

        return notifications

    def mark_as_read(self, notification_id, user):
        Notification.objects.filter(id=notification_id, recipient=user).update(
            is_read=True, read_at=timezone.now()
        )
