# SK Tech - Scalability Plan

## Current Architecture

| Component | Current | Scalability Ceiling |
|-----------|---------|-------------------|
| Backend (Django) | Single container | 500-1000 req/s per instance |
| Frontend (React) | Single container | Served via CDN |
| PostgreSQL | Single instance | 1000-2000 concurrent connections |
| Redis | Single instance | 50,000+ ops/s |
| Celery | 4 workers | Queue-dependent |

## Horizontal Scaling Strategy

### 1. Backend Scaling

**Stateless design** enables horizontal scaling:
- No server-side sessions (Redis-backed)
- JWT auth tokens (self-contained, no session lookup)
- File storage on S3-compatible service (separate from container)

**Scaling approach:**
```
Nginx Load Balancer
├── Backend Instance 1
├── Backend Instance 2
├── Backend Instance 3
└── Backend Instance N (auto-scale)
```

Docker Compose replicas:
```yaml
backend:
  deploy:
    replicas: 3
    resources:
      limits:
        cpus: "1"
        memory: "1G"
```

### 2. Database Scaling

**Read replicas** for dashboard/report queries:
```
Primary (write) → Read Replica 1 → Backend reads
                → Read Replica 2 → Analytics/Celery reads
```

Configure in settings.py:
```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "sk_tech",
        "HOST": "primary.example.com",
    },
    "read_replica": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "sk_tech",
        "HOST": "replica.example.com",
    },
}
```

**Connection pooling** with PgBouncer:
- Target: 100-200 persistent connections per backend instance
- `CONN_MAX_AGE = 60` (keep connections alive)

### 3. Redis Scaling

**Redis Cluster** for cache/broker:
- Shard across 3+ nodes
- No single point of failure
- Automatic failover

For high-throughput: separate instances per use case:
- Redis A: Cache + Sessions
- Redis B: Celery broker
- Redis C: WebSocket channel layer

### 4. Celery Scaling

**Separate worker pools per queue:**
```bash
# Email workers (low priority)
celery -A config.celery worker -Q email -c 2

# Security workers (dedicated)
celery -A config.celery worker -Q security -c 1

# Default workers (main)
celery -A config.celery worker -Q celery -c 8
```

### 5. Frontend Scaling

- Build static assets at deploy time
- Serve via CDN (CloudFront, Cloudflare)
- Nginx for SPA routing with long cache headers
- No server-side rendering needed

## Performance Targets

| Metric | Current Target | Scaled Target |
|--------|---------------|---------------|
| API response time | < 200ms | < 100ms (with caching) |
| Dashboard load | < 1s | < 500ms |
| Login | < 500ms | < 300ms |
| Concurrent users | 1000 | 100,000+ |
| Real-time updates | < 100ms | < 50ms |

## Auto-Scaling (Kubernetes Future)

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: sk-tech-backend
spec:
  minReplicas: 3
  maxReplicas: 20
  metrics:
    - type: Resource
      resource:
        name: cpu
        targetAverageUtilization: 70
    - type: Resource
      resource:
        name: memory
        targetAverageUtilization: 80
```

## Bottleneck Monitoring

| Bottleneck | Metric | Threshold | Action |
|-----------|--------|-----------|--------|
| Backend CPU | docker stats | > 80% | Add replicas |
| DB connections | django_db_connections | > 100 | Add read replicas |
| Redis memory | redis_memory_usage | > 80% | Add cluster node |
| Celery queue | celery_queue_length | > 1000 | Add workers |
| Disk I/O | iostat | > 90% | Upgrade storage |
