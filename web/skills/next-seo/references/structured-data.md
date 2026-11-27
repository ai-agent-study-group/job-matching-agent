# Structured Data for Next.js

Replace `[appName]` with the app name and `[domain]` with the production root domain before using these examples. Replace the brackets too; the app name and domain are separate values. Page topics and routes are examples to adapt to your project.

Use this reference when adding or reviewing structured data in a Next.js App Router project.

Structured data helps search engines understand the meaning of a page, but it should only describe content that is actually visible to users.

---

## Core Principles

- Use `JSON-LD` for structured data.
- Add structured data only when it matches visible page content.
- Do not add fake reviews, fake ratings, fake authors, or unsupported schema.
- Keep structured data close to the page it describes.
- Prefer page-specific structured data over generic site-wide schema.
- Validate important pages with Google Rich Results Test or Schema Markup Validator.
- Avoid duplicating the same schema multiple times on one page.
- Localize structured data values for multilingual pages.

---

## When to Add Structured Data

Add structured data when the page has a clear matching schema type.

Good candidates:

- homepage
- category pages
- article-like pages
- FAQ pages
- breadcrumb navigation
- organization or brand information
- public template/detail pages

Avoid adding structured data when:

- the schema does not match the visible content
- the page has very thin content
- the page is private or non-indexable
- the schema would be misleading
- the data is generated only to influence search results

---

## Recommended Schema Types

For a Next.js content/template service, prioritize:

- `WebSite`
- `Organization`
- `BreadcrumbList`
- `Article`
- `FAQPage`
- `WebPage`
- `CollectionPage`

Use only the schema types that match the actual page.

---

## Next.js Implementation Pattern

In App Router, add JSON-LD inside the page component.

```tsx
const jsonLd = {
  '@context': 'https://schema.org',
  '@type': 'WebSite',
  name: '[appName]',
  url: 'https://[domain]',
};

export default function Page() {
  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <main>
        <h1>{'[appName]'}</h1>
      </main>
    </>
  );
}
```

---

## Safer JSON-LD Helper

Use a helper when multiple pages need JSON-LD rendering.

```tsx
type JsonLdProps = {
  data: Record<string, unknown>;
};

export const JsonLd = ({ data }: JsonLdProps) => {
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{
        __html: JSON.stringify(data).replace(/</g, '\\u003c'),
      }}
    />
  );
};
```

Usage:

```tsx
const websiteJsonLd = {
  '@context': 'https://schema.org',
  '@type': 'WebSite',
  name: '[appName]',
  url: 'https://[domain]',
};

export default function Page() {
  return (
    <>
      <JsonLd data={websiteJsonLd} />
      <main>
        <h1>{'[appName]'}</h1>
      </main>
    </>
  );
}
```

---

## WebSite Example

Use `WebSite` for the homepage or global site identity.

```ts
const websiteJsonLd = {
  '@context': 'https://schema.org',
  '@type': 'WebSite',
  name: '[appName]',
  url: 'https://[domain]',
  inLanguage: 'en',
};
```

For multilingual pages, set `inLanguage` dynamically.

