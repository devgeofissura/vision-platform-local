---
name: refactoring-plan
description: Create a structured, risk-aware refactoring plan for existing code
category: refactoring
version: 0.1.0
author: devtiagoabreu
tags: [refactoring, technical-debt, code-quality, maintenance]
compatible:
  - opencode
  - claude-code
  - cursor
variables:
  - name: codebase_area
    description: Module or area of the codebase to refactor
  - name: goals
    description: Refactoring goals and success criteria
---

# Refactoring Plan

## Objective

Produce a step-by-step refactoring plan that improves code structure
without changing behavior, reducing technical debt and risk.

## Instructions

### Context

You are an experienced software engineer focused on code quality.
Analyze the target code, identify structural problems, and design
small, safe refactoring steps.

### Task

1. Identify code smells and structural problems
2. Define concrete goals and success criteria
3. Order refactoring steps so each stays behavior-preserving
4. Identify tests that protect each step
5. Define rollback and verification points

### Criteria

1. **Safety:** Each step preserves observable behavior
2. **Incrementality:** Steps are small and independently reviewable
3. **Coverage:** Tests exist to validate each change
4. **Measurable:** Success criteria are explicit

## Usage Example

```
Create a refactoring plan for:

Area: {{codebase_area}}

Goals: {{goals}}

Please:
1. List the main code smells found
2. Propose ordered refactoring steps
3. Specify tests that guard each step
4. Define how to verify success
```

## Variations

### Variation 1: Dead Code Cleanup

```
Plan removal of dead and unused code:
1. How to detect dead code safely
2. How to verify removal changes nothing
3. Which code to preserve for reference
```

### Variation 2: Legacy Migration

```
Plan a step-by-step migration of legacy code:
1. Identify migration increments
2. Define compatibility shims between increments
3. Sequence cutover and rollback strategy
```

## References

- [Refactoring: Improving the Design of Existing Code](https://martinfowler.com/books/refactoring.html)
- [Refactoring Guru Catalog](https://refactoring.guru/refactoring)
