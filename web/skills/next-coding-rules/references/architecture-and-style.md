# Architecture and Style

Use this reference when organizing files, writing components, extracting utilities, or reviewing code structure.

---

## Component Organization

Use `src/components/ui/` for generated or base UI primitives.

Examples:

```txt
src/components/ui/button.tsx
src/components/ui/dialog.tsx
src/components/ui/input.tsx
```

Do not directly modify generated UI primitive files unless the project explicitly allows it.

Create wrappers or feature-level components instead.

Good:

```txt
src/components/shared/submit-button.tsx
src/components/layout/site-header.tsx
src/components/category/category-card.tsx
```

Avoid:

```txt
src/components/ui/custom-business-button.tsx
src/components/ui/page-specific-card.tsx
```

---

## Organize by Domain (single axis)

Organize `src/components/` by **domain**, not by element/primitive type. Use one
consistent axis so the folder list reads as product areas, not UI widgets.

Three structural folders plus domain folders:

```txt
src/components/ui/         # shadcn/ui primitives only
src/components/layout/     # site-wide layout & navigation (header, footer, nav)
src/components/shared/     # UI reused across 2+ domains
src/components/{domain}/   # one folder per product domain
```

Examples of domain folders:

```txt
src/components/category/
src/components/write/
src/components/profile/
src/components/pricing/
src/components/auth/
```

Placement rules:

- A component used by one page/domain → that domain folder.
- A component reused by **2 or more** domains → `shared/`.
- Site-wide layout/navigation → `layout/`.
- shadcn primitives → `ui/` (never business logic).
- Do not create element/primitive folders (`button/`, `table/`, `accordion/`)
  or one-file folders. Consolidate into the owning domain.
- Do not create a feature folder that just duplicates a domain.

---

## Structure as Documentation (central, not colocation)

Let the folder structure and the import graph document relationships, instead of
hand-maintained comments that drift out of sync. A component in
`src/components/{domain}/` and a query in `src/lib/supabase/` already declare
their ownership by location; "Find All References" shows every caller and never
goes stale, unlike an `@usedIn` list.

This project keeps a **central, layered** structure — it does NOT use Next.js
route colocation:

```txt
app/api/.../route.ts      # Route Handlers (central, under app/api)
src/lib/                  # data access, SDK clients, server integrations
src/utils/                # pure functions
src/components/{domain}/  # UI by domain
```

Rules:

- Do NOT create `app/<route>/_components/` or `app/<route>/_services/`
  colocation folders. Keep components in `src/components/`, data access in
  `src/lib/`, pure logic in `src/utils/`.
- Rely on location + the import graph to convey "where is this used"; reserve
  TSDoc for behavior, params, returns, and `@see {@link}` route links
  (see `typescript-and-tsdoc.md`).
- If a helper is single-domain, move it into that domain's folder rather than
  documenting its sole caller — the move makes the relationship self-evident.

---

## Component File Size

Keep component files small and focused.

Recommended guideline:

```txt
around 100 lines preferred
maximum 200 lines when practical
```

When a component grows too large, split it into:

- smaller subcomponents
- a custom hook
- a pure utility function
- a configuration object
- a separate constants file

Good extraction candidates:

- repeated JSX blocks
- complex conditional rendering
- form state logic
- data transformation logic
- event handling logic reused across components

Avoid extracting too early when the logic is used only once and still easy to read.

---

## Function Style

Use `function` declarations in App Router page and layout files when it improves framework readability.

Good in `app/`:

```tsx
export default async function Page() {
  return <main>Page</main>;
}
```

Good in `app/` layouts:

```tsx
export default function Layout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <>{children}</>;
}
```

Use arrow functions in `src/` files.

Good in `src/`:

```ts
export const formatDate = (date: Date): string => {
  return date.toISOString();
};
```

Avoid in `src/`:

```ts
export function formatDate(date: Date): string {
  return date.toISOString();
}
```

---

## Utility Extraction Rules

Only move helper functions into `src/utils/` when they are actually reused in at least two places.

Good:

```txt
Used by:
- src/components/write/date-field.tsx
- src/components/category/category-card.tsx

Move to:
src/utils/format-date.ts
```

