---
name: review
description: Command to review current code
version: 0.1.0
author: devtiagoabreu
tags: [code-review, quality]
compatible:
  - opencode
  - claude-code
  - cursor
---

# /review

## Usage

```text
/review [file_or_directory]
```

## Description

Reviews the specified code or the current code, providing feedback
on quality, security, and best practices.

## Arguments

| Argument  | Required  | Description | Default        |
| --------- | --------- | ----------- | -------------- |
| file      | No        | File or directory to review | Current code   |

## Examples

```bash
/review
/review src/main.py
/review ./src/
```

## Notes

- If no file is specified, reviews the current code
- Uses the code review checklist
- Provides structured feedback
