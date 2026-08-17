---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: code-review-best-practices
description: Code review best practices for constructive feedback and effective checklists
category: quality
version: 0.1.0
author: devtiagoabreu
tags: [code-review, collaboration, quality, checklist, pull-request]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - A git-based workflow with pull requests or merge requests
  - A code review tool (GitHub, GitLab, Bitbucket)
  - A shared Definition of Done
provides:
  - Principles for constructive, blame-free review feedback
  - A reusable review checklist covering correctness and security
  - Guidance on review scope, speed, and prioritization
  - Templates for common review comments
---

# Code Review Best Practices

## Overview

This skill covers how to conduct code reviews that improve code quality while
keeping the team collaborative and kind. It explains how to frame feedback
constructively, how to prioritize what to review, and how to keep reviews fast
enough to stay relevant. Reviewing is a shared responsibility: authors write
reviewable code and reviewers give clear, actionable input. A solid checklist
makes the process repeatable and ensures nothing important is missed.

## Prerequisites

- Understanding of the project's language, framework, and conventions
- Ability to build and run the tests locally
- A pull request workflow with at least one reviewer

## Usage Instructions

### Step 1: Review with the Right Mindset

Approach every review as a collaboration, not a gate:

- Assume the author did their best; ask questions instead of assuming faults.
- Review the code, not the person — never use sarcasm or blame.
- Be specific: point to the exact line and describe the concrete concern.
- Distinguish must-fix from nice-to-have; avoid blocking on style.

### Step 2: Use the Review Checklist

Walk through the checklist before approving:

```markdown
Correctness
- [ ] Logic matches the task and handles edge cases
- [ ] No obvious off-by-one, null, or empty-input bugs
- [ ] Error paths are handled and observable

Security
- [ ] No injection, unsafe deserialization, or hardcoded secrets
- [ ] Input from users or external systems is validated
- [ ] AuthN/AuthZ enforced where applicable

Quality
- [ ] Tests added/updated for changed behavior
- [ ] CI passes; no new warnings or type errors
- [ ] Naming and structure are consistent with the codebase

Maintainability
- [ ] Code is readable; comments explain "why", not "what"
- [ ] No dead code, debug statements, or TODOs left behind
- [ ] Public API and config changes are documented
```

### Step 3: Comment with the Right Tone

Use a consistent comment style so intent is obvious:

```markdown
Praise:    "Nice use of the guard clause here — much easier to follow."

Question:  "Does this branch also need to handle the offline case?"

Suggestion:"Consider extracting this into a helper so it's testable."

Nit:       "Minor: align the import order with the convention."
```

Reserve blocking comments for bugs, security issues, and broken contracts.

### Step 4: Keep Reviews Fast and Small

- Review within 24 hours; momentum matters more than perfection.
- Keep PRs small (< 400 lines is a good target); split big changes.
- Review the diff in a logical order (tests first, then the core change).
- If a PR is too large to review safely, ask the author to split it.

### Step 5: Respond as an Author

Treat review comments as the cheapest bug report you will ever get:

```markdown
- Reply to every comment: fix, agree, or push back with reasoning.
- Push new commits (or amend) for fixes; keep the discussion visible.
- Mark resolved discussions with a short note on what changed.
- Thank the reviewer; never argue over style preferences.
```

### Step 6: Automate the Obvious

Let tooling catch what humans should not have to repeat:

```bash
# Example CI checks gating merge
npx eslint . --max-warnings 0
npm run typecheck
npx prettier --check .
```

## Examples

### Example 1: Constructive Review Comment

```markdown
> await saveUser(user);

Concern: if `saveUser` throws, we leave the session flag set.
Suggestion: wrap in try/catch and roll back, or set the flag after a
successful save. Tests for the failure path would be great too.
```

### Example 2: Author's Reply Template

```markdown
@reviewer Thanks for catching this. The session flag is now set only after
`saveUser` resolves, and I added a test for the DB failure path. Resolving.
```

## References

- [Google Engineering Practices: Code Review](https://google.github.io/eng-practices/review/)
- [GitHub Pull Request Best Practices](https://docs.github.com/pull-requests/collaborating-with-pull-requests)
- [The Art of Code Review](https://martinfowler.com/bliki/CodeReview.html)
- [Conventional Comments](https://conventionalcomments.org/)
- [How to do a code review — Gergely Orosz](https://blog.pragmaticengineer.com/code-review/)
- [Microsoft: Code Review at Microsoft](https://devblogs.microsoft.com/engineering-at-microsoft/code-review-at-microsoft/)

## Notes

- Review speed is a team metric: aim to review most PRs within 24 hours.
- Prefer "nit:" prefixes so authors can batch cosmetic fixes.
- Approve enthusiastically; nobody wants to guess why you stayed silent.
- Automate formatting and linting so humans review logic, not style.
- Every reviewer comment is training data for better future PRs.
- If you spot the same issue in three PRs, propose a shared helper or lint rule.
