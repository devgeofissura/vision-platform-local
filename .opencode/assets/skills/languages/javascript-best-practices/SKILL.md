---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-15
name: javascript-best-practices
description: JavaScript best practices covering modern ES2015+ syntax, modules, async patterns, and tooling
category: languages
version: 0.1.0
author: devtiagoabreu
tags: [javascript, es6, es2015, modules, async, nodejs]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Node.js 18 or newer
  - npm, yarn, pnpm, or bun package manager
provides:
  - Modern JavaScript syntax guidance (ES2015+)
  - Async programming patterns (Promises, async/await)
  - Module system best practices (ESM vs CJS)
  - Project structure and linting conventions
---

# JavaScript Best Practices

## Overview

This skill is a practical guide to writing clean, maintainable JavaScript. It
covers modern ES2015+ features, structuring code with modules, handling
asynchronous flows without callback hell, and configuring tooling such as
linters and formatters. The guidance applies to browser code, Node.js
backends, and shared libraries alike. Following these conventions makes code
easier to read, test, and debug across teams.

## Prerequisites

- Node.js 18 or newer installed locally
- A package manager (npm, yarn, pnpm, or bun)
- Basic familiarity with the JavaScript language

## Usage Instructions

Use this skill whenever you write or review JavaScript. Apply the patterns
below before finalizing a feature, and run the tooling checks before commit.

## Modern Syntax

### Prefer const and let over var

```javascript
// Prefer:
const MAX_RETRIES = 3;
let counter = 0;

// Avoid:
var name = "legacy";
```

### Use template literals

```javascript
const user = { name: "Ana", role: "admin" };
console.log(`Hello ${user.name}, your role is ${user.role}`);
```

### Use destructuring

```javascript
const { name, role } = user;
const [first, ...rest] = [1, 2, 3, 4];
```

## Asynchronous Patterns

### Prefer async/await over raw promises

```javascript
async function fetchUser(id) {
  const response = await fetch(`/api/users/${id}`);
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }
  return response.json();
}
```

### Handle errors with try/catch

```javascript
async function loadDashboard() {
  try {
    const user = await fetchUser(1);
    render(user);
  } catch (error) {
    console.error("Failed to load dashboard:", error);
    showError(error.message);
  }
}
```

### Run independent tasks in parallel

```javascript
const [users, posts] = await Promise.all([
  fetchUsers(),
  fetchPosts(),
]);
```

## Modules

### Use ESM for modern projects

```javascript
// utils/format.js
export function formatDate(date) {
  return new Intl.DateTimeFormat("pt-BR").format(date);
}

// app.js
import { formatDate } from "./utils/format.js";
```

### Keep modules small and focused

Each module should export one main concern. Split helpers by domain
(e.g., `format.js`, `validate.js`, `api.js`) instead of one giant file.

## Tooling

### Configure ESLint

```json
{
  "env": { "es2022": true, "node": true },
  "parserOptions": { "ecmaVersion": 2022, "sourceType": "module" },
  "extends": ["eslint:recommended"],
  "rules": {
    "no-unused-vars": "warn",
    "no-console": "off"
  }
}
```

### Add a test runner

```bash
npm install --save-dev vitest
```

```javascript
import { describe, it, expect } from "vitest";
import { formatDate } from "./utils/format.js";

describe("formatDate", () => {
  it("formats a date in pt-BR", () => {
    expect(formatDate(new Date("2026-08-15"))).toBe("15/08/2026");
  });
});
```

## Security Checklist

- Never commit secrets or API keys in source code
- Validate and sanitize all external input before use
- Escape output rendered into the DOM to prevent XSS
- Keep dependencies updated and audit them regularly

## Common Pitfalls

### Comparing without strict equality

```javascript
if (count === 0) { /* correct */ }
if (count == 0) { /* loose, avoid */ }
```

### Blocking the event loop

Avoid heavy synchronous work in hot paths. Offload CPU-bound tasks to worker
threads or batch processing instead.

## Examples

### Fetching data with pagination

```javascript
async function fetchAllPages(baseUrl, pageSize = 100) {
  const items = [];
  let page = 1;
  let hasMore = true;

  while (hasMore) {
    const url = `${baseUrl}?page=${page}&size=${pageSize}`;
    const response = await fetch(url);
    const data = await response.json();
    items.push(...data.items);
    hasMore = data.items.length === pageSize;
    page += 1;
  }

  return items;
}
```
