# CSS Animation Code Patterns

## Pattern 1 — Page-load fade-in (Server Component)

No `"use client"` needed. Pure CSS animation plays on mount.

```tsx
// page.tsx — Server Component
export default async function LandingPage() {
  return (
    <main>
      <div className="animate-fade-in-up">
        <h1>AI 기반 업무 자동화 플랫폼</h1>
        <p>반복 업무를 줄이고 팀의 생산성을 높이세요.</p>
      </div>
    </main>
  );
}
```

---

## Pattern 2 — Custom delay and duration

Use CSS custom properties for per-element timing.

```tsx
// Server Component — no "use client" needed
<div
  className="animate-fade-in-up"
  style={{
    "--fade-y": "20px",
    "--fade-delay": "0.15s",
    "--fade-duration": "0.5s",
  } as React.CSSProperties}
>
  <Card>...</Card>
</div>
```

Available CSS variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `--fade-y` | `40px` | Initial translateY offset |
| `--fade-delay` | `0s` | Animation delay |
| `--fade-duration` | `0.6s` | Animation duration |

---

## Pattern 3 — Staggered entrance (Server Component)

Use incrementing `--fade-delay` for stagger effect.

```tsx
// Server Component
{items.map((item, index) => (
  <div
    key={item.id}
    className="animate-fade-in-up"
    style={{
      "--fade-y": "18px",
      "--fade-duration": "0.3s",
      "--fade-delay": `${Math.min(index * 0.06, 0.3)}s`,
    } as React.CSSProperties}
  >
    <Card>{item.title}</Card>
  </div>
))}
```

---

## Pattern 4 — Scroll-triggered fade-in (FadeInView)

Use `FadeInView` for sections that should animate when scrolled into view.
This is a Client Component using IntersectionObserver.

```tsx
import { FadeInView } from "@/components/shared/FadeInView";

// Server Component page
export default async function PricingPage() {
  return (
    <section>
      <div className="animate-fade-in-up">
        <h1>Pricing</h1>
      </div>

      <FadeInView as="div" y={40}>
        <div className="grid gap-4 md:grid-cols-2">
          {plans.map((plan, index) => (
            <FadeInView key={plan.name} y={30} delay={index * 0.1} duration={0.5}>
              <Card>...</Card>
            </FadeInView>
          ))}
        </div>
      </FadeInView>
    </section>
  );
}
```

### FadeInView Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `ReactNode` | — | Content to animate |
| `as` | `"div" \| "section"` | `"div"` | HTML element tag |
| `animation` | `"fade-in-up" \| "bounce-in"` | `"fade-in-up"` | Animation variant |
| `className` | `string` | — | Additional CSS classes |
| `y` | `number` | `30` | Initial translateY in px |
| `delay` | `number` | `0` | Animation delay in seconds |
| `duration` | `number` | `0.6` | Animation duration in seconds |
| `threshold` | `number` | `0.1` | IntersectionObserver threshold |

---

## Pattern 5 — Bounce-in for CTA buttons

Single soft bounce for attention-grabbing elements like CTA buttons.
Uses `cubic-bezier(0.34, 1.56, 0.64, 1)` for a natural overshoot feel.

```tsx
import { FadeInView } from "@/components/shared/FadeInView";

// Bounce-in on scroll — ideal for CTA buttons
<FadeInView y={20} delay={0.25} duration={0.5} animation="bounce-in">
  <Button asChild>
    <Link href="/write">페이지 작성하기</Link>
  </Button>
</FadeInView>
```

Pure CSS version (page-load, no IntersectionObserver):

```tsx
// Server Component — no "use client" needed
<div
  className="animate-bounce-in"
  style={{
    "--bounce-y": "16px",
    "--bounce-delay": "0.2s",
    "--bounce-duration": "0.5s",
  } as React.CSSProperties}
>
  <Button>Get Started</Button>
</div>
```

Available CSS variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `--bounce-y` | `20px` | Initial translateY offset |
| `--bounce-delay` | `0s` | Animation delay |
| `--bounce-duration` | `0.5s` | Animation duration |

---

## Pattern 6 — Tailwind built-in animations (ongoing)

Tailwind provides built-in infinite animation utilities. These are best for
**ongoing attention effects** on non-SEO-critical UI elements (buttons, icons,
loaders). Combine with `FadeInView` entrance animation by placing the Tailwind
class on the **inner element** to avoid `animation` property conflicts.

### Available Tailwind animation utilities

| Class | Effect | Use case |
|-------|--------|----------|
| `animate-pulse` | Opacity fade in/out (2s, infinite) | CTA buttons, notifications |
| `animate-bounce` | Vertical bounce (1s, infinite) | Scroll-down indicator, arrows |
| `animate-spin` | 360° rotation (1s, infinite) | Loading spinners |
| `animate-ping` | Scale + fade out (1s, infinite) | Notification dots, live badges |

### Entrance + ongoing animation combo

Place the entrance animation (`FadeInView`) on the wrapper and the ongoing
Tailwind animation on the inner element. They animate separate DOM nodes, so
no `animation` property conflict occurs.

```tsx
import { FadeInView } from "@/components/shared/FadeInView";

// Entrance: bounce-in on scroll (wrapper div)
// Ongoing: pulse on the button itself
<FadeInView y={20} delay={0.25} duration={0.5} animation="bounce-in">
  <Button className="animate-pulse" asChild>
    <Link href="/write">페이지 작성하기</Link>
  </Button>
</FadeInView>

// Bounce arrow to hint "scroll down"
<FadeInView y={10} duration={0.4}>
  <ArrowDown className="animate-bounce h-5 w-5" />
</FadeInView>

// Loading indicator with entrance
<FadeInView y={10} duration={0.3}>
  <Loader2 className="animate-spin h-5 w-5" />
</FadeInView>
```

### Reduced motion

Use `motion-safe:` prefix to respect user preferences:

```tsx
<Button className="motion-safe:animate-pulse">Submit</Button>
```

---

## Pattern 7 — Error/feedback animation

Short, subtle animation for error messages or status changes.

```tsx
{error && (
  <div
    className="animate-fade-in-up"
    style={{ "--fade-y": "-6px", "--fade-duration": "0.2s" } as React.CSSProperties}
  >
    <p className="text-destructive text-sm">{error}</p>
  </div>
)}
```

---

## Anti-Patterns

### Bad — Using a JS animation library for simple fade-in

```tsx
// ❌ Do not do this — adds unnecessary JS bundle
"use client";

import { motion } from "framer-motion";

export default function Page() {
  return (
    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
      <h1>Title</h1>
    </motion.div>
  );
}
```

Fix: Use CSS animation.

```tsx
// ✅ Correct — no JS needed
export default function Page() {
  return (
    <div className="animate-fade-in-up">
      <h1>Title</h1>
    </div>
  );
}
```

### Bad — Making a Server Component into Client Component for animation

```tsx
// ❌ Do not do this
"use client";

export default function Page() {
  // Now loses SSR benefits just for a fade-in
  return <div className="animate-fade-in-up">...</div>;
}
```

Fix: `animate-fade-in-up` is pure CSS. It works in Server Components.

### Bad — Layout-shifting animation

```css
/* ❌ Causes CLS */
@keyframes expand {
  from { height: 0; }
  to { height: auto; }
}
```

Fix: Use `opacity` and `transform` only. Reserve space with CSS.

```css
/* ✅ No layout shift */
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
```
