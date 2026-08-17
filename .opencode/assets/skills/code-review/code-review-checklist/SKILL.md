---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: code-review-checklist
description: Comprehensive checklist for high-quality code review
category: code-review
version: 0.1.0
author: devtiagoabreu
tags: [code-review, quality, checklist]
compatible:
  - opencode
  - claude-code
  - cursor
requires: []
provides:
  - Review checklist
  - Evaluation criteria
  - Best practices
---

# Code Review Checklist

## Overview

This skill provides a complete and comprehensive checklist for code review,
helping to ensure quality, consistency, and absence of bugs.

## Prerequisites

- Access to the code being reviewed
- Knowledge of the technology stack
- Understanding of ticket/issue requirements

## Usage Instructions

### 1. Functional Checklist

- [ ] Code meets specified requirements
- [ ] Logic is correct
- [ ] Edge cases are handled
- [ ] Errors are handled properly
- [ ] Input validation present
- [ ] Exception handling adequate

### 2. Quality Checklist

- [ ] Code is readable and understandable
- [ ] Names are descriptive and consistent
- [ ] Functions are cohesive and small
- [ ] No duplicated code
- [ ] DRY principle applied
- [ ] SRP principle applied

### 3. Security Checklist

- [ ] No hardcoded secrets
- [ ] Input is validated
- [ ] Output is sanitized
- [ ] SQL injection prevented
- [ ] XSS prevented
- [ ] Authentication adequate

### 4. Performance Checklist

- [ ] No N+1 queries
- [ ] Cache is used appropriately
- [ ] No memory leaks
- [ ] Queries are optimized
- [ ] Assets are compressed
- [ ] Lazy loading implemented

### 5. Testing Checklist

- [ ] Unit tests present
- [ ] Integration tests present
- [ ] Code coverage adequate
- [ ] Tests are independent
- [ ] Tests are reproducible
- [ ] Mocks are appropriate

### 6. Documentation Checklist

- [ ] Code is self-explanatory
- [ ] Comments explain "why", not "what"
- [ ] README updated
- [ ] API documented
- [ ] Changelog updated
- [ ] Examples updated

### 7. Style Checklist

- [ ] Follows style guide
- [ ] Formatting is correct
- [ ] Indentation is consistent
- [ ] Spacing is appropriate
- [ ] Lines don't exceed 80 characters
- [ ] Imports are organized

## Examples

### Example 1: Pull Request Review

```markdown
## Code Review - PR #123

### Summary
Implements JWT authentication for the API.

### Checklist

#### Functionality
- [x] Requirements met
- [x] Logic correct
- [x] Edge cases handled

#### Quality
- [x] Code readable
- [x] Names descriptive
- [x] Functions cohesive

#### Security
- [x] No hardcoded secrets
- [x] Input validated
- [x] Output sanitized

### Comments
- Suggestion: use constant for expiration time
- Could extract validation logic to separate function

### Approval
✅ Approved with minor changes
```

### Example 2: Review Comments

````markdown
**Blocker:** This function doesn't handle network errors.

```javascript
// Bad
fetch(url).then(data => processData(data));

// Good
fetch(url)
  .then(data => processData(data))
  .catch(error => handleError(error));
```

**Major:** Function too long, suggest refactoring.

**Minor:** Style - extra space after comma.

**Nit:** Variable name could be more descriptive.
````

## References

- [Google Code Review Guide](https://google.github.io/eng-practices/review/)
- [Best Practices for Code Reviews](https://smartbear.com/best-practices-for-code-reviews/)
- [Code Review Checklist](https://www.pullrequest.com/blog/code-review-checklist/)

## Notes

- Focus on the code, not the person
- Be constructive and respectful
- Prioritize issues by severity
- Document important decisions
- Use linting tools when possible
