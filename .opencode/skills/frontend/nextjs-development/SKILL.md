---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-15
name: nextjs-development
description: Next.js development best practices covering App Router, server components, data fetching, and deployment
category: frontend
version: 0.1.0
author: devtiagoabreu
tags: [nextjs, react, app-router, server-components, deployment, vercel]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Node.js 18 or newer
  - A Next.js project (App Router recommended)
provides:
  - App Router structure and conventions
  - Server vs client component guidance
  - Data fetching and caching patterns
  - Deployment to Vercel and self-hosted setups
---

# Next.js Development

## Overview

This skill is a guide to building production-grade applications with Next.js
using the App Router. It covers project structure, the server/client component
model, data fetching strategies, and deployment to Vercel. Following these
patterns keeps applications fast, maintainable, and aligned with the framework
recommendations. It targets Next.js 14 and newer.

## Prerequisites

- Node.js 18 or newer installed locally
- An existing Next.js project or the ability to create one
- Understanding of React fundamentals and JavaScript

## Usage Instructions

Use this skill when creating or modifying pages, layouts, and data fetching
logic in a Next.js application. Follow the App Router conventions described
below and validate with `npm run build` before pushing.

## Project Structure

```
app/
├── layout.js        # Root layout
├── page.js          # Home page
├── globals.css
├── (auth)/
│   ├── login/page.js
│   └── register/page.js
├── dashboard/
│   ├── layout.js
│   ├── page.js
│   └── settings/page.js
components/
lib/
public/
```

## Server and Client Components

### Server components by default

```javascript
// app/products/page.js
import { getProducts } from "@/lib/products";

export default async function ProductsPage() {
  const products = await getProducts();
  return (
    <ul>
      {products.map((product) => (
        <li key={product.id}>{product.name}</li>
      ))}
    </ul>
  );
}
```

### Add client components only when needed

Mark a component with `"use client"` when it needs state, effects, or event
handlers:

```javascript
"use client";

import { useState } from "react";

export default function SearchInput({ onSearch }) {
  const [query, setQuery] = useState("");
  return (
    <input
      value={query}
      onChange={(e) => setQuery(e.target.value)}
      onKeyDown={(e) => e.key === "Enter" && onSearch(query)}
    />
  );
}
```

## Data Fetching

### Fetch in server components

```javascript
export default async function ProfilePage({ params }) {
  const res = await fetch(`/api/users/${params.id}`, {
    next: { revalidate: 3600 },
  });
  const user = await res.json();
  return <h1>{user.name}</h1>;
}
```

### Use the Route Handlers pattern for APIs

```javascript
// app/api/search/route.js
import { NextResponse } from "next/server";

export async function GET(request) {
  const { searchParams } = new URL(request.url);
  const q = searchParams.get("q");
  const results = await search(q);
  return NextResponse.json({ results });
}
```

## Styling

Use CSS Modules or Tailwind CSS. CSS Modules keep styles co-located:

```javascript
// components/Card.js
import styles from "./Card.module.css";

export function Card({ title, children }) {
  return (
    <div className={styles.card}>
      <h2>{title}</h2>
      {children}
    </div>
  );
}
```

## Deployment to Vercel

1. Commit and push to GitHub.
2. Import the repository in Vercel.
3. Vercel detects Next.js and uses the default build settings.
4. Configure environment variables in the Vercel dashboard.

### Environment variables

```bash
DATABASE_URL=postgres://user:password@host:5432/db
NEXT_PUBLIC_API_URL=https://api.example.com
```

Reference them safely:

```javascript
const dbUrl = process.env.DATABASE_URL;
```

## Common Pitfalls

- Using client components for everything and losing the server rendering benefits
- Fetching the same data in multiple components instead of lifting to a parent
- Hard-coding environment variables or API URLs
- Forgetting `next: { revalidate }` for static content that changes

## Examples

### Dynamic route with loading state

```javascript
// app/blog/[slug]/page.js
export default async function PostPage({ params }) {
  const post = await getPost(params.slug);
  return (
    <article>
      <h1>{post.title}</h1>
      <div dangerouslySetInnerHTML={{ __html: post.content }} />
    </article>
  );
}

// app/blog/[slug]/loading.js
export default function Loading() {
  return <p>Loading post...</p>;
}
```
