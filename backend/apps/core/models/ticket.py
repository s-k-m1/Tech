from django.db import models
from django.utils.translation import gettext_lazy as _
from .account import BaseModel, Tenant, User


class Ticket(BaseModel):
    TICKET_STATUS = (
        ("open", "Open"),
        ("in_progress", "In Progress"),
        ("resolved", "Resolved"),
        ("closed", "Closed"),
    )

    TICKET_PRIORITY = (
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("critical", "Critical"),
    )

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="tickets")
    subject = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=TICKET_STATUS, default="open")
    priority = models.CharField(max_length=20, choices=TICKET_PRIORITY, default="medium")
    category = models.CharField(max_length=100, blank=True)
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requested_tickets")
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_tickets")
    due_date = models.DateTimeField(null=True, blank=True)
    attachments = models.JSONField(default=list, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _("Ticket")
        verbose_name_plural = _("Tickets")


class TicketComment(BaseModel):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    attachments = models.JSONField(default=list, blank=True)
    is_internal = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Ticket Comment")
        verbose_name_plural = _("Ticket Comments")
