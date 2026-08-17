---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: git-workflow
description: Complete guide to Git workflow and best practices
category: git
version: 0.1.0
author: devtiagoabreu
tags: [git, workflow, version-control, branching]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Git 2.0+ installed
provides:
  - Branching strategy
  - Commit conventions
  - Best practices
---

# Git Workflow

## Overview

This skill provides a complete guide to Git workflow, including branching strategies, commit conventions, and best practices.

## Prerequisites

- Git 2.0 or higher
- Basic knowledge of Git
- Configuration of user.name and user.email

## Usage Instructions

### 1. Branching Strategy

```
main (production)
├── develop (integration)
│   ├── feature/new-feature
│   ├── feature/another-feature
│   └── bugfix/fix
├── release/v1.0.0
└── hotfix/urgent-fix
```

### 2. Branch Naming

| Type | Format | Example |
|------|--------|---------|
| Feature | feature/<name> | feature/login |
| Bugfix | bugfix/<name> | bugfix/typo |
| Hotfix | hotfix/<name> | hotfix/security |
| Release | release/<version> | release/v1.0.0 |
| Docs | docs/<name> | docs/readme |

### 3. Commit Conventions

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>: <description>

[optional body]

[optional footer]
```

#### Types

| Type | Description |
|------|-------------|
| feat | New feature |
| fix | Bug fix |
| docs | Documentation |
| style | Formatting (no logic change) |
| refactor | Refactoring |
| test | Adding tests |
| chore | Maintenance tasks |
| perf | Performance improvement |
| ci | CI/CD changes |
| build | Build changes |

#### Examples

```
feat: add user authentication

- Implement JWT token generation
- Add login endpoint
- Add middleware for token validation

Closes #123
```

```
fix: resolve memory leak in cache

The cache was not properly releasing memory when items expired.
Implemented proper cleanup mechanism.

Fixes #456
```

### 4. Workflow

#### Feature Branch

```bash
# Create branch
git checkout develop
git pull origin develop
git checkout -b feature/my-feature

# Work
git add .
git commit -m "feat: add my feature"

# Push
git push origin feature/my-feature

# Create PR to develop
```

#### Bugfix Branch

```bash
# Create branch
git checkout develop
git checkout -b bugfix/my-bug

# Fix
git add .
git commit -m "fix: correct my bug"

# Push and PR
```

#### Hotfix Branch

```bash
# Create branch
git checkout main
git checkout -b hotfix/urgent-fix

# Fix
git add .
git commit -m "fix: resolve security vulnerability"

# Push and PR to main
# Then merge to develop
```

### 5. Useful Commands

```bash
# Update develop
git checkout develop
git pull origin develop

# Create feature
git checkout -b feature/my-skill develop

# Commit
git add .
git commit -m "feat: add my-skill"

# Push
git push origin feature/my-skill

# Create PR
gh pr create --base develop --head feature/my-skill

# Merge PR
gh pr merge <pr-number> --squash

# Delete branch
git branch -d feature/my-skill
git push origin --delete feature/my-skill
```

### 6. Tags

```bash
# Create annotated tag
git tag -a v1.0.0 -m "Release 1.0.0"

# Push tags
git push origin v1.0.0

# List tags
git tag -l
```

## Examples

### Example 1: Complete Flow

```bash
# 1. Update develop
git checkout develop
git pull origin develop

# 2. Create feature
git checkout -b feature/user-auth

# 3. Implement
# ... code ...

# 4. Commit
git add .
git commit -m "feat: add user authentication"

# 5. Push
git push origin feature/user-auth

# 6. Create PR
gh pr create --base develop --title "feat: Add user authentication" --body "Implement JWT authentication"

# 7. After merge, delete branch
git checkout develop
git pull origin develop
git branch -d feature/user-auth
```

## References

- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)
- [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Pro Git Book](https://git-scm.com/book/)

## Notes

- Never commit directly to main
- Always use Pull Requests
- Keep commits atomic
- Write clear messages
- Delete branches after merge
- Use .gitignore appropriately
