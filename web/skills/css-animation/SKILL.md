---
name: css-animation
description: Use this skill when writing, reviewing, or planning animations in a Next.js App Router project. Trigger this skill for tasks involving CSS keyframe animations, scroll-triggered fade-ins (IntersectionObserver), page-load transitions, interactive feedback, and deciding whether to use CSS or a JS animation library for a given use case.
---

# CSS Animation in Next.js

Use this skill to decide when and how to use CSS animations in a Next.js App
Router project without harming SEO or Core Web Vitals.

## Core Principle

> Content is rendered on the server. Animation is CSS-only or uses a minimal
> Client Component with IntersectionObserver.

This project uses **CSS `@keyframes` + utility classes** for all animations.
No JS animation library (framer-motion, etc.) is installed. This keeps the
client bundle small and avoids unnecessary `"use client"` boundaries.

## Core Rules

- Keep SEO-critical text (titles, descriptions, prices) in Server Components.
- Use CSS `@keyframes` + `animation` for page-load fade-in effects.
- Use `FadeInView` (IntersectionObserver-based) for scroll-triggered fade-ins.
- Prefer `opacity` and `transform` animations. Avoid animating layout size.
- Use CSS custom properties (`--fade-y`, `--fade-delay`, `--fade-duration`) for
  per-element customization.
- Only add `"use client"` for components that need IntersectionObserver or
  other browser APIs.

## Project Animation System

### Page-load fade-in (CSS only, no JS)

```tsx
// Server Component — no "use client" needed
<div className="animate-fade-in-up">
  <h1>Title</h1>
</div>

// With custom delay/duration
<div
  className="animate-fade-in-up"
  style={{ "--fade-delay": "0.15s", "--fade-duration": "0.5s" } as React.CSSProperties}
>
  <p>Content</p>
</div>
```

### Scroll-triggered fade-in (IntersectionObserver)

```tsx
import { FadeInView } from "@/components/shared/FadeInView";

// Wraps children, animates when scrolled into view
<FadeInView y={40} duration={0.6}>
  <section>...</section>
</FadeInView>

// Staggered cards
{items.map((item, index) => (
  <FadeInView key={item.id} y={30} delay={index * 0.1} duration={0.5}>
    <Card>...</Card>
  </FadeInView>
))}
```

### Bounce-in for CTA buttons

Single soft bounce for attention-grabbing elements. No infinite loop.

```tsx
// Scroll-triggered bounce-in via FadeInView
<FadeInView y={20} delay={0.25} duration={0.5} animation="bounce-in">
  <Button>Get Started</Button>
</FadeInView>

// Pure CSS bounce-in (page-load)
<div
  className="animate-bounce-in"
  style={{ "--bounce-delay": "0.2s" } as React.CSSProperties}
>
  <Button>Get Started</Button>
</div>
```

### Tailwind built-in animations (ongoing attention)

Use Tailwind's `animate-*` utilities for **ongoing infinite effects** on
non-SEO-critical UI elements. Combine with `FadeInView` by placing the
Tailwind class on the **inner element** (separate DOM node = no conflict).

| Class | Effect | Use case |
|-------|--------|----------|
| `animate-pulse` | Opacity fade (2s loop) | CTA buttons, notifications |
| `animate-bounce` | Vertical bounce (1s loop) | Scroll-down arrows |
| `animate-spin` | 360° rotation (1s loop) | Loading spinners |
| `animate-ping` | Scale + fade (1s loop) | Live badges, notification dots |

```tsx
// Entrance (wrapper) + ongoing (inner) — no conflict
<FadeInView y={20} delay={0.25} animation="bounce-in">
  <Button className="motion-safe:animate-pulse">Get Started</Button>
</FadeInView>
```

Use `motion-safe:` prefix to respect reduced-motion user preferences.

## Reference Files

Use these references when more detail is needed:

- `references/usage-guidelines.md` — when to use CSS vs JS animation, decision matrix, priority table.
- `references/code-patterns.md` — recommended component patterns, anti-patterns, and corrected examples.
- `references/bundle-optimization.md` — Client Component isolation strategies and performance tips.

## Workflow

When working on animation-related code:

1. Determine whether the target element is SEO-critical content or UI
   interaction.
2. Check `references/usage-guidelines.md` to decide CSS animation vs JS library.
3. For page-load animations, use `animate-fade-in-up` CSS class.
4. For scroll-triggered animations, use `FadeInView` component.
5. Verify the animation does not shift layout (CLS) or delay largest
   contentful paint (LCP).

## Output Style

When reviewing animation code, return:

- The issue.
- Why it matters (SEO, performance, bundle size).
- The recommended fix.
- A corrected Next.js example when useful.

When writing animation code, provide production-ready TypeScript examples that
follow these rules.
