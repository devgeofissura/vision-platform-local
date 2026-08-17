---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: agile-scrum
description: Agile and Scrum ceremonies, roles, and practices for effective team delivery
category: projects
version: 0.1.0
author: devtiagoabreu
tags: [agile, scrum, ceremonies, sprint, team, project-management]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - A product team with a Product Owner and Scrum Master roles
  - A shared backlog management tool (Jira, Linear, Trello, GitHub Issues)
  - Commitment to fixed-length sprints
provides:
  - Defined Scrum roles and their responsibilities
  - Ready-to-run ceremony agendas with timeboxes
  - Templates for user stories and sprint planning
  - Guidance on retrospectives and continuous improvement
---

# Agile & Scrum

## Overview

This skill explains how to run Scrum effectively: the roles, the ceremonies,
and the artifacts that keep a team delivering value every sprint. It covers
sprint planning, daily stand-ups, backlog refinement, sprint reviews, and
retrospectives with concrete agendas and timeboxes. Scrum is lightweight by
design, so the emphasis here is on the practices that make the framework work
instead of ceremony for its own sake. The guidance applies to software teams of
all sizes, from new squads to established product groups.

## Prerequisites

- A cross-functional team (developers, designer, QA, Product Owner)
- A Product Owner empowered to prioritize the backlog
- A Scrum Master or facilitator to run the ceremonies
- An accessible tool for tracking backlog items and sprints

## Usage Instructions

### Step 1: Define Roles

Assign the three core Scrum roles explicitly:

- **Product Owner**: owns the backlog, prioritizes value, clarifies stories.
- **Scrum Master**: coaches the process, removes impediments, facilitates.
- **Development Team**: self-organizes and owns delivery of sprint work.

Document who holds each role and make the boundaries public.

### Step 2: Write User Stories

Write backlog items as user stories with acceptance criteria:

```markdown
As a registered user,
I want to reset my password by email
so that I can regain access when I forget it.

Acceptance criteria:
- [ ] Email contains a single-use reset link
- [ ] Link expires after 15 minutes
- [ ] User lands on a confirmation screen after reset
```

Use the INVEST criteria: **I**ndependent, **N**egotiable, **V**aluable,
**E**stimable, **S**mall, **T**estable.

### Step 3: Plan the Sprint

Run sprint planning at the start of each sprint (max 2 hours for a 2-week
sprint). Pull stories from the top of the backlog into a sprint goal:

```bash
# Example sprint goal statement
# "Deliver self-service password reset and MFA enrollment"
```

Output of the ceremony: a sprint backlog, a sprint goal, and team commitment.

### Step 4: Hold Daily Stand-ups

Keep the daily stand-up under 15 minutes. Each person answers three questions:

```markdown
1. What did I do yesterday?
2. What will I do today?
3. Are there any blockers?
```

Timebox each person to 60 seconds. Move detailed discussions to follow-ups.

### Step 5: Refine the Backlog

Run backlog refinement before each planning session:

- Split large items ("epics") into stories
- Clarify acceptance criteria and edge cases
- Estimate with story points using relative sizing
- Add missing details to avoid planning-time surprises

A recommended rhythm is one 45–60 minute refinement session per week.

### Step 6: Review and Retrospective

Close the sprint with two ceremonies:

**Sprint Review** (max 1 hour): demo completed work to stakeholders, collect
feedback, update the backlog.

**Sprint Retrospective** (max 45 minutes): inspect the process, not people.

```markdown
Start: what went well? (keep doing)
Stop: what is hurting us? (do less / stop)
Continue: what should we keep? 
Try: what experiment do we run next sprint?
```

Write down one concrete action per team and track it until it is done.

## Examples

### Example 1: One-Week Sprint Checklist

```markdown
Monday 09:00  - Sprint planning (2h)
Tuesday       - Backlog refinement (optional)
Daily 09:30   - Stand-up (15 min)
Friday 15:00  - Sprint review (1h)
Friday 16:00  - Retrospective (45 min)
```

### Example 2: Definition of Done Template

```markdown
A story is DONE when:
- Code is reviewed and merged to the main branch
- Unit and integration tests pass in CI
- Feature is verified manually in a staging environment
- Documentation is updated if behavior changed
- Demo is prepared for the sprint review
```

## References

- [The Scrum Guide](https://scrumguides.org/scrum-guide.html)
- [Scrum.org Learning Path](https://www.scrum.org/learning-path)
- [Atlassian: Scrum ceremonies](https://www.atlassian.com/agile/scrum/ceremonies)
- [Agile Manifesto](https://agilemanifesto.org/)
- [Mountain Goat: User Stories](https://www.mountaingoatsoftware.com/agile/user-stories)
- [Effective Retrospectives](https://retrospectivewiki.org/)

## Notes

- Keep ceremonies timeboxed; standing meetings are a symptom of weak follow-up.
- A sprint goal focuses the team when priorities shift mid-sprint.
- Velocity is a planning aid, never a team performance metric.
- Retrospective actions without owners are just notes.
- Adapt the framework (e.g., Kanban) when work is continuous rather than
  iterative.
- Protect the sprint from mid-sprint scope additions unless truly urgent.
