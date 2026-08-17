---
name: code-review-process
description: Comprehensive code review process and checklist
version: 0.1.0
author: devtiagoabreu
tags: [code-review, quality, best-practices]
compatible:
  - opencode
  - claude-code
  - cursor
steps:
  - title: Pull Code Changes
    description: Pull the latest changes from the repository
    commands:
      - git pull origin main
  - title: Create Feature Branch
    description: Create a new branch for the feature
    commands:
      - git checkout -b feature/feature-name
  - title: Make Changes
    description: Implement the required changes
    commands: []
  - title: Run Tests
    description: Ensure all tests pass
    commands:
      - npm test  # For Node.js
      - pytest  # For Python
  - title: Run Linter
    description: Check code quality
    commands:
      - npm run lint  # For Node.js
      - flake8 .  # For Python
  - title: Create Pull Request
    description: Create a PR with descriptive title and description
    commands:
      - git add .
      - git commit -m "feat: add new feature"
      - git push origin feature/feature-name
estimatedTime: 60 minutes
difficulty: intermediate
---

# Code Review Process Playbook

## Overview

This playbook provides a comprehensive code review process to ensure code quality and consistency.

## Prerequisites

- Git installed
- Repository access
- Testing framework configured

## Steps

### Step 1: Pull Code Changes

```bash
git pull origin main
```

### Step 2: Create Feature Branch

```bash
git checkout -b feature/feature-name
```

### Step 3: Make Changes

Implement your changes following the project's coding standards.

### Step 4: Run Tests

For Node.js:
```bash
npm test
```

For Python:
```bash
pytest
```

### Step 5: Run Linter

For Node.js:
```bash
npm run lint
```

For Python:
```bash
flake8 .
```

### Step 6: Create Pull Request

```bash
git add .
git commit -m "feat: add new feature"
git push origin feature/feature-name
```

## Code Review Checklist

### Functionality
- [ ] Code does what it's supposed to do
- [ ] Edge cases are handled
- [ ] Error handling is appropriate

### Code Quality
- [ ] Code is readable and maintainable
- [ ] No code duplication
- [ ] Proper naming conventions
- [ ] Comments where necessary

### Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] All tests pass

### Security
- [ ] No security vulnerabilities
- [ ] Input validation
- [ ] Proper authentication/authorization

### Documentation
- [ ] README updated
- [ ] API documentation updated
- [ ] Changelog updated

## Expected Outcome

- Clean, reviewed code
- All tests passing
- Documentation updated
- PR ready for merge