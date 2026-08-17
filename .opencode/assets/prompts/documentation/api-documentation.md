---
name: api-documentation
description: Generate clear, complete, and accurate documentation for an API
category: documentation
version: 0.1.0
author: devtiagoabreu
tags: [documentation, api, openapi, reference]
compatible:
  - opencode
  - claude-code
  - cursor
variables:
  - name: api_spec
    description: API definition, OpenAPI spec, or endpoint list
  - name: audience
    description: Target audience for the documentation
---

# API Documentation

## Objective

Produce end-to-end API documentation that lets the intended audience
integrate correctly, covering endpoints, contracts, and usage examples.

## Instructions

### Context

You are a technical writer. Turn the API specification into clear,
accurate reference and guide documentation for the target audience.

### Task

1. Inventory endpoints, methods, and payloads
2. Document authentication and authorization requirements
3. Describe each endpoint with request, response, and error examples
4. Document versioning, rate limits, and edge cases
5. Add quick-start and integration guidance

### Criteria

1. **Accuracy:** Examples match the real contract
2. **Completeness:** Every endpoint and error case is covered
3. **Clarity:** Audience can integrate without guessing
4. **Maintainability:** Structure supports automatic regeneration

## Usage Example

```
Write documentation for this API:

Spec: {{api_spec}}

Audience: {{audience}}

Please:
1. Summarize authentication requirements
2. Document each endpoint with examples
3. List error codes and edge cases
4. Provide a quick-start integration guide
```

## Variations

### Variation 1: OpenAPI-Driven Reference

```
Generate reference docs from the OpenAPI spec:
1. Auto-generate endpoint tables and schemas
2. Annotate with human-written examples
3. Flag endpoints missing descriptions
```

### Variation 2: Integration Guide

```
Write an integration guide for this API:
1. Step-by-step authentication flow
2. Common workflows with code samples
3. Troubleshooting and rate limiting guidance
```

## References

- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
- [Google Developer Documentation Style Guide](https://developers.google.com/style)
