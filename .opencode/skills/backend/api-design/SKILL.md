---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: api-design
description: Complete guide for RESTful API design
category: backend
version: 0.1.0
author: devtiagoabreu
tags: [api, rest, backend, design]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Basic HTTP knowledge
provides:
  - API design patterns
  - REST conventions
  - Best practices
---

# API Design

## Overview

This skill provides a complete guide for RESTful API design, including
conventions, patterns, and best practices.

## Prerequisites

- Basic HTTP knowledge
- Understanding of HTTP verbs
- Knowledge of status codes

## Usage Instructions

### 1. URL Conventions

```
# Resources in plural
GET    /api/v1/users
GET    /api/v1/users/123
POST   /api/v1/users
PUT    /api/v1/users/123
DELETE /api/v1/users/123

# Sub-resources
GET    /api/v1/users/123/posts
GET    /api/v1/users/123/posts/456

# Specific actions
POST   /api/v1/users/123/activate
POST   /api/v1/users/123/deactivate
```

### 2. HTTP Verbs

| Verb | Usage | Idempotent |
|------|-------|------------|
| GET | Read resource | Yes |
| POST | Create resource | No |
| PUT | Update entire resource | Yes |
| PATCH | Partial update | No |
| DELETE | Delete resource | Yes |

### 3. Status Codes

| Code | Usage |
|------|-------|
| 200 | Success |
| 201 | Created |
| 204 | No Content |
| 400 | Bad Request |
| 401 | Unauthenticated |
| 403 | Unauthorized |
| 404 | Not Found |
| 409 | Conflict |
| 422 | Unprocessable Entity |
| 500 | Internal Server Error |

### 4. Response Format

```json
// Success
{
  "data": {
    "id": 123,
    "name": "John",
    "email": "john@email.com"
  },
  "meta": {
    "timestamp": "2026-07-18T10:00:00Z"
  }
}

// List
{
  "data": [
    {"id": 1, "name": "John"},
    {"id": 2, "name": "Jane"}
  ],
  "meta": {
    "total": 2,
    "page": 1,
    "per_page": 10
  }
}

// Error
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      }
    ]
  }
}
```

### 5. Versioning

```
# Via URL (recommended)
/api/v1/users
/api/v2/users

# Via header
Accept: application/vnd.api.v1+json
```

### 6. Pagination

```
GET /api/v1/users?page=2&per_page=10

# Response
{
  "data": [...],
  "meta": {
    "total": 100,
    "page": 2,
    "per_page": 10,
    "total_pages": 10
  },
  "links": {
    "self": "/api/v1/users?page=2&per_page=10",
    "next": "/api/v1/users?page=3&per_page=10",
    "prev": "/api/v1/users?page=1&per_page=10"
  }
}
```

### 7. Filters and Search

```
# Filters
GET /api/v1/users?status=active&role=admin

# Search
GET /api/v1/users?search=john

# Sorting
GET /api/v1/users?sort=name&order=asc

# Specific fields
GET /api/v1/users?fields=id,name,email
```

## Examples

### Example 1: Complete CRUD

```python
# routes/users.py
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/v1/users", tags=["users"])

@router.get("/")
async def list_users():
    return {"data": users}

@router.get("/{id}")
async def get_user(id: int):
    user = find_user(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"data": user}

@router.post("/")
async def create_user(user: CreateUser):
    new_user = create(user)
    return {"data": new_user}, 201

@router.put("/{id}")
async def update_user(id: int, user: UpdateUser):
    updated_user = update(id, user)
    return {"data": updated_user}

@router.delete("/{id}")
async def delete_user(id: int):
    delete(id)
    return None, 204
```

## References

- [Microsoft REST API Guidelines](https://github.com/microsoft/api-guidelines)
- [JSON:API Specification](https://jsonapi.org/)
- [RESTful API Design - Best Practices](https://hackernoon.com/restful-api-designing-guidelines-the-best-practices-60e1d954e7c9)

## Notes

- Use nouns, not verbs in URLs
- Maintain consistency in naming
- Document everything with OpenAPI/Swagger
- Use versioning from the start
- Implement rate limiting
- Validate all inputs
