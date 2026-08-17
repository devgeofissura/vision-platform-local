---
name: security-audit
description: Perform a structured security audit of an application and its codebase
category: security
version: 0.1.0
author: devtiagoabreu
tags: [security, audit, vulnerabilities, owasp]
compatible:
  - opencode
  - claude-code
  - cursor
variables:
  - name: application
    description: Application, stack, or codebase to audit
  - name: scope
    description: Scope of the audit, threat model, and focus areas
---

# Security Audit

## Objective

Systematically identify security weaknesses in an application, prioritize
findings by risk, and recommend concrete remediation steps.

## Instructions

### Context

You are a security engineer. Review the application across authentication,
authorization, data handling, and dependency risk, aligned with OWASP Top 10.

### Task

1. Map the attack surface and define the threat model
2. Review authentication and authorization controls
3. Analyze input validation and output handling
4. Inspect secrets management and dependency exposure
5. Rank findings by severity and propose fixes

### Criteria

1. **Coverage:** All major attack surfaces examined
2. **Evidence:** Findings reference specific code or config
3. **Prioritization:** Severity ratings are justified
4. **Actionable:** Each finding has a concrete remediation

## Usage Example

```
Perform a security audit of:

Application: {{application}}

Scope: {{scope}}

Please:
1. Define the attack surface and threat model
2. Check authentication, authorization, and data validation
3. Identify secrets and vulnerable dependencies
4. Rank findings by severity with remediation steps
```

## Variations

### Variation 1: Dependency Audit

```
Audit the project dependencies:
1. Identify outdated and vulnerable packages
2. Check the dependency graph for supply chain risk
3. Recommend upgrades and mitigation
```

### Variation 2: Secure Code Review

```
Review this code with a security focus:
1. Look for injection and XSS vectors
2. Check for insecure cryptographic usage
3. Verify access control on every endpoint
```

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
