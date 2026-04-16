# AGENTS.md

Guidance for coding agents working in this repository.

## Scope

- Repository contains:
  - Django backend
  - Vue/Vite frontend in `ui/`
  - Mock API in `mock/`
  - Helm manifests in `helm/`
  - Documentation in `docs/`

## Core Principles

When generating or modifying code, always follow:

- **Minimize new dependencies**
- **Use descriptive naming** for functions, variables, and classes
- **Code must be written in English**
- Prefer **clarity, consistency, and minimal complexity**
- Follow existing patterns unless explicitly instructed otherwise

## Repo Layout

- Backend entrypoint: `manage.py`
- Django settings: `atlas/settings.py`
- Backend apps:
  `webservice/`, `table/`, `tables/`, `portal/`, `authz/`, `user_management/`, `homepage/`
- Frontend app: `ui/`
- Frontend source: `ui/src/`
- Frontend tests:
  - Unit: `ui/tests/unit/`
  - Browser: `ui/tests/browser/`
  - E2E: `ui/tests/e2e/`

- Mock API: `mock/`

## Install Commands

- Backend: make sure `uv` is installed.

- Frontend (make sure `pnpm` is installed):

  ```bash
  cd ui && pnpm install
  ```

- Mock API:

  ```bash
  cd mock && pnpm install
  ```

- Services:

  ```bash
  docker compose up -d postgres dex filter-proxy geoserver
  ```

## Build Commands

- Full stack:

  ```bash
  docker compose up
  ```

- Backend:

  ```bash
  uv run manage.py runserver
  ```

- Frontend:

  ```bash
  cd ui && pnpm run dev
  cd ui && pnpm run serve
  cd ui && pnpm run build
  ```

- Metadata types:

  ```bash
  cd ui && pnpm run generate-metadata-types
  ```

- Mock API:

  ```bash
  cd mock && pnpm run dev
  ```

## Lint & Format

- Backend:

  ```bash
  uv run ruff check
  ```

- Frontend:

  ```bash
  cd ui && pnpm run lint
  cd ui && pnpm run lint:fix
  cd ui && pnpm run format
  ```

- Migration drift:

  ```bash
  uv run manage.py makemigrations --check --dry-run
  ```

## Test Commands

- Backend:

  ```bash
  uv run manage.py test
  uv run coverage run manage.py test
  uv run coverage report
  ```

- Frontend:

  ```bash
  cd ui && pnpm run test:unit
  cd ui && pnpm run test:browser
  cd ui && pnpm run test:e2e
  ```

## High-Value Verification Workflow

- **Backend-only changes**
  - Run: `uv run ruff check`, backend tests
  - Check migrations if models changed

- **Frontend-only changes**
  - Run: lint + smallest relevant test

- **Full-stack changes**
  - Backend tests
  - Frontend build
  - At least one relevant frontend test

- If backend changes affect frontend enums:
  - Regenerate metadata types in `ui/`

# Backend Guidelines

- Prefer **built-in Django functionality** over custom implementations
- Follow patterns used in nearby files before introducing new ones

### Style

- `snake_case` for functions, variables, modules
- `PascalCase` for classes
- `UPPER_SNAKE_CASE` for constants
- Use explicit imports (no wildcards)
- Group imports: standard → third-party → local

### Code Practices

- Use **guard clauses / early returns**
- Raise clear, specific errors
- Do not introduce unnecessary abstractions
- Do not reformat unrelated code

### Testing

- All backend changes must include tests
- Prefer:
  - `TestCase`
  - `RequestFactory`
  - `subTest` for scenarios

### Types

- Add **type annotations** where possible (incrementally)

# Frontend Guidelines

## Architecture

- **New components MUST use Vue Composition API**
- **Refactored components MUST use Composition API**
- Prefer `script setup lang="ts"`

⚠️ Exception:

- When editing large legacy components, **do not rewrite fully** unless required

## TypeScript

- Required for:
  - New components
  - Refactored components

- Use **strict typing**
- Avoid `any` unless absolutely necessary

## State Management

- Use Pinia stores directly
- ❌ Do NOT use `storeToRefs`

## Code Quality

- Prefer:
  - Enums for fixed values
  - Named interfaces (`IThing`)
  - Enums (`EThing`)

- Use descriptive names

## Structure

- Place reusable logic in:
  - `utils/`
  - `services/`
  - `composables/`

- Naming:
  - Composables → `useX`
  - Stores → `useXStore`

## Style

- Use **arrow functions**
- Use **double quotes**
- Use **semicolons**
- Respect Prettier config (`printWidth: 120`)

## Error Handling

- Prefer early returns
- Do not swallow errors
- Use:
  - `apiFetch`
  - `showApiFetchError`

- Always check `response.ok`

## Testing

- New utility functions must have **unit tests**

Test locations:

- Unit → `ui/tests/unit`
- Browser → `ui/tests/browser`
- E2E → `ui/tests/e2e`

# Agent Do & Don't

## Do

- Make **small, focused changes**
- Follow **CONTRIBUTING.md rules strictly**
- Match **existing patterns first**, then improve where safe
- Add tests where required
- Check backend/frontend impact before changing code

## Don’t

- Add new dependencies without strong justification
- Introduce new architectural patterns unnecessarily
- Use `any` when avoidable
- Use `storeToRefs`
- Rewrite large legacy components without reason
- Reformat unrelated files

# Useful Paths

- Backend settings: `atlas/settings.py`
- Backend tests: `webservice/tests/test_layers.py`
- Frontend config:
  - Vite: `ui/vite.config.mjs`
  - ESLint: `ui/eslint.config.js`
  - Prettier: `ui/.prettierrc.json`

- Tests:
  - Unit: `ui/vitest.unit.config.mjs`
  - Browser: `ui/vitest.browser.config.mjs`
  - E2E: `ui/playwright.config.ts`
