---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: code-knowledge-graph
description: Turn any folder of code, SQL schemas, docs or images into a queryable knowledge graph for coding agents using Graphify
category: tools
version: 0.1.0
author: devtiagoabreu
tags: [graph, knowledge-graph, codebase, graphify, llm, analysis]
compatible:
  - opencode
  - claude-code
  - cursor
pointer: true
vault: tools/code-knowledge-graph
requires:
  - Node.js 18+ and npm/npx
  - Network access to fetch the Graphify package
provides:
  - Queryable knowledge graph of a codebase
  - Natural-language queries over code, SQL schemas and docs
  - Reduced tokens to describe a codebase to an LLM
---

# Code Knowledge Graph (Graphify)

## Overview

Uses Graphify to turn a folder of code, SQL schemas, scripts, docs, papers,
images or videos into a queryable knowledge graph for coding agents. Instead of
dumping an entire codebase into context, you build a graph once and query only
the nodes you need — cutting the tokens required to describe a project by an
order of magnitude.

## Pointer

This skill is an indexed catalog entry. The full, curated instructions are
loaded on demand from the vault to avoid context injection:

```bash
core/discovery/pointer.sh resolve code-knowledge-graph
```

## When to load

Load the full content when the task involves building or querying a knowledge
graph over a codebase, SQL schema or documentation set.

## Prerequisites

Node.js 18+ with npm/npx and network access to fetch the Graphify package (see
the vault entry for exact setup).
