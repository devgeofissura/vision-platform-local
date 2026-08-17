---
name: feature-planning
description: Plan a feature end-to-end from requirements to implementation tasks
category: planning
version: 0.1.0
author: devtiagoabreu
tags: [planning, feature, requirements, backlog]
compatible:
  - opencode
  - claude-code
  - cursor
variables:
  - name: feature_name
    description: Name of the feature to plan
  - name: requirements
    description: Feature requirements and constraints
---

# Feature Planning

## Objective

Break a feature down into a clear, actionable implementation plan,
covering scope, tasks, and acceptance criteria before any code is written.

## Instructions

### Context

You are a product-focused planner. Analyze the feature request, clarify
its scope, and structure it into a delivery plan that a development team
can execute.

### Task

1. Clarify the feature goal and non-negotiable requirements
2. Define scope, assumptions, and out-of-scope items
3. Decompose the feature into ordered, testable tasks
4. Identify risks, dependencies, and required skills
5. Define acceptance criteria for the completed feature

### Criteria

1. **Clarity:** Can any developer pick up the tasks?
2. **Completeness:** Are edge cases and acceptance criteria covered?
3. **Ordering:** Are tasks sequenced with dependencies in mind?
4. **Testability:** Can each task be verified independently?

## Usage Example

```
Plan the following feature:

Feature: {{feature_name}}

Requirements: {{requirements}}

Please:
1. State the goal and scope
2. List implementation tasks in dependency order
3. Define acceptance criteria for each task
4. Highlight risks and dependencies
```

## Variations

### Variation 1: Sprint Backlog Breakdown

```
Break this feature into sprint-sized tasks:
1. Estimate relative effort per task
2. Suggest task priorities
3. Flag tasks ready for parallel work
```

### Variation 2: MVP Scoping

```
Define the smallest valuable slice of this feature:
1. List must-have vs nice-to-have capabilities
2. Describe the MVP user flow
3. Outline what is explicitly deferred
```

## References

- [Sprint Planning](https://www.atlassian.com/agile/scrum/sprint-planning)
- [Acceptance Criteria](https://www.agilealliance.org/glossary/acceptance-criteria/)
