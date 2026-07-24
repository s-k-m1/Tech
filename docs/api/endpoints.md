# SK Tech - API Documentation

## Base URL

| Environment | URL |
|-------------|-----|
| Development | `http://localhost:8000/api` |
| Production | `https://api.sktech.io/api` |

## Authentication

All endpoints except auth/register and auth/login require JWT Bearer token:

```
Authorization: Bearer <access_token>
```

### Auth Endpoints

| Method | Path | Description | Rate Limit | Auth |
|--------|------|-------------|------------|------|
| POST | `/api/auth/register/` | Create account | 3/min/IP | No |
| POST | `/api/auth/login/` | Sign in | 5/min/email | No |
| POST | `/api/auth/verify-otp/` | Verify OTP (2FA) | 5/min/IP | No |
| POST | `/api/auth/logout/` | Sign out | - | Yes |
| GET | `/api/auth/profile/` | Get current user | - | Yes |
| PUT | `/api/auth/profile/` | Update profile | - | Yes |
| GET | `/api/auth/devices/` | List devices | - | Yes |
| DELETE | `/api/auth/devices/<id>/` | Remove device | - | Yes |

### CRM Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/crm/leads/` | List leads |
| POST | `/api/crm/leads/` | Create lead |
| PUT | `/api/crm/leads/<id>/` | Update lead |
| DELETE | `/api/crm/leads/<id>/` | Delete lead |
| GET | `/api/crm/clients/` | List clients |
| GET | `/api/crm/contracts/` | List contracts |
| GET | `/api/crm/meetings/` | List meetings |

### HRM Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/hrm/employees/` | List employees |
| GET | `/api/hrm/attendance/` | List attendance |
| GET | `/api/hrm/leaves/` | List leave requests |
| POST | `/api/hrm/leaves/` | Create leave request |
| PUT | `/api/hrm/leaves/<id>/` | Update leave (approve/reject) |
| GET | `/api/hrm/payroll/` | List payroll records |

### Project Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/projects/projects/` | List projects |
| GET | `/api/projects/tasks/` | List tasks |
| POST | `/api/projects/tasks/` | Create task |
| PUT | `/api/projects/tasks/<id>/` | Update task (move kanban, etc.) |
| DELETE | `/api/projects/tasks/<id>/` | Delete task |
| GET | `/api/projects/milestones/` | List milestones |
| GET | `/api/projects/sprints/` | List sprints |

### Ticket Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/tickets/tickets/` | List tickets |
| POST | `/api/tickets/tickets/` | Create ticket |
| PUT | `/api/tickets/tickets/<id>/` | Update ticket |
| GET | `/api/tickets/comments/` | List comments |

### Security Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/security/dashboard/` | Security dashboard data |
| GET | `/api/security/report/` | Generate security report |

### Notification Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/notifications/notifications/` | List notifications |
| PATCH | `/api/notifications/notifications/<id>/` | Mark as read |

### ERP Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/erp/suppliers/` | List suppliers |
| GET | `/api/erp/warehouses/` | List warehouses |
| GET | `/api/erp/categories/` | List categories |
| GET | `/api/erp/products/` | List products |
| GET | `/api/erp/inventory/` | List inventory |
| GET | `/api/erp/purchase-orders/` | List purchase orders |
| GET | `/api/erp/invoices/` | List invoices |

### Accounting Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/accounting/account-types/` | List account types |
| GET | `/api/accounting/accounts/` | List accounts |
| GET | `/api/accounting/journal-entries/` | List journal entries |
| GET | `/api/accounting/transactions/` | List transactions |
| GET | `/api/accounting/budgets/` | List budgets |

### Health & Monitoring

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health/` | Liveness check |
| GET | `/ready/` | Readiness check (DB + Redis + Celery) |
| GET | `/metrics` | Prometheus metrics |

## WebSocket

### Notification Channel

```
ws://<host>/ws/notifications/?token=<access_token>
```

**Events received:**
- `notification` — Real-time in-app notification
- `security_alert` — Security event alert

**Client heartbeat:** Send `{"type": "ping"}` every 30s

## Pagination

All list endpoints use Django pagination (page-based, 25 items/page).

```
GET /api/crm/leads/?page=2
```

Response format:
```json
{
  "count": 150,
  "next": "http://.../?page=3",
  "previous": "http://.../?page=1",
  "results": [...]
}
```

## Error Responses

```json
{
  "error": "Human-readable error message",
  "detail": "Detailed error (only for superusers in dev)"
}
```

HTTP Status Codes:
- 200: Success
- 201: Created
- 400: Bad request / Validation error
- 401: Unauthenticated
- 403: Forbidden / WAF blocked
- 404: Not found
- 429: Rate limited
- 500: Internal server error
