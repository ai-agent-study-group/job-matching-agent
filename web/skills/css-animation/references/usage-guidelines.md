# Animation Usage Guidelines

## Decision Rule

Ask these questions before choosing an animation approach:

1. Is this element SEO-critical text (title, body, price, category name)?
2. Can the effect be achieved with CSS `transition` or `@keyframes`?
3. Will this animation affect LCP or cause layout shift (CLS)?
4. Does this require the entire page to be a Client Component?

If **any** answer is "yes", use CSS animation or restructure the component tree.

---

## When to use CSS animation (default)

| Effect | Approach |
|--------|----------|
| Page-load fade-in | `animate-fade-in-up` CSS class |
| Scroll-triggered fade-in | `FadeInView` component (IntersectionObserver) |
| CTA button bounce | `animate-bounce-in` CSS class or `FadeInView` with `animation="bounce-in"` |
| CTA button pulse (ongoing) | Tailwind `animate-pulse` on inner element, combined with `FadeInView` entrance |
| Scroll-down arrow bounce | Tailwind `animate-bounce` on the arrow icon |
| Loading spinner | Tailwind `animate-spin` on the loader icon |
| Live badge / notification dot | Tailwind `animate-ping` on the indicator |
| Hover scale / shadow | CSS `transition` |
| Skeleton shimmer | CSS `@keyframes` |
| Link underline on hover | CSS `transition` |
| Card hover lift | CSS `transform` + `transition` |
| Staggered entrance | `FadeInView` with `delay` prop or CSS `--fade-delay` |

## When a JS animation library may be justified

Only consider adding a JS animation library (framer-motion, etc.) when **all**
of these are true:

- The animation requires **spring physics**, **layout animation**, **drag**,
  **AnimatePresence** (enter/exit), or **gesture-based** interaction.
- CSS cannot achieve the effect.
- The Client Component boundary is small and isolated.
- The element is **not** SEO-critical text.

Current project status: **No JS animation library is installed.** All
animations use CSS `@keyframes` and `FadeInView` (IntersectionObserver).

---

## Page-Type Matrix

### CSS animation (current approach)

| Area | Pattern |
|------|---------|
| Landing page sections | `animate-fade-in-up` for hero, `FadeInView` for below-fold sections |
| Category / template / guide lists | `FadeInView` with staggered `delay` per card |
| Pricing page | `animate-fade-in-up` for header, `FadeInView` for plan cards and FAQ |
| Login page | `animate-fade-in-up` with staggered `--fade-delay` |
| Profile page | `animate-fade-in-up` with staggered `--fade-delay` per card |
| Contact page | `animate-fade-in-up` for header and form |
| Public page detail | `animate-fade-in-up` for content sections |

### Would need JS library (not currently used)

| Area | Examples |
|------|----------|
| Modals with enter/exit animation | Login modal, image lightbox, cart drawer |
| Drag interactions | Sortable lists, drag-to-reorder |
| Spring physics | Bouncy buttons, elastic scroll |
| Layout animations | Shared element transitions, auto-height |

---

## Combining entrance + ongoing animations

Entrance animations (`FadeInView`, `animate-fade-in-up`, `animate-bounce-in`)
fire once. Ongoing Tailwind animations (`animate-pulse`, `animate-bounce`,
`animate-spin`, `animate-ping`) loop infinitely. To combine them:

1. Place the entrance animation on a **wrapper** element (`FadeInView`).
2. Place the Tailwind ongoing animation on the **inner** element.
3. They animate separate DOM nodes — no `animation` property conflict.

```tsx
<FadeInView y={20} animation="bounce-in">     {/* entrance: wrapper */}
  <Button className="animate-pulse">CTA</Button> {/* ongoing: inner */}
</FadeInView>
```

Always add `motion-safe:` prefix for ongoing animations to respect users who
prefer reduced motion: `motion-safe:animate-pulse`.

---

## Avoid

| Pattern | Why |
|---------|-----|
| Entire page as `"use client"` | Inflates client bundle; SSR benefits lost |
| SEO content rendered after JS | Google processes JS in stages; server-render is safer |
| Layout-shifting animation (`height: 0` → `auto`) | Degrades CLS |
| JS library for simple fade-in | Unnecessary bundle size increase |
| Ongoing animation on SEO-critical text | Distracting; may degrade accessibility |
| Ongoing animation without `motion-safe:` | Ignores reduced-motion user preference |

---

## Decision Checklist

### Use CSS animation when any is true

- [ ] The effect is a simple fade, slide, or scale.
- [ ] The element is SEO-critical text.
- [ ] The animation runs on page load or scroll-into-view.
- [ ] No gesture, spring, or enter/exit logic is needed.
- [ ] Keeping the component as a Server Component is preferred.

### Consider JS library when all are true

- [ ] The element is **not** SEO-critical text.
- [ ] The page works without this animation (core info is still visible).
- [ ] The Client Component boundary is small and isolated.
- [ ] Layout size stays the same before and after animation.
- [ ] CSS cannot achieve the desired effect (spring, drag, AnimatePresence).
- [ ] The animation is lightweight on low-end mobile devices.
