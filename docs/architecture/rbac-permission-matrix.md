# SK Tech - RBAC Permission Matrix

## Role Types

| Role | Scope | Description |
|------|-------|-------------|
| **SuperAdmin** | Global | Cross-tenant system administration |
| **TenantAdmin** | Tenant | Full access within a tenant |
| **Manager** | Branch | Department/branch-level management |
| **Employee** | Self | Self-service access |
| **Client** | Self | Limited client portal access |

## Permission Structure

Permissions are stored as JSON on the `Role` model:

```json
{
  "allowed": ["project.*", "task.*", "ticket.read"],
  "denied": ["settings.*"]
}
```

Pattern: `<resource>.<action>` where action is one of: `create`, `read`, `update`, `delete`, `*` (all).

## Matrix

| Resource | Action | SuperAdmin | TenantAdmin | Manager | Employee | Client |
|----------|--------|:----------:|:-----------:|:-------:|:--------:|:------:|
| **Tenant** | read | ✓ | ✓ | - | - | - |
| | update | ✓ | ✓ | - | - | - |
| **Branch** | read | ✓ | ✓ | ✓ | - | - |
| | create/update/delete | ✓ | ✓ | - | - | - |
| **Department** | read | ✓ | ✓ | ✓ | - | - |
| | create/update/delete | ✓ | ✓ | - | - | - |
| **User** | read | ✓ | ✓ | ✓ | Self | - |
| | create | ✓ | ✓ | - | - | - |
| | update | ✓ | ✓ | ✓ | Self | - |
| | delete | ✓ | ✓ | - | - | - |
| **Role** | * | ✓ | ✓ | - | - | - |
| **Lead** | * | ✓ | ✓ | ✓ | - | - |
| **Client** | * | ✓ | ✓ | ✓ | - | - |
| **Contract** | * | ✓ | ✓ | ✓ | - | - |
| **Meeting** | * | ✓ | ✓ | ✓ | ✓ | - |
| **Employee** | read | ✓ | ✓ | ✓ | Self | - |
| | create/update/delete | ✓ | ✓ | - | - | - |
| **Attendance** | read | ✓ | ✓ | ✓ | Self | - |
| | create/update | ✓ | ✓ | - | Self | - |
| **Leave** | create | ✓ | ✓ | ✓ | ✓ | - |
| | approve/reject | ✓ | ✓ | ✓ | - | - |
| | read all | ✓ | ✓ | ✓ | Self | - |
| **Payroll** | read | ✓ | ✓ | - | Self | - |
| | process | ✓ | ✓ | - | - | - |
| **Project** | * | ✓ | ✓ | ✓ | Assigned | - |
| **Task** | * | ✓ | ✓ | ✓ | Assigned | - |
| **Milestone** | * | ✓ | ✓ | ✓ | - | - |
| **Sprint** | * | ✓ | ✓ | ✓ | - | - |
| **Ticket** | create | ✓ | ✓ | ✓ | ✓ | ✓ |
| | read/update | ✓ | ✓ | ✓ | Assigned | Own |
| | delete | ✓ | ✓ | - | - | - |
| **Product** | * | ✓ | ✓ | ✓ | - | - |
| **Inventory** | read | ✓ | ✓ | ✓ | - | - |
| | adjust | ✓ | ✓ | - | - | - |
| **PurchaseOrder** | * | ✓ | ✓ | ✓ | - | - |
| **Invoice** | * | ✓ | ✓ | ✓ | - | - |
| **Account** | read | ✓ | ✓ | ✓ | - | - |
| | create/update/delete | ✓ | ✓ | - | - | - |
| **JournalEntry** | create | ✓ | ✓ | - | - | - |
| | read | ✓ | ✓ | ✓ | - | - |
| **Transaction** | * | ✓ | ✓ | ✓ | - | - |
| **Budget** | * | ✓ | ✓ | - | - | - |
| **Notification** | read | ✓ | ✓ | ✓ | Self | Self |
| | send | ✓ | ✓ | - | - | - |
| **SecurityEvent** | read | ✓ | ✓ | - | - | - |
| **AuditLog** | read | ✓ | ✓ | - | - | - |
| **Settings** | * | ✓ | ✓ | - | - | - |

## Implementation

The permission check is in `apps/core/permissions/rbac.py`:

```python
class DynamicRBACPermission(BasePermission):
    def has_permission(self, request, view):
        # SuperAdmin bypass
        if request.user.user_type == "superadmin":
            return True

        # Build required permission string
        action = view.action  # create, read, update, delete
        model_name = view.queryset.model.__name__.lower()
        required = f"{model_name}.{action}"

        # Check each user role
        for user_role in request.user.user_roles.all():
            perms = user_role.role.permissions
            if required in perms.get("allowed", []):
                return True
            if required in perms.get("denied", []):
                return False

        return False
```

## Adding New Resources

1. Create the model in `apps/core/models/<domain>.py`
2. Create serializer in `apps/core/serializers/<domain>_serializers.py`
3. Create ViewSet in `apps/core/views/<domain>_views.py` with `DynamicRBACPermission`
4. Add URL route, register in router
5. Update this matrix with the new resource
