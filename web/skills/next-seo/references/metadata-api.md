# Next.js Metadata API

Replace `[appName]` with the app name and `[domain]` with the production root domain before using these examples. Replace the brackets too; the app name and domain are separate values. Page topics and routes are examples to adapt to your project.

Use the Next.js Metadata API for SEO-related metadata in App Router projects.

## Purpose

This reference explains how to implement page-level SEO metadata in a Next.js App Router project.

Use this file when working on:

- `title`
- `description`
- `canonical`
- `openGraph`
- `twitter`
- `robots`
- `generateMetadata`
- dynamic route metadata

---

## Core Rules

- Use the Next.js Metadata API instead of manually adding SEO tags inside components.
- Every public indexable page must have a unique `title`.
- Every public indexable page must have a unique `description`.
- Every public indexable page must define a canonical URL.
- Public shareable pages must define `openGraph` and `twitter` metadata.
- Metadata should match the visible page content.
- Avoid duplicate `<title>`, `<meta>`, or `<link rel="canonical">` tags.
- Prefer static `metadata` when the values are known at build time.
- Use `generateMetadata` for dynamic routes.

---

## Static Metadata Example

Use `metadata` when page metadata is static.

```ts
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Privacy Policy Generator | [appName]',
  description: 'Create privacy policy pages for apps, SaaS products, and websites.',
  alternates: {
    canonical: '/en/privacy-policy',
  },
  openGraph: {
    title: 'Privacy Policy Generator | [appName]',
    description: 'Create privacy policy pages for apps, SaaS products, and websites.',
    url: '/en/privacy-policy',
    siteName: '[appName]',
    images: [
      {
        url: '/og/privacy-policy.png',
        width: 1200,
        height: 630,
        alt: '[appName] Privacy Policy Generator',
      },
    ],
    locale: 'en_US',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Privacy Policy Generator | [appName]',
    description: 'Create privacy policy pages for apps, SaaS products, and websites.',
    images: ['/og/privacy-policy.png'],
  },
};
```

---

## Dynamic Metadata Example

Use `generateMetadata` for dynamic routes such as:

- `app/[lang]/category/[categoryName]/page.tsx`
- `app/[lang]/[category]/[slug]/page.tsx`

```ts
import type { Metadata } from 'next';

type PageProps = {
  params: Promise<{
    lang: 'ko' | 'en';
    category: string;
    slug: string;
  }>;
};

export const generateMetadata = async ({
  params,
}: PageProps): Promise<Metadata> => {
  const { lang, category, slug } = await params;

  const title = `${slug} | [appName]`;
  const description = `View a ${category} page created with [appName].`;
  const canonical = `/${lang}/${category}/${slug}`;

  return {
    title,
    description,
    alternates: {
      canonical,
      languages: {
        ko: `/ko/${category}/${slug}`,
        en: `/en/${category}/${slug}`,
      },
    },
    openGraph: {
      title,
      description,
      url: canonical,
      siteName: '[appName]',
      type: 'article',
    },
    twitter: {
      card: 'summary_large_image',
      title,
      description,
    },
  };
};
```

---

## Robots Metadata

Use `robots` metadata when controlling index behavior per page.

```ts
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'My Page | [appName]',
  description: 'A public page created with [appName].',
  robots: {
    index: true,
    follow: true,
  },
};
```

For private, duplicate, temporary, or low-value pages:

```ts
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Preview | [appName]',
  description: 'Preview page.',
  robots: {
    index: false,
    follow: false,
  },
};
```

---

## Title Rules

Good titles:

```txt
Privacy Policy Generator | [appName]
Terms of Service Template | [appName]
Startup Landing Page Template | [appName]
```

Avoid:

```txt
Home
Page
Untitled
Privacy Policy Privacy Policy Privacy Policy
```

Rules:

- Keep titles descriptive and page-specific.
- Put the primary topic near the beginning.
- Include the brand name when useful.
- Avoid keyword stuffing.
- Avoid duplicate titles across indexable pages.

---

## Description Rules

Good descriptions:

```txt
Create privacy policy pages for apps, SaaS products, and websites with [appName].
```

Avoid:

```txt
Welcome to our website. This is a page.
```

Rules:

- Make descriptions page-specific.
- Summarize the actual page value.
- Avoid generic boilerplate.
- Avoid duplicate descriptions across indexable pages.
- Keep descriptions concise and natural.

---

## Open Graph Rules

Every public shareable page should include:

- `openGraph.title`
- `openGraph.description`
- `openGraph.url`
- `openGraph.siteName`
- `openGraph.images`
- `openGraph.type`

Recommended OG image size:

```txt
1200x630
```

---

## Twitter Card Rules

Use `summary_large_image` for public pages with a share image.

```ts
twitter: {
  card: 'summary_large_image',
  title: 'Privacy Policy Generator | [appName]',
  description: 'Create privacy policy pages for apps, SaaS products, and websites.',
  images: ['/og/privacy-policy.png'],
}
```

---

## Common Mistakes

- Adding metadata manually inside page components instead of using the Metadata API.
- Missing canonical URLs on public pages.
- Using the same title and description across many pages.
- Creating Open Graph metadata without an image.
- Setting `robots.index = true` on thin or duplicate pages.
- Cross-linking canonical URLs incorrectly between locales.
- Using dynamic metadata but not validating missing data cases.
- Returning vague fallback metadata for many different pages.

---

## Review Checklist

- [ ] Does the page use `metadata` or `generateMetadata`?
- [ ] Is the `title` unique and descriptive?
- [ ] Is the `description` unique and useful?
- [ ] Is `alternates.canonical` defined?
- [ ] Are `openGraph` and `twitter` metadata defined for public pages?
- [ ] Does metadata match the visible page content?
- [ ] Are non-indexable pages explicitly marked with `robots`?
- [ ] Are dynamic routes handling missing or invalid data safely?