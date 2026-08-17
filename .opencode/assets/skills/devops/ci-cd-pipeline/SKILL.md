---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: ci-cd-pipeline
description: Best practices for CI/CD pipeline design and implementation
category: devops
version: 0.1.0
author: devtiagoabreu
tags: [ci-cd, pipeline, automation, devops]
compatible:
  - opencode
  - claude-code
  - cursor
---

# CI/CD Pipeline Best Practices

## Overview

This skill provides best practices for designing and implementing continuous integration and continuous deployment pipelines.

## Prerequisites

- Basic understanding of CI/CD concepts
- Access to CI/CD platform (GitHub Actions, GitLab CI, etc.)

## Usage Instructions

### Step 1: Pipeline Structure

Organize pipeline into stages:

```yaml
stages:
  - build
  - test
  - security
  - deploy
```

### Step 2: Build Optimization

Cache dependencies and use parallel builds:

```yaml
cache:
  paths:
    - node_modules/
    - .npm/
```

### Step 3: Testing Strategy

Implement different testing levels:

```yaml
test:
  unit:
    script: npm run test:unit
  integration:
    script: npm run test:integration
  e2e:
    script: npm run test:e2e
```

### Step 4: Security Scanning

Add security scans to pipeline:

```yaml
security:
  sast:
    script: npm run security:sast
  dependencies:
    script: npm audit
  secrets:
    script: npm run security:secrets
```

## Examples

### GitHub Actions Workflow

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install dependencies
        run: npm ci
      - name: Run tests
        run: npm test
      - name: Build
        run: npm run build
      - name: Deploy
        if: github.ref == 'refs/heads/main'
        run: npm run deploy
```

## Best Practices

1. Keep pipelines fast
2. Fail fast
3. Use version control for pipeline configuration
4. Implement proper caching
5. Use secrets management
6. Monitor pipeline performance

## References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitLab CI Documentation](https://docs.gitlab.com/ee/ci/)