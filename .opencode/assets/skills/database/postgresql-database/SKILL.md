---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-15
name: postgresql-database
description: PostgreSQL best practices covering schema design, indexing, query tuning, and administration
category: database
version: 0.1.0
author: devtiagoabreu
tags: [postgresql, postgres, sql, indexing, database, performance]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - PostgreSQL 14 or newer
  - psql or a GUI like pgAdmin or DBeaver
provides:
  - Schema design and type guidance
  - Indexing and EXPLAIN analysis
  - Query tuning practices
  - Backup and maintenance operations
---

# PostgreSQL Database

## Overview

This skill is a guide to building and tuning PostgreSQL databases. It covers
schema and type design, indexing strategies, query analysis with EXPLAIN, and
core administration such as backups. Following these practices keeps
databases fast, consistent, and easy to maintain.

## Prerequisites

- PostgreSQL 14 or newer running locally or on a host
- psql, pgAdmin, or DBeaver to run queries
- Basic SQL knowledge

## Usage Instructions

Use this skill when designing tables, writing queries, or tuning PostgreSQL.
Always run EXPLAIN on slow queries and review index usage before deploying.

## Schema Design

### Prefer appropriate native types

```sql
CREATE TABLE customers (
    customer_id  BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name         TEXT NOT NULL,
    email        TEXT NOT NULL UNIQUE,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    is_active    BOOLEAN NOT NULL DEFAULT TRUE
);
```

### Add checks and constraints at the database level

```sql
ALTER TABLE orders
  ADD CONSTRAINT chk_orders_total
  CHECK (total >= 0);
```

## Indexing

### Index hot filters and joins

```sql
CREATE INDEX idx_orders_customer_id ON orders (customer_id);
CREATE INDEX idx_orders_created_at ON orders (created_at DESC);
```

### Use partial indexes for sparse data

```sql
CREATE INDEX idx_orders_pending
ON orders (created_at)
WHERE status = 'PENDING';
```

## Query Tuning

### Analyze with EXPLAIN ANALYZE

```sql
EXPLAIN ANALYZE
SELECT c.name, SUM(o.total) AS total_spent
FROM   customers c
JOIN   orders o ON o.customer_id = c.customer_id
WHERE  o.created_at >= '2026-01-01'
GROUP  BY c.name
ORDER  BY total_spent DESC;
```

### Keep stats fresh for the planner

```sql
VACUUM ANALYZE orders;
```

## Common Queries

### Pagination with keyset

```sql
SELECT id, name, created_at
FROM   customers
WHERE  (created_at, id) > ('2026-01-15T10:00:00Z', 12345)
ORDER  BY created_at, id
LIMIT  50;
```

### Aggregation with window functions

```sql
SELECT customer_id, order_date, total,
       RANK() OVER (PARTITION BY customer_id
                    ORDER BY total DESC) AS order_rank
FROM   orders;
```

## Administration

### Logical backup with pg_dump

```bash
pg_dump -U app_user -d mydb -F c -f mydb.dump
pg_restore -U app_user -d mydb mydb.dump
```

### Connection and activity monitoring

```sql
SELECT pid, usename, state, wait_event_type,
       now() - query_start AS duration
FROM   pg_stat_activity
WHERE  state <> 'idle'
ORDER  BY duration DESC;
```

### Check table bloat

```sql
SELECT relname, n_live_tup, n_dead_tup
FROM   pg_stat_user_tables
WHERE  n_dead_tup > 10000
ORDER  BY n_dead_tup DESC;
```

## Common Pitfalls

- Using `VARCHAR(n)` where `TEXT` or a native type is more appropriate
- Missing indexes on foreign keys, causing join slowdowns
- `SELECT *` pulling unneeded columns in hot paths
- Neglecting `VACUUM` on heavily updated tables

## Examples

### Upsert with ON CONFLICT

```sql
INSERT INTO customers (email, name)
VALUES ('ana@example.com', 'Ana Silva')
ON CONFLICT (email)
DO UPDATE SET name = EXCLUDED.name;
```

### Full-text search setup

```sql
ALTER TABLE posts
  ADD COLUMN search_vector tsvector
  GENERATED ALWAYS AS
    (to_tsvector('portuguese', coalesce(title, '') || ' ' ||
                               coalesce(body, ''))) STORED;

CREATE INDEX idx_posts_search ON posts USING GIN (search_vector);

SELECT id, title
FROM   posts
WHERE  search_vector @@ to_tsquery('portuguese', 'banco & dados');
```
