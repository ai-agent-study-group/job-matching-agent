# TypeScript and TSDoc

Use this reference when writing or reviewing TypeScript code, shared types, exported functions, hooks, utilities, or module-level helpers.

---

## TypeScript Strict Mode

Assume `strict: true`.

Rules:

- Do not use `any`.
- Prefer explicit return types for exported functions.
- Prefer precise types over broad types.
- Avoid unnecessary type assertions.
- Do not silence TypeScript errors without a clear reason.
- Prefer narrowing over casting.

Good:

```ts
type UserProfile = {
  id: string;
  email: string;
  displayName: string | null;
};

export const getDisplayName = (profile: UserProfile): string => {
  return profile.displayName ?? profile.email;
};
```

Avoid:

```ts
export const getDisplayName = (profile: any) => {
  return profile.displayName || profile.email;
};
```

---

## Path Alias

Use the project path alias:

```txt
@/* -> ./src/*
```

Good:

```ts
import { formatDate } from '@/utils/format-date';
import type { UserProfile } from '@/types/user';
```

Avoid deep relative imports when a stable alias is clearer:

```ts
import { formatDate } from '../../../utils/format-date';
```

---

## Shared Types

Place shared types in:

```txt
src/types/
```

Use `src/types/` when a type is shared by two or more files.

Keep local-only types inside the same file.

Good local type:

```ts
type Props = {
  title: string;
};

export const PageTitle = ({ title }: Props) => {
  return <h1>{title}</h1>;
};
```

Good shared type:

```txt
src/types/user.ts
src/types/api.ts
src/types/page.ts
```

---

## TSDoc Requirements

Every exported function in `src/` should have TSDoc.

Every module-level internal helper function in `src/` should also have TSDoc.

Exception:

```txt
src/components/ui/
```

TSDoc is not required for generated UI primitive files.

---

## Required TSDoc Fields

Include:

- summary
- `@param` for each parameter
- `@returns`

Use when relevant:

- `@throws`
- `@example`

Good:

```ts
/**
 * Converts a string into a URL-safe kebab-case slug.
 *
 * @param value - The text value to convert.
 * @returns A lowercase kebab-case slug.
 *
 * @example
 * createSlug('Privacy Policy') // 'privacy-policy'
 */
export const createSlug = (value: string): string => {
  return value
    .trim()
    .toLowerCase()
    .replace(/\s+/g, '-');
};
```

---

## Data-Access and API Routes (Next.js)

Route Handlers live centrally in `app/api/.../route.ts`. This project calls them
with inline `fetch` from client components/hooks (there is no `src/lib/` API
wrapper layer), so link the two ends with `{@link}` so the editor can jump
between caller and handler.

**Route Handler** — add TSDoc stating the HTTP method + route path, and link the
caller(s):

```ts
/**
 * Creates a new page from validated form data.
 *
 * Route: `POST /api/pages`.
 *
 * @see {@link ../../../src/components/write/WritePageForm.tsx} — caller (create mode).
 */
export async function POST(request: Request) {
  // ...
}
```

**Caller** — the `fetch` sits inside an event handler (TSDoc-exempt, see
"TSDoc Exclusions"), so add a one-line linking comment next to the call:

```tsx
// POST (create) / PATCH (edit) — see {@link ../../../app/api/pages/route.ts}
const response = await fetch("/api/pages", { ... });
```

Rules:

- Prefer `{@link <path>}` over hand-written `@usedIn` lists of caller files.
  Caller lists rot the moment a file is renamed; "Find All References" / the
  import graph is the source of truth and never goes stale.
- Document the route once on the handler; on callers keep it to a one-line
  `{@link}` comment, not a full duplicate.
- Use a relative path in `{@link}` (e.g. `../../../app/api/...`) since `app/`
  has no `@/` alias.
- Keep data access central (`app/api/`, `src/lib/`). Do not scatter API helpers
  into route folders (see "Structure as Documentation" in
  `architecture-and-style.md`).

---

## Service Page (URL) Links

For a component, document **which service page (URL) it renders on** by linking
its TSDoc to the route's top-level `page.tsx` — not a plain text path that can't
be followed and rots on rename.

In App Router the folder IS the URL, so `{@link}` to `app/.../page.tsx` answers
"where does this show up?" in one click.

```tsx
/**
 * Renders the pricing FAQ accordion.
 *
 * @param props - Localized FAQ copy and locale.
 * @returns A pricing FAQ section.
 *
 * @see {@link ../../../app/[lang]/pricing/page.tsx} — Pricing (`/pricing`)
 * @see {@link ../../../app/[lang]/(auth)/write/page.tsx} — Write (`/write`)
 * @see {@link ../../../app/[lang]/login/page.tsx} — Login (`/login`)
 */
export const PricingFaq = ({ ... }: Props) => { ... };
```

Rules:

- Only annotate components rendered by a **small, stable set of pages (≤ ~3)** —
  typically domain view/section components and single-page UI.
- Do NOT list pages for broadly-shared or cross-cutting components (e.g.
  `seo/JsonLd`, `shared/FadeInView`, `home/WriteCta`, `layout/SiteHeader`).
  A long page list is exactly the kind of caller list that rots — rely on
  "Find All References" instead.
- Link the route's `page.tsx`, and put the human URL in the trailing comment.
- This is the central-architecture alternative to route colocation
  (`app/<route>/_components/`), which this project does not use — see
  "Structure as Documentation" in `architecture-and-style.md`.

---

## Internal Helper Example

Module-level helpers also need TSDoc.

```ts
/**
 * Checks whether a value is a non-empty string after trimming whitespace.
 *
 * @param value - The value to check.
 * @returns Whether the value is a non-empty string.
 */
const isNonEmptyString = (value: string): boolean => {
  return value.trim().length > 0;
};
```

---

## TSDoc Exclusions

TSDoc is not required for:

- inline event handlers
- `useCallback` callbacks
- `useMemo` callbacks
- small inline render helpers inside components
- generated files in `src/components/ui/`

Example:

```tsx
const handleClick = () => {
  setOpen(true);
};
```

---

## React Component Props

Prefer a named `Props` type for components.

```tsx
type Props = {
  title: string;
  description?: string;
};

/**
 * Renders a section heading with an optional description.
 *
 * @param props - The component props.
 * @returns A section heading element.
 */
export const SectionHeading = ({ title, description }: Props) => {
  return (
    <section>
      <h2>{title}</h2>
      {description ? <p>{description}</p> : null}
    </section>
  );
};
```

---

## Avoid `React.FC`

Prefer explicit props and return inference over `React.FC`.

Good:

```tsx
type Props = {
  children: React.ReactNode;
};

export const Card = ({ children }: Props) => {
  return <div>{children}</div>;
};
```

Avoid:

```tsx
export const Card: React.FC<Props> = ({ children }) => {
  return <div>{children}</div>;
};
```

---

## Review Checklist

- [ ] Is `any` avoided?
- [ ] Are exported functions explicitly typed?
- [ ] Are shared types placed in `src/types/`?
- [ ] Are local-only types kept local?
- [ ] Are imports using `@/*` where appropriate?
- [ ] Do exported functions have TSDoc?
- [ ] Do module-level helpers have TSDoc?
- [ ] Are unnecessary type assertions avoided?