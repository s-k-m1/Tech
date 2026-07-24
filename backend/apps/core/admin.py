from django.contrib import admin
from apps.core.models import (
    Tenant, Branch, Department, User, Role, UserRole, Device, Session, AuditLog,
    Lead, Client, Contract, Meeting,
    Employee, Attendance, Leave, Payroll,
    Project, Milestone, Sprint, Task, TaskComment,
    Ticket, TicketComment,
    Notification, NotificationTemplate,
    Supplier, Warehouse, Category, Product, Inventory, PurchaseOrder, PurchaseOrderItem, Invoice, InvoiceItem,
    AccountType, Account, JournalEntry, JournalLineItem, Transaction, Budget, BudgetLineItem,
    IPBlacklist, SecurityEvent,
)


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "subscription_plan", "is_active"]
    search_fields = ["name", "slug"]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["email", "username", "user_type", "tenant", "is_verified", "is_active"]
    list_filter = ["user_type", "is_verified", "is_active"]
    search_fields = ["email", "username"]


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "tenant", "is_system"]
    list_filter = ["is_system"]


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ["action", "user", "tenant", "risk_level", "created_at"]
    list_filter = ["action", "risk_level"]
    readonly_fields = ["created_at"]


@admin.register(SecurityEvent)
class SecurityEventAdmin(admin.ModelAdmin):
    list_display = ["event_type", "severity", "ip_address", "created_at"]
    list_filter = ["event_type", "severity"]


@admin.register(IPBlacklist)
class IPBlacklistAdmin(admin.ModelAdmin):
    list_display = ["ip_address", "reason", "is_permanent", "expires_at", "created_at"]


for model in [Branch, Department, UserRole, Device, Session,
              Lead, Client, Contract, Meeting,
              Employee, Attendance, Leave, Payroll,
              Project, Milestone, Sprint, Task, TaskComment,
              Ticket, TicketComment,
              Notification, NotificationTemplate,
              Supplier, Warehouse, Category, Product, Inventory,
              PurchaseOrder, PurchaseOrderItem, Invoice, InvoiceItem,
              AccountType, Account, JournalEntry, JournalLineItem, Transaction, Budget, BudgetLineItem]:
    admin.site.register(model)
