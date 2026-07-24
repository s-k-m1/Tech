# SK Tech - Coding Standards

## Python (Backend)

### Formatting
- **Formatter:** Black (line length: 120)
- **Import order:** isort (profile: black, line length: 120)
- **Linter:** flake8 (max line length: 120, exclude migrations)

### Django Conventions
- Models: Singular noun, lowercase class name
- Viewsets for CRUD endpoints, APIView for custom endpoints
- Serializers mirror model field names
- Business logic in `services/`, not in views or serializers

### Naming
- `snake_case` for variables, functions, methods
- `PascalCase` for classes
- `UPPER_CASE` for constants
- File names match class names: `LoginView` → `auth_views.py`

### Model Conventions
- All data models inherit from `BaseModel` (UUID PK, timestamps, is_active)
- All data models have a `tenant` FK for multi-tenant isolation
- Use `unique_together` for tenant-scoped uniqueness
- Define `__str__` on all models
- Use `verbose_name`/`verbose_name_plural` in Meta class

## JavaScript/React (Frontend)

### Formatting
- **Linter:** ESLint (React recommended rules)
- **Components:** Functional components with hooks only
- **Exports:** Default export for pages and components

### State Management
- Global state: Redux Toolkit (slices in `features/` by domain)
- Server state: Direct API calls via `services/api.js`
- Local state: `useState` / `useReducer`
- No prop drilling beyond 2 levels

### Styling
- Tailwind CSS utility classes only (no CSS modules, no styled-components)
- Responsive: mobile-first with `sm`, `md`, `lg` breakpoints

### File Organization
- Pages in `pages/<domain>/`, Redux slices in `features/<domain>/`
- Shared UI components in `components/ui/`
- API client in `services/api.js`, custom hooks in `hooks/`

## Git Conventions
- Commit messages: imperative mood, 50-char subject, blank line, body
- Branches: `feature/<name>`, `fix/<name>`, `docs/<name>`
- No direct commits to `main` — PR + review required

## Testing
- Backend: Django TestCase, one test file per domain
- Frontend: Vitest + Testing Library
- Test file location: `backend/apps/core/tests/test_<domain>.py`
- Test naming: `test_<action>_<expected_result>`
