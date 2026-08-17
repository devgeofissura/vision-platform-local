---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: open-source-contributing
description: Guide for contributing effectively to open source projects
category: community
version: 0.1.0
author: devtiagoabreu
tags: [open-source, contributing, community, github]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Git and GitHub account
  - Basic understanding of PRs
provides:
  - Contribution checklist
  - PR template
  - Issue triage workflow
---

# Open Source Contributing

## Overview

This skill provides a complete guide for contributing to open source projects
effectively: finding good first issues, writing useful issues and pull requests,
and communicating with maintainers and the community.

## Prerequisites

- Git installed and configured
- A GitHub (or equivalent) account
- Basic knowledge of branching and pull requests

## Usage Instructions

### 1. Finding Your First Contribution

Start with small, well-scoped tasks:

```bash
# Search for beginner-friendly issues
gh search issues --label "good first issue" --state open

# Browse a project's contribution guide first
gh repo view owner/repo --web
```

### 2. Writing a Good Issue

A good issue is specific and reproducible:

```markdown
### Description
[What is broken or what feature is missing]

### Steps to Reproduce
1. Run `command`
2. Open page X
3. Observe error

### Expected Behavior
[What should happen]

### Environment
- Version: 0.1.0
- OS: Ubuntu 24.04
```

### 3. Opening a Pull Request

Keep PRs small and descriptive:

```bash
git checkout -b fix/typo-in-docs
# make your change
git add .
git commit -m "fix(docs): correct typo in installation guide"
git push -u origin fix/typo-in-docs
gh pr create --title "fix(docs): correct typo" --body "Closes #123"
```

## Examples

### Example 1: Reading the Project Before Contributing

```bash
# Always read these first
cat CONTRIBUTING.md
cat CODE_OF_CONDUCT.md
cat README.md
```

### Example 2: Responding to Review Feedback

```bash
# Amend and force-push is expected on feature branches
git add .
git commit --amend --no-edit
git push --force-with-lease
```

## References

- [GitHub Contributing Guidelines](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [How to Contribute to Open Source](https://opensource.guide/how-to-contribute/)

## Notes

- Always respect the project's code of conduct
- Communicate clearly and patiently with maintainers
- Never rewrite public commit history with force push
- Link related issues in your PR description
