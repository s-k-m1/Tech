# SK Tech - Testing Strategy

## Test Pyramid

```
        ╱╲
       ╱  ╲          E2E Tests (5%)
      ╱    ╲       Playwright/Cypress
     ╱──────╲
    ╱        ╲     Integration Tests (25%)
   ╱          ╲   API, WebSocket, Firewall
  ╱────────────╲
 ╱              ╲  Unit Tests (70%)
╱                ╲ Models, Serializers, Services, Components
```

## Backend Tests

**Framework:** Django TestCase + Django REST Framework's APIClient

### Unit Tests (`backend/apps/core/tests/`)

| Test File | Coverage | Examples |
|-----------|----------|----------|
| `test_models.py` | All model creation, `__str__`, unique constraints | `test_user_creation`, `test_tenant_creation` |
| `test_auth.py` | Registration, login, OTP, edge cases | `test_login_invalid_credentials`, `test_login_success` |
| `test_security.py` | WAF patterns, rate limiter, IP blacklist | `test_sql_injection_detection`, `test_clean_request_passes` |
| `test_erp.py` | Product, supplier, warehouse models | `test_product_creation`, `test_warehouse_creation` |
| `test_accounting.py` | Account, account type models | `test_account_creation`, `test_account_type_creation` |

### Running Tests

```bash
# All tests
cd backend && python manage.py test --settings=config.settings.test

# Specific file
python manage.py test apps.core.tests.test_security

# With coverage
coverage run --source='.' manage.py test
coverage report
```

### Test Conventions
- One `setUp` method per test class (create common fixtures)
- Test name: `test_<action>_<expected_result>`
- Each test tests one behavior
- Use `APIClient` for endpoint tests
- Use SQLite in-memory for CI (`settings/test.py`)

## Frontend Tests

**Framework:** Vitest + @testing-library/react

### Component Tests (`frontend/src/__tests__/`)

| Test File | Coverage | Examples |
|-----------|----------|----------|
| `Button.test.jsx` | Button rendering, variants, disabled state | `renders button with text`, `applies variant classes` |

### Running Tests

```bash
cd frontend
npm run test        # Single run
npm run test:watch  # Watch mode
```

### Coverage Goals
- Models: 100%
- Serializers: 90%
- Views: 80%
- Services: 90%
- Firewall/AI: 95%
- Frontend components: 70%

## CI Integration

GitHub Actions runs these jobs in parallel:

```
backend-test    → python manage.py test
frontend-test   → npm run test
security-scan   → bandit -r backend/
```

## Manual Testing Checklist

Before production deployment:
- [ ] Register new user → email verification sent
- [ ] Login → JWT returned
- [ ] 2FA OTP → verify with valid/invalid codes
- [ ] WAF → SQLi/XSS request returns 403
- [ ] Rate limit → rapid requests return 429
- [ ] IP blacklist → 5 WAF blocks = 24h ban
- [ ] Health check → /health/ returns 200, /ready/ returns 200
- [ ] WebSocket → connect, receive notification, ping/pong
- [ ] Multi-tenant → User A cannot see User B's data
- [ ] RBAC → Employee cannot delete projects
