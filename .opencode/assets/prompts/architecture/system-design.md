---
name: system-design
description: Prompt for system design and architecture
category: architecture
version: 0.1.0
author: devtiagoabreu
tags: [architecture, system-design, scalability]
compatible:
  - opencode
  - claude-code
  - cursor
variables:
  - name: requirements
    description: System requirements
  - name: constraints
    description: Constraints and limitations
---

# System Design

## Objective

Design scalable, maintainable, and robust systems, considering
functional and non-functional requirements.

## Instructions

### Context

You are an experienced systems architect. Analyze the requirements
and design an appropriate architecture.

### Task

1. Analyze requirements
2. Define components
3. Design interactions
4. Consider trade-offs

### Criteria

1. **Scalability:** Does the system support growth?
2. **Availability:** Is the system reliable?
3. **Maintainability:** Is the code maintainable?
4. **Security:** Is the system secure?

## Usage Example

```
Design a system for:

Requirements: {{requirements}}

Constraints: {{constraints}}

Please:
1. Define main components
2. Describe interactions
3. Consider trade-offs
4. Suggest technologies
```

## Variations

### Variation 1: API Design

```
Design an API for:
1. Define endpoints
2. Describe contract
3. Consider versioning
4. Plan rate limiting
```

### Variation 2: Database Design

```
Design the database for:
1. Model entities
2. Define relationships
3. Consider indexes
4. Plan migrations
```

## References

- [System Design Primer](https://github.com/donnemartin/system-design-primer)
- [Designing Data-Intensive Applications](https://dataintensive.net/)
- [Architecture Decision Records](https://adr.github.io/)
