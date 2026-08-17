---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-15
name: multi-tenant-saas
description: Design and implement multi-tenant SaaS backends with Shared Database + Shared Schema + tenantId isolation, tenant resolution, and cross-tenant protection
category: architecture
version: 0.1.0
author: devtiagoabreu
tags: [multi-tenant, saas, isolation, tenant-id, rbac, postgresql, nextjs]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Familiarity with a backend framework and a relational database
  - Basic understanding of authentication and session context
provides:
  - Multi-tenant isolation model decision guidance
  - Tenant resolution and per-request context patterns
  - Repository/service rules that prevent cross-tenant leaks
  - Plan limits, audit and global entity handling
---

# Multi-Tenant SaaS Architecture

## Overview

A multi-tenant SaaS serves many independent companies ("tenants") from a single
deployment. The chosen isolation model for this kit's reference apps is
**Shared Database + Shared Schema + `tenantId`**: one PostgreSQL database, one
schema, and every business table carries a `tenantId` column. Every query is
scoped by tenant. This model has the lowest cost, scales fine for an MVP
(10,000+ tenants, 1,000,000+ customers), and works on serverless (Vercel).
Security comes from discipline: the backend must *always* filter by tenant —
never rely on the frontend hiding UI.

## Prerequisites

- A relational database (PostgreSQL recommended) and an ORM (Prisma recommended)
- An authentication layer (session/JWT/OAuth) that identifies the logged-in user
- Basic knowledge of REST APIs and repository/service layering

## Usage Instructions

### Step 1: Choose the isolation model

Evaluate the three common models:

| Model | Description | Trade-off |
|-------|-------------|-----------|
| Shared schema + tenantId | One DB, one schema, `tenantId` on every row | Lowest cost, highest discipline needed |
| Schema per tenant | One DB, one schema per tenant | Better isolation, complex migrations |
| Database per tenant | One DB per tenant | Strongest isolation, most expensive |

For serverless MVPs choose **Shared Schema + tenantId**. Never allow a query
without a tenant for business entities.

### Step 2: Standard columns on every business table

Every business entity must include the audit/tenant columns:

```text
id          tenantId   createdAt   updatedAt
deletedAt   createdBy  updatedBy   deletedBy
```

Global (non-tenant) tables — countries, states, system plans, default
permissions — have no `tenantId`.

### Step 3: Tenant resolution

After authentication, resolve the tenant before any business call:

```ts
// auth middleware → request context
const ctx = { userId: "user_123", tenantId: "t_456", role: "MANAGER" };
```

Rules:

- No authenticated request may exist without a resolved tenant.
- Carry `{ userId, tenantId, role }` in the request context.
- Services and repositories receive the context and use `tenantId` in every
  query — never accept a bare primary key.

### Step 4: Repository discipline

Forbid repository methods that read business data without a tenant:

```ts
// WRONG - leaks across tenants
async function getCustomer(id: string) { ... }

// CORRECT - always tenant-scoped
async function getCustomer(ctx: Ctx, id: string) {
  return db.customer.findFirst({ where: { id, tenantId: ctx.tenantId } });
}
```

- Every update must scope by `{ id, tenantId }` — never by `id` alone.
- Use `findFirst` (not `findUnique`) with `tenantId` in the `where`.
- Add a unique constraint including `tenantId` for tenant-local uniqueness.

### Step 5: Enforce tenant context end-to-end

- Backend-only limit checks: never trust the frontend with plan limits.
- Structured errors (`AppError`, `ForbiddenError`, `NotFoundError`) that never
  leak stack traces, database errors, or API keys.
- Logging with `requestId`/`X-Request-Id` to trace requests across tenants.
- Wrap services so any missing tenant fails closed (fail secure).

### Step 6: RBAC on top of tenants

Combine tenant isolation with roles per tenant: `ADMIN`, `MANAGER`,
`DISPATCHER`, `DRIVER`, `VIEWER`. Check permission by
`(role, resource, action)` inside the service layer, not only in the UI.

### Step 7: Plans and limits

Track a `Plan` (Starter/Professional/Enterprise) per tenant with limits (users,
customers, drivers, vehicles, routes/month). Enforce limits in the backend at
creation time (e.g. `TRIAL_DAYS = 14`, then subscription via Stripe/Asaas).

### Step 8: Audit and soft delete

- Append-only `AuditLog` (`tenantId`, `userId`, `action`, `resource`,
  `changes`) for compliance (e.g. `CUSTOMER_CREATED`, `ROUTE_OPTIMIZED`).
- Use `deletedAt` soft delete; every query excludes soft-deleted rows.

## Examples

### Tenant context from a session (Next.js + Clerk style)

```ts
// middleware.ts
export function requireTenant(session): Ctx {
  if (!session?.user?.id) throw new ForbiddenError("unauthenticated");
  const membership = db.tenantMembership.findFirst({
    where: { userId: session.user.id, active: true },
  });
  if (!membership) throw new ForbiddenError("no tenant");
  return { userId: session.user.id, tenantId: membership.tenantId, role: membership.role };
}
```

### Tenant-scoped repository (Prisma)

```ts
const customer = await prisma.customer.findFirst({
  where: { id: input.id, tenantId: ctx.tenantId, deletedAt: null },
});
```

### Unique per tenant

```prisma
model Customer {
  id       String @id @default(cuid())
  tenantId String
  name     String
  @@unique([tenantId, name])
}
```

## Best Practices

- Treat `tenantId` as part of the identity, not a filter you may forget.
- Add tests that actively attempt cross-tenant access (tenant A reads tenant B)
  and assert they fail.
- Use UUIDv7 for distributed ordering; money as `Decimal`, distances in meters
  (Int), durations in seconds (Int), dates in UTC.
- Keep global tables small and documented.

## References

- RouteOS SaaS spec — Documento 04 (Arquitetura Multi-Tenant) and Documento 10
- Prisma multi-tenancy guide: <https://www.prisma.io/docs/orm/prisma-schema/data-model/relations>
- OWASP tenant isolation guidance
