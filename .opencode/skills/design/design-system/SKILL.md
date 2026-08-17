---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: design-system
description: "Create and maintain design systems: tokens, components, documentation and versioning. Use when building or extending a design system, defining design tokens, colors, typography, spacing, dark mode, shadcn/ui or Radix component libraries, documenting components, or when users mention design system, tokens, component library, shadcn, Radix or design tokens."
category: design
version: 0.1.0
author: devtiagoabreu
tags: [design-system, design-tokens, components, shadcn, radix, tailwind, dark-mode]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - A styling foundation (Tailwind CSS, vanilla CSS variables, or similar)
  - A component primitive set (Radix, Base UI, or hand-rolled)
  - Storybook or equivalent for documentation (optional but recommended)
provides:
  - Design token architecture (color, spacing, typography, radii)
  - Component API design and naming conventions
  - Dark mode via CSS variables
  - Documentation and usage guidelines
  - Versioning and governance of the system
difficulty: intermediate
frameworks: [tailwind, shadcn, radix]
languages: [typescript, css]
---

# Design System

## Overview

A design system is a **source of truth** for how a product looks and behaves:
tokens → primitives → components → patterns. Consistency beats cleverness —
the goal is that new screens can be assembled from existing pieces without
designing anything new.

## Prerequisites

- A styling foundation (Tailwind CSS, vanilla CSS variables, or similar)
- A component primitive set (Radix, Base UI, or hand-rolled)
- Storybook or equivalent for documentation (optional but recommended)

## 1. Token Architecture

Tokens are the atomic decisions. Define them once, reference everywhere.

### Color

```css
:root {
  --background: hsl(0 0% 100%);
  --foreground: hsl(222 47% 11%);
  --primary: hsl(221 83% 53%);
  --primary-foreground: hsl(0 0% 100%);
  --secondary: hsl(210 40% 96%);
  --secondary-foreground: hsl(222 47% 11%);
  --muted: hsl(210 40% 96%);
  --muted-foreground: hsl(215 16% 47%);
  --border: hsl(214 32% 91%);
  --ring: hsl(221 83% 53%);
  --destructive: hsl(0 72% 51%);
}
```

Use HSL so dark mode is just a swap of the same names (see §3). Never use raw
`#hex` colors in components — always the token.

### Spacing, radius, typography

```
spacing: 0.25rem base scale (0, 0.5, 1, 1.5, 2, 3, 4, 6, 8) → p-0.5 ... p-8
radius:  0.5rem cards, 0.375rem inputs, 0.75rem larger surfaces
typography scale:
  --text-xs 0.75rem    (labels, dense data)
  --text-sm 0.875rem   (body, table cells)
  --text-base 1rem     (default)
  --text-2xl 1.5rem    (page titles)
  --font-semibold for headings on dense data, not giant weights
```

**Rule:** the design system defines the tokens; components may only use tokens.

## 2. Component Hierarchy

```
Tokens
 └─ Primitives (Button, Input, Select, Dialog, Tabs, Table, Badge, ...)
     └─ Domain components (DataTable, ListFilters, ConfirmModal, PageSkeleton, ...)
         └─ Screens/Pages
```

### Primitive API conventions

- **One component per file**, PascalCase, props typed with TypeScript.
- Style variants with `cva` (class-variance-authority): `default | destructive | outline | ghost | link`.
- Sizes via a `size` prop, not bespoke classes per usage.
- Support `className` passthrough and `asChild`/compound where the primitive model requires it (Radix).
- Dark mode is a first-class concern of **every** primitive (see §3).

```tsx
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-white hover:bg-destructive/90",
        outline: "border border-input bg-background hover:bg-accent",
        ghost: "hover:bg-accent hover:text-accent-foreground",
      },
      size: {
        default: "h-9 px-4 py-2",
        sm: "h-8 rounded-md px-3 text-xs",
        lg: "h-10 rounded-md px-8",
        icon: "h-9 w-9",
      },
    },
    defaultVariants: { variant: "default", size: "default" },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {}

export function Button({ className, variant, size, ...props }: ButtonProps) {
  return <button className={cn(buttonVariants({ variant, size }), className)} {...props} />
}
```

## 3. Dark Mode (citizen, not afterthought)

Model every token as a semantic name and swap the value per theme:

```css
.dark {
  --background: hsl(222 47% 11%);
  --foreground: hsl(210 40% 98%);
  --primary: hsl(217 91% 60%);
  --border: hsl(217 33% 17%);
  --muted: hsl(217 33% 17%);
  --muted-foreground: hsl(215 20% 65%);
}
```

- Components must only use tokens (`bg-background`, `text-foreground`, `border-border`), never fixed colors, so both themes work for free.
- `next-themes`/`dark` class on `<html>`; guard against flash-of-wrong-theme with an inline init script.
- Always test every new component in **both** themes before calling it done.

## 4. Documentation

Each component gets a doc entry with:

```
## Button
Purpose: the one action component.
Usage: <Button variant="destructive" size="sm">Excluir</Button>
Variants table (variant/size → visual + when to use)
Accessibility: focus-visible ring, aria-label for icon-only, keyboard support
Examples: primary action, destructive, loading state
```

- Document **when NOT to use** each component (e.g. "don't use Select for 3 options — use RadioGroup").
- Keep a "known pitfalls" section (e.g. lucide-react import quirks under `skipLibCheck`).
- Storybook or a live story page beats screenshots: people trust running code.

## 5. Versioning and Governance

- Treat the design system as a package: semantic versioning, CHANGELOG, deprecation notices.
- **Deprecate, don't delete** — old screens still use components; provide a migration path.
- New UI must be assembled from existing tokens/primitives; if something is missing, extend the system (token first), then the component.
- Review UI additions like code: consistent API, both themes, accessibility, no new magic colors.

## Examples

### Example 1: Token usage in a screen

```tsx
<h1 className="text-2xl font-bold">Fornecedores</h1>
<p className="text-sm text-muted-foreground">Gerencie seus fornecedores</p>
<Button size="sm" variant="outline">Exportar</Button>
```

### Example 2: Badge with status variants

```tsx
const statusStyles = {
  ativo: "bg-green-100 text-green-700 dark:bg-green-900/40 dark:text-green-300",
  pendente: "bg-yellow-100 text-yellow-700 dark:bg-yellow-900/40 dark:text-yellow-300",
  bloqueado: "bg-red-100 text-red-700 dark:bg-red-900/40 dark:text-red-300",
} as const
```

## Notes

- The system wins over individual taste: "follow the system" beats "this looks nicer".
- Dense B2B dashboards prioritize clarity: readable small type, clear hierarchy, no gratuitous decoration.
- If you use shadcn/ui + Tailwind, keep the generated tokens as the single source — extend, don't fork.
- Pair with `ui-ux-design` for screen-level guidance and `frontend` skills for implementation details.

## References

- [Design Tokens (W3C community)](https://design-tokens.github.io/community-group/)
- [shadcn/ui](https://ui.shadcn.com/)
- [Radix UI](https://www.radix-ui.com/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Material Design tokens](https://m3.material.io/foundations/design-tokens/overview)
