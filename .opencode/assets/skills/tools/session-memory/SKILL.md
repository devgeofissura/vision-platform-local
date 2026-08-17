---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-15
name: session-memory
description: Persistent local-first memory across sessions using context/memory/memory.py (SQLite FTS + optional vector recall)
category: tools
version: 0.1.0
author: devtiagoabreu
tags: [memory, sessions, persistence, sqlite, chromadb, context]
compatible:
  - opencode
  - claude-code
  - cursor
security:
  risk_level: low
  permissions:
    - filesystem
    - network
  audited: true
requires:
  - python3
provides:
  - Remember preferences and decisions across sessions
  - Full-text and (optionally) vector search over stored context
  - Session-scoped notes with healthcheck
difficulty: beginner
---

# Session Memory

## Overview

By default an AI assistant forgets everything between sessions. This skill
gives the kit a local-first, opt-in memory: notes are stored in SQLite
(outside the repository) and can be searched back later. Use it to remember
user preferences, project decisions, "why" notes, and recurring constraints.

Activation: set `KIT_MEMORY=1` and run the memory helper.

## Prerequisites

- Python 3
- SQLite (built into Python) — no extra install needed
- Optional: `chromadb` (pip) for vector recall with `KIT_MEMORY_VECTOR=1`

## Usage Instructions

### Step 1: Initialize

```bash
export KIT_MEMORY=1
python3 context/memory/memory.py init
```

### Step 2: Save a memory

Feed content through stdin, scoped to a session:

```bash
printf 'O usuário prefere TypeScript com Fastify e vitest.' \
  | python3 context/memory/memory.py save --key tech-stack --session projeto-x
```

### Step 3: Recall

```bash
# exact key
python3 context/memory/memory.py get --key tech-stack

# full-text search with recency boost
python3 context/memory/memory.py search pdf --limit 5

# scoped to a session
python3 context/memory/memory.py search vitest --session projeto-x
```

### Step 4: Review and maintain

```bash
python3 context/memory/memory.py sessions   # list sessions + counts
python3 context/memory/memory.py stats      # totals by kind
python3 context/memory/memory.py healthcheck
```

## Examples

### Example 1: Remember a decision

```bash
printf 'Decisão: API de relatórios gera PDF server-side (biblioteca pinada).' \
  | python3 context/memory/memory.py save --key decision-reports --kind decision --session projeto-x
```

Later: `python3 context/memory/memory.py search PDF` returns the note with the
decision and why.

### Example 2: User preference across sessions

```bash
printf 'Prefere commits pequenos e rebase, nunca merge.' \
  | python3 context/memory/memory.py save --key git-prefs --session projeto-x
```

On a new session: `python3 context/memory/memory.py get --key git-prefs` recalls
the preference before making changes.

## Best Practices

1. Keep keys short, descriptive and stable (`project-<x>-decision-y`)
2. Scope notes to sessions to avoid cross-project noise
3. Store decisions and constraints, not ephemeral chatter
4. Run `healthcheck` occasionally to confirm FTS is consistent
5. The database lives in `~/.local/share/opencode-engineering-kit/` — it is
   never committed to the repository
6. Enable vector recall only if `chromadb` is available

## References

- [SQLite FTS5](https://www.sqlite.org/fts5.html)
- [ChromaDB](https://docs.trychroma.com/)
- [Shokunin — Technical Overview (memory)](https://github.com/EliasOulkadi/shokunin)
