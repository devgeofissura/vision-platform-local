---
name: documentation-context
description: Documentation conventions for OpenCode Engineering Kit
type: conventions
version: 0.1.0
author: devtiagoabreu
---

# Documentation Conventions

## Documentation Types

| Type | Location | Purpose |
|------|----------|---------|
| README | Project root | Overview |
| CONTRIBUTING | Project root | How to contribute |
| CHANGELOG | Project root | History |
| PROJECT_SPEC | Project root | Specification |
| ROADMAP | Project root | Roadmap |
| API Docs | docs/api.md | API reference |
| Skills Docs | In each skill | Skill usage |
| Agent Docs | In each agent | Agent usage |

## Documentation Patterns

### README.md

````markdown
# Project Name

> Brief description

## Overview

Detailed description...

## Installation

### Prerequisites

- Requirement 1
- Requirement 2

### Installation

```bash
command
```

## Usage

### Basic Example

```bash
command
```

### Advanced Example

```bash
command
```

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md)

## License

[MIT](./LICENSE)
````

### CONTRIBUTING.md

````markdown
# Contributing

## How to Contribute

1. Fork the project
2. Create a branch
3. Implement your feature
4. Add tests
5. Update documentation
6. Create a PR

## Branch Naming

- `feature/<name>` - New feature
- `bugfix/<name>` - Bug fix
- `hotfix/<name>` - Urgent fix

## Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add new skill
fix: correct typo in README
docs: update installation guide
```

## Code Review

Every PR needs at least 1 approval.

## Tests

Run tests before submitting PR:

```bash
./scripts/test.sh
```
````

## Documentation Generation

| Tool | Usage | Automation |
|------|-------|------------|
| Markdown lint | Check formatting | GitHub Actions |
| Link checker | Check links | GitHub Actions |
| Spell check | Check spelling | Manual |
| Screenshot | Capture images | Manual |

## Documentation Maintenance

1. **Auto-update:** CHANGELOG via commits
2. **Manual review:** README and CONTRIBUTING
3. **Validation:** Links and examples
4. **Versioning:** Synced with releases

## File Formats

### Skills

```markdown
---
name: skill-name
description: Description
category: category
version: 1.0.0
author: Author
tags: [tag1, tag2]
compatible:
  - opencode
  - claude-code
  - cursor
---

# Skill Name

## Overview
## Prerequisites
## Usage Instructions
## Examples
## References
## Notes
```

### Agents

```markdown
---
name: agent-name
description: Description
version: 1.0.0
author: Author
tags: [tag1, tag2]
compatible:
  - opencode
  - claude-code
  - cursor
skills: []
personas: []
---

# Agent Name

## Persona
## Capabilities
## Context
## Usage Examples
## References
```

### Templates

```markdown
---
name: template-name
description: Description
category: category
version: 1.0.0
author: Author
tags: [tag1, tag2]
compatible:
  - opencode
  - claude-code
  - cursor
variables: []
---

# Template Name

## Overview
## Usage
## Structure
## Variables
## Example
## References
```
