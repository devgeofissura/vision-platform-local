---
name: performance-review
description: Analyze and improve the performance of a codebase or running system
category: performance
version: 0.1.0
author: devtiagoabreu
tags: [performance, optimization, profiling, benchmarks]
compatible:
  - opencode
  - claude-code
  - cursor
variables:
  - name: codebase
    description: Codebase or system under review
  - name: performance_concerns
    description: Known bottlenecks and performance requirements
---

# Performance Review

## Objective

Identify performance bottlenecks in a codebase or system, quantify their
impact, and recommend optimizations backed by benchmarks.

## Instructions

### Context

You are a performance engineer. Analyze algorithmic, query, and
infrastructure hot spots against stated performance requirements.

### Task

1. Review algorithms and data structures for complexity
2. Analyze database queries, N+1 patterns, and indexing
3. Inspect caching, batching, and async behavior
4. Profile memory and I/O hot spots
5. Recommend targeted optimizations with expected impact

### Criteria

1. **Evidence:** Recommendations are backed by measurements
2. **Impact:** Optimizations target real bottlenecks
3. **Safety:** Changes do not regress correctness
4. **Prioritized:** Fixes ordered by effort-to-benefit ratio

## Usage Example

```
Review the performance of:

Codebase: {{codebase}}

Concerns: {{performance_concerns}}

Please:
1. Find algorithmic and query hot spots
2. Check caching and batching opportunities
3. Suggest benchmarks to verify improvements
4. Prioritize optimizations by impact and effort
```

## Variations

### Variation 1: Query Optimization

```
Optimize the database access patterns:
1. Detect N+1 queries and missing indexes
2. Suggest query rewrites and pagination
3. Estimate query latency improvement
```

### Variation 2: Frontend Performance

```
Review frontend performance:
1. Analyze bundle size and code splitting
2. Check render-blocking resources
3. Suggest caching and lazy loading
```

## References

- [High Performance Browser Networking](https://hpbn.co/)
- [Use the Platform](https://web.dev/learn/performance)
