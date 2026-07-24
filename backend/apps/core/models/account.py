import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class Tenant(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    domain = models.CharField(max_length=255, blank=True)
    logo = models.ImageField(upload_to="tenants/logos/", blank=True)
    contact_email = models.EmailField()
    subscription_plan = models.CharField(max_length=50, default="free")
    settings = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name = _("Tenant")
        verbose_name_plural = _("Tenants")

    def __str__(self):
        return self.name


class Branch(BaseModel):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="branches")
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    is_head_office = models.BooleanField(default=False)

    class Meta:
        unique_together = ["tenant", "code"]
        verbose_name = _("Branch")
        verbose_name_plural = _("Branches")

    def __str__(self):
        return f"{self.tenant.name} - {self.name}"


class Department(BaseModel):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="departments")
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="departments")
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ["tenant", "code"]

    def __str__(self):
        return f"{self.branch.name} - {self.name}"


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ("superadmin", "Super Admin"),
        ("tenant_admin", "Tenant Admin"),
        ("manager", "Manager"),
        ("employee", "Employee"),
        ("client", "Client"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True, blank=True, related_name="users")
    branches = models.ManyToManyField(Branch, blank=True, related_name="users")
    departments = models.ManyToManyField(Department, blank=True, related_name="users")
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default="employee")
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to="users/avatars/", blank=True)
    is_verified = models.BooleanField(default=False)
    is_2fa_enabled = models.BooleanField(default=False)
    last_login_ip = models.GenericIPAddressField(blank=True, null=True)
    risk_score = models.FloatField(default=0.0)

    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.email


class Role(BaseModel):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True, blank=True, related_name="roles")
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    permissions = models.JSONField(default=dict, blank=True)
    is_system = models.BooleanField(default=False)

    class Meta:
        unique_together = ["tenant", "slug"]

    def __str__(self):
        return self.name


class UserRole(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_roles")
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="user_roles")
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = ["user", "role", "branch"]


class Device(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="devices")
    device_name = models.CharField(max_length=255)
    device_type = models.CharField(max_length=50)
    os = models.CharField(max_length=100, blank=True)
    browser = models.CharField(max_length=100, blank=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    is_trusted = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now=True)
    push_token = models.TextField(blank=True)

    class Meta:
        verbose_name = _("Device")
        verbose_name_plural = _("Devices")


class Session(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sessions")
    device = models.ForeignKey(Device, on_delete=models.CASCADE, null=True, blank=True)
    token = models.TextField()
    refresh_token = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField()
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField()
    last_activity = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Session")
        verbose_name_plural = _("Sessions")


class AuditLog(BaseModel):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255)
    resource = models.CharField(max_length=100)
    resource_id = models.CharField(max_length=255, blank=True)
    details = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    risk_level = models.CharField(max_length=20, default="low")

    class Meta:
        verbose_name = _("Audit Log")
        verbose_name_plural = _("Audit Logs")
        indexes = [
            models.Index(fields=["tenant", "action"]),
            models.Index(fields=["tenant", "user"]),
            models.Index(fields=["created_at"]),
        ]
