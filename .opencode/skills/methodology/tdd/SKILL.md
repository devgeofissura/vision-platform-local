---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-15
name: tdd
description: Test-driven development discipline — write a failing test, make it pass, refactor, repeat
category: methodology
version: 0.1.0
author: devtiagoabreu
tags: [tdd, testing, red-green-refactor, quality, methodology]
compatible:
  - opencode
  - claude-code
  - cursor
provides:
  - Red-Green-Refactor discipline
  - Confidence from tests written before code
  - Minimal, behavior-focused test suites
difficulty: intermediate
---

# Test-Driven Development (TDD)

## Overview

TDD is a development rhythm: write a failing test that describes the next
behavior (Red), make it pass with the simplest change (Green), then improve
the code without changing behavior (Refactor). The result is a suite that
documents behavior and catches regressions early.

This skill complements `testing/unit-testing` (which covers structure and
technique) by adding the discipline and ordering.

## Prerequisites

- A testing framework for the language (pytest, Jest, go test, ...)
- A runnable test command with fast feedback

## Usage Instructions

### Step 1: Red — write the failing test

Write the smallest test that describes the next behavior. Run it and confirm
it fails for the right reason (not a setup error):

```python
def test_invoice_total_applies_discount():
    invoice = Invoice(amount=100, discount_pct=10)
    assert invoice.total() == 90
```

### Step 2: Green — make it pass

Implement the simplest thing that satisfies the test. Do not gold-plate:

```python
class Invoice:
    def __init__(self, amount, discount_pct):
        self._amount = amount
        self._discount_pct = discount_pct

    def total(self):
        return self._amount * (1 - self._discount_pct / 100)
```

### Step 3: Refactor

Remove duplication and improve naming while keeping tests green. This is the
only step where you can safely reshape the code.

### Step 4: Repeat

Pick the next behavior and go around the loop. Keep steps small — minutes,
not hours.

### Step 5: Apply outside-in when needed

For integrated features, write a coarse end-to-end test first (see
`testing/e2e-testing`) to anchor the feature, then drive the internals with
unit tests.

## Examples

### Example 1: Full loop in pytest

```python
# test_checkout.py (Red)
def test_checkout_charges_tax_for_state():
    assert checkout_total(100, state="CA") == 108.25
```

```python
# checkout.py (Green)
def checkout_total(amount, state):
    rates = {"CA": 0.0825}
    return round(amount * (1 + rates.get(state, 0)), 2)
```

### Example 2: Refactor step

```python
def checkout_total(amount, state):
    return round(amount * (1 + TAX_RATES.get(state, 0.0)), 2)  # extracted constant
```

## Best Practices

1. Test one behavior per test
2. Confirm Red fails for the right reason before writing code
3. Smallest change to get Green
4. Refactor only between Red and Green
5. Keep the suite fast; run it continuously
6. Commit on each Green, never on Red

## References

- [Kent Beck — Test-Driven Development](https://www.goodreads.com/book/show/387190.Test_Driven_Development)
- [The Three Laws of TDD (Uncle Bob)](https://blog.cleancoder.com/uncle-bob/2014/12/17/TheCyclesOfTDD.html)
