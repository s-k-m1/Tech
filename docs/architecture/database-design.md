# SK Tech - Database Design

## ERD Overview

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│   Tenant    │────>│   Branch     │────>│  Department  │
└─────────────┘     └──────────────┘     └──────────────┘
       │                    │                    │
       │                    │                    │
       ▼                    ▼                    ▼
  ┌─────────────┐     ┌──────────────┐     ┌──────────────┐
  │    User     │<────│  UserRole    │────>│    Role      │
  └──────┬──────┘     └──────────────┘     └──────────────┘
         │
    ┌────┴───────────────────────────────┐
    │                                    │
    ▼                                    ▼
┌──────────┐                      ┌──────────┐
│  Device  │                      │  Session │
└──────────┘                      └──────────┘
```

## Multi-Tenant Strategy

**Approach: Shared database, row-level isolation**

- Every data table has a `tenant_id` UUID foreign key
- `TenantMiddleware` resolves tenant from domain and attaches to `request.tenant`
- All ViewSets filter by `request.user.tenant` automatically
- `BaseModel` abstract class provides `id` (UUID), `created_at`, `updated_at`, `is_active`

```
BaseModel (abstract)
├── id: UUID (PK, auto)
├── created_at: DateTime (auto_now_add)
├── updated_at: DateTime (auto_now)
└── is_active: Boolean (default=True)
```

## Domain Models

### Account Domain (`models/account.py`)

| Model | Key Fields | Relationships |
|-------|-----------|--------------|
| **Tenant** | name, slug (unique), domain, subscription_plan | Root entity |
| **Branch** | name, code (unique per tenant), is_head_office | FK → Tenant |
| **Department** | name, code (unique per tenant) | FK → Tenant, FK → Branch |
| **User** | email, username, user_type, is_2fa_enabled, risk_score | FK → Tenant, M2M → Branch, M2M → Department |
| **Role** | name, slug (unique per tenant), permissions (JSON) | FK → Tenant |
| **UserRole** | — | FK → User, FK → Role, FK → Branch (nullable) |
| **Device** | device_name, device_type, ip_address, is_trusted | FK → User |
| **Session** | token, refresh_token, is_active, expires_at | FK → User, FK → Device |
| **AuditLog** | action, resource, details (JSON), risk_level | FK → Tenant (nullable), FK → User (nullable) |

### CRM Domain (`models/crm.py`)

| Model | Key Fields | Relationships |
|-------|-----------|--------------|
| **Lead** | first_name, last_name, email, status, score | FK → Tenant, FK → User (assignee) |
| **Client** | company_name, contact_person, email | FK → Tenant, FK → User (nullable) |
| **Contract** | title, content, start_date, end_date, value, status | FK → Tenant, FK → Client |
| **Meeting** | title, meeting_date, duration_minutes | FK → Tenant, FK → Client, M2M → User |

### HRM Domain (`models/hrm.py`)

| Model | Key Fields | Relationships |
|-------|-----------|--------------|
| **Employee** | employee_id (unique per tenant), designation, salary | FK → User, FK → Tenant, FK → Branch, FK → Department |
| **Attendance** | date, check_in, check_out, status | FK → Employee |
| **Leave** | leave_type, start_date, end_date, status | FK → Employee, FK → User (approver) |
| **Payroll** | month, year, basic_salary, net_salary, is_paid | FK → Employee |

### Project Domain (`models/project.py`)

| Model | Key Fields | Relationships |
|-------|-----------|--------------|
| **Project** | name, status, priority, budget | FK → Tenant, FK → User (owner), M2M → User (members) |
| **Milestone** | name, due_date, is_completed | FK → Project |
| **Sprint** | name, start_date, end_date, is_active | FK → Project |
| **Task** | title, status, priority, due_date, kanban_order | FK → Project, FK → Milestone, FK → Sprint, FK → User (assignee) |
| **TaskComment** | content, attachments (JSON) | FK → Task, FK → User (author) |

### Ticket Domain (`models/ticket.py`)

| Model | Key Fields | Relationships |
|-------|-----------|--------------|
| **Ticket** | subject, description, status, priority, category | FK → Tenant, FK → User (requester), FK → User (assignee) |
| **TicketComment** | content, is_internal | FK → Ticket, FK → User (author) |

### ERP Domain (`models/erp.py`)

| Model | Key Fields | Relationships |
|-------|-----------|--------------|
| **Supplier** | name, email, phone, tax_id | FK → Tenant |
| **Warehouse** | name, code (unique per tenant) | FK → Tenant, FK → Branch |
| **Category** | name (unique per tenant) | FK → Tenant, FK → self (parent) |
| **Product** | name, sku (unique), purchase_price, selling_price | FK → Tenant, FK → Category |
| **Inventory** | quantity, reserved_quantity | FK → Product, FK → Warehouse |
| **PurchaseOrder** | order_number (unique), status, grand_total | FK → Tenant, FK → Supplier, FK → Warehouse, FK → User (creator) |
| **PurchaseOrderItem** | quantity, unit_price, total_price | FK → PurchaseOrder, FK → Product |
| **Invoice** | invoice_number (unique), status, grand_total | FK → Tenant, FK → User (creator) |
| **InvoiceItem** | description, quantity, unit_price, total_price | FK → Invoice, FK → Product |

### Accounting Domain (`models/accounting.py`)

| Model | Key Fields | Relationships |
|-------|-----------|--------------|
| **AccountType** | name (unique per tenant), category | FK → Tenant |
| **Account** | name, code (unique per tenant), current_balance | FK → Tenant, FK → Branch, FK → AccountType, FK → self (parent) |
| **JournalEntry** | entry_number (unique), entry_date, is_posted | FK → Tenant, FK → User (creator) |
| **JournalLineItem** | debit, credit | FK → JournalEntry, FK → Account |
| **Transaction** | transaction_number (unique), amount, transaction_type, status | FK → Tenant, FK → Branch, FK → Account (from/to), FK → User (creator) |
| **Budget** | name, fiscal_year, total_amount, status | FK → Tenant, FK → Branch, FK → User (creator) |
| **BudgetLineItem** | allocated_amount, spent_amount | FK → Budget, FK → Account |

### Security Domain (`models/security.py`)

| Model | Key Fields | Relationships |
|-------|-----------|--------------|
| **IPBlacklist** | ip_address, reason, blocked_by, expires_at | FK → Tenant (nullable) |
| **SecurityEvent** | event_type, severity, source_ip, description, metadata (JSON) | FK → Tenant (nullable) |

### Notification Domain (`models/notification.py`)

| Model | Key Fields | Relationships |
|-------|-----------|--------------|
| **Notification** | notification_type, title, message, data (JSON), is_read | FK → Tenant, FK → User (recipient) |
| **NotificationTemplate** | name, subject, body, variables (JSON), channels (JSON) | FK → Tenant (nullable) |

## Indexing Strategy

- All `tenant_id` FKs are indexed (tenant isolation queries)
- `AuditLog`: indexes on `(tenant, action)`, `(tenant, user)`, `created_at`
- `IPBlacklist`: indexes on `(ip_address, is_active)`, `(tenant, ip_address)`
- `SecurityEvent`: indexes on `(tenant, severity)`, `event_type`, `created_at`
- All `status` and `user_type` fields are indexed for filtering
- Unique constraints enforced on `(tenant, code)` for Branch, Department, Warehouse, Account

## Migration Strategy

- Migrations are version-controlled in `backend/apps/core/migrations/`
- Use `python manage.py makemigrations` + `python manage.py migrate`
- Zero-downtime migrations: add columns as nullable, backfill, then set NOT NULL
- Rollback: `python manage.py migrate core <previous_migration>`