```ts
const websiteJsonLd = {
  '@context': 'https://schema.org',
  '@type': 'WebSite',
  name: '[appName]',
  url: `https://[domain]/${lang}`,
  inLanguage: lang,
};
```

---

## Organization Example

Use `Organization` when describing the company or service owner.

```ts
const organizationJsonLd = {
  '@context': 'https://schema.org',
  '@type': 'Organization',
  name: '[appName]',
  url: 'https://[domain]',
  logo: 'https://[domain]/logo.png',
  sameAs: [],
};
```

Rules:

- `name` should match the visible brand name.
- `url` should use the canonical site URL.
- `logo` should be crawlable.
- Only include `sameAs` profiles that actually exist.

---

## BreadcrumbList Example

Use `BreadcrumbList` when the page has visible breadcrumb navigation.

```ts
const breadcrumbJsonLd = {
  '@context': 'https://schema.org',
  '@type': 'BreadcrumbList',
  itemListElement: [
    {
      '@type': 'ListItem',
      position: 1,
      name: 'Home',
      item: 'https://[domain]/en',
    },
    {
      '@type': 'ListItem',
      position: 2,
      name: 'Privacy Policy',
      item: 'https://[domain]/en/privacy-policy',
    },
  ],
};
```

Rules:

- Breadcrumb JSON-LD should match visible breadcrumbs.
- `position` should start from `1`.
- `item` should use absolute canonical URLs.
- Localize breadcrumb `name` values.

---

## Article Example

Use `Article` only for article-like or editorial pages.

```ts
const articleJsonLd = {
  '@context': 'https://schema.org',
  '@type': 'Article',
  headline: 'How to Create a Privacy Policy Page',
  description: 'A guide to creating a privacy policy page for apps and websites.',
  author: {
    '@type': 'Organization',
    name: '[appName]',
  },
  publisher: {
    '@type': 'Organization',
    name: '[appName]',
    logo: {
      '@type': 'ImageObject',
      url: 'https://[domain]/logo.png',
    },
  },
  mainEntityOfPage: 'https://[domain]/en/privacy-policy-guide',
};
```

Avoid `Article` for pages that are only forms, dashboards, or thin template listings.

---

## FAQPage Example

Use `FAQPage` only when the page visibly contains the same questions and answers.

```ts
const faqJsonLd = {
  '@context': 'https://schema.org',
  '@type': 'FAQPage',
  mainEntity: [
    {
      '@type': 'Question',
      name: 'Can I create a privacy policy page for my app?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'Yes. [appName] helps you create privacy policy pages for apps, SaaS products, and websites.',
      },
    },
    {
      '@type': 'Question',
      name: 'Can I publish the page publicly?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'Yes. Published pages can be shared through a public URL.',
      },
    },
  ],
};
```

Rules:

- FAQ content must be visible on the page.
- Do not add FAQ schema for hidden or unrelated questions.
- Keep answers concise and accurate.
- Localize FAQ schema per language.

---

## CollectionPage Example

Use `CollectionPage` for category listing pages.

```ts
const collectionPageJsonLd = {
  '@context': 'https://schema.org',
  '@type': 'CollectionPage',
  name: 'Privacy Policy Templates',
  description: 'Browse privacy policy page templates for apps and websites.',
  url: 'https://[domain]/en/category/privacy-policy',
};
```

Use this for:

- category pages
- template listing pages
- collection-style landing pages

---

## WebPage Example

Use `WebPage` for general static pages when no more specific schema applies.

```ts
const webPageJsonLd = {
  '@context': 'https://schema.org',
  '@type': 'WebPage',
  name: 'Contact [appName]',
  description: 'Contact [appName] for support or feedback.',
  url: 'https://[domain]/en/contact',
  inLanguage: 'en',
};
```

---

## Absolute URL Rules

Structured data should use absolute URLs.

Good:

```txt
https://[domain]/en/privacy-policy
```

Avoid:

```txt
/en/privacy-policy
```

Use absolute URLs for:

- `url`
- `item`
- `logo`
- `image`
- `mainEntityOfPage`

---

## Multilingual Structured Data

For multilingual pages:

- set `inLanguage`
- localize text values
- use locale-specific canonical URLs
- do not reuse English schema text on Korean pages
- keep schema content aligned with visible translated content

Example:

```ts
const webPageJsonLd = {
  '@context': 'https://schema.org',
  '@type': 'WebPage',
  name: lang === 'ko' ? '개인정보 처리방침 생성기' : 'Privacy Policy Generator',
  description:
    lang === 'ko'
      ? '앱과 웹서비스를 위한 개인정보 처리방침 페이지를 생성하세요.'
      : 'Create privacy policy pages for apps and websites.',
  url: `https://[domain]/${lang}/privacy-policy`,
  inLanguage: lang,
};
```

---

## Common Mistakes

- Adding schema that does not match visible content.
- Adding fake reviews or aggregate ratings.
- Using relative URLs inside JSON-LD.
- Forgetting to localize schema values.
- Adding FAQ schema for questions not shown on the page.
- Duplicating the same schema block multiple times.
- Using `Article` schema for non-article pages.
- Adding structured data to private, preview, or `noindex` pages.
- Injecting unsafe JSON without escaping `<`.

---

## Review Checklist

- [ ] Does the schema type match the visible page content?
- [ ] Is JSON-LD used?
- [ ] Are URLs absolute?
- [ ] Are text values localized?
- [ ] Is the schema added only once?
- [ ] Are fake reviews, ratings, or unsupported claims avoided?
- [ ] Does FAQ schema match visible FAQ content?
- [ ] Does breadcrumb schema match visible breadcrumbs?
- [ ] Is structured data omitted from private or `noindex` pages?
- [ ] Has the page been validated when the schema is important?