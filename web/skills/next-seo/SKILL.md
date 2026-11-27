---
name: nextjs-seo
description: Use this skill when implementing, reviewing, or improving SEO in a Next.js App Router project. Trigger this skill for tasks involving metadata, canonical URLs, Open Graph, Twitter cards, robots, sitemap, hreflang, international SEO, structured data, SSR/SSG rendering strategy, Core Web Vitals, image SEO, internal links, or SEO-related code review.
---

# Next.js SEO

Use this skill to implement and review SEO for Next.js App Router projects.

## Core Principles

- Prefer server-rendered or statically generated pages for SEO-critical routes.
- Ensure important page content is available in the initial HTML.
- Use the Next.js Metadata API instead of manually writing head tags unless there is a specific reason.
- Keep URLs lowercase and `kebab-case`.
- Avoid unnecessary `query string` URLs for indexable public pages.
- Always define clear `canonical` URLs for public pages.
- Provide `openGraph` and `twitter` metadata for public pages.
- Use meaningful heading hierarchy: `h1` → `h2` → `h3`.
- Avoid creating thin, duplicate, or near-duplicate indexable pages.
- Minimize unnecessary Client Components on SEO-critical pages.

## Reference Files

Use the reference files when the task requires more detail:

- `references/metadata-api.md` — Next.js metadata implementation examples.
- `references/structured-data.md` — JSON-LD and Schema.org implementation.
- `references/seo-checklist.md` — practical SEO review checklist.

## Workflow

1. Identify whether the page is SEO-critical.
2. Check rendering strategy: prefer `SSG`, `SSR`, or static metadata where possible.
3. Review URL, canonical, metadata, Open Graph, and Twitter card settings.
4. Check heading structure and content quality.
5. Check image SEO and Core Web Vitals risks.
6. For multilingual pages, verify locale URLs, canonical URLs, and `hreflang`.
7. Add structured data only when it matches the visible page content.
8. Provide code examples using Next.js App Router conventions.

## Output Style

When reviewing SEO code, return:

- The issue.
- Why it matters.
- The recommended fix.
- A corrected Next.js example when useful.

When implementing SEO code, provide production-ready TypeScript examples.