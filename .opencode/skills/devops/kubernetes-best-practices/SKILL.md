---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: kubernetes-best-practices
description: Best practices for Kubernetes container orchestration and deployment
category: devops
version: 0.1.0
author: devtiagoabreu
tags: [kubernetes, containers, orchestration, devops]
compatible:
  - opencode
  - claude-code
  - cursor
---

# Kubernetes Best Practices

## Overview

This skill provides best practices for working with Kubernetes, including container orchestration, deployment strategies, and cluster management.

## Prerequisites

- Kubernetes cluster access
- kubectl CLI installed
- Basic understanding of containers

## Usage Instructions

### Step 1: Pod Configuration

Always use resource limits and requests:

```yaml
resources:
  requests:
    memory: "64Mi"
    cpu: "250m"
  limits:
    memory: "128Mi"
    cpu: "500m"
```

### Step 2: Health Checks

Implement liveness and readiness probes:

```yaml
livenessProbe:
  httpGet:
    path: /healthz
    port: 8080
  initialDelaySeconds: 30
  periodSeconds: 10
readinessProbe:
  httpGet:
    path: /ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 5
```

### Step 3: Security Context

Run containers as non-root:

```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  readOnlyRootFilesystem: true
```

## Examples

### Deployment with Best Practices

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app
        image: my-app:latest
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "64Mi"
            cpu: "250m"
          limits:
            memory: "128Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
        securityContext:
          runAsNonRoot: true
          runAsUser: 1000
          readOnlyRootFilesystem: true
```

## Common Mistakes to Avoid

1. Not setting resource limits
2. Not implementing health checks
3. Running containers as root
4. Using latest tag in production
5. Not implementing rolling updates

## References

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/)