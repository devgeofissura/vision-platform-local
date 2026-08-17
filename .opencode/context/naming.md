---
name: naming-context
description: Naming conventions for OpenCode Engineering Kit
type: conventions
version: 0.1.0
author: devtiagoabreu
---

# Naming Conventions

## Files

| Type | Format | Example |
|------|--------|---------|
| Skill | kebab-case.md | `docker-best-practices.md` |
| Agent | kebab-case.md | `devops-engineer.md` |
| Template | kebab-case/ | `new-project/` |
| Prompt | kebab-case.md | `code-review-checklist.md` |
| Command | kebab-case.md | `/review` |
| Context | kebab-case.md | `project.md` |
| Script | kebab-case.sh | `bootstrap.sh` |
| Document | kebab-case.md | `getting-started.md` |

## Directories

| Type | Format | Example |
|------|--------|---------|
| Category | kebab-case | `code-quality/` |
| Project | kebab-case | `opencode-engineering-kit/` |
| Template | kebab-case | `new-project/` |

## Variables

| Context | Format | Example |
|---------|--------|---------|
| YAML | snake_case | `skill_name` |
| Bash | UPPER_SNAKE | `SKILL_NAME` |
| Markdown | {{snake_case}} | `{{skill_name}}` |

## Commands

| Context | Format | Example |
|---------|--------|---------|
| CLI | kebab-case | `opencode-engineering-kit` |
| Internal command | /kebab-case | `/review` |

## Tags

| Context | Format | Example |
|---------|--------|---------|
| YAML tags | lowercase | `docker, containers` |
| GitHub tags | lowercase | `enhancement, bug` |

## General Rules

1. **Consistency:** Maintain the same format throughout the project
2. **Clarity:** Names should be self-explanatory
3. **Brevity:** Short but descriptive names
4. **No spaces:** Use hyphens or underscores
5. **No special characters:** Only [a-z0-9-_]

## Examples

### Skills

```
✅ docker-best-practices
✅ kubernetes-deployment
✅ code-review-checklist
❌ Docker Best Practices
❌ kubernetes_deployment
❌ CodeReviewChecklist
```

### Agents

```
✅ devops-engineer
✅ frontend-developer
✅ fullstack-developer
❌ DevOps Engineer
❌ frontend_developer
❌ FullstackDeveloper
```

### Templates

```
✅ new-project/
✅ opencode-config/
✅ skill/
❌ New Project/
❌ opencode_config/
❌ Skill/
```

### Variables

```yaml
# YAML - snake_case
skill_name: docker-best-practices
author_name: devtiagoabreu
```

```bash
# Bash - UPPER_SNAKE_CASE
SKILL_NAME="docker-best-practices"
AUTHOR_NAME="devtiagoabreu"
```

```markdown
# Markdown - {{snake_case}}
{{skill_name}}
{{author_name}}
```
