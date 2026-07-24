from django.db import models
from django.utils import timezone
from datetime import timedelta
from .account import BaseModel, Tenant


class IPBlacklist(BaseModel):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True, blank=True, related_name="blacklisted_ips")
    ip_address = models.GenericIPAddressField(db_index=True)
    reason = models.CharField(max_length=255)
    blocked_by = models.CharField(max_length=100, default="auto")
    blocked_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    attack_count = models.IntegerField(default=0)

    class Meta:
        verbose_name = "IP Blacklist"
        verbose_name_plural = "IP Blacklist"
        indexes = [
            models.Index(fields=["ip_address", "is_active"]),
            models.Index(fields=["tenant", "ip_address"]),
        ]

    def __str__(self):
        return f"{self.ip_address} - {self.reason}"

    @property
    def is_expired(self):
        if self.expires_at and timezone.now() > self.expires_at:
            return True
        return False


class SecurityEvent(BaseModel):
    SEVERITY_LEVELS = (
        ("info", "Info"),
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("critical", "Critical"),
    )

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True, blank=True, related_name="security_events")
    event_type = models.CharField(max_length=100, db_index=True)
    severity = models.CharField(max_length=20, choices=SEVERITY_LEVELS, default="info")
    source_ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    description = models.TextField()
    metadata = models.JSONField(default=dict, blank=True)
    is_automated_block = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Security Event"
        verbose_name_plural = "Security Events"
        indexes = [
            models.Index(fields=["tenant", "severity"]),
            models.Index(fields=["event_type"]),
            models.Index(fields=["created_at"]),
        ]
        ordering = ["-created_at"]
