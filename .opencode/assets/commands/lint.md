---
name: lint
description: Command to check code linting
version: 0.1.0
author: devtiagoabreu
tags: [linting, code-quality]
compatible:
  - opencode
  - claude-code
  - cursor
---

# /lint

## Usage

```text
/lint [file_or_directory]
```

## Description

Runs linting tools on the code, checking formatting, style, and possible errors.

## Arguments

| Argument  | Required  | Description | Default        |
| --------- | --------- | ----------- | -------------- |
| file      | No        | File or directory to check | Entire project |

## Examples

```bash
/lint
/lint src/main.py
/lint ./src/
```

## Notes

- Automatically detects available linting tools
- Reports errors and warnings
- Suggests fixes when possible
