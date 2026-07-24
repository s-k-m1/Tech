# SK Tech - Agent Instructions

## Project Structure
This is a monorepo containing:
- `backend/` - Django REST API (single `core` app with modules)
- `frontend/` - React + Vite + Tailwind + Redux Toolkit
- `infra/` - Docker, nginx, prometheus, grafana configs
- `scripts/` - Deployment and automation scripts

## Conventions
- Python: Black formatter, Django coding style
- JS/React: ESLint, functional components with hooks
- All models go in `backend/apps/core/models/` by domain
- All views go in `backend/apps/core/views/` by domain
- All serializers go in `backend/apps/core/serializers/` by domain
- All tests go in `backend/apps/core/tests/`

## Key Commands
- Backend dev: `cd backend && python manage.py runserver`
- Celery: `cd backend && celery -A config.celery worker -l info`
- Frontend dev: `cd frontend && npm run dev`
- Docker: `docker compose -f infra/docker-compose.yml up -d`
- Tests: `cd backend && python manage.py test`

## Patterns
- Always filter querysets by tenant using `request.user.tenant`
- Use Celery for async tasks (email, notifications, security scans)
- Use Redis for caching, sessions, rate limiting
- All new endpoints need authentication + RBAC checks
- Log all non-GET operations via AuditLog
