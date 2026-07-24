import time
from collections import defaultdict
from django.core.cache import cache


class RateLimiter:
    def __init__(self):
        self.store = defaultdict(list)

    def is_rate_limited(self, key, action, limit=100, period=60):
        cache_key = f"ratelimit:{action}:{key}"
        now = time.time()

        timestamps = cache.get(cache_key, [])
        timestamps = [t for t in timestamps if t > now - period]

        if len(timestamps) >= limit:
            return True

        timestamps.append(now)
        cache.set(cache_key, timestamps, timeout=period)
        return False

    def get_remaining(self, key, action, limit=100, period=60):
        cache_key = f"ratelimit:{action}:{key}"
        now = time.time()

        timestamps = cache.get(cache_key, [])
        timestamps = [t for t in timestamps if t > now - period]

        return max(0, limit - len(timestamps))
