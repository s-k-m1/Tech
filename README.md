# SK Tech - Enterprise SaaS Platform

AI-powered multi-tenant SaaS platform with CRM, HRM, ERP, Accounting, Project Management, and Security modules.

## Tech Stack

- **Backend:** Django 5 + Django REST Framework + Celery + Channels (WebSocket)
- **Frontend:** React 18 + Vite + Tailwind CSS + Redux Toolkit
- **Database:** PostgreSQL
- **Cache/Broker:** Redis
- **Auth:** JWT (SimpleJWT) + OAuth2 (Google, GitHub, Microsoft)
- **Monitoring:** Prometheus + Grafana
- **Containerization:** Docker + Docker Compose

## Quick Start

```bash
# Backend
cd backend
pip install -r requirements/dev.txt
python manage.py migrate
python manage.py runserver

# Frontend
cd frontend
npm install
npm run dev
```

## Documentation

All documentation is in the `docs/` directory:
- **Architecture:** Database design, RBAC matrix, Redis, AI workflows, monitoring
- **Deployment:** Deployment guide, production checklist, coding standards, scalability, testing
- **API:** Full API endpoint reference

## License

Proprietary - SK Tech Enterprise
