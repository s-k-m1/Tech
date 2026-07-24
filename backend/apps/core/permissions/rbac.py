from rest_framework.permissions import BasePermission


class DynamicRBACPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.user_type == "superadmin":
            return True

        if not request.user.tenant:
            return False

        if not hasattr(view, "permission_map"):
            return True

        action = view.action
        model_name = getattr(view, "model_name", view.queryset.model.__name__.lower() if hasattr(view, "queryset") else None)

        if not model_name:
            return True

        required_permission = f"{model_name}.{action}"

        user_roles = request.user.user_roles.select_related("role").all()
        for user_role in user_roles:
            permissions = user_role.role.permissions
            if required_permission in permissions.get("allowed", []):
                return True
            if required_permission in permissions.get("denied", []):
                return False

        return False

    def has_object_permission(self, request, view, obj):
        if request.user.user_type == "superadmin":
            return True
        if hasattr(obj, "tenant") and obj.tenant != request.user.tenant:
            return False
        return True


class IsTenantAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type in ["superadmin", "tenant_admin"]


class IsBranchManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type in [
            "superadmin", "tenant_admin", "manager"
        ]
