---
name: stack-context
description: Tech stack for OpenCode Engineering Kit
type: architecture
version: 0.1.0
author: devtiagoabreu
---

# Tech Stack

## Core Components

### Markdown

- **Usage:** Documentation, Skills, Agents, Templates, Prompts
- **Version:** CommonMark
- **Extensions:** YAML frontmatter

### YAML

- **Usage:** File metadata, configuration
- **Version:** 1.2
- **Indentation:** 2 spaces

### Bash

- **Usage:** Automation scripts
- **Version:** 4.0+
- **Options:** `set -euo pipefail`

### Git

- **Usage:** Version control
- **Version:** 2.0+
- **Features:** Tags, branches, conventional commits

## Development Tools

### Linting

| Tool | Usage | Configuration |
|------|-------|---------------|
| ShellCheck | Bash linting | .shellcheckrc |
| markdownlint | Markdown linting | .markdownlint.json |
| yamllint | YAML linting | .yamllint.yml |

### CI/CD

| Tool | Usage | File |
|------|-------|------|
| GitHub Actions | Automation | .github/workflows/ |

### Editor

| Tool | Usage | Configuration |
|------|-------|---------------|
| VS Code | Primary editor | .vscode/ |
| Vim | Alternative editor | .editorconfig |

## External Dependencies

### Required

| Dependency | Version | Usage |
|------------|---------|-------|
| Git | 2.0+ | Version control |
| Bash | 4.0+ | Scripts |

### Optional

| Dependency | Version | Usage |
|------------|---------|-------|
| curl | Any | Downloads |
| jq | 1.6+ | JSON processing |
| ShellCheck | Latest | Linting |

## Supported Platforms

### Primary

- **OpenCode:** Native format, full support

### Compatible

- **Claude Code:** Via CLAUDE.md
- **Cursor:** Via .cursor/rules/
- **GitHub Copilot:** Via .github/copilot-instructions.md

## File Formats

| Format | Extension | Usage |
|--------|-----------|-------|
| Markdown | .md | Documentation |
| YAML | .yml, .yaml | Metadata |
| Bash | .sh | Scripts |
| JSON | .json | Configuration |

## References

- [Security](./security.md) - Security best practices
- [Performance](./performance.md) - Performance guidelines
- [Decisions](./decisions.md) - Architecture decisions
