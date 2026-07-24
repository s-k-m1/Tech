# SK Tech - Redis Architecture

## Overview

Redis serves as the central data layer for caching, session storage, message queuing, rate limiting, and WebSocket communication.

```
                    ┌──────────────────────────────────────┐
                    │              Redis 7                 │
                    │                                      │
    ┌───────────────┼──────────────────────────────────────┼───────────────┐
    │               │                                      │               │
    ▼               ▼                                      ▼               ▼
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│ DB 0     │  │ DB 1     │  │ DB 2     │  │ DB 3     │  │ DB 4+    │  │ Celery   │
│ Celery   │  │ Cache    │  │ Channels │  │ Sessions │  │ Rate     │  │ Result   │
│ Broker   │  │ (default)│  │ (WS)     │  │          │  │ Limits   │  │ Backend  │
└──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘
```

## Database Assignments

| DB # | Purpose | Key Pattern | TTL |
|------|---------|-------------|-----|
| 0 | Celery message broker | `celery-task-meta-*`, `unacked-*` | N/A (Celery managed) |
| 1 | Django cache (default) | `:1:django_cache_*` | Varies by cache call |
| 2 | Channels WebSocket layer | `asgi:channel:*`, `asgi:group:*` | N/A |
| 3 | Django sessions | `django.contrib.sessions.cache*` | Session expiry |
| 4 | Rate limiting counters | `ratelimit:*` | Per-window period |
| 5+ | Future use | — | — |

## Usage by Component

### 1. Session Cache (DB 3)

```python
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
```

- All user sessions stored in Redis (not database)
- Enables horizontal scaling (no server-local sessions)
- Session expiry matches JWT refresh token lifetime (7 days)

### 2. API Response Cache (DB 1)

Used for caching expensive/dashboard queries:

```
Cache key: dashboard_stats:{tenant_id}
TTL: 300 seconds (5 minutes)
Invalidation: On data mutation via cache.delete()
```

### 3. Celery Broker (DB 0)

- All async tasks routed through Redis
- Task queues: `celery`, `email`, `notifications`, `security`, `backups`
- Priority routing via separate queues

### 4. Rate Limiting (DB 4)

```python
class RateLimiter:
    def is_rate_limited(self, key, action, limit, period):
        cache_key = f"ratelimit:{action}:{key}"
        timestamps = cache.get(cache_key, [])
        # Filter timestamps within window
        timestamps = [t for t in timestamps if t > now - period]
        if len(timestamps) >= limit:
            return True
        timestamps.append(now)
        cache.set(cache_key, timestamps, timeout=period)
```

Scopes: `global`, `login`, `register`, `otp_verify`, `password_reset`

### 5. WebSocket Channel Layer (DB 2)

```python
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis", 6379)],
        },
    },
}
```

- Real-time notification delivery across multiple backend instances
- Symmetric encryption for channel data
- Group-based routing: `user_{id}`, `tenant_{id}`

### 6. Distributed Locks

Used for:
- Celery beat task deduplication
- Concurrent inventory adjustments
- Payroll processing (prevent double-run)

```
Lock pattern: SET lock:{resource} 1 EX 30 NX
Release: DEL lock:{resource}
```

## Performance

- Connection pooling via `django-redis` with Hiredis parser
- `CONN_MAX_AGE = 60` for persistent connections
- `PARSER_CLASS = redis.connection.HiredisParser` (C-based parser, ~10x faster)

## Monitoring

Redis metrics exported via `django-prometheus`:
- `redis_commands_total` — Command rate
- `redis_keyspace_hits_total` / `redis_keyspace_misses_total` — Hit ratio
- `redis_memory_usage_bytes` — Memory pressure
- `redis_connected_clients` — Connection count

## Failure Mode

If Redis goes down:
- Session cache falls back to database (if `SESSION_ENGINE` configured)
- Celery tasks queue in memory (potential loss on broker restart)
- Rate limiting resets (allows burst traffic)
- WebSocket disconnect (reconnect on recovery)
