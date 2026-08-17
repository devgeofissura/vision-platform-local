---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-15
name: writing-plans
description: Transform an approved direction into a concrete, executable plan with phases, tasks and acceptance criteria
category: methodology
version: 0.1.0
author: devtiagoabreu
tags: [planning, plans, methodology, execution, architecture]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - brainstorming
provides:
  - A plan document with clear phases and tasks
  - Acceptance criteria for every task
  - Identification of dependencies and risks
difficulty: intermediate
---

# Writing Plans

## Overview

A plan is the bridge between a decided direction and its execution. This
skill produces a plan that another agent or a developer can execute without
re-deciding anything: each task has a goal, an owner, a checklist and
acceptance criteria.

Follow `brainstorming` first so the direction is already confirmed.

## Prerequisites

- A confirmed direction (from `brainstorming` or the user)
- Knowledge of the relevant stack and existing kit assets

## Usage Instructions

### Step 1: Split into phases

Break the work into 3-8 phases, each ending in a checkable state. Example:
investigate -> scaffold -> core -> tests -> docs -> release.

### Step 2: Define tasks

For each phase list tasks. A task must be small enough to be done in one
sitting and explicit enough that no judgment call is left open. Name tasks
with an action verb: "add endpoint", "write test", "update README".

### Step 3: Write acceptance criteria

For every task write at least one checkable outcome. "Feature works" is not
checkable; "GET /reports returns 200 with a valid PDF" is.

### Step 4: Map dependencies

Order tasks so each one only depends on completed tasks. Note which tasks can
run in parallel (e.g. using `git-worktrees`).

### Step 5: Identify risks and rollback

List the top risks and, for each, the mitigation. State how to roll back a
failed phase (git revert, feature flag, worktree deletion).

### Step 6: Present the plan

Show phases, tasks, criteria, and risks as a table. Ask for approval before
executing. Use the orchestrator agent for large multi-agent plans.

## Examples

### Example 1: Phase table

| Phase | Task | Acceptance criterion |
|-------|------|----------------------|
| Scaffold | Add project structure | `npm run dev` starts with empty state |
| Core | Add report endpoint | `GET /reports` returns 200 + valid PDF |
| Tests | Cover report endpoint | `pytest` green, branch covered |
| Docs | Update README | README documents the endpoint |

### Example 2: Risk table

| Risk | Mitigation | Rollback |
|------|-----------|----------|
| PDF library breaking | Pin version, golden tests | Revert dependency bump |
| API contract change | Version the endpoint | Keep old route |

### Example 3: Plan skeleton

```markdown
# Plan: <title>

## Phase 1 — <name>
- [ ] Task 1 (acceptance: <criterion>)
- [ ] Task 2 (acceptance: <criterion>)

## Phase 2 — <name>
- [ ] Task 3 (acceptance: <criterion>)

## Risks
| Risk | Mitigation | Rollback |
|------|-----------|----------|
| ...   | ...        | ...      |
```

## Best Practices

1. Write acceptance criteria before writing code
2. Keep tasks atomic and actionable
3. Order tasks by dependency, not by comfort
4. State rollback strategy per risky task
5. Get explicit approval before execution
6. Execute with `executing-plans`

## References

- [Superpowers writing-plans](https://github.com/obra/superpowers/blob/main/skills/writing-plans/writing-plans.md)
- [Google's Design Docs](https://www.industrialempathy.com/posts/design-docs-at-google/)
