---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: skill-spector
description: Scan AI agent skills for vulnerabilities, prompt injection and supply-chain risks before installing them, using NVIDIA SkillSpector
category: security
version: 0.1.0
author: devtiagoabreu
tags: [security, scanner, skills, prompt-injection, supply-chain, skillspector]
compatible:
  - opencode
  - claude-code
  - cursor
pointer: true
vault: security/skill-spector
requires:
  - Python 3.12+ and uv or pip
  - A skill to scan (directory, zip, SKILL.md or Git URL)
provides:
  - Pre-install security vetting of agent skills
  - Risk score (0-100) with severity labels
  - SARIF/JSON/Markdown reports for CI
---

# Skill Spectator (NVIDIA SkillSpector)

## Overview

Answers one question before you install an agent skill: *should I install this
at all?* Detects 64 vulnerability patterns across 16 categories (prompt
injection, data exfiltration, privilege escalation, supply-chain, excessive
agency, system prompt leakage, MCP tool poisoning) using static analysis plus
optional LLM semantic evaluation.

## Pointer

This skill is an indexed catalog entry. The full, curated instructions are
loaded on demand from the vault to avoid context injection:

```bash
core/discovery/pointer.sh resolve skill-spector
```

## When to load

Load the full content when the task involves vetting an agent skill before
installation, running a vulnerability scan, or generating SARIF/JSON reports
for CI gates.

## Prerequisites

Python 3.12+ with uv or pip, and a skill to scan (directory, zip, SKILL.md or
Git URL). See the vault entry for exact setup.
