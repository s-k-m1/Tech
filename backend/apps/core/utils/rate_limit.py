from functools import wraps
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import status


def rate_limit(key, limit=100, period=60):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(self, request, *args, **kwargs):
            client_ip = request.META.get("REMOTE_ADDR", "unknown")
            cache_key = f"ratelimit:{key}:{client_ip}"

            count = cache.get(cache_key, 0)
            if count >= limit:
                return Response(
                    {"error": "Rate limit exceeded. Try again later."},
                    status=status.HTTP_429_TOO_MANY_REQUESTS,
                )

            cache.set(cache_key, count + 1, timeout=period)
            return view_func(self, request, *args, **kwargs)
        return wrapper
    return decorator
