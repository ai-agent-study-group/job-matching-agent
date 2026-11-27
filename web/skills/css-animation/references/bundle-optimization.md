# Animation Bundle Optimization

## 1. CSS-first animation = zero JS cost

The primary optimization strategy: use CSS `@keyframes` animation instead of
JS animation libraries. This adds **zero bytes** to the client JavaScript
bundle.

```tsx
// ✅ Good — Server Component, no JS for animation
export default async function Page() {
  return (
    <div className="animate-fade-in-up">
      <h1>Zero JS animation cost</h1>
    </div>
  );
}
```

```tsx
// ❌ Bad — imports a JS animation library (adds ~30-50 KB gzipped)
"use client";

import { motion } from "framer-motion";

export default function Page() {
  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
      <h1>Expensive animation</h1>
    </motion.div>
  );
}
```

---

## 2. Minimize Client Components

Only use `"use client"` when the component needs browser APIs like
IntersectionObserver. The `FadeInView` component is the only animation-related
Client Component in the project.

```tsx
// ✅ Good — server content + minimal client animation
<ServerRenderedContent />
<FadeInView y={40}>
  <BelowFoldSection />
</FadeInView>
```

```tsx
// ❌ Bad — entire page is a Client Component for animation
"use client";

export default function Page() {
  return (
    <main>
      <h1>...</h1>
      <AnimatedSection />
    </main>
  );
}
```

---

## 3. CSS custom properties for flexibility

Instead of JavaScript logic to compute animation parameters, use CSS custom
properties. This keeps computation in the browser's style engine (fast) rather
than JavaScript (slower, increases bundle).

```tsx
// ✅ Good — CSS variables, no JS animation logic
<div
  className="animate-fade-in-up"
  style={{
    "--fade-delay": `${index * 0.06}s`,
    "--fade-duration": "0.3s",
    "--fade-y": "18px",
  } as React.CSSProperties}
>
```

---

## 4. When a JS animation library becomes necessary

If the project later needs complex animations (spring physics, drag, layout
animation, AnimatePresence), consider:

- **Isolate to smallest Client Component** — never wrap a whole page.
- **Use tree-shakeable imports** (e.g. `LazyMotion` with `domAnimation`).
- **Use `next/dynamic` with `ssr: false`** for modals, drawers, and other
  initially-hidden components.
- **Keep SEO-critical text in Server Components** — pass as `children` to
  animated wrappers.

---

## 5. Performance by page type

| Page type | Animation approach | JS cost |
|-----------|--------------------|---------|
| SEO pages (home, template, guide, example, pricing) | CSS `animate-fade-in-up` + `FadeInView` | ~1 KB (FadeInView only) |
| Auth pages (login) | CSS `animate-fade-in-up` | 0 KB |
| Protected pages (profile, write) | CSS `animate-fade-in-up` | 0 KB |
| Public page detail | CSS `animate-fade-in-up` | 0 KB |
| Contact page | CSS `animate-fade-in-up` | 0 KB |

---

## 6. CSS keyframes definition

All animation CSS is defined in `app/globals.css`:

```css
@keyframes fade-in-up {
  from {
    opacity: 0;
    transform: translateY(var(--fade-y, 40px));
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in-up {
  animation: fade-in-up var(--fade-duration, 0.6s) ease-out var(--fade-delay, 0s) both;
}
```

The `both` fill mode ensures elements start invisible and stay visible after
animation completes.
