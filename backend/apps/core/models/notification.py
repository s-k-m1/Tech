from django.db import models
from django.utils.translation import gettext_lazy as _
from .account import BaseModel, Tenant, User


class Notification(BaseModel):
    NOTIFICATION_TYPE = (
        ("email", "Email"),
        ("push", "Push"),
        ("browser", "Browser"),
        ("sms", "SMS"),
        ("in_app", "In-App"),
    )

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True, blank=True, related_name="notifications")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE, default="in_app")
    title = models.CharField(max_length=255)
    message = models.TextField()
    data = models.JSONField(default=dict, blank=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")
        ordering = ["-sent_at"]


class NotificationTemplate(BaseModel):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True, blank=True, related_name="notification_templates")
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    variables = models.JSONField(default=list, blank=True)
    channels = models.JSONField(default=list, blank=True)

    class Meta:
        verbose_name = _("Notification Template")
        verbose_name_plural = _("Notification Templates")
