# Code Knowledge Graph (Graphify) — vault entry

## Purpose

Turn a folder of code, SQL schemas, scripts, docs, papers, images or videos
into a queryable knowledge graph for coding agents. Instead of dumping an
entire codebase into context, build the graph once and query only the nodes you
need — cutting the tokens required to describe a project by an order of
magnitude while improving accuracy. Compatible with Claude Code, Codex,
OpenCode, Cursor, Gemini CLI and more, and can combine application code,
database schema and infrastructure in a single graph.

## Prerequisites

- Node.js 18+ with npm/npx
- A folder containing the code, schema or docs you want to index
- (Optional) a database to store large graphs — Graphify ships an embedded
  option for small projects

## Usage

### 1. Install Graphify

```bash
npm install -g @graphify-labs/graphify
graphify --version
```

### 2. Build a graph from a project

```bash
cd /path/to/your/project
graphify build --input . --output ./graph
```

For larger projects you can scope the input (code only, SQL only, docs only):

```bash
graphify build --input ./src --input ./schema.sql --output ./graph
```

### 3. Query the graph

```bash
graphify query --graph ./graph "list all API endpoints"
graphify query --graph ./graph "which files implement authentication?"
graphify query --graph ./graph "what depends on the database layer?"
```

### 4. Use the graph with a coding agent

Expose the graph to the agent so it queries on demand instead of reading whole
files. In OpenCode, reference the query commands as part of your workflow or
skills — the agent runs a query, gets only the relevant nodes, and keeps its
context small.

## Best practices

- Build once, refresh when code changes: keep the graph updated in CI.
- Scope inputs: index only the folders that matter; exclude tests and generated
  code to keep the graph lean.
- Query before reading: always ask the graph for the specific symbols,
  endpoints or schema relevant to the task before opening files.
- Combine with the resolver: this kit's `core/resolver` dependency graph
  complements Graphify's code graph for asset-level dependencies.

## Examples

### Example 1: Index a backend and find the auth flow

```bash
graphify build --input . --output ./graph --exclude node_modules,dist
graphify query --graph ./graph "trace the login flow from route to database"
```

### Example 2: Index SQL schema for a data question

```bash
graphify build --input ./migrations --output ./schema-graph
graphify query --graph ./schema-graph "which tables reference users?"
```

### Example 3: Document-only knowledge base

```bash
graphify build --input ./docs --output ./docs-graph
graphify query --graph ./docs-graph "how do we deploy to production?"
```

## Notes

- Graphify stores the graph locally; no code leaves your machine unless you
  choose a remote store.
- Build times scale with input size — use `--exclude` for generated folders.
- Graph queries return node summaries, not full files; fetch a file only when
  the node points to it as relevant.
