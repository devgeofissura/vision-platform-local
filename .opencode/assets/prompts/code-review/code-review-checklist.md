---
name: code-review-checklist
description: Prompt for code review using comprehensive checklist
category: code-review
version: 0.1.0
author: devtiagoabreu
tags: [code-review, quality, checklist]
compatible:
  - opencode
  - claude-code
  - cursor
variables:
  - name: code
    description: Code to be reviewed
  - name: language
    description: Programming language
---

# Code Review Checklist

## Objective

Review code systematically and comprehensively, ensuring quality,
security, and best practices.

## Instructions

### Context

You are an experienced code reviewer. Analyze the provided code
following the checklist below.

### Task

Review the code and provide structured feedback.

### Criteria

1. **Functionality:** Does code meet requirements?
2. **Quality:** Is code readable and maintainable?
3. **Security:** Are there vulnerabilities?
4. **Performance:** Are there performance issues?
5. **Tests:** Are there adequate tests?

## Usage Example

```
Please review the following code using the code review checklist:

[code here]

Provide feedback for each checklist item:
1. Functionality
2. Quality
3. Security
4. Performance
5. Tests
```

## Variations

### Variation 1: Security-Focused Review

```
Analyze the code focusing specifically on security:
1. Are there hardcoded secrets?
2. Is input validated?
3. Is output sanitized?
4. Are there known vulnerabilities?
5. Is authentication implemented?
```

### Variation 2: Performance-Focused Review

```
Analyze the code focusing specifically on performance:
1. Is there O(n²) or worse?
2. Are queries optimized?
3. Is cache used appropriately?
4. Are there memory leaks?
5. Are assets compressed?
```

## References

- [Code Review Checklist](../skills/code-review/code-review-checklist/SKILL.md)
- [Google Code Review Guide](https://google.github.io/eng-practices/review/)
