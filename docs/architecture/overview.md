# SK Tech - System Architecture Overview

## High-Level Architecture

```
                         ┌─────────────┐
                         │   Frontend   │
                         │  React/Vite  │
                         └──────┬──────┘
                                │ HTTPS
                         ┌──────▼──────┐
                         │    Nginx    │
                         │  (Reverse   │
                         │   Proxy)    │
                         └───┬────┬────┘
                             │    │
                    ┌────────▼┐  └──────────────┐
                    │ Backend │                 │
                    │ Django  │            ┌────▼────┐
                    │  REST   │            │  Static │
                    │   API   │            │  Files  │
                    └──┬──┬───┘            └─────────┘
                       │  │
              ┌────────▼┐ └──────────┐
              │ Celery  │            │
              │ Workers │     ┌──────▼──────┐
              └────┬────┘     │   Redis     │
                   │          │ Sessions,   │
              ┌────▼────┐     │ Cache, Queue│
              │PostgreSQL│    │ WebSocket   │
              └─────────┘     └─────────────┘
```

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | React 18 + Vite + Tailwind CSS | SPA UI |
| State | Redux Toolkit | Client-side state management |
| Styling | Tailwind CSS | Utility-first CSS |
| Backend | Django 5 + DRF | REST API framework |
| Auth | JWT (SimpleJWT) | Stateless authentication |
| Database | PostgreSQL 16 | Primary data store |
| Cache | Redis 7 | Sessions, cache, rate limiting |
| Queue | Celery 5 | Async task processing |
| WebSocket | Django Channels 4 | Real-time notifications |
| Reverse Proxy | Nginx | Load balancing, SSL termination |
| Monitoring | Prometheus + Grafana | Metrics & dashboards |
| Container | Docker + Compose | Orchestration |

## Multi-Tenant Design

- **Row-level isolation**: Every model has a `tenant` FK field
- **TenantMiddleware**: Extracts tenant from domain header, attaches it to the request
- **Dynamic RBAC**: Permissions stored as JSON on Role model, checked by `DynamicRBACPermission`
- **User roles**: SuperAdmin (cross-tenant), TenantAdmin, Manager, Employee, Client

## Request Flow

1. **Nginx** terminates SSL, proxies to Django or serves static files
2. **SecurityMiddleware** (WAF): validates request, checks IP blacklist, rate limiting
3. **TenantMiddleware**: resolves tenant from domain
4. **Auth check** (DRF + JWT): validates access token
5. **DynamicRBACPermission**: checks user role permissions
6. **ViewSet**: handles business logic, queries tenant-scoped data
7. **AuditLogMiddleware**: logs all non-GET operations
8. **Prometheus middleware**: records request metrics

## Security Architecture

- **WAF**: Pattern-based blocking (SQLi, XSS, path traversal, file upload validation)
- **Rate Limiting**: Global (1000/min), Login (5/min), Register (3/min), per-endpoint
- **IP Blacklist**: Auto-block after 5 critical events in 1 hour
- **Login Risk Analysis**: Scores 0-1 based on device, geo, failure rate; blocks >0.7
- **2FA OTP**: TOTP-based, sent via Celery async email
- **Audit Logging**: All non-GET operations logged with tenant, user, IP, action
- **JWT**: 30-min access + 7-day refresh, rotating tokens

## Scalability

- **Horizontal scaling**: Stateless backend (no server-side sessions), Redis-backed sessions
- **Database**: Connection pooling (`CONN_MAX_AGE=60`), read replicas support
- **Celery**: Multiple workers, separate queues for email/notifications/security
- **WebSocket**: Redis channel layer for distributed real-time messaging
- **Docker Compose**: Service replicas, health checks, resource limits
