from prometheus_client import Counter, Gauge, Histogram

security_events_total = Counter(
    "django_security_events_total",
    "Total security events by type and severity",
    ["event_type", "severity"],
)

threats_blocked_total = Counter(
    "django_security_threats_total",
    "Total threats blocked by attack type",
    ["attack_type"],
)

blacklisted_ips_active = Gauge(
    "django_blacklisted_ips_active",
    "Currently active blacklisted IPs",
)

rate_limit_exceeded_total = Counter(
    "django_rate_limit_exceeded_total",
    "Total rate limit exceeded events",
)

active_users_total = Gauge(
    "django_active_users_total",
    "Currently active users",
)

celery_queue_length = Gauge(
    "celery_queue_length",
    "Celery queue length by queue name",
    ["queue"],
)
