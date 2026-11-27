# CLAUDE.md

Guidance for Claude Code (claude.ai/code) in this repo. Keep concise and in English.

`web/` is the job-matching-agent frontend (JMA app). Docs default to Korean; keep
code identifiers and commands verbatim. Backend/doc tooling lives at repo root (`uv`/npm).

## Stack

Next.js 16 (App Router) · React 19 · TypeScript (strict) · Tailwind v4 ·
shadcn/ui (new-york, Radix) · lucide-react. Package manager: **npm**.

State: **Zustand** (client) · **TanStack Query** (server cache, injected in
`components/shared/Providers.tsx`). Animation: **CSS first**, Framer Motion only for
spring/drag/enter-exit (ANIMATION.md). **No i18n** — single language, `<html lang="ko">`
fixed; no `[lang]` segment, Dictionary, hreflang, or next-intl. Local storage
(`idb`/`localforage`), test runners (Vitest/Playwright), and Cloudflare are **not set up**.

## Commands

```bash
npm install          # applies .npmrc legacy-peer-deps=true (shadcn peer conflicts)
npm run dev          # http://localhost:3000
npm run build
npm run lint         # eslint
npm run type-check   # tsc --noEmit
npm run format       # prettier --write (excludes docs/·skills/·components/ui/)
```

No test runner yet (Vitest/Playwright not configured).

## Required checks before commit or push

After AI vibe-coding, always run the checks before committing or pushing.

- Inspect `package.json` and `.github/workflows/` to find required checks. Use npm (CI-equivalent).
- Run in dependency order: `npm run type-check` → `npm run lint` → `npm run build`
  (add `npm run format:check`·`npm run generate:types` when relevant). Don't skip for
  small or docs-only changes.
- Commit or push only after every check passes for the exact staged content.
- If a check fails or can't run (missing deps, credentials, services), stop and report.
  Never mark an unrun check as passed or bypass hooks. Report unconfigured categories
  (e.g. test runner) as "not configured".
- Summarize the commands run and their results before committing or pushing.

## Source of truth — `web/docs/`

FE rules live in **[`web/docs/`](docs/)**. Read before coding. **CLAUDE.md is a summary;
these are canonical.**

- [TECH.md](docs/TECH.md) — stack, purpose-first layers, state, accessibility (a11y), SEO, naming, performance.
- [AI_RULES.md](docs/AI_RULES.md) — server/client split, declaration style, lift state up, Tailwind priority, JSDoc, response rules.
- [API.md](docs/API.md) — backend API, type reuse, loading/error/empty states, resume-matching flow.
- [TESTING.md](docs/TESTING.md) — pre-commit manual checks: responsive, keyboard/a11y, supported browsers.
- [ANIMATION.md](docs/ANIMATION.md) — animation vocabulary and CSS implementation.
- [FEATURE.md](docs/FEATURE.md) — shared feature patterns (settings, share, error handling).
- [DESIGN.md](docs/DESIGN.md) — LinkedIn-style design tone: tokens, layout, component patterns.

## Architecture (purpose-first layers)

Split code by **what it does** into purpose folders at root. No `src/` wrapper, no
`features/` isolation. Alias `@/*` → `web/` root. Dependencies flow top→down only, no reverse import.

```
app·components  →  domain  →  data·constants  →  utils·lib
(pages·UI)         (app logic)  (data·config)      (pure utils·external)
```

- `app/` — App Router pages, layouts, route handlers, sitemap, robots.
- `components/` — `ui/` (shadcn output) · `layout/` (global nav) · `shared/` (reused by 2+ domains) · `<domain>/`. No colocation (`_components`); centralize.
- `domain/` — app-specific logic (calc·matching·validation). No UI import, pure functions.
- `constants/` — fixed config (`site.ts` `SITE_URL`). No hardcoding elsewhere.
- `utils/` — pure utils (`style.ts` `cn`). `lib/` — external SDK / infra adapters only.

### Component rules (core)

- Only route entry points (`app/**/page.tsx`·`layout.tsx`·`error.tsx`) use
  `export default function`; all other components are `const` arrow functions.
- **Server Component** by default; `'use client'` only for user input / browser APIs.
  Indexable content renders server-side (SEO).
- `components/ui/` is shadcn output — **never edit directly**. Customize via wrappers outside `ui/`.
- Tailwind: default scale first, no arbitrary `[]` values. Brand values as `globals.css` tokens (`bg-brand-subtle`).
- No `any`.
- JSDoc (`@param {type} name - desc`, `@returns {type}`) above every top-level
  function/component. Format: [AI_RULES.md](docs/AI_RULES.md) › 함수 주석 (JSDoc).

## Style tokens

`app/globals.css` is the single source. Implement the palette as shadcn semantic
tokens (`--background`·`--primary`…) + brand/status tokens (`--brand-hover`·`--brand-subtle`·
`--success`·`--warning`) + light/dark blocks. Tone: LinkedIn web (blue `#0A66C2`, warm gray bg, white cards). Change
colors/radius here only.

State location, responsive, backend API, and accessibility rules moved out —
see [AI_RULES.md](docs/AI_RULES.md) · [API.md](docs/API.md) ·
[TESTING.md](docs/TESTING.md) · [TECH.md](docs/TECH.md).

## Adding shadcn components

`components.json` `aliases.utils` is `@/lib/utils`; `web/lib/utils.ts` is a shim
re-exporting the real `cn` (`utils/style.ts`). This keeps the TECH.md rule (cn lives
in `utils/style.ts`) while shadcn generates `import { cn } from "@/lib/utils"` correctly.
Previously the utils alias was `@/utils/style`, so `add` broke as `import { cn } from "cn"`
and installed a fake `cn` npm package, needing sed·uninstall each time — fixed by the shim.

Generated `hooks/use-mobile.ts` hits next's strict rule and is in `eslint.config.mjs`
ignore (generated, not edited).

## Skills

Before coding, use the relevant skill in `web/skills/`: `next-coding-rules`, `shadcn`,
`next-seo`, `css-animation`, `frontend-design`. Follow project rules where a generic
skill example differs.

## Branch / PR

Branch from `main` as `<type>/<short-desc>` (`feat`·`fix`·`refactor`·`test`·`docs`·`chore`).
Code/UI/config changes need PR + 1 approval + CI pass. See root [CONTRIBUTING.md](../CONTRIBUTING.md).