Keep one-off helpers inside the same file.

Good:

```ts
const getVisibleItems = (items: Item[]): Item[] => {
  return items.filter((item) => item.visible);
};
```

Rules:

- Do not move helpers to `src/utils/` based only on expected future reuse.
- Check `src/utils/` before creating a new utility.
- Avoid duplicate utilities with slightly different names.
- Keep utilities pure when possible.
- Utilities should not depend on React rendering behavior.

---

## Avoid Generic Dumping Grounds

`src/components/shared/` is a sanctioned home for UI reused across 2+ domains —
but it is not a junk drawer. Only place a component there once it has a real
second consumer in a different domain; default new components to their owning
domain folder.

Keep `shared/` flat and bounded:

- Do NOT add subfolders inside `shared/` (e.g. `shared/form/`, `shared/ui/`).
  That just recreates scattered one-file folders one level deeper.
- When a cohesive group inside `shared/` grows to ~4+ related files, graduate
  it to a flat top-level concern folder (sibling of `layout/`, e.g. `motion/`,
  `form/`) — never a `shared/` subfolder.
- Re-check entry on every add: if a `shared/` component turns out to be used by
  only one domain, move it back to that domain folder.

Avoid creating or overusing vague folders like:

```txt
src/components/common/
src/components/misc/
src/utils/misc.ts
src/helpers/
```

Prefer domain-specific placement, with `shared/` reserved for genuine cross-domain reuse.

Good:

```txt
src/components/write/
src/components/layout/
src/components/shared/data-table.tsx   # used by category + page domains
src/utils/format-date.ts
src/utils/slugify.ts
```

---

## Naming Rules

Use descriptive names.

Good:

```txt
category-card.tsx
language-switcher.tsx
submit-button.tsx
format-date.ts
create-slug.ts
```

Avoid vague names:

```txt
card.tsx
helper.ts
utils.ts
component.tsx
data.ts
```

---

## Spacing: Prefer Flex Gap Over Margin

Use `flex flex-col gap-*` (or `flex-row gap-*`) instead of individual `mt-*` / `mb-*` on child elements.

Gap-based spacing is more predictable, easier to maintain, and avoids margin-collapse edge cases.

Good:

```tsx
<div className="flex flex-col gap-6">
  <Heading />
  <Content />
  <Footer />
</div>
```

Avoid:

```tsx
<div>
  <Heading />
  <Content className="mt-6" />
  <Footer className="mt-6" />
</div>
```

Rules:

- Default to `flex flex-col gap-*` for vertical stacking and `flex gap-*` or `flex-row gap-*` for horizontal layouts.
- Only use `mt-*` / `mb-*` when a single element genuinely needs unique spacing that differs from its siblings.
- For grid layouts, use `grid gap-*` instead of margins on grid children.
- When refactoring existing code, replace repeated `mt-*` / `mb-*` patterns with a parent `gap-*`.

---

## Global Base Styles for Repeated Elements

When an HTML element (e.g. `<section>`) is used across many pages with the same layout styles, define those styles once in `globals.css` under `@layer base` instead of repeating `className` on every instance.

Reference — current `globals.css` base styles:

```css
@layer base {
  section {
    @apply mx-auto box-border w-full max-w-7xl px-4 py-14;
  }
}
```

Rules:

- Use `@layer base` in `globals.css` for element-level defaults that apply project-wide (e.g. `section`, `body`, `*`).
- Only add element-level base styles for tags that are genuinely reused across multiple pages with identical layout.
- Page-specific overrides should still use `className` on the element.
- Do not put component-specific or feature-specific styles in `@layer base`. Use Tailwind utility classes or component-level styles instead.

---

## Review Checklist

- [ ] Is the component in the right folder?
- [ ] Is the file reasonably small?
- [ ] Should any logic be moved into a custom hook?
- [ ] Should any pure repeated logic be moved into `src/utils/`?
- [ ] Are `src/components/ui/` files left untouched?
- [ ] Are function declarations used only where allowed?
- [ ] Are arrow functions used in `src/`?