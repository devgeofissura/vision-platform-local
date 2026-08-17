---
name: debug-analysis
description: Prompt for bug analysis and diagnosis
category: debugging
version: 0.1.0
author: devtiagoabreu
tags: [debugging, error-analysis, troubleshooting]
compatible:
  - opencode
  - claude-code
  - cursor
variables:
  - name: error_message
    description: Error message
  - name: code_context
    description: Code where the error occurs
---

# Debug Analysis

## Objective

Analyze and diagnose bugs systematically, identifying the root cause
and proposing solutions.

## Instructions

### Context

You are an experienced software engineer in debugging. Analyze the provided
error and identify the root cause.

### Task

1. Analyze the error message
2. Identify the root cause
3. Propose a solution
4. Suggest prevention

### Criteria

1. **Root cause:** Identified correctly?
2. **Solution:** Feasible and tested?
3. **Prevention:** How to avoid in the future?

## Usage Example

````
Analyze the following error:

Error message: {{error_message}}

Code where it occurs:
```{{language}}
{{code_context}}
```

Please:
1. Identify the root cause
2. Propose a solution
3. Suggest how to prevent it in the future
````

## Variations

### Variation 1: Runtime Error Analysis

```
Analyze this runtime error:
1. What caused the error?
2. Where exactly did it occur?
3. What variables were involved?
4. How to fix it?
```

### Variation 2: Compilation Error Analysis

```
Analyze this compilation error:
1. What does the error mean?
2. Which line causes the problem?
3. How to fix the syntax?
```

## References

- [Debugging Best Practices](https://stackoverflow.com/questions/2112975/debugging-best-practices)
- [Rubber Duck Debugging](https://en.wikipedia.org/wiki/Rubber_duck_debugging)
