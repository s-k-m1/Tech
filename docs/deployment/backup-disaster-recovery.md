# SK Tech - Backup & Disaster Recovery Plan

## Backup Strategy

| Data | Method | Frequency | Retention | Location |
|------|--------|-----------|-----------|----------|
| PostgreSQL | `pg_dump` (full) | Daily | 30 days | Local disk + S3 |
| PostgreSQL | WAL archiving | Continuous | 7 days | S3 |
| Media files | `rsync` / s3 sync | Daily | 30 days | S3 |
| Redis data | `SAVE` / RDB snapshots | Every 6 hours | 7 days | Local disk |
| Docker volumes | Volume backup | Weekly | 90 days | S3 |
| Environment secrets | Manual export | On change | Permanent | Vault/1Password |

### Automated Backup Script

Located at `scripts/backup.py`:

```
Usage: python scripts/backup.py
Output: /backups/sk_tech_YYYYMMDD_HHMMSS.sql
```

### Docker Command

```bash
# Manual backup
docker compose exec -T postgres pg_dump -U sk_tech sk_tech > /backups/db_$(date +%Y%m%d).sql

# Restore
cat /backups/db_20260101.sql | docker compose exec -T postgres psql -U sk_tech sk_tech
```

## Recovery Time Objectives

| Scenario | RTO | RPO | Procedure |
|----------|-----|-----|-----------|
| Application crash | < 5 min | 0 | Docker restart policy: `unless-stopped` |
| Database corruption | < 1 hour | < 1 hour | Restore latest pg_dump + replay WAL |
| Full server failure | < 4 hours | < 1 hour | Provision new server, restore from S3 |
| Regional outage | < 24 hours | < 1 hour | Deploy to secondary region, restore DB from S3 |

## Disaster Scenarios

### 1. Application Crash

```
Detection: Docker health check failure / Prometheus alert
Action: docker compose restart backend
Verification: /health/ returns 200
```

### 2. Database Failure

```
Detection: /ready/ returns 503 (DB check fails)
Action:
  1. docker compose stop backend celery
  2. docker compose exec postgres psql -U sk_tech -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname='sk_tech';"
  3. docker compose restart postgres
  4. If corrupt: restore from backup
  5. docker compose start backend celery
Verification: /ready/ returns 200
```

### 3. Redis Failure

```
Detection: Redis ping fails / metrics drop
Action:
  1. docker compose restart redis
  2. Verify: docker compose exec redis redis-cli ping → PONG
Impact: Sessions lost (users re-login), rate limits reset, WS connections drop
```

### 4. Full Server Loss

```
Detection: Uptime monitor alert (Pingdom)
Action:
  1. Provision new server with Docker + Docker Compose
  2. Clone repo: git clone https://github.com/s-k-m1/Tech.git
  3. Restore .env from Vault/1Password
  4. Restore latest database dump from S3
  5. docker compose -f infra/docker-compose.prod.yml up -d
  6. Update DNS to new server IP
  7. Verify: /health/, /ready/, smoke test all endpoints
RTO: ~4 hours
```

## Disaster Recovery Runbook

### Pre-requisites
- [ ] S3 bucket for backups configured
- [ ] IAM credentials with write access to S3
- [ ] Secondary DNS provider configured
- [ ] Incident response contact list documented

### Immediate Actions (first 15 minutes)
1. Identify scope: single service or full outage
2. Notify stakeholders
3. Check monitoring dashboards for root cause
4. Apply fix or initiate recovery procedure

### Recovery Verification
- [ ] All services running: `docker compose ps`
- [ ] Database accepting connections: `/ready/`
- [ ] API returning 200: `curl /health/`
- [ ] Redis responsive: `redis-cli ping`
- [ ] Celery processing: `celery inspect stats`
- [ ] Frontend loading: HTTP 200 on domain
- [ ] User login working: smoke test
- [ ] Backup system operational after recovery

## Prevention

- Automated daily backups with 30-day retention
- Docker health checks on all services
- Prometheus alerting for disk, memory, CPU
- Regular disaster recovery drills (quarterly)
- Immutable infrastructure (no manual server config)
- Database migration rollback plan for every release
