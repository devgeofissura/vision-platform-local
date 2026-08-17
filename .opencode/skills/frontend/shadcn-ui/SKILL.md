---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-15
name: shadcn-ui
description: Build consistent UI with shadcn/ui + Tailwind + Radix — component copy-in patterns, theming (light/dark/system), composition, and DataTable/form conventions
category: frontend
version: 0.1.0
author: devtiagoabreu
tags: [shadcn, tailwind, radix, design-system, components, dark-mode]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Tailwind CSS configured in the project
  - React 18+/Next.js (App Router preferred)
provides:
  - shadcn/ui setup and component conventions
  - Theme architecture (CSS variables, light/dark/system)
  - Page/DataTable/form composition patterns
  - Accessibility defaults via Radix primitives
---

# shadcn/ui

## Overview

shadcn/ui is not a component library you install wholesale — it is a set of
copy-paste components built on **Radix primitives** + **Tailwind CSS** + CSS
variables. You run `npx shadcn init` and then `npx shadcn add <component>` to
drop a component's source into your project, where you own and can modify it.
This gives you full control of the codebase with accessibility and styling
baked in. The stack pairs with Tailwind tokens to deliver a modern, consistent
SaaS UI (Linear/Stripe/Vercel-style) including light, dark and system themes.

## Prerequisites

- Tailwind installed: `npx shadcn init` requires a Tailwind setup
- Next.js (App Router) or Vite + React
- `npx shadcn init` to scaffold `components.json` and theme tokens

## Usage Instructions

### Step 1: Initialize and add components

```bash
# scaffold (creates components.json, css variables, lib/utils.ts)
npx shadcn@latest init

# add only what you need
npx shadcn@latest add button card input label table dialog
npx shadcn@latest add select dropdown-menu tabs toast sonner
npx shadcn@latest add checkbox form sheet skeleton tooltip
```

Components live under `src/components/ui/` and are yours to edit — this is the
intended workflow, not a package dependency.

### Step 2: Theme with CSS variables

shadcn themes are token-driven. The root defines HSL variables and `dark`
overrides via a class:

```css
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222 47% 11%;
    --primary: 221 83% 53%;
    --ring: 221 83% 53%;
    --radius: 0.5rem;
  }
  .dark {
    --background: 222 47% 6%;
    --foreground: 213 31% 91%;
  }
}
```

- `next-themes` toggles `class="dark"`; offer Light/Dark/System.
- Reference tokens only via Tailwind utilities (`bg-background`, `text-foreground`).

### Step 3: Compose pages with a consistent pattern

Follow a predictable page layout so every screen feels the same:

```text
PageHeader → Toolbar → Filters → Content → Pagination
```

```tsx
export function CustomersPage() {
  return (
    <div className="space-y-4 p-6">
      <PageHeader title="Clientes" description="Cadastro e importação" actions={<Button>Novo</Button>} />
      <Toolbar>
        <Input placeholder="Buscar..." className="max-w-sm" />
        <CustomerFilters />
      </Toolbar>
      <CustomersTable />
      <Pagination />
    </div>
  );
}
```

### Step 4: DataTable with column definition (TanStack Table)

shadcn's `Table` primitives + `@tanstack/react-table` handle sorting,
pagination and selection:

```tsx
const columns: ColumnDef<Customer>[] = [
  { accessorKey: "name", header: "Nome", cell: ({ row }) => <b>{row.original.name}</b> },
  { accessorKey: "city", header: "Cidade" },
  { accessorKey: "phone", header: "Telefone" },
  {
    id: "actions",
    cell: ({ row }) => (
      <DropdownMenu>
        <DropdownMenuTrigger asChild><Button variant="ghost">⋯</Button></DropdownMenuTrigger>
        <DropdownMenuContent>
          <DropdownMenuItem onSelect={() => edit(row.original)}>Editar</DropdownMenuItem>
          <DropdownMenuItem className="text-destructive" onSelect={() => confirmDelete(row.original)}>Excluir</DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    ),
  },
];
```

### Step 5: Dialogs and forms

- Modals: `Dialog`/`Sheet` with `confirm-on-delete` pattern (never delete without
  a confirmation dialog).
- Forms: `shadcn` form primitives + React Hook Form + Zod resolver (see the
  form-validation skill). Use `FormField`, `FormItem`, `FormLabel`, `FormMessage`.
- Feedback: `Sonner` toasts for success/error; loading and empty states for
  every table.

### Step 6: Shell and layout

SaaS dashboard layout: Header + Sidebar + Breadcrumb + main area + user menu +
theme selector. On mobile (<768px) collapse the sidebar into a drawer (`Sheet`);
desktop ≥1024px shows it fixed.

## Examples

### Themed button variants

```tsx
<Button size="sm">Save</Button>
<Button variant="outline">Cancel</Button>
<Button variant="destructive">Delete</Button>
<Button variant="ghost" size="icon"><MoreHorizontal /></Button>
```

### Confirmation dialog for delete

```tsx
<AlertDialog>
  <AlertDialogTrigger asChild><Button variant="destructive">Excluir</Button></AlertDialogTrigger>
  <AlertDialogContent>
    <AlertDialogHeader>
      <AlertDialogTitle>Excluir cliente?</AlertDialogTitle>
      <AlertDialogDescription>Esta ação não pode ser desfeita.</AlertDialogDescription>
    </AlertDialogHeader>
    <AlertDialogFooter>
      <AlertDialogCancel>Cancelar</AlertDialogCancel>
      <AlertDialogAction onClick={onConfirm}>Excluir</AlertDialogAction>
    </AlertDialogFooter>
  </AlertDialogContent>
</AlertDialog>
```

## Best Practices

- Add components on demand; avoid importing the entire library surface.
- Keep `components.json` and tokens in source control; document theme choices.
- Use Radix accessibility defaults (focus rings via `--ring`, keyboard nav).
- Use spacing scale (`space-y-*`, `p-*`, `gap-*`) instead of magic values.
- Consistent empty/loading/error states across all lists and tables.

## References

- shadcn/ui: <https://ui.shadcn.com>
- TanStack Table: <https://tanstack.com/table>
- next-themes: <https://github.com/pacocoursey/next-themes>
- RouteOS SaaS spec — Documento 12 (Design System e Wireframes)
