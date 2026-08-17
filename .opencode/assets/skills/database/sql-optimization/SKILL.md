---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: sql-optimization
description: Optimize SQL queries with indexes, EXPLAIN analysis, and database normalization
category: database
version: 0.1.0
author: devtiagoabreu
tags: [sql, postgresql, mysql, indexing, explain, performance, normalization]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Basic SQL (SELECT, JOIN, WHERE)
  - Access to a relational database to run EXPLAIN
  - Understanding of primary keys and foreign keys
provides:
  - Index selection and design guidelines
  - EXPLAIN/EXPLAIN ANALYZE interpretation guidance
  - Query rewriting patterns to avoid slow scans
  - Normalization and denormalization decision guidance
---

# SQL Query Optimization

## Overview

SQL optimization is the practice of reducing the time and resources a query consumes,
usually by ensuring the query planner can use indexes instead of full table scans.
The first step is measuring with `EXPLAIN ANALYZE`, which reveals whether the planner
chose a scan, an index lookup, or a join strategy that is expensive. Correct indexing,
good schema design through normalization, and query rewrites such as avoiding
functions on indexed columns combine to keep queries fast as data grows. Optimizing is
an empirical activity: always measure before and after a change rather than guessing.

## Prerequisites

- A running PostgreSQL or MySQL instance with sample data
- Comfort reading and writing SELECT queries with joins and filters
- A sense of the application queries that matter most (hot paths)

## Usage Instructions

### Step 1: Understand EXPLAIN Output

Run `EXPLAIN` to see the plan and `EXPLAIN ANALYZE` to execute and get timings:

```sql
EXPLAIN ANALYZE
SELECT id, email
FROM customers
WHERE country = 'DE'
ORDER BY created_at DESC
LIMIT 50;
```

```
 Seq Scan on customers  (cost=0.00..1453.22 rows=180 width=32)
   Filter: (country = 'DE'::text)
 Planning Time: 0.4 ms
 Execution Time: 58.7 ms
```

A `Seq Scan` over the whole table is the typical signal that an index is missing for
the filtered column.

### Step 2: Create Indexes That Match the Query

Add indexes on columns used in `WHERE`, `JOIN`, and `ORDER BY`. Cover the filter and
the ordering column together:

```sql
CREATE INDEX idx_customers_country_created
ON customers (country, created_at DESC);
```

Re-run `EXPLAIN ANALYZE`; the plan should now show an `Index Scan` or
`Index Only Scan` and a much smaller `Execution Time`. For equality filters plus a
range, lead with the equality column.

### Step 3: Rewrite Queries to Use Indexes

Avoid patterns that force the planner to discard the index:

```sql
-- Slow: function on the indexed column
SELECT * FROM orders WHERE DATE(created_at) = CURRENT_DATE;

-- Fast: range condition on the raw column
SELECT * FROM orders
WHERE created_at >= CURRENT_DATE AND created_at < CURRENT_DATE + INTERVAL '1 day';
```

Also avoid `%LIKE%` leading wildcards on indexed text; use trigram indexes (PG)
or full-text search instead. Selecting only needed columns lets an index-only scan
skip the heap.

### Step 4: Normalize the Schema

Apply 1NF, 2NF, and 3NF so each fact is stored once, which keeps updates consistent
and reduces join complexity:

```sql
-- Before (denormalized, repeated supplier data)
CREATE TABLE products (
  id int PRIMARY KEY,
  name text,
  supplier_name text,
  supplier_city text
);

-- After (3NF: supplier is its own table)
CREATE TABLE suppliers (
  id int PRIMARY KEY,
  name text,
  city text
);

CREATE TABLE products (
  id int PRIMARY KEY,
  name text,
  supplier_id int REFERENCES suppliers(id)
);
```

### Step 5: Analyze and Fix the Top Slow Queries

Enable slow query logging, collect the worst offenders, and work through them one by
one using the previous steps. PostgreSQL exposes `pg_stat_statements`, and MySQL has
the slow query log, both of which rank queries by total time.

## Examples

### Example 1: Fix a Slow Join

```sql
-- Before: seq scan on orders.customer_id
SELECT c.name, COUNT(o.id)
FROM customers c
JOIN orders o ON o.customer_id = c.id
GROUP BY c.name;

-- Fix: index the join column
CREATE INDEX idx_orders_customer_id ON orders (customer_id);
```

### Example 2: Use EXPLAIN to Compare Plans

```sql
EXPLAIN (ANALYZE, BUFFERS) SELECT id FROM customers WHERE country = 'DE';
-- After adding idx_customers_country, compare Execution Time and buffers read.
```

## References

- [PostgreSQL Documentation - Using EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html)
- [PostgreSQL Documentation - Indexes](https://www.postgresql.org/docs/current/indexes.html)
- [MySQL Documentation - EXPLAIN](https://dev.mysql.com/doc/refman/en/explain-output.html)
- [Use The Index, Luke - SQL indexing tutorial](https://use-the-index-luke.com/)
- [Wikipedia - Database normalization](https://en.wikipedia.org/wiki/Database_normalization)

## Notes

- Index everything you filter on, but not everything: each index slows writes and
  consumes disk, so drop unused ones with `pg_stat_user_indexes` or equivalent.
- Favor composite indexes and keep the column order matching the query's equality
  filters first.
- `EXPLAIN ANALYZE` actually runs the query; use it on reads and sample data in
  production, not on heavy writes.
- Normalize by default, then denormalize deliberately (materialized views, cached
  aggregates) when joins are proven slow.
- Re-check plans after schema or data changes; a previously fast plan can regress.
