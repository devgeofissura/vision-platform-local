---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-15
name: two-stage-code-review
description: Code review in two passes — machine-checkable correctness first, then design and intent — before merging
category: methodology
version: 0.1.0
author: devtiagoabreu
tags: [code-review, review, methodology, quality, collaboration]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - git-worktrees
provides:
  - A repeatable two-stage review process
  - Clear separation of mechanical and design feedback
  - A done definition for merging
difficulty: intermediate
---

# Two-Stage Code Review

## Overview

Reviews fail when a single pass mixes trivial nits with deep design concerns.
Split review into two stages with different goals:

1. **Stage 1 — Correctness**: machine-checkable properties (builds, tests,
   lint, no secrets, no obvious bugs).
2. **Stage 2 — Intent and design**: whether the change fits the architecture,
   is readable, and matches the plan's acceptance criteria.

Only merge when both stages pass. This complements `quality/code-review-best-practices`
by defining an explicit two-pass order.

## Prerequisites

- A mergeable branch with passing CI where available
- The plan's acceptance criteria for the change (`writing-plans`)

## Usage Instructions

### Step 1: Stage 1 — mechanical correctness

Run, in this order, and stop at the first failure:

```bash
./scripts/test.sh          # or the project test command
./core/quality/validate.sh
git diff --check           # whitespace errors
```

Additionally scan for: secrets or keys committed, debug statements,
unintended files (build output, local config). Flag anything found as a
Stage 1 blocker.

### Step 2: Stage 2 — intent and design

Review the diff with these questions:

- Does it fulfill the acceptance criteria from the plan?
- Does it follow the architecture of the codebase?
- Are names, structure and error handling clear?
- Is there duplication that should be extracted?
- Are tests meaningful, or do they just assert the implementation?

### Step 3: Give structured feedback

Tag each comment as `[blocker]` (must fix) or `[nit]` (nice to have). Blocker
comments cite the violated criterion or guideline. Nits never block the merge.

### Step 4: Verify fixes and merge

Confirm every `[blocker]` is addressed with evidence, re-run Stage 1, then
merge. Close the loop by checking the worktree was removed.

## Examples

### Example 1: Stage 1 finding

```
[blocker] assets/.env committed with a real API key.
Evidence: git show HEAD -- assets/.env
Fix: remove from history, rotate key, add to .gitignore.
```

### Example 2: Stage 2 finding

```
[nit] error handling duplicated between reports.py and invoices.py.
Suggestion: extract a shared decorator. Not blocking.
```

## Best Practices

1. Run Stage 1 before reading for design
2. Cite evidence for every blocker
3. Tag feedback `[blocker]`/`[nit]` explicitly
4. Review the plan's criteria, not just the diff
5. Do not merge with unresolved blockers
6. Keep reviews short and review early, review often

## References

- [Google's Engineering Practices — code review](https://google.github.io/eng-practices/review/review-look-for/)
- [Superpowers two-stage code review](https://github.com/obra/superpowers/blob/main/skills/two-stage-code-review/two-stage-code-review.md)
