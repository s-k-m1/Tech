from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils import timezone
from apps.core.models.notification import Notification


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

        self._push_ws(recipient, notification)
        self._push_ws_tenant(tenant, notification)

        if notification_type == "email":
            from apps.core.tasks.notification_tasks import send_email
            send_email.delay(recipient.email, title, message)

        return notification

    def send_bulk(self, tenant, recipients, notification_type, title, message, data=None):
        notifications = []
        for recipient in recipients:
            n = Notification(
                tenant=tenant,
                recipient=recipient,
                notification_type=notification_type,
                title=title,
                message=message,
                data=data or {},
            )
            notifications.append(n)
            self._push_ws(recipient, n)

        Notification.objects.bulk_create(notifications)

        if notification_type == "email":
            from apps.core.tasks.notification_tasks import send_bulk_email
            emails = [(r.email, title, message) for r in recipients]
            send_bulk_email.delay(emails)

        return notifications

    def send_security_alert(self, tenant, alert):
        channel_layer = get_channel_layer()
        group = f"tenant_{tenant.id}"
        async_to_sync(channel_layer.group_send)(
            group,
            {
                "type": "security_alert",
                "alert": {
                    "title": alert.get("title", "Security Alert"),
                    "message": alert.get("message", ""),
                    "severity": alert.get("severity", "medium"),
                    "timestamp": str(timezone.now()),
                },
            },
        )

    def _push_ws(self, recipient, notification):
        channel_layer = get_channel_layer()
        group = f"user_{recipient.id}"
        async_to_sync(channel_layer.group_send)(
            group,
            {
                "type": "send_notification",
                "notification": {
                    "id": str(notification.id),
                    "title": notification.title,
                    "message": notification.message,
                    "notification_type": notification.notification_type,
                    "is_read": notification.is_read,
                    "created_at": str(notification.sent_at),
                },
            },
        )

    def _push_ws_tenant(self, tenant, notification):
        if not tenant:
            return
        channel_layer = get_channel_layer()
        group = f"tenant_{tenant.id}"
        async_to_sync(channel_layer.group_send)(
            group,
            {
                "type": "send_notification",
                "notification": {
                    "id": str(notification.id),
                    "title": notification.title,
                    "message": notification.message,
                    "notification_type": notification.notification_type,
                    "is_read": notification.is_read,
                    "created_at": str(notification.sent_at),
                },
            },
        )

    def mark_as_read(self, notification_id, user):
        Notification.objects.filter(id=notification_id, recipient=user).update(
            is_read=True, read_at=timezone.now()
        )
