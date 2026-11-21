# AGENTS.md

Guide for Codex and other coding agents. This folder (`web/`) is the
job-matching-agent frontend (Next.js JMA app). **Full guide: [CLAUDE.md](CLAUDE.md) is the
single source — read before working.** Below is a quick reference.

## Stack

Next.js 16 (App Router) · React 19 · TypeScript (strict) · Tailwind v4 · shadcn/ui
(Radix) · lucide-react · **Zustand** (client state) · **TanStack Query** (server data,
`components/shared/Providers.tsx`) · npm. Animation CSS-first. **No i18n** (single
language, `lang="ko"`). Cloudflare and test runners not adopted.

## Commands

```bash
npm install          # applies .npmrc legacy-peer-deps
npm run dev          # :3000
npm run build
npm run lint         # eslint
npm run type-check   # tsc --noEmit
```

## Must follow

- **Rules live in [`web/docs/`](docs/)** — [TECH.md](docs/TECH.md) (structure·stack·a11y) ·
  [AI_RULES.md](docs/AI_RULES.md) (server/client·declaration·lift state) ·
  [API.md](docs/API.md) (backend) · [TESTING.md](docs/TESTING.md) (responsive·a11y checks) ·
  [ANIMATION.md](docs/ANIMATION.md) · [FEATURE.md](docs/FEATURE.md).
- **Structure**: purpose-first layers. `app·components → domain → data·constants → utils·lib`.
  No reverse import. Alias `@/*` → `web/` root.
- **Components**: only route entry points use `export default function`; others are `const`
  arrow functions. Server Component by default, `'use client'` only when needed. No `any`.
- **`components/ui/` is shadcn output** — never edit directly; customize via wrappers outside.
- **shadcn add pitfall**: after `npx shadcn@latest add`, `cn` import breaks →
  `sed -i '' 's|from "cn"|from "@/utils/style"|g' components/ui/*.tsx`.
- **Tailwind**: default scale first, no arbitrary `[]` values. Tokens in `app/globals.css`.
- **Checks before commit/push**: after vibe-coding, pass `npm run type-check` → `lint` →
  `build` before committing. Stop and report on failure. Details in [CLAUDE.md](CLAUDE.md).
- **Skills**: before coding, use the relevant skill in `web/skills/` (`next-coding-rules`·
  `shadcn`·`next-seo`·`css-animation`·`frontend-design`).
- **Branch/PR**: branch from `main` as `<type>/<desc>`; code changes need PR + CI pass.
  Root [CONTRIBUTING.md](../CONTRIBUTING.md).

See [CLAUDE.md](CLAUDE.md) for details.
