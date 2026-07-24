import re
from django.utils.deprecation import MiddlewareMixin
from apps.core.models import Tenant


class TenantMiddleware(MiddlewareMixin):
    def process_request(self, request):
        host = request.get_host().split(":")[0]

        if host in ["localhost", "127.0.0.1"] or host.startswith("192.168."):
            return

        tenant = Tenant.objects.filter(domain=host).first()
        if tenant:
            request.tenant = tenant
        else:
            request.tenant = None
