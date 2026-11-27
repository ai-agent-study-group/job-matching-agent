---
name: next-coding-rules
description: Use this skill when writing, reviewing, refactoring, or organizing code in a Next.js App Router project. Trigger this skill for tasks involving project structure, component organization, TypeScript strict mode, function style conventions, TSDoc, utility extraction, protected generated files, hooks, providers, src folder organization, and general Next.js coding standards.
---

# Next Coding Rules

Use this skill to follow consistent coding rules in a Next.js App Router project.

This skill focuses on:

- architecture and folder organization
- component placement
- function declaration style
- TypeScript strict mode
- TSDoc requirements
- utility extraction rules
- protected generated files
- spacing and layout conventions
- global base styles
- code review checklist

## Core Rules

- Keep `CLAUDE.md` or project-level agent instructions short.
- Put detailed coding rules in this skill and its `references/` files.
- Follow the existing project structure before creating new folders.
- Prefer small, focused components over large component files.
- Use (shadcn) `src/components/ui/` as generated UI primitives only.
- Organize `src/components/` by domain: domain folders, `layout/` for site-wide nav, `shared/` for UI reused by 2+ domains.
- Do not directly modify generated or protected files.
- Use TypeScript strictly and avoid `any`.
- Use arrow functions in `src/` files.
- Use `function` declarations only where the framework convention benefits from it, such as App Router page and layout files.

## Reference Files

Use these references when more detail is needed:

- `references/architecture-and-style.md` — component structure, central-vs-colocation (structure as documentation), function style, file size, utility extraction, spacing conventions, global base styles.
- `references/typescript-and-tsdoc.md` — TypeScript strict mode, type placement, TSDoc rules, data-access/API route TSDoc links (`@see {@link}`).
- `references/project-structure.md` — generic reusable Next.js folder structure.
- `references/protected-files.md` — files and folders that should not be directly edited.
- `references/review-checklist.md` — checklist before finishing code changes.

## Workflow

When working on code:

1. Identify whether the task touches `app/`, `src/`, generated UI files, shared types, hooks, or utilities.
2. Check the relevant reference file before proposing or writing code.
3. Preserve the existing folder structure unless there is a clear reason to change it.
4. Keep reusable logic in the correct layer:
   - UI(shadcn) primitives: `src/components/ui/`
   - domain components: `src/components/{domain}/` (layout/ for nav, shared/ for 2+ domain reuse)
   - shared hooks: `src/hooks/`
   - pure utilities: `src/utils/`
   - external SDK setup: `src/lib/`
5. Avoid premature abstraction.
6. Use explicit types.
7. Add TSDoc where required.
8. Mention validation commands when appropriate, such as `yarn type-check`, `yarn lint`, and `yarn build`.

## Output Style

When reviewing code, return:

- the issue
- why it matters
- the recommended fix
- a corrected example when useful

When writing code, provide production-ready TypeScript examples that follow these rules.