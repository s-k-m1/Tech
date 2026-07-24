from rest_framework.permissions import BasePermission, SAFE_METHODS


class DynamicRBACPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.user_type == "superadmin":
            return True
        if request.method in SAFE_METHODS:
            return True
        return request.user.user_type in ("tenant_admin", "manager")

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.user_type == "superadmin":
            return True
        tenant = getattr(obj, "tenant", None)
        if tenant and request.user.tenant != tenant:
            return False
        if request.method in SAFE_METHODS:
            return True
        return request.user.user_type in ("tenant_admin", "manager")
