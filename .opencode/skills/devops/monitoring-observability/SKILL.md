---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: monitoring-observability
description: Best practices for monitoring and observability in cloud applications
category: devops
version: 0.1.0
author: devtiagoabreu
tags: [monitoring, observability, logging, metrics]
compatible:
  - opencode
  - claude-code
  - cursor
---

# Monitoring and Observability Best Practices

## Overview

This skill provides best practices for implementing monitoring and observability in cloud applications, including logging, metrics, and tracing.

## Prerequisites

- Basic understanding of monitoring concepts
- Access to monitoring tools (Prometheus, Grafana, etc.)

## Usage Instructions

### Step 1: Logging Strategy

Implement structured logging:

```json
{
  "timestamp": "2024-01-01T00:00:00Z",
  "level": "info",
  "message": "User logged in",
  "userId": "12345",
  "service": "auth-service",
  "traceId": "abc123"
}
```

### Step 2: Metrics Collection

Define key metrics (RED method):

- **Rate**: Requests per second
- **Errors**: Error rate
- **Duration**: Response time

```promql
# Rate
rate(http_requests_total[5m])

# Errors
rate(http_requests_total{status=~"5.."}[5m])

# Duration
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
```

### Step 3: Distributed Tracing

Implement trace context propagation:

```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("process_request") as span:
    span.set_attribute("user.id", user_id)
    # Process request
```

### Step 4: Alerting

Configure meaningful alerts:

```yaml
groups:
  - name: application
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: High error rate detected
```

## Examples

### Prometheus Configuration

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'my-app'
    static_configs:
      - targets: ['localhost:8080']
```

### Grafana Dashboard

```json
{
  "panels": [
    {
      "title": "Request Rate",
      "type": "graph",
      "targets": [
        {
          "expr": "rate(http_requests_total[5m])",
          "legendFormat": "{{method}} {{status}}"
        }
      ]
    }
  ]
}
```

## Best Practices

1. Use structured logging
2. Implement the RED method for metrics
3. Use distributed tracing
4. Set up meaningful alerts
5. Monitor business metrics
6. Implement log correlation

## References

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [OpenTelemetry Documentation](https://opentelemetry.io/docs/)