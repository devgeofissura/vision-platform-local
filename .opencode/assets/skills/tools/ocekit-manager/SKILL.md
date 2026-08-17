---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-15
name: ocekit-manager
description: Manage the OpenCode Engineering Kit (ocekit). Use when the user says "instale ocekit", "instale o ocekit", "install ocekit", "install the ocekit", "install opencode-engineering-kit", "ocekit install", "stop ocekit", "start ocekit", "status ocekit", "o que é ocekit", or pastes a GitHub repository link asking to install it. Covers installing the kit globally (~/.config/opencode) or in the current project, and enabling/disabling/status afterwards.
category: tools
version: 0.1.0
author: devtiagoabreu
tags: [ocekit, install, lifecycle, kit, setup, opencode-engineering-kit]
compatible:
  - opencode
requires:
  - Node.js 18+ (to run the CLI via npx)
  - Network access to fetch the kit from GitHub
provides:
  - One-command install of the kit (global or project) from a repository link
  - Lifecycle control: status / start / stop
  - Feedback to the user after each operation
security:
  risk_level: low
  permissions:
    - network
  audited: true
---

# Ocekit Manager

## Overview

`ocekit` is the OpenCode Engineering Kit: a library of skills, personas
(agents), commands, prompts, playbooks and context that make opencode more
productive. This skill tells the assistant how to react when the user wants to
install, check, start or stop the kit — including when they just paste a
GitHub repository link.

The kit is installed through its own CLI (`npx opencode-engineering-kit`),
which supports:

- `install` — copy assets into the current project (`.opencode/`) or globally
  (`~/.config/opencode/` with `--global`).
- `status` — report where the kit is installed and whether it is enabled.
- `start` / `stop` — re-enable or disable the kit without deleting files.

## Prerequisites

- Node.js 18+ (the CLI runs through `npx opencode-engineering-kit`).
- Network access to GitHub (unless the user points `--source` at a local
  checkout).

## Usage Instructions

### 1. Install (project or global)

When the user asks to install the kit — e.g. "instale ocekit" or pastes a
repository link:

1. **Ask the user** whether they want a **global** install (available in every
   project) or **only this project**. Use the question tool; default to
   project install if they do not specify.
2. Extract the repository from the link the user provided (default:
   `devtiagoabreu/opencode-engineering-kit`). The CLI accepts `owner/repo`,
   a full `https://github.com/owner/repo` URL or a `git@github.com:...` SSH
   URL.
3. Run the install:

   ```bash
   # Project install (into .opencode/ of the current directory)
   npx opencode-engineering-kit install --repo <owner/repo>

   # Global install (into ~/.config/opencode/)
   npx opencode-engineering-kit install --global --repo <owner/repo>
   ```

4. Report the result and tell the user to **restart opencode** so the new
   config is loaded.

### 2. Status

When the user says "status ocekit":

```bash
npx opencode-engineering-kit status
```

Summarize the output: whether the kit is installed globally and/or in the
project, whether it is enabled, and the number of skills/agents/commands.

### 3. Start / Stop

When the user says "stop ocekit", disable the kit without deleting files:

```bash
npx opencode-engineering-kit stop
```

When the user says "start ocekit", re-enable it:

```bash
npx opencode-engineering-kit start
```

Both commands keep all files on disk and only remove/restore the
`opencode.json` wiring (`skills.paths` + `instructions`). After either,
remind the user to restart opencode.

### 4. Nothing installed yet

If `status` says the kit is not installed, do not guess — run the install
flow (section 1) or tell the user the exact command to run.

## Notes

- Always keep the user informed: after every `install`, `start` or `stop`,
  say what happened and that opencode needs a restart.
- Prefer the CLI over hand-editing `opencode.json`. Use `--dry-run` first if
  you want to preview what the installer would do.
