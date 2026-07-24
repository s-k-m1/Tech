from django.db import models
from django.utils.translation import gettext_lazy as _
from .account import BaseModel, Tenant, User


class Lead(BaseModel):
    LEAD_STATUS = (
        ("new", "New"),
        ("contacted", "Contacted"),
        ("qualified", "Qualified"),
        ("converted", "Converted"),
        ("lost", "Lost"),
    )

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="leads")
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=255, blank=True)
    source = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=20, choices=LEAD_STATUS, default="new")
    score = models.IntegerField(default=0)
    notes = models.TextField(blank=True)
    converted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _("Lead")
        verbose_name_plural = _("Leads")


class Client(BaseModel):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="clients")
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    company_name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    website = models.URLField(blank=True)
    industry = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = _("Client")
        verbose_name_plural = _("Clients")


class Contract(BaseModel):
    CONTRACT_STATUS = (
        ("draft", "Draft"),
        ("active", "Active"),
        ("expired", "Expired"),
        ("terminated", "Terminated"),
    )

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="contracts")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="contracts")
    title = models.CharField(max_length=255)
    content = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    value = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=CONTRACT_STATUS, default="draft")
    file = models.FileField(upload_to="contracts/", blank=True)

    class Meta:
        verbose_name = _("Contract")
        verbose_name_plural = _("Contracts")


class Meeting(BaseModel):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="meetings")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="meetings")
    title = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    meeting_date = models.DateTimeField()
    duration_minutes = models.IntegerField(default=30)
    meeting_link = models.URLField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    attendees = models.ManyToManyField(User, blank=True)

    class Meta:
        verbose_name = _("Meeting")
        verbose_name_plural = _("Meetings")
