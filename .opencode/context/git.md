---
name: git-context
description: Git conventions for OpenCode Engineering Kit
type: git
version: 0.1.0
author: devtiagoabreu
---

# Git Conventions

## Branch Naming

| Type | Pattern | Example |
|------|---------|---------|
| Feature | `feature/<name>` | `feature/docker-skill` |
| Bug fix | `bugfix/<name>` | `bugfix/fix-typo` |
| Hotfix | `hotfix/<name>` | `hotfix/security-patch` |
| Documentation | `docs/<name>` | `docs/update-readme` |
| Refactor | `refactor/<name>` | `refactor/restructure-skills` |

## Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types

| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature | `feat: add docker-best-practices skill` |
| `fix` | Bug fix | `fix: correct typo in README` |
| `docs` | Documentation | `docs: update installation guide` |
| `style` | Formatting (no logic change) | `style: fix indentation` |
| `refactor` | Refactoring | `refactor: restructure skill format` |
| `test` | Adding tests | `test: add skill validation tests` |
| `chore` | Maintenance tasks | `chore: update dependencies` |

### Examples

```bash
git commit -m "feat: add docker-best-practices skill"
git commit -m "fix: correct typo in README"
git commit -m "docs: update installation guide"
git commit -m "style: fix indentation in conventions.md"
git commit -m "refactor: restructure skill format"
git commit -m "test: add skill validation tests"
git commit -m "chore: update dependencies"
```

## Pull Requests

### Title

Use Conventional Commits format:

```
feat: add docker-best-practices skill
```

### Description

Include:

- What was done
- Why it was done
- Related issues
- Screenshots if applicable

### Checklist

- [ ] Code follows style guide
- [ ] Tests pass locally
- [ ] Documentation updated
- [ ] At least 1 example included
- [ ] Commit messages follow Conventional Commits
- [ ] Branch is up to date with main

## Tags

Use semantic versioning:

```bash
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

## Gitignore

The project uses a standard `.gitignore` for:

- Operating system files
- IDE configuration
- Node modules (if applicable)
- Build artifacts
- Environment variables
