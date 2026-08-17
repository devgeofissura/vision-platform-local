---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: performance
description: Best practices for frontend performance optimization
category: frontend
version: 0.1.0
author: devtiagoabreu
tags: [performance, optimization, frontend, speed]
compatible:
  - opencode
  - claude-code
  - cursor
---

# Frontend Performance Best Practices

## Overview

This skill provides best practices for frontend performance optimization, including loading, rendering, and runtime performance.

## Prerequisites

- Basic understanding of web performance
- Browser developer tools knowledge

## Usage Instructions

### Step 1: Loading Performance

Optimize asset loading:

```html
<!-- Preload critical resources -->
<link rel="preload" href="/fonts/main.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/css/critical.css" as="style">

<!-- Lazy load non-critical resources -->
<img src="hero.jpg" alt="Hero" loading="lazy">
<video src="video.mp4" preload="none"></video>
```

### Step 2: Bundle Optimization

Split bundles:

```javascript
// Dynamic imports
const LazyComponent = React.lazy(() => import('./LazyComponent'));

// Route-based splitting
const Home = React.lazy(() => import('./pages/Home'));
const About = React.lazy(() => import('./pages/About'));
```

### Step 3: Caching Strategy

Implement proper caching:

```javascript
// Service Worker
self.addEventListener('fetch', (event) => {
  if (event.request.url.includes('/api/')) {
    // Network first for API calls
    event.respondWith(
      fetch(event.request).catch(() => {
        return caches.match(event.request);
      })
    );
  } else {
    // Cache first for static assets
    event.respondWith(
      caches.match(event.request).then((response) => {
        return response || fetch(event.request);
      })
    );
  }
});
```

### Step 4: Runtime Performance

Optimize JavaScript execution:

```javascript
// Use requestAnimationFrame for animations
function animate() {
  // Update animation
  requestAnimationFrame(animate);
}

// Use Web Workers for heavy computations
const worker = new Worker('worker.js');
worker.postMessage({ data: largeDataSet });

// Debounce scroll events
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}
```

## Examples

### Performance Monitoring

```javascript
// Measure Core Web Vitals
function measureLCP() {
  const observer = new PerformanceObserver((list) => {
    const entries = list.getEntries();
    const lastEntry = entries[entries.length - 1];
    console.log('LCP:', lastEntry.startTime);
  });
  
  observer.observe({ entryTypes: ['largest-contentful-paint'] });
}

// Measure FID
function measureFID() {
  const observer = new PerformanceObserver((list) => {
    const entries = list.getEntries();
    entries.forEach((entry) => {
      console.log('FID:', entry.processingStart - entry.startTime);
    });
  });
  
  observer.observe({ entryTypes: ['first-input'] });
}
```

## Best Practices

1. Optimize asset loading
2. Split bundles
3. Implement proper caching
4. Optimize JavaScript execution
5. Monitor Core Web Vitals
6. Use performance budgets

## References

- [Web Performance Best Practices](https://web.dev/performance/)
- [Core Web Vitals](https://web.dev/vitals/)