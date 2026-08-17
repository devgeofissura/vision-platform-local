---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: graphql-api
description: Best practices for GraphQL API design and implementation
category: backend
version: 0.1.0
author: devtiagoabreu
tags: [graphql, api, design, backend]
compatible:
  - opencode
  - claude-code
  - cursor
---

# GraphQL API Design Best Practices

## Overview

This skill provides best practices for designing and implementing GraphQL APIs, including schema design, query optimization, and security.

## Prerequisites

- Basic understanding of GraphQL concepts
- Programming language knowledge

## Usage Instructions

### Step 1: Schema Design

Use clear, consistent naming:

```graphql
type User {
  id: ID!
  name: String!
  email: String!
  posts: [Post!]!
}

type Post {
  id: ID!
  title: String!
  content: String!
  author: User!
}
```

### Step 2: Query Optimization

Implement DataLoader for N+1 problem:

```javascript
const userLoader = new DataLoader(async (userIds) => {
  const users = await User.findByIds(userIds);
  return userIds.map(id => users.find(user => user.id === id));
});
```

### Step 3: Error Handling

Use GraphQL errors correctly:

```graphql
type Query {
  user(id: ID!): User
}

# Error response
{
  "errors": [
    {
      "message": "User not found",
      "locations": [{"line": 1, "column": 1}],
      "path": ["user"],
      "extensions": {
        "code": "NOT_FOUND"
      }
    }
  ],
  "data": {
    "user": null
  }
}
```

### Step 4: Security

Implement query depth limiting:

```javascript
const depthLimit = require('graphql-depth-limit');
const depthLimitRule = depthLimit(10);
```

## Examples

### GraphQL Schema

```graphql
type Query {
  users(limit: Int, offset: Int): [User!]!
  user(id: ID!): User
  posts(authorId: ID): [Post!]!
}

type Mutation {
  createUser(input: CreateUserInput!): User!
  updateUser(id: ID!, input: UpdateUserInput!): User!
  deleteUser(id: ID!): Boolean!
}

input CreateUserInput {
  name: String!
  email: String!
}

input UpdateUserInput {
  name: String
  email: String
}
```

## Best Practices

1. Use clear, consistent naming
2. Implement DataLoader for N+1 problem
3. Use GraphQL errors correctly
4. Implement query depth limiting
5. Use fragments for reusability
6. Implement proper authorization

## References

- [GraphQL Best Practices](https://graphql.org/learn/best-practices/)
- [Apollo Server Documentation](https://www.apollographql.com/docs/)