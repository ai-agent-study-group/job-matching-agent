# Project Structure

Use this reference when creating, moving, or reviewing folders in a Next.js App Router project.

This structure is intentionally generic so it can be shared across multiple projects.

---

## Recommended Structure

```txt
app/
  ├── [lang]/             # Optional locale-based routing when the project supports i18n
  ├── api/                # Route handlers and backend endpoints
  ├── layout.tsx
  └── page.tsx

src/
  ├── components/         # Domain-organized components (single axis)
  │   ├── ui/             # Generated UI primitives such as shadcn/ui components
  │   ├── layout/         # Site-wide layout & navigation
  │   ├── shared/         # UI reused across 2+ domains
  │   └── ...             # One folder per product domain
  ├── constants/          # Shared constants and fixed configuration values
  ├── types/              # Shared TypeScript types used by multiple files
  ├── providers/          # Global providers such as theme, auth, query, or state providers
  ├── hooks/              # Reusable React hooks
  ├── utils/              # Pure utility functions unrelated to React rendering
  └── lib/                # External SDK setup, clients, adapters, and infrastructure helpers

dictionaries/             # Optional i18n dictionaries
e2e/                      # End-to-end tests
```

---

## `app/`

Use `app/` for Next.js App Router files.

Common files:

```txt
page.tsx
layout.tsx
loading.tsx
error.tsx
not-found.tsx
route.ts
```

Rules:

- Keep route-level logic in `app/`.
- Move reusable UI into `src/components/`.
- Move reusable data transformation into `src/utils/`.
- Move SDK clients and server integrations into `src/lib/`.
- Use `function` declarations for `Page` and `Layout` files when appropriate.

---

## `src/components/`

Use `src/components/` for React components, organized by domain (single axis).

Recommended categories:

```txt
src/components/ui/         # shadcn/ui primitives
src/components/layout/     # site-wide layout & navigation
src/components/shared/     # UI reused across 2+ domains
src/components/{domain}/   # one folder per product domain
```

Rules:

- `ui/` is for base UI primitives only.
- Domain folders own components used by a single page/domain.
- `shared/` is for components reused by 2 or more domains (not a dumping ground).
  Keep it flat: no subfolders. When a group grows to ~4+ files, graduate it to a
  flat top-level concern folder (e.g. `motion/`), not a `shared/` subfolder.
- `layout/` is for site-wide header/footer/navigation.
- Avoid placing business logic in `ui/`.
- Do not create element/primitive folders (`button/`, `table/`) or one-file folders.
- Avoid `components/common/` or `components/misc/` as a dumping ground.

---

## `src/constants/`

Use `src/constants/` for stable values.

Examples:

```txt
src/constants/locales.ts
src/constants/routes.ts
src/constants/pagination.ts
```

Good candidates:

- supported locales
- route constants
- pagination limits
- static UI options
- enum-like values used by multiple files

Avoid placing runtime data fetching logic here.

---

## `src/types/`

Use `src/types/` for shared TypeScript types.

Examples:

```txt
src/types/api.ts
src/types/user.ts
src/types/page.ts
```

Rules:

- Use this folder only for types shared by multiple files.
- Keep component-only props near the component.
- Keep feature-specific types in feature folders if they are not global.

---

## `src/providers/`

Use `src/providers/` for global React providers.

Examples:

```txt
src/providers/theme-provider.tsx
src/providers/auth-provider.tsx
src/providers/query-provider.tsx
```

Rules:

- Providers should be small and focused.
- Avoid mixing unrelated provider logic in one large file.
- Place provider composition in a clear root provider when needed.

---

## `src/hooks/`

Use `src/hooks/` for reusable React hooks.

Examples:

```txt
src/hooks/use-mounted.ts
src/hooks/use-media-query.ts
src/hooks/use-debounce.ts
```

Rules:

- Hooks should start with `use`.
- Hooks should encapsulate reusable React state or lifecycle logic.
- Do not place pure non-React utilities in `src/hooks/`.
- Move pure logic from hooks into `src/utils/` when it can be tested independently.

---

## `src/utils/`

Use `src/utils/` for pure functions.

Examples:

```txt
src/utils/create-slug.ts
src/utils/format-date.ts
src/utils/cn.ts
```

Rules:

- Utilities should not depend on React rendering.
- Utilities should be reusable in at least two places.
- Check existing utilities before creating a new one.
- Avoid large generic `utils.ts` files.

---

## `src/lib/`

Use `src/lib/` for external integrations and infrastructure setup.

Examples:

```txt
src/lib/supabase/
src/lib/cloudflare/
src/lib/stripe/
src/lib/auth/
```

Good candidates:

- SDK clients
- server clients
- adapters
- database helpers
- storage helpers
- API wrappers

Avoid placing UI components here.

---

## `dictionaries/`

Use `dictionaries/` when the project supports i18n.

Example:

```txt
dictionaries/
  ├── en/
  └── ko/
```

Rules:

- Keep user-visible translated strings in dictionaries.
- Avoid hardcoded user-facing text in components when i18n is enabled.
- Keep locale keys consistent across languages.

---

## `e2e/`

Use `e2e/` for end-to-end tests.

Examples:

```txt
e2e/auth.spec.ts
e2e/navigation.spec.ts
e2e/public-page.spec.ts
```

Rules:

- Test critical user flows.
- Prefer stable selectors.
- Avoid testing implementation details.

---

## Review Checklist

- [ ] Is the new file placed in the correct folder?
- [ ] Is the structure generic enough for the project?
- [ ] Are page-specific details kept out of shared folders?
- [ ] Are generated UI primitives separated from business components?
- [ ] Are pure utilities placed in `src/utils/` only when reused?
- [ ] Are external clients placed in `src/lib/`?