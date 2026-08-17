---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: incident-response
description: Best practices for incident response and management
category: devops
version: 0.1.0
author: devtiagoabreu
tags: [incident-response, management, on-call, devops]
compatible:
  - opencode
  - claude-code
  - cursor
---

# Incident Response Best Practices

## Overview

This skill provides best practices for incident response and management, including preparation, detection, containment, and post-incident review.

## Prerequisites

- Basic understanding of incident management
- Access to communication tools

## Usage Instructions

### Step 1: Preparation

Create an incident response plan:

```markdown
# Incident Response Plan

## Roles
- Incident Commander: Overall responsibility
- Technical Lead: Technical investigation
- Communications Lead: Internal/external communications

## Severity Levels
- P1: Critical - Complete outage
- P2: High - Major feature unavailable
- P3: Medium - Minor feature affected
- P4: Low - Cosmetic issue
```

### Step 2: Detection and Alerting

Implement monitoring alerts:

```yaml
alerts:
  - name: Service Down
    condition: up == 0
    severity: P1
  - name: High Error Rate
    condition: rate(errors[5m]) > 0.05
    severity: P2
```

### Step 3: Containment

Isolate affected systems:

```bash
# Scale down affected service
kubectl scale deployment my-service --replicas=0

# Enable maintenance mode
curl -X POST https://api.example.com/maintenance/enable
```

### Step 4: Communication

Send status updates:

```markdown
# Incident Update - [INCIDENT-ID]

**Status**: Investigating
**Severity**: P1
**Impact**: Users unable to login
**Next Update**: 30 minutes

## Timeline
- 10:00 AM - Alert triggered
- 10:05 AM - Incident declared
- 10:10 AM - Investigation started
```

### Step 5: Post-Incident Review

Conduct blameless post-mortem:

```markdown
# Post-Incident Review

## What happened?
- Service became unavailable due to database connection exhaustion

## What went well?
- Alert triggered within 1 minute
- Incident response followed plan

## What could be improved?
- Better connection pooling
- Automated failover

## Action Items
- [ ] Implement connection pooling
- [ ] Add automated failover
```

## Examples

### Incident Communication Template

```markdown
# [SEVERITY] [SERVICE] - [TITLE]

**Status**: [Investigating/Identified/Monitoring/Resolved]
**Impact**: [Description of user impact]
**Next Update**: [Time]

## Updates
- [TIME] - [Update message]
```

## Best Practices

1. Have a documented incident response plan
2. Define clear roles and responsibilities
3. Communicate regularly with stakeholders
4. Conduct blameless post-mortems
5. Track action items to completion
6. Review and update plan regularly

## References

- [Google SRE Book](https://sre.google/sre-book/table-of-contents/)
- [Incident Management Best Practices](https://www.atlassian.com/incident-management)