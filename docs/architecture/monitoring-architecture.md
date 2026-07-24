# SK Tech - Monitoring Architecture

## Overview

```
┌──────────┐    ┌─────────────┐    ┌──────────┐
│ Backend  │───>│ Prometheus  │───>│ Grafana  │
│ /metrics │    │ scrape      │    │ dashboards│
└──────────┘    └─────────────┘    └──────────┘
       │               │                  │
       │               ▼                  ▼
       │        ┌─────────────┐    ┌──────────┐
       │        │ Alertmanager│───>│ Slack/   │
       │        │ (future)    │    │ Email    │
       │        └─────────────┘    └──────────┘
       ▼
┌──────────┐
│ Logging  │
│ (file)   │
└──────────┘
```

## Metrics Export

**Endpoint:** `GET /metrics` (served by `django-prometheus`)

### Django Metrics (auto-collected)

| Metric | Type | Labels | Description |
|--------|------|--------|-------------|
| `django_http_requests_total` | Counter | method, view, status | Total HTTP requests |
| `django_http_requests_duration_seconds` | Histogram | method, view, status | Request latency |
| `django_http_responses_total_by_status` | Counter | status | Responses by status code |
| `django_db_connections` | Gauge | — | Active DB connections |
| `django_cache_get_total` | Counter | — | Cache get operations |
| `django_cache_miss_total` | Counter | — | Cache misses |

### Custom Metrics (from `apps/core/metrics.py`)

| Metric | Type | Labels | Description |
|--------|------|--------|-------------|
| `django_security_events_total` | Counter | event_type, severity | Security events |
| `django_security_threats_total` | Counter | attack_type | Threats blocked by WAF |
| `django_blacklisted_ips_active` | Gauge | — | Currently blacklisted IPs |
| `django_rate_limit_exceeded_total` | Counter | — | Rate limit hits |
| `django_active_users_total` | Gauge | — | Active user sessions |
| `celery_queue_length` | Gauge | queue | Celery queue depth |

## Grafana Dashboards

Three pre-built dashboards (auto-provisioned):

### 1. System Overview (`sk-tech-system`)
- HTTP requests/second (rate)
- Request duration p95
- Active DB connections
- Redis operations/second
- Celery queue length

### 2. Security Events (`sk-tech-security`)
- Blocked threats by type (pie)
- Security events over time by severity
- Active IP blacklist count (stat)
- Rate limit exceeded rate

### 3. Business Metrics (`sk-tech-business`)
- Active users per tenant
- Top 10 API endpoints by call volume
- Error rate by status code (4xx, 5xx)

## Prometheus Configuration

```yaml
scrape_interval: 15s
evaluation_interval: 15s

scrape_configs:
  - job_name: 'backend'      # Django /metrics endpoint
    targets: ['backend:8000']
  - job_name: 'postgres'     # PostgreSQL exporter
    targets: ['postgres:9187']
  - job_name: 'redis'        # Redis exporter
    targets: ['redis:9121']
  - job_name: 'celery'       # Celery exporter
    targets: ['celery:9800']
```

## Health Checks

| Endpoint | Type | Checks | Expected Status |
|----------|------|--------|-----------------|
| `GET /health/` | Liveness | None (always returns 200) | 200 OK |
| `GET /ready/` | Readiness | DB connection, Redis ping, Celery stats | 200 OK or 503 |

## Logging

Production logging configuration (`settings/prod.py`):
- Console logger (stdout — collected by Docker)
- File logger (rotating, 10MB per file, 10 backups)
- Log level: INFO
- Location: `backend/logs/django.log`

## Alerting (Future)

Recommended alert rules for Prometheus:

```yaml
groups:
  - name: sk-tech-alerts
    rules:
      - alert: HighLatency
        expr: django_http_requests_duration_seconds{p95} > 0.5
        for: 5m
      - alert: HighErrorRate
        expr: rate(django_http_responses_total_by_status{status=~"5.."}[5m]) > 0.01
        for: 5m
      - alert: HighSecurityEvents
        expr: rate(django_security_events_total{severity="critical"}[5m]) > 5
      - alert: RedisDown
        expr: redis_up == 0
```
