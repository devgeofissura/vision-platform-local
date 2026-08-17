---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-15
name: prisma-orm
description: Model, migrate and query PostgreSQL with Prisma ORM — schema design, relations, enums, soft delete, tenant scoping, and connection management for serverless
category: backend
version: 0.1.0
author: devtiagoabreu
tags: [prisma, orm, postgresql, schema, migrations, serverless, nextjs]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Node.js and a PostgreSQL database (Neon, Supabase or local)
  - A TypeScript project
provides:
  - Prisma schema modeling with relations and enums
  - Migration workflow (dev vs deploy)
  - Query patterns for filtering, pagination and aggregation
  - Soft delete and tenant scoping patterns
  - Connection pooling guidance for serverless (Vercel + Neon)
---

# Prisma ORM

## Overview

Prisma is a type-safe ORM for TypeScript that maps a declarative `schema.prisma`
to a real database (PostgreSQL here). The flow is: define the data model, run a
migration to create the SQL, then query through typed methods
(`prisma.customer.findMany`, `prisma.route.create`). This skill covers modeling
relations and enums, the migration workflow, common query patterns, soft
delete, tenant scoping, and the connection-pooling setup required on
serverless platforms like Vercel with Neon.

## Prerequisites

- A `prisma` schema installed (`npm i prisma @prisma/client`)
- `DATABASE_URL` configured (e.g. `postgresql://user:pass@host/db?sslmode=require`)
- `prisma generate` producing the client types

## Usage Instructions

### Step 1: Model the schema

Use `@default` for ids, `@map`/`@@map` for snake_case column names, enums for
fixed sets, and explicit relations:

```prisma
enum Role {
  ADMIN
  MANAGER
  DISPATCHER
  DRIVER
}

model Customer {
  id       String   @id @default(cuid())
  tenantId String
  name     String
  phone    String?
  address  Address?
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  deletedAt DateTime?
  routes   RouteStop[]

  @@unique([tenantId, name])
  @@map("customers")
}

model RouteStop {
  id         String  @id @default(cuid())
  customerId String?
  customer   Customer? @relation(fields: [customerId], references: [id])
  latitude   Float
  longitude  Float
  position   Int
}
```

- Money as `Decimal`, distances in meters (`Int`), durations in seconds
  (`Int`), dates in UTC.
- Use UUIDv7 (or `cuid()`) for ids when distributed ordering matters.
- Prefer `@relation` with explicit `onDelete: SetNull`/`Cascade` matching your
  domain (soft delete often avoids hard cascades).

### Step 2: Migrations

```bash
# dev: create and apply a migration from schema changes
npx prisma migrate dev --name add_route_stops

# prod: apply existing migrations (used in CI/deploy)
npx prisma migrate deploy

# regenerate the typed client after schema edits
npx prisma generate
```

Never hand-edit generated SQL unless you understand drift: keep migrations in
source control so every environment matches.

### Step 3: Query patterns

```ts
import { PrismaClient } from "@prisma/client";
export const prisma = new PrismaClient();

// filter + paginate + order
const { page, pageSize = 20 } = params;
const customers = await prisma.customer.findMany({
  where: { tenantId: ctx.tenantId, deletedAt: null },
  orderBy: { createdAt: "desc" },
  skip: (page - 1) * pageSize,
  take: pageSize,
});

// include relations
const route = await prisma.route.findFirst({
  where: { id, tenantId },
  include: { stops: { orderBy: { position: "asc" } } },
});

// aggregate
const count = await prisma.customer.count({ where: { tenantId } });
const stats = await prisma.route.aggregate({
  _sum: { distanceMeters: true },
  where: { tenantId, scheduledDate: date },
});
```

### Step 4: Soft delete and tenant scoping

Treat `tenantId` as part of the row's identity:

```ts
// soft delete
await prisma.customer.update({
  where: { id, tenantId },           // tenant-scoped
  data: { deletedAt: new Date() },
});

// every read excludes soft-deleted rows
const rows = await prisma.customer.findMany({
  where: { tenantId: ctx.tenantId, deletedAt: null },
});
```

Optionally create a reusable `scopeWhere(tenantId, extra)` helper so filters
stay consistent across the codebase.

### Step 5: Serverless connection management (Vercel + Neon)

Serverless functions are ephemeral — do not create a new client per request
and do not exhaust pooled connections:

```ts
// lib/prisma.ts - singleton pattern
import { PrismaClient } from "@prisma/client";

const globalForPrisma = globalThis as unknown as { prisma?: PrismaClient };
export const prisma =
  globalForPrisma.prisma ??
  new PrismaClient({
    log: process.env.NODE_ENV === "development" ? ["query", "error"] : ["error"],
  });

if (process.env.NODE_ENV !== "production") globalForPrisma.prisma = prisma;
```

For Neon use a pooled connection string (`?pgbouncer=true` or the pooled
endpoint) so many serverless invocations share connections safely. Keep the
Prisma client warm where possible and never run heavy queries inside render.

### Step 6: Seeding

```ts
// prisma/seed.ts - idempotent dev data
import { PrismaClient } from "@prisma/client";
const prisma = new PrismaClient();

async function main() {
  await prisma.plan.upsert({
    where: { name: "Starter" },
    update: {},
    create: { name: "Starter", maxUsers: 3, maxCustomers: 1000 },
  });
}
main().finally(() => prisma.$disconnect());
```

Run with `npx prisma db seed`.

## Best Practices

- Scope every business query by `tenantId`; use `findFirst` with `tenantId` in
  `where` instead of `findUnique` for tenant data.
- Add `@@unique([tenantId, ...])` for tenant-local uniqueness.
- Keep `.env` out of source control; use `.env.example`.
- Use transactions (`prisma.$transaction([...])`) when creating a parent plus
  children (e.g. customer + address).
- Prefer `select`/`include` over loading full rows; watch N+1 queries in loops
  (batch with `findMany` + `where: { id: { in: ids } }`).

## References

- Prisma docs: <https://www.prisma.io/docs>
- Neon pooling: <https://neon.tech/docs/connect/connection-pooling>
- RouteOS SaaS spec — Documento 10 (Schema Prisma)
