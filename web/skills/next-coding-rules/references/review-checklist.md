# Code Review Checklist

Use this checklist before finalizing code changes in a Next.js App Router project.

---

## Architecture

- [ ] The file is placed in the correct folder.
- [ ] The change follows the existing project structure.
- [ ] No unnecessary new folder was introduced.
- [ ] No generic dumping-ground folder was created.
- [ ] Generated UI files were not directly modified.

---

## Components

- [ ] Component files are reasonably small.
- [ ] Large components are split when appropriate.
- [ ] Business-specific components are outside `src/components/ui/`.
- [ ] Repeated JSX is extracted when it improves readability.
- [ ] Client Components are used only when necessary.

---

## Function Style

- [ ] `app/` page and layout files use framework-friendly `function` declarations when appropriate.
- [ ] `src/` files use arrow functions.
- [ ] Helper functions are not prematurely moved to `src/utils/`.
- [ ] Shared utilities are reused instead of duplicated.

---

## TypeScript

- [ ] `any` is avoided.
- [ ] Exported functions have clear types.
- [ ] Shared types are placed in `src/types/`.
- [ ] Local-only types remain close to usage.
- [ ] Type assertions are avoided unless necessary.

---

## TSDoc

- [ ] Exported functions in `src/` have TSDoc.
- [ ] Module-level helpers in `src/` have TSDoc.
- [ ] `@param` and `@returns` are included where applicable.
- [ ] `@throws` is included when the function can throw.
- [ ] Inline handlers and hook callbacks are not over-documented.

---

## Imports

- [ ] Imports use `@/*` alias where appropriate.
- [ ] Unused imports are removed.
- [ ] Import paths are stable and readable.
- [ ] Circular dependencies are avoided.

---

## Protected Files

- [ ] `src/components/ui/` was not directly modified.
- [ ] `/.agents/` was not changed unintentionally.
- [ ] Generated database type files were not manually edited.
- [ ] Wrappers or adapters were used when possible.

---

## Validation

Run or recommend these checks when appropriate:

```bash
yarn type-check
yarn lint
yarn build
```

Optional:

```bash
yarn test:e2e
yarn format:check
```

---

## Final Response Checklist

When explaining the result:

- [ ] Mention important structural decisions.
- [ ] Mention any rule-based tradeoffs.
- [ ] Mention validation commands if relevant.
- [ ] Avoid over-explaining obvious code.