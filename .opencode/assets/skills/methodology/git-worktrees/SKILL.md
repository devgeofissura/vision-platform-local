---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-15
name: git-worktrees
description: Isolate parallel tasks in git worktrees so execution never blocks on a dirty working directory
category: methodology
version: 0.1.0
author: devtiagoabreu
tags: [git, worktree, parallel-work, methodology, branch-management]
compatible:
  - opencode
  - claude-code
  - cursor
provides:
  - Parallel working directories for concurrent tasks
  - A clean main checkout for verification
  - Trivial rollback by deleting a worktree
difficulty: intermediate
---

# Git Worktrees

## Overview

A git worktree is a second working directory checked out to a different
branch of the same repository. Instead of stashing and switching, you keep one
worktree per task. This makes parallel work safe and makes rollback as simple
as deleting a directory.

## Prerequisites

- Git 2.5+
- A plan with tasks that can proceed in parallel (`writing-plans`)

## Usage Instructions

### Step 1: Create a worktree per task

```bash
git worktree add ../kit-task-report -b feat/report-endpoint
```

### Step 2: Work inside the worktree

All normal git commands work inside it. Commit there; your main checkout stays
clean:

```bash
cd ../kit-task-report
# ... implement, test, commit ...
git push origin feat/report-endpoint
```

### Step 3: Run verification from a clean checkout

Use your main checkout (or a CI run) for final verification, since worktrees
may carry unmerged changes.

### Step 4: Merge and clean up

```bash
git switch main && git merge feat/report-endpoint
git worktree remove ../kit-task-report
```

### Step 5: Roll back a failed task

```bash
git worktree remove ../kit-task-report  # discards the failed experiment
git branch -D feat/report-endpoint
```

## Examples

### Example 1: Two parallel tasks

```bash
git worktree add ../kit-report    -b feat/report-endpoint
git worktree add ../kit-cache     -b feat/cache-layer
# work on both simultaneously without interference
```

### Example 2: Inspect without leaving your branch

```bash
git worktree add ../kit-spike -b spike/pg-migration
# try the migration there, delete the worktree, main is untouched
```

## Best Practices

1. One worktree per task, named after the branch
2. Keep the main checkout clean for verification
3. Delete worktrees after merging
4. Use worktrees to make risky experiments free to discard
5. Use short-lived worktrees; long-lived ones lose the benefit

## References

- [Git documentation — git-worktree](https://git-scm.com/docs/git-worktree)
- [Superpowers git-worktrees](https://github.com/obra/superpowers/blob/main/skills/git-worktrees/git-worktrees.md)
