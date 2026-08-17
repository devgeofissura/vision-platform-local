---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: accessibility
description: Best practices for web accessibility (WCAG compliance)
category: frontend
version: 0.1.0
author: devtiagoabreu
tags: [accessibility, a11y, wcag, frontend]
compatible:
  - opencode
  - claude-code
  - cursor
---

# Accessibility Best Practices

## Overview

This skill provides best practices for web accessibility, including WCAG compliance, ARIA attributes, and assistive technology support.

## Prerequisites

- Basic understanding of accessibility concepts
- HTML knowledge

## Usage Instructions

### Step 1: Semantic HTML

Use semantic HTML elements:

```html
<!-- Good -->
<header>
  <nav aria-label="Main navigation">
    <ul>
      <li><a href="/">Home</a></li>
      <li><a href="/about">About</a></li>
    </ul>
  </nav>
</header>

<main>
  <article>
    <h1>Page Title</h1>
    <p>Content...</p>
  </article>
</main>

<footer>
  <p>&copy; 2024</p>
</footer>

<!-- Bad -->
<div class="header">
  <div class="nav">
    <div class="nav-item">Home</div>
    <div class="nav-item">About</div>
  </div>
</div>
```

### Step 2: ARIA Attributes

Use ARIA attributes when needed:

```html
<!-- Custom component with ARIA -->
<button 
  aria-expanded="false"
  aria-controls="menu-content"
  aria-label="Toggle menu"
>
  Menu
</button>

<div id="menu-content" role="menu" aria-hidden="true">
  <a role="menuitem" href="/home">Home</a>
  <a role="menuitem" href="/about">About</a>
</div>
```

### Step 3: Keyboard Navigation

Implement keyboard navigation:

```javascript
// Handle keyboard events
function handleKeyDown(event) {
  if (event.key === 'Enter' || event.key === ' ') {
    event.preventDefault();
    activateElement();
  }
  
  if (event.key === 'Escape') {
    closeModal();
  }
  
  if (event.key === 'ArrowDown') {
    moveFocusToNextElement();
  }
}

// Focus management
function trapFocus(element) {
  const focusableElements = element.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );
  
  const firstElement = focusableElements[0];
  const lastElement = focusableElements[focusableElements.length - 1];
  
  element.addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
      if (e.shiftKey) {
        if (document.activeElement === firstElement) {
          lastElement.focus();
          e.preventDefault();
        }
      } else {
        if (document.activeElement === lastElement) {
          firstElement.focus();
          e.preventDefault();
        }
      }
    }
  });
}
```

### Step 4: Color and Contrast

Ensure proper color contrast:

```css
/* Good contrast */
.text {
  color: #333333; /* Dark text */
  background-color: #ffffff; /* Light background */
}

/* Poor contrast */
.text-bad {
  color: #999999; /* Light text */
  background-color: #ffffff; /* Light background */
}

/* Focus indicators */
:focus {
  outline: 2px solid #007bff;
  outline-offset: 2px;
}
```

## Examples

### Accessible Form

```html
<form>
  <div>
    <label for="email">Email address</label>
    <input 
      type="email" 
      id="email" 
      name="email"
      aria-required="true"
      aria-describedby="email-hint"
    >
    <span id="email-hint">We'll never share your email.</span>
  </div>
  
  <div>
    <label for="password">Password</label>
    <input 
      type="password" 
      id="password" 
      name="password"
      aria-required="true"
      aria-describedby="password-hint"
    >
    <span id="password-hint">Must be at least 8 characters.</span>
  </div>
  
  <button type="submit">Submit</button>
</form>
```

## Best Practices

1. Use semantic HTML
2. Use ARIA attributes when needed
3. Implement keyboard navigation
4. Ensure proper color contrast
5. Provide alternative text for images
6. Test with screen readers

## References

- [WCAG Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apd/)