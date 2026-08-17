---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: caching-strategies
description: Best practices for caching strategies and implementation
category: backend
version: 0.1.0
author: devtiagoabreu
tags: [caching, performance, redis, backend]
compatible:
  - opencode
  - claude-code
  - cursor
---

# Caching Strategies Best Practices

## Overview

This skill provides best practices for caching strategies and implementation, including cache invalidation, patterns, and tools.

## Prerequisites

- Basic understanding of caching concepts
- Access to caching tools (Redis, Memcached, etc.)

## Usage Instructions

### Step 1: Cache-Aside Pattern

Implement cache-aside pattern:

```python
def get_user(user_id):
    # Try to get from cache
    cache_key = f"user:{user_id}"
    user = redis.get(cache_key)
    
    if user:
        return json.loads(user)
    
    # Cache miss - get from database
    user = db.query("SELECT * FROM users WHERE id = %s", user_id)
    
    # Store in cache
    redis.setex(cache_key, 3600, json.dumps(user))
    
    return user
```

### Step 2: Cache Invalidation

Implement cache invalidation:

```python
def update_user(user_id, data):
    # Update database
    db.execute("UPDATE users SET ... WHERE id = %s", user_id)
    
    # Invalidate cache
    cache_key = f"user:{user_id}"
    redis.delete(cache_key)
    
    # Optionally, invalidate related caches
    redis.delete(f"user:{user_id}:posts")
```

### Step 3: TTL Strategy

Set appropriate TTL values:

```python
# Static data - long TTL
redis.setex("config:app", 86400, json.dumps(config))

# User data - medium TTL
redis.setex(f"user:{user_id}", 3600, json.dumps(user))

# Session data - short TTL
redis.setex(f"session:{session_id}", 1800, json.dumps(session))
```

### Step 4: Cache Warming

Implement cache warming:

```python
def warm_cache():
    # Get popular items
    popular_items = db.query(
        "SELECT * FROM products ORDER BY sales DESC LIMIT 100"
    )
    
    # Cache them
    for item in popular_items:
        redis.setex(
            f"product:{item['id']}",
            3600,
            json.dumps(item)
        )
```

## Examples

### Redis Configuration

```python
import redis

# Connection pool
pool = redis.ConnectionPool(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True
)

r = redis.Redis(connection_pool=pool)

# Cache with TTL
r.setex('key', 3600, 'value')

# Cache with hash
r.hset('user:1', mapping={
    'name': 'John',
    'email': 'john@example.com'
})
```

## Best Practices

1. Use cache-aside pattern
2. Implement proper cache invalidation
3. Set appropriate TTL values
4. Implement cache warming
5. Monitor cache hit rates
6. Handle cache failures gracefully

## References

- [Redis Documentation](https://redis.io/documentation)
- [Caching Patterns](https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/Patterns.html)