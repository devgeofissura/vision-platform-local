---
name: test
description: Command to run tests
version: 0.1.0
author: devtiagoabreu
tags: [testing, automation]
compatible:
  - opencode
  - claude-code
  - cursor
---

# /test

## Usage

```text
/test [type] [filter]
```

## Description

Runs project tests, allowing filtering by type and/or file.

## Arguments

| Argument  | Required  | Description | Default        |
| --------- | --------- | ----------- | -------------- |
| type      | No        | Test type (unit, integration, all) | all            |
| filter    | No        | Filter for specific tests | All            |

## Examples

```bash
/test
/test unit
/test integration
/test unit test_main
```

## Notes

- Automatically detects the test framework
- Provides coverage report
- Shows tests that failed
