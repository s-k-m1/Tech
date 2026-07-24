# SK Tech - Deployment Guide

## Prerequisites

- Docker & Docker Compose (v2+)
- Git
- Domain name with DNS pointing to server
- SSL certificate (Let's Encrypt or commercial)
- PostgreSQL 16 (or use Docker image)
- Redis 7 (or use Docker image)

## Environment Setup

### 1. Clone Repository

```bash
git clone https://github.com/s-k-m1/Tech.git /app/sk
cd /app/sk
```

### 2. Configure Environment

```bash
cp backend/.env.example backend/.env
# Edit backend/.env with production values
```

Required production variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `DJANGO_SECRET_KEY` | 50+ char random string | `openssl rand -hex 32` |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated domains | `sktech.io,api.sktech.io` |
| `DB_NAME` | PostgreSQL database name | `sk_tech` |
| `DB_USER` | Database user | `sk_tech` |
| `DB_PASSWORD` | Strong password | |
| `DB_HOST` | Database host | `postgres` |
| `REDIS_URL` | Redis connection string | `redis://redis:6379/1` |
| `CORS_ALLOWED_ORIGINS` | Frontend domains | `https://sktech.io` |
| `EMAIL_HOST_USER` | SMTP username | |
| `EMAIL_HOST_PASSWORD` | SMTP password | |
| `DEFAULT_FROM_EMAIL` | Sender address | `noreply@sktech.io` |

### 3. Deploy with Docker Compose

```bash
# Production deployment
docker compose -f infra/docker-compose.prod.yml up -d

# Run migrations
docker compose -f infra/docker-compose.prod.yml exec backend python manage.py migrate --noinput

# Collect static files
docker compose -f infra/docker-compose.prod.yml exec backend python manage.py collectstatic --noinput

# Create superuser
docker compose -f infra/docker-compose.prod.yml exec backend python manage.py createsuperuser

# Seed demo data (optional)
docker compose -f infra/docker-compose.prod.yml exec backend python scripts/seed_data.py
```

### 4. Setup SSL (Let's Encrypt)

```bash
docker compose -f infra/docker-compose.prod.yml exec nginx certbot --nginx -d sktech.io -d api.sktech.io
```

## CI/CD Pipeline

The GitHub Actions workflow in `.github/workflows/ci-cd.yml`:

1. Runs on push to `main` or `develop`, and on PRs to `main`
2. **Backend Lint**: flake8, black, isort
3. **Backend Tests**: Django test suite with PostgreSQL + Redis
4. **Frontend Lint**: ESLint
5. **Frontend Tests**: Vitest
6. **Docker Build Check**: All Dockerfiles build successfully
7. **Security Scan**: bandit (SAST), safety (dependency vulns)
8. **Deploy**: SSH into production server, pull, rebuild, migrate

## Monitoring

- **Prometheus**: Available at `http://<server>:9090`
- **Grafana**: Available at `http://<server>:3000` (default admin/admin)
- **Health Checks**: `GET /health/` (liveness), `GET /ready/` (readiness)

## Backup

### Automated Database Backup

```bash
docker compose exec postgres pg_dump -U sk_tech sk_tech > /backups/sk_tech_$(date +%Y%m%d_%H%M%S).sql
```

### Restore

```bash
cat /backups/sk_tech_20260101_000000.sql | docker compose exec -T postgres psql -U sk_tech sk_tech
```

## Rollback

```bash
# Revert to previous Docker image
docker compose -f infra/docker-compose.prod.yml down
git checkout <previous-commit>
docker compose -f infra/docker-compose.prod.yml up -d --build
```

## Troubleshooting

| Issue | Check |
|-------|-------|
| Backend won't start | `docker compose logs backend` |
| Database connection | `docker compose exec backend python -c "from django.db import connection; connection.ensure_connection(); print('OK')"` |
| Redis connection | `docker compose exec redis redis-cli ping` |
| Celery not processing | `docker compose logs celery` |
| WebSocket not connecting | Check `REDIS_URL` in env, channel layer config |
