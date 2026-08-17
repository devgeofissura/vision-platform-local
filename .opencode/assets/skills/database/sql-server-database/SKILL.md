---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-15
name: sql-server-database
description: SQL Server best practices covering T-SQL, indexing, query tuning, and administration
category: database
version: 0.1.0
author: devtiagoabreu
tags: [sqlserver, tsql, database, indexing, performance, azure]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - SQL Server 2019 or newer (or Azure SQL Database)
  - SQL Server Management Studio (SSMS) or Azure Data Studio
provides:
  - T-SQL query and indexing practices
  - Execution plan analysis
  - Stored procedure conventions
  - Basic administration and monitoring
---

# SQL Server Database

## Overview

This skill is a guide to working effectively with Microsoft SQL Server. It
covers T-SQL query writing, indexing strategy, execution plan analysis, stored
procedure conventions, and core administration. These practices apply to both
on-premises SQL Server and Azure SQL Database.

## Prerequisites

- SQL Server 2019 or newer, or an Azure SQL Database
- SSMS or Azure Data Studio to run queries
- Basic SQL knowledge

## Usage Instructions

Use this skill when writing or reviewing T-SQL. Check execution plans for slow
queries, verify index usage, and follow the stored procedure conventions
before deploying.

## Query Tuning

### Capture the actual execution plan

```sql
SET STATISTICS IO, TIME ON;

SELECT c.CustomerID, c.Name, SUM(o.Total) AS TotalSpent
FROM   Sales.Customers c
JOIN   Sales.Orders o ON o.CustomerID = c.CustomerID
WHERE  o.OrderDate >= '2026-01-01'
GROUP  BY c.CustomerID, c.Name;
```

### Avoid functions on indexed columns

```sql
-- Avoid: function blocks index seek
SELECT * FROM Sales.Customers
WHERE  LOWER(Email) = 'ana@example.com';

-- Prefer:
SELECT * FROM Sales.Customers
WHERE  Email = 'ana@example.com';
```

## Indexing

### Cover frequent filter and join columns

```sql
CREATE INDEX IX_Orders_CustomerID ON Sales.Orders (CustomerID);
CREATE INDEX IX_Orders_OrderDate ON Sales.Orders (OrderDate);
```

### Use included columns to cover queries

```sql
CREATE INDEX IX_Orders_CustomerDate
ON Sales.Orders (CustomerID, OrderDate)
INCLUDE (Total);
```

### Find missing index suggestions

```sql
SELECT * FROM sys.dm_db_missing_index_details;
SELECT * FROM sys.dm_db_missing_index_group_stats;
```

## Stored Procedures

### Use SET NOCOUNT ON and bound parameters

```sql
CREATE PROCEDURE Sales.GetCustomerOrders
    @CustomerID INT
AS
BEGIN
    SET NOCOUNT ON;

    SELECT OrderID, OrderDate, Total
    FROM   Sales.Orders
    WHERE  CustomerID = @CustomerID
    ORDER  BY OrderDate DESC;
END;
GO
```

### Wrap data changes in transactions

```sql
CREATE PROCEDURE Sales.CreateOrder
    @CustomerID INT,
    @Total MONEY
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    BEGIN TRY
        BEGIN TRANSACTION;
            INSERT INTO Sales.Orders (CustomerID, Total)
            VALUES (@CustomerID, @Total);
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH;
END;
GO
```

## Administration

### Check index fragmentation

```sql
SELECT OBJECT_NAME(s.object_id) AS TableName,
       i.name AS IndexName,
       s.avg_fragmentation_in_percent
FROM   sys.dm_db_index_physical_stats
       (DB_ID(), NULL, NULL, NULL, 'LIMITED') s
JOIN   sys.indexes i
  ON   i.object_id = s.object_id
 AND   i.index_id = s.index_id
WHERE  s.avg_fragmentation_in_percent > 30;
```

### Rebuild fragmented indexes

```sql
ALTER INDEX ALL ON Sales.Orders REBUILD;
```

## Common Pitfalls

- `SELECT *` in production queries pulling unnecessary columns
- Missing indexes on foreign keys, causing join and filter scans
- Using scalar functions on columns in the WHERE clause
- Ignoring blocking and long-running queries

## Examples

### Top 10 expensive queries

```sql
SELECT TOP 10
       qs.total_worker_time,
       qs.total_logical_reads,
       SUBSTRING(st.text,
         (qs.statement_start_offset / 2) + 1,
         ((CASE qs.statement_end_offset
             WHEN -1 THEN DATALENGTH(st.text)
             ELSE qs.statement_end_offset
           END - qs.statement_start_offset) / 2) + 1) AS sql_text
FROM   sys.dm_exec_query_stats qs
CROSS  APPLY sys.dm_exec_sql_text(qs.sql_handle) st
ORDER  BY qs.total_worker_time DESC;
```

### Row version with OFFSET/FETCH pagination

```sql
SELECT OrderID, OrderDate, Total
FROM   Sales.Orders
ORDER  BY OrderID
OFFSET 0 ROWS
FETCH NEXT 50 ROWS ONLY;
```
