---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: project-setup
description: New project setup covering repository layout, configuration, and tooling
category: projects
version: 0.1.0
author: devtiagoabreu
tags: [project-setup, scaffolding, repository, config, tooling]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Git 2.0 or newer
  - A language runtime and package manager for the chosen stack
  - Node.js 18+ or Python 3.9+ (depending on stack)
provides:
  - Standard repository directory layout
  - Editor, lint, and format configuration templates
  - Git and CI/CD baseline (branching, hooks, actions)
  - Checklist to bootstrap a new project in minutes
---

# Project Setup

## Overview

This skill walks through bootstrapping a new software project from an empty
directory to a working repository with tests, linting, and CI. It covers the
standard folder layout, essential configuration files, git conventions, and
developer tooling so every engineer on the team starts from the same baseline.
A consistent project skeleton reduces onboarding time and prevents config
drift between repositories. The templates work for libraries, services, and
applications across most ecosystems.

## Prerequisites

- Git installed and configured with `user.name` and `user.email`
- A code editor (VS Code, Cursor, Neovim, or similar)
- Runtime and package manager for your primary language

## Usage Instructions

### Step 1: Initialize Git and Core Files

Create the repository skeleton and ignore files:

```bash
git init
touch .gitignore .editorconfig .gitattributes
mkdir -p src tests docs .github/workflows
```

A minimal, stack-aware `.gitignore`:

```text
node_modules/
dist/
coverage/
.venv/
.env
*.log
.DS_Store
```

### Step 2: Add Editor and Style Baseline

Create `.editorconfig` to normalize whitespace across editors:

```ini
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
indent_style = space
indent_size = 2
trim_trailing_whitespace = true
```

Create `.gitattributes` to keep line endings consistent:

```text
* text=auto eol=lf
*.bat text eol=crlf
```

### Step 3: Add Language Configuration

Generate the manifest and tool config for your stack:

```bash
# Node.js
npm init -y
npm pkg set type=module scripts.test="node --test" scripts.lint="eslint ."

# Python
python3 -m venv .venv && source .venv/bin/activate
pip install ruff pytest
```

Add the linting configuration (ESLint example):

```json
{
  "extends": ["eslint:recommended", "prettier"],
  "parserOptions": { "ecmaVersion": "latest", "sourceType": "module" },
  "rules": { "no-unused-vars": "warn" }
}
```

### Step 4: Set Up Git Hooks

Enable a pre-commit hook so broken code never lands in history:

```bash
git config core.hooksPath .githooks
mkdir -p .githooks
cat > .githooks/pre-commit << 'EOF'
#!/bin/sh
set -e
npm run lint
npm test
EOF
chmod +x .githooks/pre-commit
```

For teams, prefer a managed tool such as `husky` or `pre-commit`.

### Step 5: Add CI Pipeline

Add a minimal GitHub Actions workflow:

```yaml
# .github/workflows/ci.yml
name: CI
on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npm run lint
      - run: npm test
```

### Step 6: Document and Commit

Write a concise `README.md` and make the first commit:

```bash
git add -A
git commit -m "chore: scaffold project with tooling and CI"
```

Include: project name, one-line description, setup commands, test command, and
contribution notes.

## Examples

### Example 1: Standard Directory Layout

```text
my-project/
├── src/              # application or library source
├── tests/            # automated tests
├── docs/             # documentation
├── .github/workflows/  # CI pipelines
├── .githooks/        # local git hooks
├── .editorconfig
├── .gitignore
├── .gitattributes
├── package.json      # or pyproject.toml
└── README.md
```

### Example 2: Repository Protection Rules

```markdown
Branch: main
- Require pull request reviews (1 approval)
- Require status checks to pass (CI)
- Require linear history (no merge commits)
- Require signed commits (recommended)
- Block force pushes to main
```

## References

- [EditorConfig specification](https://editorconfig.org/)
- [GitHub Actions documentation](https://docs.github.com/actions)
- [Git Hooks documentation](https://git-scm.com/docs/githooks)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [pre-commit framework](https://pre-commit.com/)
- [The Twelve-Factor App](https://12factor.net/)
- [GitHub Community Standards](https://opensource.guide/)

## Notes

- Bootstrapping manually is fine; consider `degit`, `cookiecutter`, or
  `create-*` scaffolds for repeatable setups.
- Keep configuration files minimal at first; add tooling only when needed.
- Pin the Node/Python version in `.nvmrc`, `.python-version`, or CI matrix.
- Commit early and often; the first commit should be the scaffolding baseline.
- Add a `LICENSE` and `SECURITY.md` before making the repo public.
- Standardize branch names (`feature/`, `bugfix/`) from day one.
