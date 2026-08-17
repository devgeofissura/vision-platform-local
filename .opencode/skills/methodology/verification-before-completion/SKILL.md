---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-15
name: verification-before-completion
description: Verify a task is actually done by re-checking every claim against evidence before declaring completion
category: methodology
version: 0.1.0
author: devtiagoabreu
tags: [verification, quality, methodology, acceptance-criteria, completion]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - executing-plans
provides:
  - Evidence-based definition of done
  - Detection of false completion claims
  - A final verification checklist before handoff
difficulty: beginner
---

# Verification Before Completion

## Overview

The most common failure mode in AI-assisted development is declaring work done
when it is not. This skill requires re-verifying every claim with evidence
before a task is marked complete. "I think it works" is not completion;
"the command ran and its output shows X" is.

## Prerequisites

- The acceptance criteria for the task (from the plan)
- Access to the commands that can prove each criterion

## Usage Instructions

### Step 1: List the claims

Restate the task's acceptance criteria as claims, one per line. Example
claims: "tests pass", "build succeeds", "README updated".

### Step 2: Re-run, don't recall

Run the actual command for each claim and capture the output. Never rely on a
previous run or on memory.

### Step 3: Map evidence to claims

For each claim record the command and its result:

| Claim | Command | Result |
|-------|---------|--------|
| Tests pass | `./scripts/test.sh` | 21/21 |
| Build works | `npm run build` | exit 0 |

### Step 4: Handle failures honestly

If any claim cannot be evidenced, the task is NOT complete. Record the gap,
update the plan (`executing-plans`) and continue. Do not mark it done.

### Step 5: State the completion summary

Report the evidence table to the user. Completion is only declared when every
row has a positive result.

## Examples

### Example 1: Honest verification

```
Claim: "added discount to invoice"
Evidence: pytest tests/test_invoice.py -k discount -> 3 passed
          curl /invoice/1 -> {"total": 90}
Status: DONE
```

### Example 2: False completion caught

```
Claim: "all tests pass"
Claimed but not re-run; running ./scripts/test.sh -> 2 failures.
Status: NOT DONE — failures reported, plan updated.
```

## Best Practices

1. Write claims before starting the work
2. Re-run the command, never trust memory
3. Record command and output for every claim
4. A missing evidence row means the task is not done
5. Report the evidence table in the completion summary

## References

- [Superpowers verification-before-completion](https://github.com/obra/superpowers/blob/main/skills/verification-before-completion/verification-before-completion.md)
- [Definition of Done (Agile)](https://www.agilealliance.org/glossary/definition-of-done/)
