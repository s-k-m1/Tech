# SK Tech - Folder Structure

```
sk/
├── backend/                          # Django project
│   ├── config/                       # Project configuration
│   │   ├── settings/
│   │   │   ├── base.py               # Shared settings (all envs)
│   │   │   ├── dev.py                # Development overrides
│   │   │   ├── prod.py               # Production overrides
│   │   │   └── test.py               # Test settings (SQLite)
│   │   ├── urls.py                   # Root URL routing
│   │   ├── wsgi.py                   # WSGI entry point
│   │   ├── asgi.py                   # ASGI entry point (Channels)
│   │   └── celery.py                 # Celery app config
│   ├── apps/                         # Django applications
│   │   └── core/                     # Single app with domain modules
│   │       ├── models/               # Data models by domain
│   │       │   ├── account.py        # Tenant, User, Role, Device, Session
│   │       │   ├── crm.py            # Lead, Client, Contract, Meeting
│   │       │   ├── hrm.py            # Employee, Attendance, Leave, Payroll
│   │       │   ├── project.py        # Project, Milestone, Sprint, Task
│   │       │   ├── ticket.py         # Ticket, TicketComment
│   │       │   ├── notification.py   # Notification, NotificationTemplate
│   │       │   ├── erp.py            # Supplier, Product, Inventory, PO, Invoice
│   │       │   ├── accounting.py     # Account, JournalEntry, Transaction, Budget
│   │       │   └── security.py       # IPBlacklist, SecurityEvent
│   │       ├── serializers/          # DRF serializers by domain
│   │       ├── views/                # ViewSets by domain
│   │       │   ├── auth_views.py
│   │       │   ├── crm_views.py
│   │       │   ├── hrm_views.py
│   │       │   ├── project_views.py
│   │       │   ├── ticket_views.py
│   │       │   ├── notification_views.py
│   │       │   ├── security_views.py
│   │       │   ├── erp_views.py
│   │       │   ├── accounting_views.py
│   │       │   └── health_views.py   # /health/, /ready/
│   │       ├── urls/                 # URL routing by domain
│   │       ├── services/             # Business logic
│   │       │   ├── auth_service.py   # Login flow, OTP, session mgmt
│   │       │   ├── notification_service.py  # Email + WebSocket push
│   │       │   └── security_ai_service.py   # Dashboard, reports
│   │       ├── tasks/                # Celery async tasks
│   │       │   ├── notification_tasks.py    # Email sending
│   │       │   └── security_tasks.py        # Security scans
│   │       ├── middleware/           # Request processing
│   │       │   ├── tenant.py         # Multi-tenant resolution
│   │       │   ├── audit.py          # Audit logging
│   │       │   └── security.py       # WAF, rate limit, IP blacklist
│   │       ├── permissions/          # RBAC
│   │       │   └── rbac.py           # DynamicRBACPermission
│   │       ├── ai/                   # AI Security Engine
│   │       │   ├── login_risk_analyzer.py  # Login scoring
│   │       │   └── anomaly_detector.py     # Threat detection
│   │       ├── firewall/             # Security firewall
│   │       │   ├── waf.py            # Pattern-based blocking
│   │       │   ├── rate_limiter.py   # Redis-based rate limiting
│   │       │   └── request_validator.py   # Input validation
│   │       ├── consumers/            # WebSocket consumers
│   │       │   └── notification_consumer.py
│   │       ├── tests/                # Backend tests
│   │       ├── management/commands/  # Custom management commands
│   │       └── utils/                # Utilities
│   ├── requirements/                 # Python dependencies
│   ├── templates/                    # Django templates
│   └── manage.py
│
├── frontend/                         # React + Vite
│   ├── src/
│   │   ├── components/ui/            # Reusable UI components
│   │   │   ├── Button.jsx
│   │   │   ├── Card.jsx
│   │   │   ├── Modal.jsx
│   │   │   ├── DataTable.jsx
│   │   │   └── StatusBadge.jsx
│   │   ├── pages/                    # Page-level components
│   │   │   ├── auth/                 # Login, Register
│   │   │   ├── dashboard/            # Dashboard
│   │   │   ├── crm/                  # Leads, Clients
│   │   │   ├── hrm/                  # Employees, Leaves
│   │   │   ├── projects/             # Kanban board
│   │   │   ├── tickets/              # Tickets, detail
│   │   │   ├── security/             # Security dashboard
│   │   │   ├── erp/                  # Products
│   │   │   ├── accounting/           # Accounts
│   │   │   └── settings/             # Profile, security, branches, roles
│   │   ├── features/                 # Redux Toolkit slices
│   │   │   ├── store.js              # Root store config
│   │   │   ├── auth/                 # Auth slice
│   │   │   ├── crm/                  # CRM slice
│   │   │   ├── hrm/                  # HRM slice
│   │   │   ├── projects/             # Projects slice
│   │   │   ├── tickets/              # Tickets slice
│   │   │   ├── dashboard/            # Dashboard slice
│   │   │   ├── security/             # Security slice
│   │   │   ├── notifications/        # Notifications slice
│   │   │   ├── erp/                  # ERP slice
│   │   │   └── accounting/           # Accounting slice
│   │   ├── services/                 # API client (Axios)
│   │   ├── hooks/                    # Custom hooks
│   │   │   ├── useAuth.js
│   │   │   └── useWebSocket.js
│   │   ├── layouts/                  # Layouts
│   │   ├── App.jsx                   # Root router
│   │   └── main.jsx                  # Entry point
│   ├── package.json
│   └── vite.config.js
│
├── infra/                            # Infrastructure
│   ├── docker/                       # Docker configs
│   │   ├── backend.Dockerfile
│   │   ├── frontend.Dockerfile
│   │   ├── celery.Dockerfile
│   │   ├── celery-beat.Dockerfile
│   │   ├── nginx/                    # Nginx configs
│   │   ├── prometheus/               # Prometheus config
│   │   ├── grafana/                  # Grafana dashboards + datasources
│   │   └── postgres/                 # Init SQL
│   ├── docker-compose.yml            # Dev compose
│   └── docker-compose.prod.yml       # Prod compose (+ replicas)
│
├── scripts/                          # Automation
│   ├── deploy.sh                     # Deployment script
│   ├── seed_data.py                  # Demo data seeder
│   ├── backup.py                     # Database backup
│   └── ci-cd.yml                     # GitHub Actions (reference)
│
├── .github/workflows/                # GitHub Actions
│   └── ci-cd.yml                     # CI/CD pipeline
│
├── docs/                             # Documentation
│   ├── architecture/
│   │   ├── overview.md               # System architecture
│   │   └── folder-structure.md       # This file
│   ├── api/
│   │   └── endpoints.md              # API reference
│   └── deployment/
│       ├── deployment-guide.md       # How to deploy
│       └── production-checklist.md   # Go-live checklist
│
├── tests/                            # Integration/E2E tests
├── .gitignore
├── AGENTS.md                         # Agent instructions
└── README.md
```
