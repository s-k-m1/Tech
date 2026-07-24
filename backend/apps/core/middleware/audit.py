from django.utils.deprecation import MiddlewareMixin
from apps.core.models import AuditLog


class AuditLogMiddleware(MiddlewareMixin):
    SAFE_METHODS = ["GET", "HEAD", "OPTIONS"]

    def process_response(self, request, response):
        if request.method in self.SAFE_METHODS:
            return response

        if not request.user or not request.user.is_authenticated:
            return response

        if request.path.startswith("/admin/"):
            return response

        AuditLog.objects.create(
            tenant=getattr(request, "tenant", None) or getattr(request.user, "tenant", None),
            user=request.user,
            action=f"{request.method.lower()}_{request.resolver_match.view_name}" if request.resolver_match else request.method.lower(),
            resource=request.path,
            details={
                "method": request.method,
                "path": request.path,
                "query_params": dict(request.GET),
                "status_code": response.status_code,
            },
            ip_address=request.META.get("REMOTE_ADDR", ""),
            user_agent=request.META.get("HTTP_USER_AGENT", "")[:500],
        )

        return response
