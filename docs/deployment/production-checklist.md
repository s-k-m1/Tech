# SK Tech - Production Readiness Checklist

## Application Configuration

- [ ] `DJANGO_SECRET_KEY` is a long random string (not default)
- [ ] `DEBUG = False` in production settings
- [ ] `ALLOWED_HOSTS` set to specific domains
- [ ] `CORS_ALLOWED_ORIGINS` restricted to frontend domain(s)
- [ ] `DATABASES` configured with strong password
- [ ] `REDIS_URL` uses password in production
- [ ] Session engine is Redis-backed (not database)
- [ ] Cache is Redis-backed
- [ ] Celery broker is Redis with password

## Security

- [ ] SSL/TLS enabled (HTTPS only)
- [ ] `SECURE_SSL_REDIRECT = True`
- [ ] `SESSION_COOKIE_SECURE = True`
- [ ] `CSRF_COOKIE_SECURE = True`
- [ ] `SECURE_HSTS_SECONDS` set to 31536000+
- [ ] `X_FRAME_OPTIONS = "DENY"`
- [ ] Rate limiting configured per endpoint
- [ ] WAF patterns loaded and tested
- [ ] IP blacklist auto-block active
- [ ] Login risk analysis enabled
- [ ] 2FA OTP verification working
- [ ] Audit logging operational
- [ ] All admin URLs restricted or renamed
- [ ] File upload size limits configured (10MB)

## Database

- [ ] PostgreSQL connection pooling (PgBouncer) in production
- [ ] `CONN_MAX_AGE` set to 60 (keep-alive)
- [ ] Backups configured (daily + hourly WAL)
- [ ] Backup retention policy defined (30 days)
- [ ] Read replica strategy documented
- [ ] Migration rollback plan documented
- [ ] Database maintenance window scheduled

## Infrastructure

- [ ] Docker resource limits set (CPU/memory per container)
- [ ] Log rotation configured (max 10MB, 10 backups)
- [ ] Container restart policy: `unless-stopped`
- [ ] Health check endpoints monitored (`/health/`, `/ready/`)
- [ ] Prometheus + Grafana dashboards imported
- [ ] Alert rules defined in Prometheus
- [ ] Uptime monitoring configured (Pingdom/UptimeRobot)
- [ ] Error tracking (Sentry) configured

## Scaling

- [ ] Backend replicas: at least 2
- [ ] Celery workers: at least 2
- [ ] Nginx worker processes: auto
- [ ] PostgreSQL: connection limit > 100
- [ ] Redis: maxmemory policy: allkeys-lru
- [ ] Load balancer health check configured

## CI/CD

- [ ] All tests pass before merge
- [ ] Docker images build without errors
- [ ] Security scan passes (bandit, safety)
- [ ] Secrets stored in GitHub Actions secrets
  - `DEPLOY_HOST`
  - `DEPLOY_USER`
  - `DEPLOY_SSH_KEY`
- [ ] Zero-downtime deploy strategy documented
- [ ] Rollback procedure tested

## Monitoring & Alerting

- [ ] Grafana alerts configured for:
  - CPU > 80%
  - Memory > 80%
  - Disk > 85%
  - 5xx errors > 1%
  - p95 latency > 500ms
  - Redis down
  - PostgreSQL connection pool exhausted
- [ ] Email alert channel configured in Grafana
- [ ] Log aggregation (ELK/Loki) considered

## DR & Business Continuity

- [ ] Database backups tested with restore
- [ ] Docker volumes backed up
- [ ] Disaster recovery plan documented
- [ ] RTO (Recovery Time Objective): < 4 hours
- [ ] RPO (Recovery Point Objective): < 1 hour
- [ ] Multi-region deployment considered
