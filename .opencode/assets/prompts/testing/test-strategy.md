---
name: test-strategy
description: Design a comprehensive test strategy that balances coverage and effort
category: testing
version: 0.1.0
author: devtiagoabreu
tags: [testing, strategy, coverage, quality]
compatible:
  - opencode
  - claude-code
  - cursor
variables:
  - name: project
    description: Project, stack, and testing constraints
  - name: testing_goals
    description: Quality goals and risk areas to cover
---

# Test Strategy

## Objective

Define a pragmatic, layered test strategy that protects critical
functionality with the right test types and coverage targets.

## Instructions

### Context

You are a QA strategist. Analyze the project to decide where unit,
integration, and end-to-end testing provide the most value.

### Task

1. Identify critical functionality and risk areas
2. Choose the test pyramid layers that fit the stack
3. Define test types, tools, and coverage targets
4. Specify test data strategy and CI integration
5. Define quality gates and reporting

### Criteria

1. **Proportionality:** Coverage matches risk and complexity
2. **Clarity:** Responsibilities of each test layer are explicit
3. **Feasibility:** Strategy fits the stack and CI setup
4. **Measurable:** Targets and gates are quantified

## Usage Example

```
Design a test strategy for:

Project: {{project}}

Goals: {{testing_goals}}

Please:
1. Rank critical areas by risk
2. Propose unit, integration, and E2E layers with tools
3. Define coverage targets per layer
4. Outline CI integration and quality gates
```

## Variations

### Variation 1: Regression Strategy

```
Design a regression test strategy:
1. Identify high-churn, high-risk modules
2. Prioritize automated regression suites
3. Define smoke tests for every release
```

### Variation 2: Test Data Strategy

```
Plan the test data approach:
1. Choose fixtures, factories, or seed data
2. Isolate tests from shared data
3. Handle sensitive data in test environments
```

## References

- [Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html)
- [Google Testing on the Toilet](https://testing.googleblog.com/)
