---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: database-design
description: Best practices for database design and modeling
category: backend
version: 0.1.0
author: devtiagoabreu
tags: [database, design, modeling, sql]
compatible:
  - opencode
  - claude-code
  - cursor
---

# Database Design Best Practices

## Overview

This skill provides best practices for database design and modeling, including normalization, indexing, and query optimization.

## Prerequisites

- Basic understanding of database concepts
- SQL knowledge

## Usage Instructions

### Step 1: Normalization

Normalize to at least 3NF:

```sql
-- Users table (1NF, 2NF, 3NF)
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Posts table (1NF, 2NF, 3NF)
CREATE TABLE posts (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  title VARCHAR(255) NOT NULL,
  content TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Step 2: Indexing

Create indexes for frequent queries:

```sql
-- Index for user lookup by email
CREATE INDEX idx_users_email ON users(email);

-- Index for post lookup by user
CREATE INDEX idx_posts_user_id ON posts(user_id);

-- Composite index for common queries
CREATE INDEX idx_posts_user_created ON posts(user_id, created_at);
```

### Step 3: Constraints

Use constraints for data integrity:

```sql
ALTER TABLE users ADD CONSTRAINT email_format 
  CHECK (email ~* '^[A-Za-z0-9._+%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$');

ALTER TABLE posts ADD CONSTRAINT content_length 
  CHECK (length(content) > 0);
```

### Step 4: Query Optimization

Use EXPLAIN to analyze queries:

```sql
EXPLAIN ANALYZE
SELECT * FROM posts 
WHERE user_id = 1 
ORDER BY created_at DESC 
LIMIT 10;
```

## Examples

### E-commerce Database Design

```sql
-- Products table
CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  price DECIMAL(10, 2) NOT NULL,
  stock INTEGER NOT NULL DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Orders table
CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  status VARCHAR(50) NOT NULL,
  total DECIMAL(10, 2) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Order items table
CREATE TABLE order_items (
  id SERIAL PRIMARY KEY,
  order_id INTEGER REFERENCES orders(id),
  product_id INTEGER REFERENCES products(id),
  quantity INTEGER NOT NULL,
  price DECIMAL(10, 2) NOT NULL
);
```

## Best Practices

1. Normalize to at least 3NF
2. Create indexes for frequent queries
3. Use constraints for data integrity
4. Use EXPLAIN to analyze queries
5. Implement proper backup strategies
6. Use connection pooling

## References

- [Database Design Best Practices](https://www.essentialsql.com/database-design-best-practices/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)