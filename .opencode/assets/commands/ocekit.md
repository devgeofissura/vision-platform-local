---
name: ocekit
description: Manage the OpenCode Engineering Kit (ocekit) — install globally or in the project, status, start, stop
version: 0.1.0
author: devtiagoabreu
tags: [ocekit, install, lifecycle, kit]
compatible:
  - opencode
---

# /ocekit

## Usage

```text
/ocekit install [--global] [repo]
/ocekit status
/ocekit start
/ocekit stop
```

## Description

Manages the OpenCode Engineering Kit through its CLI
(`npx opencode-engineering-kit`).

- `install` — copy the kit into the current project (`.opencode/`) or
  globally (`~/.config/opencode/` with `--global`). `repo` may be
  `owner/repo`, a `https://github.com/...` URL or an SSH URL; defaults to
  `devtiagoabreu/opencode-engineering-kit`.
- `status` — show where the kit is installed and whether it is enabled.
- `start` / `stop` — re-enable or disable the kit without deleting files.

## Examples

```text
/ocekit install
/ocekit install --global
/ocekit install https://github.com/devtiagoabreu/opencode-engineering-kit
/ocekit status
/ocekit stop
/ocekit start
```

## Notes

- Ask the user whether they want a global or project install when not
  specified.
- Remind the user to restart opencode after any change.
