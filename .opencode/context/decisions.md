---
name: decisions-context
description: Architectural decisions for OpenCode Engineering Kit
type: decisions
version: 0.1.0
author: devtiagoabreu
---

# Architectural Decisions

## Overview

This document records important architectural decisions for the project. Each decision follows the ADR (Architecture Decision Record) format.

## AD-001: SKILL.md Format

**Status:** Approved

**Date:** 2026-07-18

**Context:**

We need a standard format for skills that is human-readable and machine-readable, compatible with multiple AI platforms.

**Decision:**

Skills use markdown format with YAML frontmatter.

**Rationale:**

- Markdown is human-readable and machine-readable
- YAML frontmatter allows structured metadata
- Compatible with OpenCode, Claude Code, and Cursor
- Easy to version and review

**Consequences:**

- YAML parser required for metadata
- 600-line limit per SKILL.md
- Standard format for all skills

## AD-002: Category Organization

**Status:** Approved

**Date:** 2026-07-18

**Context:**

We need to organize skills in a way that is easy to find and manage.

**Decision:**

Skills are organized in directories by category.

**Rationale:**

- Facilitates navigation and discovery
- Groups related skills
- Allows expandable categories
- Follows Shokunin pattern

**Consequences:**

- Fixed directory structure
- Categories predefined in bootstrap
- New category requires bootstrap update

## AD-003: Agents as .md Files

**Status:** Approved

**Date:** 2026-07-18

**Context:**

We need a format for agents that is consistent with skills and easy to edit.

**Decision:**

Agents are markdown files with personas.

**Rationale:**

- Consistent with Skills format
- Easy to edit and maintain
- Can include usage examples
- Compatible with OpenCode

**Consequences:**

- 200-line limit per agent
- Persona defined in content
- Skill references in frontmatter

## AD-004: Context as Separate Files

**Status:** Approved

**Date:** 2026-07-18

**Context:**

We need a way to provide project context that is modular and easy to update.

**Decision:**

Context consists of independent .md files.

**Rationale:**

- Allows partial updates
- Facilitates caching by section
- Can be combined dynamically
- Separation of responsibilities

**Consequences:**

- Multiple files to manage
- Composition mechanism required
- Each file has defined scope

## AD-005: Bash Scripts

**Status:** Approved

**Date:** 2026-07-18

**Context:**

We need installation and configuration scripts that work across multiple platforms.

**Decision:**

Installation and configuration scripts in Bash.

**Rationale:**

- Available on all Unix systems
- Easy to understand and modify
- No external dependencies
- Can be read and audited

**Consequences:**

- Does not work natively on Windows (requires WSL)
- Error handling required
- Must be tested on multiple distributions

## References

- [ADR Template](https://github.com/joelparkerhenderson/architecture-decision-record)
- [PROJECT_SPEC.md](../PROJECT_SPEC.md#5-architecture)
