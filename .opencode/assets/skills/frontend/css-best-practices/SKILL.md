---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: css-best-practices
description: Best practices for CSS architecture and styling
category: frontend
version: 0.1.0
author: devtiagoabreu
tags: [css, styling, frontend, architecture]
compatible:
  - opencode
  - claude-code
  - cursor
---

# CSS Best Practices

## Overview

This skill provides best practices for CSS architecture and styling, including methodology, organization, and performance.

## Prerequisites

- Basic understanding of CSS
- HTML knowledge

## Usage Instructions

### Step 1: CSS Methodology

Use BEM methodology:

```css
/* Block */
.card {
  /* Element */
  &__header {
    /* Modifier */
    &--featured {
      border: 2px solid blue;
    }
  }
  
  &__content {
    padding: 16px;
  }
  
  &__footer {
    display: flex;
    justify-content: space-between;
  }
}
```

### Step 2: CSS Variables

Use CSS variables for theming:

```css
:root {
  --primary-color: #007bff;
  --secondary-color: #6c757d;
  --font-size-base: 16px;
  --spacing-unit: 8px;
}

.button {
  background-color: var(--primary-color);
  font-size: var(--font-size-base);
  padding: var(--spacing-unit) calc(var(--spacing-unit) * 2);
}
```

### Step 3: Responsive Design

Use mobile-first approach:

```css
/* Mobile first */
.container {
  padding: 16px;
}

/* Tablet */
@media (min-width: 768px) {
  .container {
    padding: 24px;
    max-width: 720px;
    margin: 0 auto;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .container {
    padding: 32px;
    max-width: 960px;
  }
}
```

### Step 4: Performance

Optimize CSS performance:

```css
/* Use efficient selectors */
.class-name {
  /* Avoid */
  div > p > .class-name {
    color: red;
  }
  
  /* Prefer */
  .class-name {
    color: red;
  }
}

/* Use will-change for animations */
.animated-element {
  will-change: transform;
  transition: transform 0.3s ease;
}
```

## Examples

### CSS Grid Layout

```css
.grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
}

.grid-item {
  background: white;
  padding: 24px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
```

## Best Practices

1. Use BEM methodology
2. Use CSS variables for theming
3. Use mobile-first approach
4. Optimize CSS performance
5. Use CSS Grid or Flexbox for layout
6. Avoid !important

## References

- [CSS Best Practices](https://www.sitepoint.com/css-best-practices/)
- [BEM Methodology](https://getbem.com/)