import re
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from apps.core.firewall.waf import WAFEngine
from apps.core.firewall.rate_limiter import RateLimiter


class SecurityMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        super().__init__(get_response)
        self.waf = WAFEngine()
        self.rate_limiter = RateLimiter()

    def process_request(self, request):
        client_ip = request.META.get("REMOTE_ADDR", "")

        if self.rate_limiter.is_rate_limited(client_ip, "global", limit=1000, period=60):
            return JsonResponse({"error": "Rate limit exceeded"}, status=429)

        waf_result = self.waf.validate_request(request)
        if not waf_result["allowed"]:
            return JsonResponse(
                {"error": "Request blocked by security firewall", "reason": waf_result["reason"]},
                status=403,
            )

        return None
