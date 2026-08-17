---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: repo-to-llm
description: Convert any Git repository into clean, token-efficient Markdown (with llms.txt) ready for LLM context, RAG and code review
category: tools
version: 0.1.0
author: devtiagoabreu
tags: [llm, markdown, repository, tokens, llms.txt, gittomd, git2md, context]
compatible:
  - opencode
  - claude-code
  - cursor
pointer: true
vault: tools/repo-to-llm
requires:
  - Git 2.0+ and network access to the target repository
  - One of: gittomd, git2md or repo2txt (see vault content)
provides:
  - Single-file Markdown snapshot of a repository
  - llms.txt index for LLM context
  - Filtered source-only output (no noise, no binaries)
---

# Repo to LLM Markdown

## Overview

Converts any Git repository (or local folder) into a single structured Markdown
document with a directory tree, file-path headers and only the source files
that matter — ready for LLM context, RAG and code review. Three community tools
are covered: gittomd (web), git2md (local CLI with llms.txt output) and
repo2txt (browser picker with private-repo support).

## Pointer

This skill is an indexed catalog entry. The full, curated instructions are
loaded on demand from the vault to avoid context injection:

```bash
core/discovery/pointer.sh resolve repo-to-llm
```

## When to load

Load the full content when the task involves converting a repository to
Markdown, generating an `llms.txt` index or packaging a codebase for an LLM
context window.

## Prerequisites

Git 2.0+, network access to the target repository, and at least one of gittomd,
git2md or repo2txt (see the vault entry for exact setup).
