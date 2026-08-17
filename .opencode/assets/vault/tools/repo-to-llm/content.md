# Repo to LLM Markdown (vault entry)

## Purpose

Convert any Git repository (or local folder) into a single, structured
Markdown document that fits into a model's context window. Output includes the
directory tree, file-path headers and only the source files that matter, so a
prompt gets the full picture without wasting tokens on node_modules, lock files
or build artifacts. This is the core "context engineering" pattern.

## The three community tools

- gittomd: web tool that converts a public GitHub repository into one Markdown
  file. Replace the repository URL with the gittomd equivalent in the browser
  and download the generated file. Free for public repositories; private
  repositories need a token.
- git2md: local CLI that also emits the llms.txt format for LLM context. Runs
  fully local, which is safe for sensitive codebases. Install or run via npx.
- repo2txt: browser-based picker with private-repo support via a personal
  access token. Paste the repository URL, select the files, download plain
  text.

## Prerequisites

- Git 2.0+ and Bash 4.0+ (for the local options)
- Node.js 16+ if using git2md via npx
- A target repository (local path or public GitHub URL)

## Usage

### 1. Quickest option: gittomd (web)

Replace the repository URL with the gittomd equivalent in your browser, or use
the GitHub-hosted endpoint. Download the generated Markdown file.

### 2. Local CLI: git2md

```bash
# Run from anywhere, against a local or remote repository
npx git2md /path/to/repository --output ./llm-context.md

# Emit the llms.txt format (index of all files)
npx git2md /path/to/repository --format llms.txt

# Filter by extensions and exclude noise
npx git2md /path/to/repository \
  --extensions .py,.md,.yaml \
  --exclude tests,build,dist \
  --output ./llm-context.md
```

### 3. Browser picker: repo2txt

Paste the repository URL, select the files you want and download a plain-text
file ready to paste into any LLM. Supports private repositories with a personal
access token.

## Best practices for token economy

- Filter aggressively: exclude tests, generated code, lock files and build
  artifacts. A medium frontend repo usually fits a 100K-200K window after
  filtering.
- Generate once, reuse: package the context once per sprint and reuse it for
  code review, docs, onboarding and architecture discussions.
- Scan for secrets first: before feeding any snapshot to a model, run the
  secret scan from this kit (`./core/security/secret-scan.sh`) or a tool like
  truffleHog.
- Check the output size: conversion tools report total tokens/bytes; match the
  size to your model's context window.

## Examples

### Example 1: Package a local codebase for a code review

```bash
cd /path/to/your/project
npx git2md . --extensions .ts,.tsx,.json --exclude node_modules,dist,tests \
  --output ./codebase.md
wc -c ./codebase.md
```

### Example 2: Generate an llms.txt index for a project

```bash
npx git2md /path/to/your/project --format llms.txt --output ./llms.txt
```

### Example 3: Combine with this kit's secret scan

```bash
npx git2md . --output ./context.md
./core/security/secret-scan.sh ./context.md
```

## Notes

- Keep the generated files out of git (`*.context.md`, and `llms.txt` if
  unwanted).
- Treat private repositories as sensitive: prefer the local CLI.
