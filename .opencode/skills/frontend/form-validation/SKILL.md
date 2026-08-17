---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-15
name: form-validation
description: Schema-first form validation with Zod and React Hook Form — shared schemas across API and UI, resolvers, error messages, and reusable form patterns
category: frontend
version: 0.1.0
author: devtiagoabreu
tags: [zod, react-hook-form, validation, forms, typescript, schemas]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - React and TypeScript
  - "npm i zod react-hook-form @hookform/resolvers"
  - shadcn/ui form primitives (optional but recommended)
provides:
  - Shared Zod schemas between client and server
  - RHF + zodResolver wiring with typed fields
  - Error message localization and field-level display
  - Dynamic forms (nested fields, arrays, conditional) and wizards
---

# Form Validation (Zod + React Hook Form)

## Overview

Zod is a TypeScript-first schema library; React Hook Form (RHF) manages form
state without heavy re-renders. Combining them (via `@hookform/resolvers`) gives
schema-first validation where the **same Zod schema validates both the API
payload and the form fields**. Rules live in one place, inputs are inferred as
exact TypeScript types, and errors are localized at the field level. This is the
standard pattern for typed React apps and pairs with shadcn/ui form primitives.

## Prerequisites

- TypeScript strict mode (Zod inference is type-safe)
- RHF + resolvers installed: `npm i react-hook-form @hookform/resolvers`
- shadcn/ui added (`npx shadcn add form`)

## Usage Instructions

### Step 1: Define a shared schema (API + UI)

```ts
import { z } from "zod";

export const customerSchema = z.object({
  name: z.string().min(2, "Nome deve ter ao menos 2 caracteres"),
  phone: z.string().regex(/^[\d\s()-]+$/, "Telefone inválido").optional(),
  email: z.string().email("E-mail inválido").optional().or(z.literal("")),
  address: z.object({
    street: z.string().min(1, "Rua é obrigatória"),
    city: z.string().min(1, "Cidade é obrigatória"),
    state: z.string().length(2, "UF inválida"),
  }),
});

export type CustomerInput = z.infer<typeof customerSchema>;
```

Use the same schema in the API route handler and in the form; only the
`output` (`z.output`) shapes differ when transforming.

### Step 2: Wire the form with zodResolver

```tsx
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { customerSchema, type CustomerInput } from "@/schemas/customer";

export function CustomerForm({ initial, onSubmit }: Props) {
  const form = useForm<CustomerInput>({
    resolver: zodResolver(customerSchema),
    defaultValues: initial ?? { name: "", address: { street: "", city: "", state: "" } },
  });

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField
          control={form.control}
          name="name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Nome</FormLabel>
              <FormControl><Input {...field} /></FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit" disabled={form.formState.isSubmitting}>Salvar</Button>
      </form>
    </Form>
  );
}
```

### Step 3: Localized, user-friendly errors

- Keep human-readable messages in the schema (`min(2, "…")`) instead of raw
  Zod messages.
- Use `setError` for server-side failures mapped to fields:

```tsx
const res = await api.post("/api/v1/customers", data);
if (!res.ok) {
  const issue = res.data.issues?.[0];
  if (issue?.path?.length) form.setError(issue.path[0], { message: issue.message });
}
```

- Show a `Sonner` toast for cross-field errors (e.g. "CEP não encontrado").

### Step 4: Arrays and conditional fields

```tsx
export const routeSchema = z.object({
  scheduledDate: z.coerce.date(),
  driverId: z.string().min(1, "Motorista obrigatório"),
  vehicleId: z.string().optional(),
  stops: z.array(z.object({ customerId: z.string(), position: z.number() }))
    .min(1, "Selecione ao menos um cliente"),
});
```

With `useFieldArray` for dynamic lists:

```tsx
const { fields, append, remove } = useFieldArray({ control: form.control, name: "stops" });
```

### Step 5: API-side validation (server)

Route Handlers validate the incoming body with the same schema — never trust
the client:

```ts
export async function POST(req: Request) {
  const body = await req.json();
  const parsed = customerSchema.safeParse(body);
  if (!parsed.success) {
    return Response.json(
      { success: false, issues: parsed.error.issues.map(({ path, message }) => ({ path, message })) },
      { status: 422 },
    );
  }
  const { data } = parsed;
  // create in DB with tenant context...
}
```

### Step 6: Wizard/multi-step forms (route planning)

For the route planning screen split state across steps but validate with one
final schema (or per-step schemas):

```tsx
const [step, setStep] = useState<1 | 2 | 3>(1);
// step 1: config (driver/vehicle/date), step 2: select customers, step 3: review+optimize
```

Keep the whole thing driven by `RoutePlanningState` (single source of truth);
forms update it, the map/list read from it.

## Best Practices

- One schema per domain entity; reuse across client and server.
- Infer types with `z.infer` — never duplicate interfaces by hand.
- Use `safeParse` on the server; show `issues` mapped to fields.
- Debounce searches; validate on submit + `mode: "onTouched"` for UX.
- Coerce dates/numbers at the boundary (`z.coerce`).

## References

- Zod: <https://zod.dev>
- React Hook Form: <https://react-hook-form.com>
- RouteOS SaaS spec — Documento 08 (Arquitetura Frontend)
