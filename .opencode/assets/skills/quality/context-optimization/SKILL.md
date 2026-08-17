---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: context-optimization
description: Reduce token usage and cost of AI coding agents using context engineering, compaction, caching and repomix
category: quality
version: 0.1.0
author: devtiagoabreu
tags: [tokens, context, cost, optimization, repomix, compaction, caching]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - A coding agent (OpenCode, Claude Code or Cursor)
  - Node.js 16+ for repomix
provides:
  - Token budget discipline for agent sessions
  - Repomix-packaged codebase snapshots
  - Guidance on compaction, prompt caching and progressive disclosure
---

# Context Optimization (Token Economy)

## Overview

This skill teaches how to reduce the token usage and cost of AI coding agents.
Long sessions burn tokens mainly by re-sending conversation history (50-60% of
total spend) and by reading whole files "just in case". Context engineering
fixes that by keeping the prompt payload lean, relevant and in the right shape:
package the codebase once, load context on demand, compact proactively and
cache what repeats.

Tools covered:

- **[Repomix](https://github.com/yamadashy/repomix)** — packages a codebase into
  a single LLM-ready file (Markdown/XML/JSON) with ignore filters and built-in
  secret scan.
- **Prompt caching** — reuse the stable prefix of your context for a ~90% cost
  discount on cached tokens.
- **Compaction** — summarize and drop noise from conversation history before it
  hits the context ceiling.

## Prerequisites

- A coding agent session where you control the context (system prompt, files)
- Node.js 16+ and npm/npx for repomix

## Usage Instructions

### 1. Package the codebase with Repomix

```bash
npx repomix --style markdown --output ./codebase.md
```

Filter out noise and scan for secrets:

```bash
npx repomix \
  --ignore "**/tests/**" \
  --ignore "**/*.lock" \
  --output ./codebase.md \
  --security-check
```

Repomix reports the total size and token estimate — check it fits your window.

### 2. Follow a context budget

| Context fill | Action |
|--------------|--------|
| 0-40% | Keep going, no action |
| 40-60% | Prefer on-demand retrieval over file dumps |
| 60-75% | Compact with a directive: "keep decisions and paths, drop tool output" |
| 75%+ | Hand off to a fresh session with a summary |

### 3. Use progressive disclosure

Never load everything at session start. Keep instructions in small files and
reference them from the system prompt so the agent reads a file only when the
task needs it. This kit's `context/*.md` files and `assets/skills/**/SKILL.md`
are designed exactly for this pattern.

### 4. Cache the stable prefix

Place everything that stays constant (system prompt, tool descriptions, project
overview) at the beginning of the context and reuse it across turns so the
provider's prompt cache hits.

### 5. Compute, don't read

Instead of reading 50 files, ask the agent to write a script that greps,
counts and summarizes — replacing ten tool calls (and their re-sent history)
with one compact result. This routinely saves 10x-100x context.

## Examples

### Example 1: Package a repo for a focused code review

```bash
npx repomix --style markdown --security-check \
  --ignore "**/node_modules/**" --ignore "**/dist/**" \
  --output ./review.md
```

### Example 2: Compact a long session with a directive

Ask the agent: "Compact the conversation now. Keep all architectural
decisions, file paths and unresolved issues. Drop tool outputs and error
traces."

### Example 3: Trim skill instructions

Keep each `SKILL.md` under 600 lines and load it only when the task matches its
description — that is the difference between a 2K-token on-demand read and a
permanent 50K-token attachment.

## References

- [Repomix](https://github.com/yamadashy/repomix)
- [Gitingest](https://gitingest.com) / [repo2txt](https://repo2txt.simplebasedomain.com)
- [SkillOpt (microsoft) — skill text optimization](https://github.com/microsoft/SkillOpt)
- [Anthropic prompt caching](https://platform.openai.com/docs/guides/prompt-caching)

## Notes

- Bigger context windows do not fix context rot; budget by fill percentage.
- Cache hit savings depend on the provider — verify your plan supports caching.
- Compaction is most useful on open-ended sessions; for structured workflows,
  split sessions explicitly and carry a short spec forward.
