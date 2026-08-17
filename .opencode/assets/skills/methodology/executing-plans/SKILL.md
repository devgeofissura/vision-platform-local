---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-15
name: executing-plans
description: Execute an approved plan task by task, verifying each acceptance criterion before moving on
category: methodology
version: 0.1.0
author: devtiagoabreu
tags: [planning, execution, methodology, verification, discipline]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - writing-plans
provides:
  - Disciplined task-by-task execution of an approved plan
  - Verification of acceptance criteria before progress
  - Progress reporting with evidence
difficulty: intermediate
---

# Executing Plans

## Overview

Execution is where plans fail. This skill keeps execution honest: do one task
at a time, verify its acceptance criteria with evidence, and only then move to
the next task. If something in the plan proves wrong, stop and revise the plan
— do not silently improvise.

## Prerequisites

- An approved plan from `writing-plans`
- The tools needed to verify each criterion (test runner, linter, build)

## Usage Instructions

### Step 1: Load the plan

Restate the current phase, its tasks and their acceptance criteria. If any
criterion is unclear, clarify before starting.

### Step 2: Do one task

Work on exactly one task. Keep changes scoped: one branch or worktree per
task (see `git-worktrees`).

### Step 3: Verify with evidence

Run the verification for the task and capture the result. Evidence is a
command plus its output: `pytest tests/test_reports.py` -> "3 passed". Never
claim a criterion is met without evidence.

### Step 4: Record and commit

Update the plan's status for the task, commit with a clear message, and move
to the next task. If a task cannot be completed, record exactly what blocked
it and which criterion failed.

### Step 5: Handle deviation

If a task violates a plan assumption (new dependency, changed API, scope
creep), stop, update the plan and get approval before continuing. Never
silently expand scope.

### Step 6: Report

At the end of each phase, summarize what passed, what failed, and what
remains. Use the orquestrador persona to coordinate multi-agent plans.

## Examples

### Example 1: Task verification log

```
[phase: core] [task: report endpoint]
criterion: GET /reports returns 200 + valid PDF
evidence: curl -s -o /tmp/out.pdf -w "%{http_code}" localhost:8000/reports
          -> 200; file /tmp/out.pdf -> PDF document
status: PASSED
```

### Example 2: Blocked task

```
criterion: e2e green
evidence: npx playwright test -> 1 of 12 failed (selector timeout)
status: BLOCKED -> selector unstable, plan updated, awaiting approval
```

## Best Practices

1. One task at a time, one branch/worktree per task
2. Evidence before claims — always show command output
3. Stop on plan violations instead of improvising
4. Commit after each verified task
5. Update the plan document as you go
6. Report status with evidence at phase boundaries

## References

- [Superpowers executing-plans](https://github.com/obra/superpowers/blob/main/skills/executing-plans/executing-plans.md)
- [The Checklist Manifesto — evidence over memory](https://en.wikipedia.org/wiki/The_Checklist_Manifesto)
