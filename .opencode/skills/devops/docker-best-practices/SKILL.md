---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: docker-best-practices
description: Complete guide for Docker and containers best practices in production
category: devops
version: 0.1.0
author: devtiagoabreu
tags: [docker, containers, devops, production]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Docker 20.10+ installed
  - Docker Compose v2+ (optional)
provides:
  - Optimized Dockerfile
  - docker-compose.yml
  - .dockerignore
---

# Docker Best Practices

## Overview

This skill provides a complete guide of best practices for creating, optimizing,
and managing Docker containers in a production environment.

## Prerequisites

- Docker 20.10 or higher
- Docker Compose v2 or higher (optional, for multi-container)
- Basic container knowledge

## Usage Instructions

### 1. Creating an Optimized Dockerfile

Use multi-stage builds to reduce image size:

```dockerfile
# Stage 1: Build
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Stage 2: Production
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
EXPOSE 3000
CMD ["node", "dist/main.js"]
```

### 2. Using .dockerignore

```
node_modules
.git
.env
*.md
docker-compose*.yml
```

### 3. Managing Environment Variables

```bash
# Never hardcode secrets
docker run -e DATABASE_URL=$DATABASE_URL myapp
```

### 4. Health Checks

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1
```

### 5. Security

```dockerfile
# Run as non-root user
RUN addgroup -g 1001 -S appgroup
RUN adduser -S appuser -u 1001 -G appgroup
USER appuser
```

## Examples

### Example 1: Node.js API

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 3000
USER node
CMD ["node", "server.js"]
```

### Example 2: Python Flask

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

### Example 3: Docker Compose Multi-Service

```yaml
version: '3.8'
services:
  api:
    build: ./api
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
    depends_on:
      - db
  db:
    image: postgres:14-alpine
    environment:
      - POSTGRES_DB=myapp
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
volumes:
  postgres_data:
```

## References

- [Docker Official Docs](https://docs.docker.com/)
- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Docker Security](https://docs.docker.com/engine/security/)

## Notes

- Always use official base images
- Run as non-root user
- Use health checks in production
- Minimize Dockerfile layers
- Use .dockerignore to ignore unnecessary files
