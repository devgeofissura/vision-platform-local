---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: refactoring-techniques
description: Safe refactoring techniques and patterns to improve code without changing behavior
category: quality
version: 0.1.0
author: devtiagoabreu
tags: [refactoring, patterns, code-quality, extract-method, test-driven]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - A working codebase with tests (or willingness to add them first)
  - Git for safe rollback of each step
  - Familiarity with the language's unit test framework
provides:
  - A catalog of proven refactoring patterns with examples
  - A step-by-step safety process for behavior-preserving changes
  - Guidance on when to refactor and when to stop
  - Techniques to reduce risk during large restructures
---

# Refactoring Techniques

## Overview

This skill explains how to improve the internal structure of code without
changing its external behavior. It covers a catalog of classic refactoring
patterns such as Extract Method, Rename, and Replace Conditional with
Polymorphism, each with a concrete example. Every technique follows the same
safe rhythm: cover with tests, change in small steps, run the tests, and commit.
Refactoring is the foundation of keeping a codebase healthy and is best done in
short, focused sessions rather than as a separate "big rewrite".

## Prerequisites

- An automated test suite that exercises the code being changed
- Git available for committing after each safe step
- Ability to run the tests quickly from the command line

## Usage Instructions

### Step 1: Start from a Green Baseline

Never refactor on a red build. Establish safety first:

```bash
git status --short
npm test        # or pytest, cargo test, etc.
git commit -am "test: baseline before refactor"
```

If coverage is missing, add characterization tests that lock in current
behavior before touching anything.

### Step 2: Extract Method

Move a cohesive block into its own named function:

```python
# Before
def process_order(order, discount_rate):
    total = sum(item.price for item in order.items)
    discount = total * discount_rate
    if discount > 100:
        discount = 100
    total -= discount
    save(order.id, total)

# After
def apply_discount(total, discount_rate):
    discount = total * discount_rate
    return total - min(discount, 100)

def process_order(order, discount_rate):
    total = sum(item.price for item in order.items)
    total = apply_discount(total, discount_rate)
    save(order.id, total)
```

Run the tests. Commit. The block now has a name, can be unit tested, and is
reusable.

### Step 3: Replace Conditional with Polymorphism

Swap chains of conditionals for dispatch tables or subclasses:

```python
# Before
def area(shape):
    if shape.kind == "circle":
        return 3.14159 * shape.radius ** 2
    if shape.kind == "rectangle":
        return shape.width * shape.height
    raise ValueError(f"unknown shape {shape.kind}")

# After
class Shape:
    def area(self):
        raise NotImplementedError

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    def area(self):
        return 3.14159 * self.radius ** 2

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width, self.height = width, height
    def area(self):
        return self.width * self.height
```

### Step 4: Work in Micro-Steps

Adopt the Red–Green–Refactor loop with frequent commits:

```bash
# 1. Write failing test
# 2. Make it pass with the simplest change
npm test
# 3. Refactor now that behavior is locked
npm test
git commit -m "refactor: extract apply_discount helper"
```

Keep each step small enough that a failure points to exactly one change.

### Step 5: Rename for Clarity

Rename aggressively when names mislead. Use IDE or language tooling:

```bash
# Python: manual but mechanical
mv report_generator.py report_builder.py

# TypeScript with eslint: find and replace usages
npm run lint -- --fix
```

Prefer renames over comments that explain confusing names.

### Step 6: Know When to Stop

Avoid these anti-patterns:

- **Big-bang rewrites**: replace incrementally instead.
- **Refactoring for its own sake**: no behavior gain, no productivity gain.
- **Mixing refactor and feature work**: keep them in separate commits/PRs.
- **Refactoring on a deadline**: defer to a dedicated, calm session.

## Examples

### Example 1: Guard Clauses Instead of Nested Ifs

```javascript
// Before
function validate(input) {
  if (input) {
    if (input.length > 3) {
      return true;
    } else {
      return false;
    }
  }
  return false;
}

// After
function validate(input) {
  if (!input || input.length <= 3) return false;
  return true;
}
```

### Example 2: Replace Magic Number with Constant

```python
# Before
def retry_after(attempts):
    return attempts * 30

# After
RETRY_BACKOFF_SECONDS = 30

def retry_after(attempts):
    return attempts * RETRY_BACKOFF_SECONDS
```

## References

- [Refactoring.com](https://refactoring.com/)
- [Martin Fowler: Refactoring, Second Edition](https://martinfowler.com/books/refactoring.html)
- [Catalog of Refactorings](https://refactoring.com/catalog/)
- [Source Making: Refactoring](https://sourcemaking.com/refactoring)
- [Working Effectively with Legacy Code](https://www.oreilly.com/library/view/working-effectively-with/0131177052/)
- [Test-Driven Development by Example](https://www.oreilly.com/library/view/test-driven-development/0321146530/)

## Notes

- The tests are the safety net; never refactor without them.
- One behavior change per refactoring session; commit each green step.
- Use your language's refactoring tools (IDE, codemods, jscodeshift).
- Refactor when you touch a file anyway ("camping rule"): leave it cleaner.
- Review large refactors with a reviewer familiar with the subsystem.
- If a step is painful, it is a signal the design needs fixing — not a
  reason to stop.
