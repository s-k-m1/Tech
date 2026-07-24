from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from apps.core.firewall.waf import WAFEngine
from apps.core.firewall.rate_limiter import RateLimiter
from apps.core.models.security import IPBlacklist, SecurityEvent
from apps.core.metrics import (
    security_events_total, threats_blocked_total,
    blacklisted_ips_active, rate_limit_exceeded_total,
)


class SecurityMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        super().__init__(get_response)
        self.waf = WAFEngine()
        self.rate_limiter = RateLimiter()

    def process_request(self, request):
        client_ip = request.META.get("REMOTE_ADDR", "")

        if not client_ip:
            return None

        if self._is_blacklisted(client_ip):
            return JsonResponse(
                {"error": "Your IP has been blocked due to suspicious activity"},
                status=403,
            )

        if self.rate_limiter.is_rate_limited(client_ip, "global", limit=1000, period=60):
            rate_limit_exceeded_total.inc()
            SecurityEvent.objects.create(
                event_type="rate_limit_exceeded",
                severity="medium",
                source_ip=client_ip,
                description=f"Global rate limit exceeded from {client_ip}",
            )
            return JsonResponse({"error": "Rate limit exceeded"}, status=429)

        waf_result = self.waf.validate_request(request)
        if not waf_result["allowed"]:
            attack_type = waf_result.get("attack_type", "unknown")
            security_events_total.labels(event_type=f"waf_blocked_{attack_type}", severity="high").inc()
            threats_blocked_total.labels(attack_type=attack_type).inc()

            SecurityEvent.objects.create(
                event_type=f"waf_blocked_{attack_type}",
                severity="high",
                source_ip=client_ip,
                description=waf_result["reason"],
                metadata={"attack_type": attack_type},
            )
            self._auto_block_if_needed(client_ip, waf_result["reason"])
            blacklisted_ips_active.set_function(self._count_active_blacklist)
            return JsonResponse(
                {"error": "Request blocked by security firewall", "reason": waf_result["reason"]},
                status=403,
            )

        return None

    def _is_blacklisted(self, ip):
        return IPBlacklist.objects.filter(
            ip_address=ip,
            is_active=True,
        ).exclude(
            expires_at__lt=timezone.now()
        ).exists()

    def _count_active_blacklist(self):
        return IPBlacklist.objects.filter(is_active=True).exclude(
            expires_at__lt=timezone.now()
        ).count()

    def _auto_block_if_needed(self, ip, reason):
        recent_critical = SecurityEvent.objects.filter(
            source_ip=ip,
            severity__in=["high", "critical"],
            created_at__gte=timezone.now() - timedelta(hours=1),
        ).count()

        if recent_critical >= 5:
            blacklist, created = IPBlacklist.objects.get_or_create(
                ip_address=ip,
                defaults={
                    "reason": f"Auto-blocked: {recent_critical} critical events in 1 hour",
                    "blocked_by": "auto",
                    "expires_at": timezone.now() + timedelta(hours=24),
                    "attack_count": recent_critical,
                },
            )
            if not created:
                blacklist.attack_count = recent_critical
                blacklist.is_active = True
                blacklist.save(update_fields=["attack_count", "is_active"])
