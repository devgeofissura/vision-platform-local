---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-15
name: oracle-database
description: Oracle Database best practices covering SQL tuning, PL/SQL, schema design, and administration
category: database
version: 0.1.0
author: devtiagoabreu
tags: [oracle, plsql, sql, database, performance]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Oracle Database 19c or newer
  - SQL*Plus or SQL Developer
provides:
  - SQL tuning and execution plan analysis
  - PL/SQL development patterns
  - Schema design and indexing guidance
  - Basic DBA operational practices
---

# Oracle Database

## Overview

This skill is a guide to working effectively with Oracle Database. It covers
SQL tuning using execution plans, PL/SQL development conventions, schema and
indexing design, and day-to-day administration. Applying these patterns keeps
queries fast, code maintainable, and databases healthy.

## Prerequisites

- Oracle Database 19c or newer (local or cloud)
- SQL*Plus, SQLcl, or SQL Developer for running statements
- Basic SQL knowledge

## Usage Instructions

Use this skill when writing or reviewing SQL and PL/SQL. Always inspect
execution plans for expensive queries and follow the indexing guidance before
deploying schema changes.

## SQL Tuning

### Use EXPLAIN PLAN to inspect execution

```sql
EXPLAIN PLAN FOR
SELECT c.customer_id, c.name, SUM(o.total) AS total_spent
FROM   customers c
JOIN   orders o ON o.customer_id = c.customer_id
WHERE  o.order_date >= DATE '2026-01-01'
GROUP  BY c.customer_id, c.name
HAVING SUM(o.total) > 1000;

SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);
```

### Avoid functions on indexed columns

```sql
-- Avoid: function prevents index use
SELECT * FROM customers
WHERE  UPPER(email) = 'ANA@EXAMPLE.COM';

-- Prefer: store emails consistently or use a function-based index
SELECT * FROM customers
WHERE  email = 'ana@example.com';
```

## Indexing

### Create indexes on foreign keys and hot filters

```sql
CREATE INDEX idx_orders_customer ON orders (customer_id);
CREATE INDEX idx_orders_order_date ON orders (order_date);
```

### Use composite indexes matching the WHERE order

```sql
CREATE INDEX idx_orders_cust_date
ON orders (customer_id, order_date DESC);
```

## PL/SQL Patterns

### Prefer bound variables

```plsql
DECLARE
  l_email VARCHAR2(200) := :email;
  l_customer customers%ROWTYPE;
BEGIN
  SELECT * INTO l_customer
  FROM   customers
  WHERE  email = l_email;

  DBMS_OUTPUT.PUT_LINE('Found: ' || l_customer.name);
EXCEPTION
  WHEN NO_DATA_FOUND THEN
    DBMS_OUTPUT.PUT_LINE('Not found');
END;
/
```

### Use bulk collect for large result sets

```plsql
DECLARE
  TYPE t_ids IS TABLE OF customers.customer_id%TYPE;
  l_ids t_ids;
BEGIN
  SELECT customer_id BULK COLLECT INTO l_ids
  FROM   customers
  WHERE  status = 'ACTIVE';

  FOR i IN 1 .. l_ids.COUNT LOOP
    process_customer(l_ids(i));
  END LOOP;
END;
/
```

## Administration

### Check fragmentation and growth

```sql
SELECT segment_name, segment_type,
       ROUND(bytes / 1024 / 1024, 2) AS size_mb
FROM   user_segments
ORDER  BY bytes DESC
FETCH FIRST 10 ROWS ONLY;
```

### Take backups with RMAN

```bash
rman target /
RMAN> BACKUP DATABASE PLUS ARCHIVELOG;
RMAN> BACKUP INCREMENTAL LEVEL 1 DATABASE;
```

## Common Pitfalls

- Writing queries that force full table scans on large tables
- Missing indexes on foreign keys, causing join slowdowns
- Unbounded `SELECT *` in PL/SQL procedures
- Ignoring bind variables and suffering hard parses

## Examples

### Reporting query with a window function

```sql
SELECT customer_id, order_date, total,
       RANK() OVER (PARTITION BY customer_id
                    ORDER BY total DESC) AS order_rank
FROM   orders;
```

### Find and kill a blocking session

```sql
SELECT s.sid, s.serial#, s.username, s.status
FROM   v$session s
WHERE  s.blocking_session IS NOT NULL;

ALTER SYSTEM KILL SESSION '123,456' IMMEDIATE;
```
