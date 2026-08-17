---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-15
name: brainstorming
description: Structured brainstorming to explore ideas, requirements and trade-offs before committing to a plan
category: methodology
version: 0.1.0
author: devtiagoabreu
tags: [brainstorming, ideation, planning, methodology, requirements]
compatible:
  - opencode
  - claude-code
  - cursor
provides:
  - Divergent exploration of the problem space
  - Structured capture of ideas and constraints
  - Clear decision point before writing a plan
difficulty: beginner
---

# Brainstorming

## Overview

Before writing a plan you need to understand the problem, surface
assumptions and explore the space of possible solutions. This skill turns an
open-ended request into a focused set of ideas, options and open questions
that can feed directly into the `writing-plans` skill.

Use it at the very start of a task, when the goal is broad, ambiguous, or
there are several plausible directions.

## Prerequisites

- A clear statement of the user's desire (however broad)
- No plan exists yet (or the plan is clearly wrong)

## Usage Instructions

### Step 1: Restate the goal

Ask "what is the actual goal?" and restate it in one sentence. Separate the
goal from the means. Example: the goal is "ship a payment flow", not "add a
checkout page".

### Step 2: Generate options

List at least 3 candidate approaches. Do not judge during generation — capture
everything, including ideas that seem weak. Use these prompts:

- What are the main ways to achieve the goal?
- What would each option cost in effort, risk and maintenance?
- What existing assets in this kit (skills, agents, templates) apply?

### Step 3: Surface constraints

Record hard constraints (deadlines, budget, tech stack, laws, team skills)
and soft constraints (preferences, nice-to-haves). Mark which are non-negotiable.

### Step 4: Identify open questions

List what you do not know yet. For each, note who can answer it or which
experiment would answer it.

### Step 5: Recommend

Present the options with a recommendation and the reasoning. Ask the user to
confirm before moving to `writing-plans`. Never silently pick for the user.

## Examples

### Example 1: New feature

```
Goal: allow users to export reports as PDF.

Options:
1. Browser print-to-PDF (fast, low quality)
2. Server-side PDF generation (reliable, more work)
3. Headless browser rendering (flexible, heavy)

Constraints: must work offline, no external API budget.
Open questions: what fidelity is required?
Recommendation: option 2.
```

### Example 2: Ambiguous request

```
"Make the app faster" -> restate: reduce page load to under 1s on 4G.
Options: code splitting, edge caching, image optimization.
```

## Best Practices

1. Restate the goal before generating options
2. Generate first, judge later
3. Separate hard and soft constraints
4. Write down open questions explicitly
5. Always end with a recommendation and a confirmation prompt
6. Hand the result to `writing-plans` once confirmed

## References

- [The Decision-Making Process](https://www.mindtools.com/pages/article/newTED_00.htm)
- [Superpowers brainstorming](https://github.com/obra/superpowers/blob/main/skills/brainstorming/brainstorming.md)
