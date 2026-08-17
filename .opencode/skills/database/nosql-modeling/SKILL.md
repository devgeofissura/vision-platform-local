---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: nosql-modeling
description: Model data for NoSQL databases across document, key-value, and graph stores
category: database
version: 0.1.0
author: devtiagoabreu
tags: [nosql, mongodb, redis, document, key-value, graph, data-modeling]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Understanding of relational modeling concepts
  - Basic familiarity with JSON and map/dict structures
  - A target NoSQL engine (MongoDB, Redis, Neo4j) for experiments
provides:
  - Store selection guidance per access pattern
  - Document schema design and embedding rules
  - Key-value design patterns (cache, counter, session)
  - Graph modeling with nodes, edges, and traversal examples
---

# NoSQL Data Modeling

## Overview

NoSQL modeling starts from the application's access patterns instead of entity
normalization. A document store such as MongoDB embeds related data to enable single
round-trip reads, while a key-value store such as Redis optimizes for ultra-fast
point lookups of precomputed values. Graph databases such as Neo4j model relationships
as first-class data for traversals. Choosing the right store means choosing the model
that naturally serves the queries you will run, and being explicit about the
eventual-consistency and denormalization trade-offs that come with it.

## Prerequisites

- Basic JSON and array/data structure skills
- A mental model of reads vs. writes per use case
- A local instance or Docker container of the store you pick

## Usage Instructions

### Step 1: List Access Patterns Before Choosing a Store

Write down the concrete queries the application performs, with their frequency and
latency goals. This determines the store family:

```
Pattern                              Best store
Point lookup by key                  key-value (Redis)
Rich ad-hoc queries, nested docs     document (MongoDB)
Friend-of-friend, path traversal     graph (Neo4j)
Search / analytics                   search & columnar (OpenSearch, ClickHouse)
```

Never pick a store by hype; pick it because the dominant access pattern fits.

### Step 2: Model Documents with Embedding Rules

In MongoDB, embed related data when it is read together with the parent and bounded in
size; reference it when it grows unboundedly or is shared:

```javascript
// Embed: order items are read with the order and are bounded
{
  _id: ObjectId("..."),
  customerId: "c-42",
  createdAt: ISODate("2026-08-06T10:00:00Z"),
  items: [
    { sku: "A1", name: "Mouse", qty: 2, price: 25.0 }
  ],
  total: 50.0
}
```

If an order could hold thousands of items, move them to a separate collection keyed by
`orderId` instead of embedding.

### Step 3: Use the Right Indexes for Query Patterns

Model documents around the queries and index them accordingly:

```javascript
db.orders.createIndex({ customerId: 1, createdAt: -1 });
db.orders.find({ customerId: "c-42" }).sort({ createdAt: -1 }).limit(20);
```

Single-field and compound indexes behave like relational indexes; use them before
designing around denormalization.

### Step 4: Apply Key-Value Patterns in Redis

Design keys with clear namespaces and pick the data structure that matches the access:

```bash
# Cache with TTL - a short-lived object read by key
SET session:user:42 "{...}" EX 3600
GET session:user:42

# Counter - atomic increment
INCR page:views:2026-08-06

# Sorted set - leaderboard ordered by score
ZADD leaderboard:game1 100 "alice"
ZREVRANGE leaderboard:game1 0 9
```

### Step 5: Model Graphs with Nodes and Edges

Represent every entity as a node and every relationship as an edge with a type, so
traversals are expressed directly:

```cypher
CREATE (alice:Person {name: "Alice"})
CREATE (bob:Person {name: "Bob"})
CREATE (alice)-[:KNOWS]->(bob)
CREATE (bob)-[:KNOWS]->(carol)

// friends of friends of Alice
MATCH (alice:Person {name: "Alice"})-[:KNOWS]->()-[:KNOWS]->(fof:Person)
WHERE fof.name <> "Alice"
RETURN DISTINCT fof.name;
```

## Examples

### Example 1: Mongo Document with References

```javascript
// users (embedded profile)
db.users.insertOne({ _id: "u-1", name: "Ada", profile: { bio: "Engineer", city: "London" } });
// posts (reference to user; unbounded list, so separate collection)
db.posts.insertOne({ _id: "p-1", authorId: "u-1", text: "Hello!" });
db.posts.find({ authorId: "u-1" }).sort({ _id: -1 }).limit(50);
```

### Example 2: Redis Rate Limiter with Atomic Lua-Free Scripting

```bash
# Window counter: 100 requests per minute per user
SETEX rate:user:42 60 0
INCR rate:user:42
# check the returned value <= 100 to accept
```

## References

- [MongoDB Data Modeling](https://www.mongodb.com/docs/manual/data-modeling/)
- [MongoDB - 6 Rules of Thumb for MongoDB Schema Design](https://www.mongodb.com/blog/post/6-rules-of-thumb-for-mongodb-schema-design-part-1)
- [Redis Data Types](https://redis.io/docs/data-types/)
- [Neo4j Graph Data Modeling](https://neo4j.com/docs/getting-started/data-modeling/)
- [Martin Fowler - NoSQL Distilled](https://martinfowler.com/books/nosql.html)

## Notes

- Model first, then store; write the access patterns before touching a schema.
- Denormalization is a feature here, but each duplicate must be updated deliberately;
  consider change streams or scheduled reconciliation.
- Keys in key-value stores are strings; design a hierarchy such as
  `namespace:entity:id:field` and respect the store's memory limits.
- For graphs, model edge types precisely; a traversal is only meaningful if the edge
  semantics are clear.
- NoSQL does not remove the need for indexes, consistency review, or capacity planning.
