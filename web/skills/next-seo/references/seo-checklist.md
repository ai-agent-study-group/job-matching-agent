# Next.js SEO Checklist

Use this checklist when reviewing or implementing SEO in a Next.js App Router project.

This checklist focuses on:

- crawlability
- metadata
- rendering strategy
- Core Web Vitals
- multilingual SEO
- structured data
- content quality
- internal linking

---

# 1. URL Structure

## Rules

- URLs should be lowercase.
- URLs should use `kebab-case`.
- Public pages should avoid unnecessary query strings.
- Public pages should have stable canonical URLs.
- URL structure should remain consistent across the project.

Good:

```txt
/en/privacy-policy
/ko/terms-of-service
/en/startup-landing-page
```

Avoid:

```txt
/PrivacyPolicy
/privacy_policy
/page?id=privacy-policy
```

## Checklist

- [ ] URLs are lowercase.
- [ ] URLs use `kebab-case`.
- [ ] Public pages avoid unnecessary query parameters.
- [ ] Canonical URLs are stable and consistent.
- [ ] Duplicate URL variations are redirected or canonicalized.

---

# 2. Metadata

## Rules

Every public indexable page should define:

- `title`
- `description`
- `canonical`
- `openGraph`
- `twitter`

Metadata should:

- match visible content
- remain unique across pages
- avoid keyword stuffing
- avoid generic placeholders

## Checklist

- [ ] Every page has a unique `title`.
- [ ] Every page has a unique `description`.
- [ ] `canonical` URLs are defined.
- [ ] `openGraph` metadata exists.
- [ ] `twitter` metadata exists.
- [ ] Metadata matches visible content.
- [ ] No duplicate metadata across important pages.

---

# 3. Rendering Strategy

## Rules

SEO-critical pages should prefer:

- `SSG`
- `SSR`
- server-rendered metadata

Avoid relying entirely on client-side rendering for indexable content.

Important page content should exist in the initial HTML response.

## Checklist

- [ ] SEO-critical pages are server-rendered or statically generated.
- [ ] Important content exists in initial HTML.
- [ ] Unnecessary Client Components are minimized.
- [ ] Critical metadata is not generated only on the client.
- [ ] Suspense/loading states do not hide primary content excessively.

---

# 4. Heading Structure

## Rules

- Pages should have one clear `h1`.
- Heading hierarchy should remain logical.
- Headings should describe actual content.
- Headings should not exist only for styling.

Good:

```txt
h1 → h2 → h3
```

Avoid:

```txt
h1 → h4
multiple unrelated h1 tags
```

## Checklist

- [ ] One primary `h1` exists.
- [ ] Heading hierarchy is logical.
- [ ] Headings describe the visible content.
- [ ] Headings are not skipped unnecessarily.

---

# 5. Content Quality

## Rules

- Pages should provide unique value.
- Thin pages should be avoided.
- Duplicate pages should be canonicalized or excluded from indexing.
- Content should satisfy user intent.
- Generated pages should still contain meaningful information.

Avoid:

- placeholder pages
- auto-generated thin pages
- duplicated metadata
- near-identical pages

## Checklist

- [ ] Content is useful and unique.
- [ ] Thin content pages are avoided.
- [ ] Duplicate pages are handled correctly.
- [ ] Metadata reflects actual page content.
- [ ] Important pages provide sufficient detail.

---

# 6. Internal Linking

## Rules

- Important pages should receive internal links.
- Related pages should connect naturally.
- Anchor text should be descriptive.
- Orphan pages should be avoided.

Good:

```txt
Read the privacy policy template
Explore startup landing page templates
```

Avoid:

```txt
Click here
Read more
```

## Checklist

- [ ] Important pages are internally linked.
- [ ] Related pages link naturally.
- [ ] Anchor text is descriptive.
- [ ] Orphan pages do not exist.

---

# 7. Images

## Rules

- Meaningful images should include descriptive `alt`.
- Decorative images should use empty `alt=""`.
- Use `next/image` when appropriate.
- Define image dimensions to reduce CLS.
- Use optimized image formats when possible.

## Checklist

- [ ] Meaningful images include `alt`.
- [ ] Decorative images use empty alt text.
- [ ] `next/image` is used appropriately.
- [ ] Width and height are defined.
- [ ] Images are optimized for performance.

---

# 8. Core Web Vitals

## Rules

Avoid performance problems that hurt:

- `LCP`
- `CLS`
- `INP`

Common causes:

- excessive hydration
- large JavaScript bundles
- layout shifts
- blocking fonts
- oversized images
- unnecessary animations

## Checklist

- [ ] Large images are optimized.
- [ ] Layout shifts are minimized.
- [ ] Excessive client-side hydration is avoided.
- [ ] Heavy animations are minimized.
- [ ] Fonts load efficiently.
- [ ] Large unused JavaScript is reduced.

---

# 9. International SEO

## Rules

- Locale pages should use dedicated URLs.
- Locale pages should self-canonicalize.
- `hreflang` relationships should remain consistent.
- Metadata should be localized.
- Main content should be translated.

Good:

```txt
/en/privacy-policy
/ko/privacy-policy
```

Avoid:

```txt
/privacy-policy?lang=en
```

## Checklist

- [ ] Locale URLs are crawlable.
- [ ] Locale pages self-canonicalize.
- [ ] `hreflang` values are correct.
- [ ] Metadata is localized.
- [ ] Main content is translated.
- [ ] Locale URLs remain consistent.

---

# 10. Structured Data

## Rules

- Use JSON-LD.
- Structured data should match visible content.
- Use only valid schema types.
- Avoid fake or misleading schema.

Recommended schema types:

- `WebSite`
- `Organization`
- `BreadcrumbList`
- `Article`
- `FAQPage`

## Checklist

- [ ] Structured data uses JSON-LD.
- [ ] Schema matches visible content.
- [ ] Absolute URLs are used.
- [ ] Schema values are localized.
- [ ] Important pages validate successfully.

---

# 11. Indexation

## Rules

Only valuable public pages should be indexable.

Use `noindex` for:

- preview pages
- duplicate pages
- private pages
- temporary pages
- low-value utility pages

## Checklist

- [ ] Important pages are indexable.
- [ ] Low-value pages are `noindex`.
- [ ] Canonical URLs are correct.
- [ ] Robots directives are intentional.
- [ ] Duplicate pages are handled correctly.

---

# 12. Final Review

Before shipping:

- [ ] Metadata is complete.
- [ ] Canonical URLs are correct.
- [ ] Locale routing is consistent.
- [ ] Headings are logical.
- [ ] Internal links exist.
- [ ] Images are optimized.
- [ ] Structured data is valid.
- [ ] Content is useful.
- [ ] Performance issues are minimized.
- [ ] No major duplicate-content risks exist.