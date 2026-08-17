---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: ui-ux-design
description: UI/UX and interface design principles for web apps. Use when creating, reviewing or auditing screens, layouts, tables, forms, dark mode, responsiveness, accessibility, or when users mention design, UX, layout, interface, frontend design, review my UI, accessibility, or visual hierarchy.
category: design
version: 0.1.0
author: devtiagoabreu
tags: [ui, ux, design, accessibility, layout, typography, responsive, dark-mode]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - A UI framework (React/Tailwind, etc.) and the design system tokens of the project
  - Basic understanding of HTML/CSS
provides:
  - Design principles for web interfaces
  - Screen composition patterns (lists, forms, detail pages, dashboards)
  - Accessibility and contrast guidelines
  - Dark mode and responsive guidance
  - UI review checklist
difficulty: beginner
frameworks: [react, tailwind, html, css]
languages: [css, typescript]
---

# UI/UX Design

## Overview

Design principles that make interfaces **clear, dense and pleasant** — no
decorative fluff. Aim for interfaces a senior designer would ship: consistent,
readable, accessible, and responsive, in both themes.

## Prerequisites

- A UI framework (React/Tailwind, etc.) and the design system tokens of the project
- Basic understanding of HTML/CSS

## 1. Principles

- **Consistency > creativity.** Reuse existing tokens and components before creating anything new.
- **One goal per screen.** Clear title + clear primary action; everything else is secondary.
- **Dense but breathable.** B2B users scan lots of data — compact, but with clear hierarchy and spacing.
- **Dark mode is a first-class citizen.** Every new screen must work in both themes.
- **No free decoration.** No heavy shadows, gradients or oversized icons in internal dashboards.

## 2. Typography and Hierarchy

- One typeface family (e.g. Inter) with system fallbacks; weights limited to `regular/semibold/bold`.
- Page title: `text-2xl font-bold`. Section headers: `text-sm font-semibold`. Body/data: `text-sm`. Dense labels: `text-xs`.
- Use **size and weight** for hierarchy, not color alone.
- Line length: keep paragraphs under ~70 chars; tables are exempt.

## 3. Screen Patterns

### List/Table screen (the workhorse of internal apps)

```
Title + subtitle + primary actions (New, Export, Import) + InfoButton
└─ Search input + filters (status, period)
└─ Table (sticky header, sortable, compact)
    └─ per-row actions (edit, delete in ConfirmModal)
└─ States: loading skeleton → data | empty state (with CTA) | error (toast + retry)
```

- Search across **all** fields, accent-insensitive (remove diacritics).
- Deletion always asks for confirmation; destructive variants are red.
- Show empty state with a hint ("Nenhum fornecedor cadastrado") and the main CTA.

### Form screen

- Group related fields; label every field; placeholder as hint only.
- Validate on blur; show inline errors; disable submit while saving.
- Default submit label = the action ("Salvar"), not "Submit".

### Detail/ficha screen

- Header: entity name + status badge + key actions.
- Sections stacked with `space-y-6`; use tabs only when sections are long.
- Timeline/audit when the entity has a history — trust through transparency.

## 4. Accessibility (not optional)

- **Contrast:** body text ≥ 4.5:1; large text ≥ 3:1. Use tokens that pass.
- **Focus:** every interactive element needs a visible `focus-visible` ring.
- **Keyboard:** dialogs trap focus and close on Esc; dropdowns arrow-key navigable; labels tied to inputs.
- **Semantics:** real `<button>`, `<input type=...>`, native `<table>` structure; don't make divs clickable.
- **Icon-only buttons** need `aria-label`; error toasts need `role="status"`/`role="alert"`.
- Don't rely on color alone to convey status — pair with text/icons.

## 5. Dark Mode

- Build with tokens (`bg-background`, `text-foreground`, `border-border`) so both themes come free.
- Check contrast specifically in dark (white text on `slate-900` is fine; `slate-500` on `slate-900` is not).
- Test: every new component in light AND dark before done.

## 6. Responsive

- Dashboards are desktop-first but must not break below tablet: tables scroll horizontally, grids collapse to single column.
- Use breakpoints `sm/md/lg`; test at 375px and 1440px.
- Touch targets ≥ 44px for mobile.

## 7. UI Review Checklist (use for "review my UI" requests)

1. Tokens used, not magic colors/spacing? Both themes pass contrast?
2. Clear title + one primary action per screen?
3. Loading/empty/error states exist and are consistent?
4. Dense data readable (compact table, sticky header, sortable)?
5. Keyboard + focus + aria-labels on icon buttons?
6. No decorative fluff (no gratuitous shadows/gradients/gigantic icons)?
7. Responsive at 375px and 1440px?
8. Actions use the correct variant (danger only for destructive)?

## Examples

### Example 1: List screen skeleton (React + Tailwind)

```tsx
<div className="space-y-6">
  <div className="flex items-start justify-between">
    <div>
      <h1 className="text-2xl font-bold">Fornecedores</h1>
      <p className="text-sm text-muted-foreground">Gerencie seus fornecedores</p>
    </div>
    <div className="flex gap-2">
      <Button variant="outline" size="sm">Exportar</Button>
      <Button size="sm">Novo fornecedor</Button>
    </div>
  </div>
  <Card>
    <div className="p-3">
      <Input placeholder="Buscar em todos os campos..." />
    </div>
    <div className="overflow-x-auto">
      <Table>
        <TableHeader className="sticky top-0">
          <TableRow>
            <TableHead>Nome</TableHead>
            <TableHead>Cidade</TableHead>
            <TableHead>Status</TableHead>
            <TableHead className="w-[120px]">Ações</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>{/* rows */}</TableBody>
      </Table>
    </div>
  </Card>
</div>
```

### Example 2: Empty state

```tsx
<EmptyState
  icon={<Package className="h-10 w-10 text-muted-foreground" />}
  title="Nenhum fornecedor cadastrado"
  description="Comece adicionando seu primeiro fornecedor."
  action={<Button>Novo fornecedor</Button>}
/>
```

## Notes

- When in doubt, mirror the closest existing screen in the project — consistency is the design.
- Fast is a feature: aim for < 2s loads with skeletons, not spinners after content.
- Pair with `design-system` for tokens/components and with `frontend`/`react-patterns` skills for implementation.

## References

- [Web Content Accessibility Guidelines (WCAG 2.2)](https://www.w3.org/WAI/WCAG22/quickref/)
- [Refactoring UI](https://www.refactoringui.com/)
- [Vercel Web Interface Guidelines](https://github.com/vercel-labs/web-interface-guidelines)
