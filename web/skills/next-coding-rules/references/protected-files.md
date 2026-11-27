# Protected Files

Use this reference before editing generated files, UI primitives, agent configuration, or schema-generated types.

Protected files and folders should not be directly modified unless the user explicitly asks for it and understands the risk.

---

## Common Protected Paths

```txt
/.agents/
/src/components/ui/
/src/types/*.database.types.ts
/src/types/supabase.database.types.ts
```

Project-specific protected paths may also exist. Always check the project instructions first.

---

## `/.agents/`

The `/.agents/` folder may contain agent configuration, skills, prompts, or automation-related files.

Rules:

- Do not rename this folder.
- Do not delete files inside it unless explicitly requested.
- Do not modify unrelated skills or agent configuration.
- When adding a new skill, create a dedicated skill folder instead of changing unrelated files.

Good:

```txt
/.agents/skills/next-coding-rules/
```

Avoid:

```txt
Editing unrelated existing skills without request.
Deleting existing agent configuration.
```

---

## `src/components/ui/`

The `src/components/ui/` folder is commonly used for generated UI primitives such as shadcn/ui components.

Rules:

- Do not directly modify generated UI primitives.
- Create wrapper components outside `ui/` when customization is needed.
- Keep business-specific logic out of `ui/`.

Good:

```txt
src/components/shared/submit-button.tsx
src/components/layout/theme-toggle.tsx
```

Avoid:

```txt
src/components/ui/business-submit-button.tsx
src/components/ui/category-filter-card.tsx
```

---

## Generated Database Types

Generated database type files should not be manually edited.

Examples:

```txt
src/types/supabase.database.types.ts
src/types/database.types.ts
```

Rules:

- Do not manually change generated schema types.
- Regenerate them from the source tool or CLI.
- Create separate adapter types if app-level transformations are needed.

Good:

```txt
src/types/profile.ts
src/types/page.ts
```

Avoid:

```txt
Manually editing src/types/supabase.database.types.ts
```

---

## What to Do Instead

When protected files need customization:

1. Create a wrapper.
2. Create an adapter.
3. Create a separate app-level type.
4. Regenerate from the official source.
5. Ask for confirmation if direct modification is unavoidable.

---

## Review Checklist

- [ ] Is the file generated?
- [ ] Is the file inside `src/components/ui/`?
- [ ] Is the file inside `/.agents/`?
- [ ] Is the file a database-generated type file?
- [ ] Can the change be made with a wrapper instead?
- [ ] Can the change be made with a separate app-level type instead?