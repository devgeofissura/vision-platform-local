---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: git-advanced
description: Advanced Git techniques covering rebase, bisect, worktrees, and hooks
category: tools
version: 0.1.0
author: devtiagoabreu
tags: [git, rebase, bisect, worktree, hooks, history]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Git 2.30 or newer
  - Comfort with basic Git (commit, branch, merge, push)
  - Access to a remote repository (GitHub, GitLab, or self-hosted)
provides:
  - Workflows for clean history with interactive rebase and fixup
  - Steps to bisect and pinpoint regressions automatically
  - Parallel development using linked worktrees
  - Custom git hooks for automation and safety gates
---

# Advanced Git

## Overview

This skill covers Git workflows beyond the basics: rewriting history safely
with interactive rebase, bisecting to find the exact commit that broke a build,
working on multiple branches at once with linked worktrees, and automating
workflow rules with hooks. These techniques turn Git from a storage tool into a
development accelerator. Every workflow here follows a shared principle: make
changes reversible, keep history meaningful, and never rewrite commits that
others have already based work on.

## Prerequisites

- Git 2.30+ (some features like `git switch -c --track` need 2.23+)
- A cloned repository you are allowed to push to
- Backups of any branch before force-pushing rewritten history

## Usage Instructions

### Step 1: Interactive Rebase for Clean History

Squash, reorder, and reword commits before sharing a branch:

```bash
git switch feature/login
git log --oneline main..HEAD
git rebase -i HEAD~5
```

In the editor:

```text
pick 3a1b2c3 add login form
fixup d4e5f6a fix typo in login
pick 7f8a9b0 wire up auth endpoint
reword 1c2d3e4 document env vars
```

Use `fixup` to fold trivial fixes into the commit they belong to. After the
rebase, verify and force-push only your own feature branch:

```bash
git rebase main
git push --force-with-lease origin feature/login
```

### Step 2: Use Fixup and Autosquash

Let Git prepare the fixup for you:

```bash
git add -p
git commit --fixup 3a1b2c3
git rebase --autosquash -i main
```

`--autosquash` automatically places `fixup!` commits under their target.

### Step 3: Bisect a Regression

Let Git binary-search the history to find the offending commit:

```bash
git bisect start
git bisect bad HEAD
git bisect good v1.0.0
git bisect run ./scripts/check.sh   # script exits 0 for good, 1 for bad
```

When the run finishes, Git reports the first bad commit. Automate the check
with the unit test that fails, then:

```bash
git bisect reset
```

### Step 4: Work with Linked Worktrees

Check out multiple branches in parallel without stashing:

```bash
git worktree add ../myproject-feature -b feature/login
git worktree add ../myproject-hotfix -b hotfix/critical
```

Each worktree is a full working directory sharing the same `.git`. List and
clean up when done:

```bash
git worktree list
git worktree remove ../myproject-feature
```

### Step 5: Write Custom Git Hooks

Add a pre-push hook to block secrets and force-pushes to main:

```bash
git config core.hooksPath .githooks
cat > .githooks/pre-push << 'EOF'
#!/bin/sh
set -e
if echo "$@" | grep -q "refs/heads/main" && [ "$1" = "--force" ]; then
  echo "Forbidden: force-push to main is blocked by pre-push hook." >&2
  exit 1
fi
grep -rn --include="*.py" --include="*.ts" --include="*.env*" "BEGIN PRIVATE KEY" . || true
EOF
chmod +x .githooks/pre-push
```

### Step 6: Use Reflog as a Safety Net

Recover from any misstep using the reflog:

```bash
git reflog
git checkout HEAD@{2}        # jump back in time
git branch -f recover HEAD@{2}  # resurrect a lost branch
```

The reflog records every HEAD move, so almost nothing is permanently lost.

## Examples

### Example 1: Finding the Breaking Commit

```bash
git bisect start
git bisect bad                  # current state is broken
git bisect good main~20         # known good point
git bisect run pytest -x tests/test_login.py
# ...automated passes/fails narrow the range...
git bisect reset
git show --stat <bad-commit>
```

### Example 2: One-Fixup-Per-Review-Comment Flow

```bash
# after review, respond with a fixup commit
git add src/login.ts
git commit --fixup 7f8a9b0
git rebase --autosquash -i main
git push --force-with-lease
```

## References

- [Git Documentation](https://git-scm.com/doc)
- [Git Rebase Documentation](https://git-scm.com/docs/git-rebase)
- [Git Bisect Documentation](https://git-scm.com/docs/git-bisect)
- [Git Worktree Documentation](https://git-scm.com/docs/git-worktree)
- [Git Hooks Documentation](https://git-scm.com/docs/githooks)
- [Pro Git book (free)](https://git-scm.com/book/en/v2)
- [Git Flight Rules](https://github.com/k88hudson/git-flight-rules)

## Notes

- Never rebase branches that others have based work on (public main history).
- Use `--force-with-lease` instead of `--force` to avoid clobbering remote
  updates.
- `git bisect skip` handles commits that cannot build or are unrelated.
- Worktrees are ideal for reviewing PRs and hotfixes while keeping dev state.
- Prefer `git switch` and `git restore` over the older `checkout` semantics.
- Commit messages should explain *why*; the diff already shows *what*.
