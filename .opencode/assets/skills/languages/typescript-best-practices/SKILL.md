---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: typescript-best-practices
description: TypeScript best practices covering strict typing, generics, and modern tooling
category: languages
version: 0.1.0
author: devtiagoabreu
tags: [typescript, javascript, strict, generics, typing]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Node.js 18 or newer
  - npm, yarn, pnpm, or bun package manager
  - Basic familiarity with JavaScript/TypeScript
provides:
  - Strict TypeScript compiler configuration
  - Patterns for type safety, generics, and unions
  - Rules for ergonomic typing without ceremony
  - Project setup with tsconfig and package scripts
---

# TypeScript Best Practices

## Overview

This skill is a guide to writing production-grade TypeScript that is type-safe,
maintainable, and idiomatic. It covers compiler configuration with strict mode
enabled, using generics and discriminated unions to model real-world data, and
structuring types so they stay in sync with runtime behavior. The goal is to let
the compiler catch bugs at build time instead of runtime. It applies equally to
Node.js backends, browser frontends, and shared libraries.

## Prerequisites

- Node.js 18+ and a package manager installed
- A project with a `package.json` file
- Working knowledge of JavaScript fundamentals

## Usage Instructions

### Step 1: Enable Strict Mode

Turn on `strict` and related flags in `tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "exactOptionalPropertyTypes": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "outDir": "dist",
    "rootDir": "src"
  },
  "include": ["src"]
}
```

Resist the temptation to disable `strict` or sprinkle `any`; instead narrow
types explicitly.

### Step 2: Prefer Types Over Interfaces for Unions

Use `type` when modeling unions and intersections, and `interface` for object
shapes that may be extended:

```typescript
type Status = "idle" | "loading" | "success" | "error";

interface ApiError {
  code: number;
  message: string;
}

type ApiResponse<T> =
  | { status: "success"; data: T }
  | { status: "error"; error: ApiError };
```

This discriminated union gives exhaustive, compile-checked state handling.

### Step 3: Write Generic Helpers

Generic functions reuse logic across types while preserving type information:

```typescript
function groupBy<T, K extends PropertyKey>(
  items: readonly T[],
  keyOf: (item: T) => K
): Record<K, T[]> {
  const groups = {} as Record<K, T[]>;
  for (const item of items) {
    const key = keyOf(item);
    (groups[key] ??= []).push(item);
  }
  return groups;
}

const byRole = groupBy(users, (u) => u.role);
```

Add constraints (`extends`) only when the logic actually needs them.

### Step 4: Type the Boundaries, Not Everything

Type public APIs, module exports, and data crossing the network boundary. Let
TypeScript infer the rest:

```typescript
interface User {
  id: string;
  name: string;
  email: string;
}

export async function fetchUser(id: string): Promise<User> {
  const res = await fetch(`/api/users/${id}`);
  if (!res.ok) throw new Error(`Request failed: ${res.status}`);
  return res.json() as Promise<User>;
}
```

Validate external payloads with a runtime guard so the cast is safe:

```typescript
function isUser(value: unknown): value is User {
  return typeof value === "object" && value !== null &&
    "id" in value && "email" in value;
}
```

### Step 5: Use `satisfies` for Literal Preserving

Verify an expression conforms to a type without widening its literal type:

```typescript
const routes = {
  home: "/",
  profile: "/users/:id",
  admin: "/admin",
} satisfies Record<string, string>;

type Route = keyof typeof routes; // "home" | "profile" | "admin"
```

### Step 6: Add Tooling to package.json

Wire up type checking, linting, and builds as explicit scripts:

```json
{
  "scripts": {
    "build": "tsc -p tsconfig.build.json",
    "typecheck": "tsc --noEmit",
    "lint": "eslint src --max-warnings 0",
    "format": "prettier --write src"
  },
  "devDependencies": {
    "typescript": "^5.6.0",
    "eslint": "^9.0.0",
    "prettier": "^3.3.0"
  }
}
```

Run `npm run typecheck` before every commit and in CI.

## Examples

### Example 1: Exhaustive Switch with `never`

```typescript
function statusLabel(status: Status): string {
  switch (status) {
    case "idle": return "Waiting";
    case "loading": return "Loading…";
    case "success": return "Done";
    case "error": return "Failed";
    default: {
      const _exhaustive: never = status;
      return _exhaustive;
    }
  }
}
```

### Example 2: Typed Event Emitter

```typescript
type Events = {
  login: { userId: string };
  logout: undefined;
  error: { message: string };
};

class Emitter<E extends Record<string, unknown>> {
  private listeners: {
    [K in keyof E]?: Array<(payload: E[K]) => void>;
  } = {};

  on<K extends keyof E>(event: K, handler: (payload: E[K]) => void): void {
    (this.listeners[event] ??= []).push(handler);
  }

  emit<K extends keyof E>(event: K, payload: E[K]): void {
    this.listeners[event]?.forEach((handler) => handler(payload));
  }
}
```

## References

- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
- [TypeScript Handbook: Generics](https://www.typescriptlang.org/docs/handbook/2/generics.html)
- [TypeScript Handbook: Discriminated Unions](https://www.typescriptlang.org/docs/handbook/2/narrowing.html#discriminated-unions)
- [tsconfig reference](https://www.typescriptlang.org/tsconfig)
- [The TypeScript Evolution blog](https://blog.mariusschulz.com/legacy-type-articles)
- [TypeScript ESLint](https://typescript-eslint.io/)

## Notes

- Set `"strict": true` on every new project; migrate legacy code incrementally.
- Prefer `readonly T[]` for function parameters that are not mutated.
- Use `Array.isArray` and `typeof` guards before trusting external input.
- Never use `any` to silence the compiler; use `unknown` and narrow it.
- Keep type definitions next to the code that uses them.
- Run `tsc --noEmit` in CI; skip `skipLibCheck` only for stubborn deps.
