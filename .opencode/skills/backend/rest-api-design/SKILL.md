---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: rest-api-design
description: Best practices for REST API design and implementation
category: backend
version: 0.1.0
author: devtiagoabreu
tags: [rest, api, design, backend]
compatible:
  - opencode
  - claude-code
  - cursor
---

# REST API Design Best Practices

## Overview

This skill provides best practices for designing and implementing REST APIs, including resource modeling, error handling, and versioning.

## Prerequisites

- Basic understanding of HTTP and REST concepts
- Programming language knowledge

## Usage Instructions

### Step 1: Resource Design

Use nouns for resources, HTTP methods for actions:

```
GET    /users          # List users
POST   /users          # Create user
GET    /users/:id      # Get user
PUT    /users/:id      # Update user
DELETE /users/:id      # Delete user
```

### Step 2: Versioning

Use URL versioning:

```
/api/v1/users
/api/v2/users
```

### Step 3: Error Handling

Return consistent error responses:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      }
    ]
  }
}
```

### Step 4: Pagination

Implement pagination for list endpoints:

```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "perPage": 20,
    "total": 100,
    "totalPages": 5
  }
}
```

## Examples

### User API

```yaml
openapi: 3.0.0
info:
  title: User API
  version: 1.0.0
paths:
  /users:
    get:
      summary: List users
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/User'
                  pagination:
                    $ref: '#/components/schemas/Pagination'
```

## Best Practices

1. Use nouns for resources
2. Use HTTP methods correctly
3. Implement proper versioning
4. Return consistent error responses
5. Implement pagination
6. Use proper status codes
7. Support filtering and sorting

## References

- [REST API Design Best Practices](https://restfulapi.net/)
- [OpenAPI Specification](https://swagger.io/specification/)