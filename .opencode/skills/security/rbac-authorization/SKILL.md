---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-15
name: rbac-authorization
description: Implement role-based access control (RBAC) with roles, permission matrix, and server-side enforcement — combined with tenant isolation in multi-tenant SaaS
category: security
version: 0.1.0
author: devtiagoabreu
tags: [rbac, authorization, roles, permissions, security, access-control]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - An authentication layer (session/JWT) providing the user identity
  - Knowledge of the application's modules and actions
provides:
  - Role and permission model design
  - Permission matrix patterns (resource × action)
  - Server-side enforcement in services/route handlers
  - UI-level permission control (hiding, disabling)
  - Audit integration for access events
---

# RBAC Authorization

## Overview

Role-Based Access Control (RBAC) authorizes users by role: each role maps to a
set of allowed (resource, action) pairs, and every request is checked against
that matrix before any business logic runs. Authorization is enforced
**server-side** — the UI only hides what the user cannot do, it never protects
it. In a multi-tenant SaaS, RBAC composes with tenant isolation: a user's
permissions apply *within* their tenant. Typical roles: `ADMIN`, `MANAGER`,
`DISPATCHER`, `DRIVER`, plus a read-only `VIEWER`.

## Prerequisites

- Authentication resolved to a session context (`{ userId, tenantId, role }`)
- A list of modules/actions to secure (customers, routes, drivers, users, audit…)
- Centralized request handling (services or route handlers) where checks run

## Usage Instructions

### Step 1: Define roles and a permission matrix

```ts
export type Action = "create" | "read" | "update" | "delete" | "optimize" | "import";
export type Resource = "customer" | "route" | "driver" | "vehicle" | "user" | "audit";

export const PERMISSIONS: Record<Role, Record<Resource, Action[]>> = {
  ADMIN: {
    customer: ["create", "read", "update", "delete", "import"],
    route: ["create", "read", "update", "delete", "optimize"],
    user: ["create", "read", "update", "delete"],
    audit: ["read"],
  },
  MANAGER: {
    customer: ["create", "read", "update", "import"],
    route: ["create", "read", "update", "optimize"],
    audit: ["read"],
  },
  DISPATCHER: {
    customer: ["read"],
    route: ["create", "read", "update", "optimize"],
  },
  DRIVER: {
    route: ["read", "update"],
  },
  VIEWER: {
    customer: ["read"],
    route: ["read"],
  },
};
```

### Step 2: Enforce server-side with a guard

```ts
export function requirePermission(ctx: Ctx, resource: Resource, action: Action) {
  const allowed = PERMISSIONS[ctx.role]?.[resource] ?? [];
  if (!allowed.includes(action)) throw new ForbiddenError("permission denied");
}
```

Call it at the top of services/route handlers **after** tenant resolution:

```ts
export async function deleteCustomer(ctx: Ctx, id: string) {
  requirePermission(ctx, "customer", "delete"); // 403 if not allowed
  return repo.delete({ id, tenantId: ctx.tenantId }); // tenant scope
}
```

- Fail closed: unknown role → deny.
- Combine with tenant isolation — never return data the user may not touch
  even if they hold the permission for another tenant.

### Step 3: UI-level control (cosmetic only)

Use a hook to hide or disable actions, but remember the server is the real gate:

```tsx
const canDelete = usePermission("customer", "delete");

<Button disabled={!canDelete} variant="destructive">
  Excluir
</Button>
```

### Step 4: Role hierarchy (optional)

If ADMIN should imply all of MANAGER, resolve permissions by walking up the
hierarchy instead of duplicating matrices:

```ts
const ROLE_HIERARCHY: Record<Role, Role[]> = {
  ADMIN: ["ADMIN", "MANAGER", "DISPATCHER", "DRIVER", "VIEWER"],
  MANAGER: ["MANAGER", "DISPATCHER", "DRIVER", "VIEWER"],
  DISPATCHER: ["DISPATCHER", "VIEWER"],
  DRIVER: ["DRIVER", "VIEWER"],
  VIEWER: ["VIEWER"],
};
```

### Step 5: Audit authorization-sensitive events

Log changes and access to sensitive resources in `AuditLog`
(`tenantId`, `userId`, `action`, `resource`, `changes`) with values like
`CUSTOMER_DELETED`, `USER_ROLE_CHANGED`, `ROUTE_OPTIMIZED`.

### Step 6: Guard the API surface (RBAC summary)

| Layer | Enforces |
|-------|----------|
| Route handler | Auth (identity) + tenant resolution |
| Service | Permission check per action |
| Repository | Tenant scoping on every query |
| UI | Hide/disable (cosmetic) |

## Examples

### Permission guard in a Next.js Route Handler

```ts
export async function DELETE(req: Request, { params }: { params: { id: string } }) {
  const ctx = await requireSession(req); // resolves userId, tenantId, role
  try {
    await deleteCustomer(ctx, params.id);
    return Response.json({ success: true });
  } catch (err) {
    if (err instanceof ForbiddenError) {
      return Response.json({ success: false, message: "sem permissão" }, { status: 403 });
    }
    throw err;
  }
}
```

### Seeding default roles with plans

```ts
// prisma seed
await prisma.role.upsert({
  where: { name: "MANAGER" },
  update: {},
  create: { name: "MANAGER", permissions: { customer: ["create", "read", "update", "import"] } },
});
```

## Best Practices

- Enforce permissions in the service layer, never only in the UI.
- Keep the matrix data-driven (JSON/config) so it can be reviewed and tested.
- Write tests asserting each role's matrix (allowed and denied cases).
- Combine RBAC with tenant scoping: check role AND tenant on every call.
- Return 403 with a generic message; log the real reason server-side.

## References

- OWASP RBAC: <https://owasp.org/www-community/access_control>
- RouteOS SaaS spec — Documento 05 (RBAC) and Documento 16 (Autenticação, RBAC e Segurança)
