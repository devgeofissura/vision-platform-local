---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: classroom-management
description: Build routines, positive reinforcement, engagement, and proactive behavior support in the classroom
category: education
version: 0.1.0
author: devtiagoabreu
tags: [classroom-management, routines, positive-reinforcement, engagement, behavior-support, PBIS, teaching]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - A class or group of learners you teach regularly
  - A defined set of classroom expectations
  - Willingness to be consistent across lessons
  - Time to teach and rehearse routines
provides:
  - A routines and procedures bank
  - A positive reinforcement system template
  - Engagement check strategies
  - A tiered behavior support framework
---

# Classroom Management

## Overview

Classroom management is not about control; it is about design. The most
effective classrooms run on predictable routines, positive reinforcement for
what learners do well, high engagement that prevents off-task behavior, and
proactive support for the few students who need more than routines provide.

The 80-20 rule usually applies: invest most effort in proactive prevention
(expectations, routines, relationships, engaging lessons) and only a little in
reacting to misbehavior. Good management makes the teaching you planned actually
reach the learners.

This skill provides a routines bank, a positive reinforcement system,
engagement checkpoints, and a tiered behavior support framework that can be
implemented from day one.

## Prerequisites

- Your classroom expectations (3-5, stated positively, e.g., "be ready to
  learn" instead of "do not run")
- A regular schedule and a place to display it
- A way to record data (paper sheet, spreadsheet, or app)
- Follow-through: routines only work when repeated consistently

## Usage Instructions

### Step 1: Define and Teach Expectations

Define 3-5 positive expectations and teach them like content:

```
Expectations: respect, responsibility, readiness, safety
Teach each one: what it looks like, sounds like, feels like
Practice: rehearse the desired behavior in role-plays
Revisit: quick review at the start of each week
```

Never assume learners know the behavior. Demonstrate it, model it, and have
learners practice the correct version.

### Step 2: Install Non-Negotiable Routines

Routines remove decision-making friction and off-task time. Teach these first:

```
Entry:   enter, sit, start the warm-up silently (2 min target)
Materials: where to get and return supplies
Transitions: signal (bell, light, countdown), then move quietly
Attention: teacher signal, learners stop and look (teach a response)
Exit:    tidy, pack, quick review question
```

Each routine needs a visual cue or verbal signal and should be rehearsed until
it takes less than a minute.

### Step 3: Reinforce Positive Behavior

Reinforce the behavior you want, immediately and specifically:

```
Specific praise: "Maria waited for the signal before speaking. That was
responsibility." (not "good job")
Ratio: aim for 4-5 positive statements for every correction
Class-wide system: token, point, or chart tied to a group reward
Individual plans: for learners who need more frequent recognition
```

State the observed behavior and the expectation it meets. The reward should be
a privilege learners value, agreed in advance.

### Step 4: Manage Engagement to Prevent Problems

Most misbehavior is the result of boredom or confusion. Keep learners engaged:

```
Chunking: switch activity type every 10-15 minutes
Cold calling: random questions keep everyone accountable
Checkpoints: quick thumbs-up / mini-quiz every few minutes
Pacing: keep a visible timer; move briskly between phases
Choice: offer two acceptable options ("this page or this page")
```

If behavior problems cluster, audit the lesson first: was the task too hard,
too easy, or too long?

### Step 5: Respond to Misbehavior with Tiers

Use the lightest effective response, escalating only when needed:

```
Tier 1 (prevent):     routines, praise, engagement, relationship
Tier 2 (correct):     proximity, eye contact, quiet redirect, reminder of
                      the routine, private conversation after class
Tier 3 (support):     documented plan, parent contact, counseling or
                      functional behavior assessment
```

Correct privately and calmly. Never humiliate; the behavior is the problem, not
the person.

### Step 6: Track Data and Adjust

Write down what actually happens so decisions are evidence-based:

```
Daily: note the 2 most frequent problems and what preceded them
Weekly: count praise-to-correction ratio and transitions time
Monthly: review which learners need Tier 2 support and adjust
```

Data converts classroom management from opinion to engineering: you can measure
whether a new routine or reinforcement system is working.

## Examples

### Example 1: First-Week Routine Launch

```text
Day 1: teach expectations; model "entry" and "attention" signals
Day 2: rehearse entry routine until 2 minutes; start warm-up habit
Day 3: teach transitions; practice the 3 signals in a game
Day 4: introduce the praise and class-reward system
Day 5: run a full period using every routine; debrief with the class
```

### Example 2: Positive Reinforcement Point System

```yaml
expectation: respect
point_card:
  - "caught being ready": +1
  - "helps a peer": +1
  - "perfect transition": +1
class_reward_options:
  - "10 minutes free choice"
  - "game day"
  - "extra recess"
individual_tier2_plan:
  goal: "Raise hand before speaking (5 times per period)"
  check_every: "each 20 minutes"
  reward: "special helper role for the next period"
```

### Example 3: Transition Signal Script

```python
def run_transition(signal, routine, timeout_seconds):
    print(f"1. Give signal: {signal}")
    print(f"2. Learners respond: {routine}")
    print(f"3. Time the transition; target under {timeout_seconds}s")
    print("4. Praise fast, correct slow, record the time")
    print("5. Re-teach the routine if it takes too long")

run_transition("2 claps", "stop, look, listen", 30)
```

## References

- [Positive Behavioral Interventions & Supports (PBIS)](https://www.pbis.org)
- [CASEL — SEL and classroom management](https://casel.org)
- [Edutopia — Classroom Management](https://www.edutopia.org/topic/classroom-management)
- [Center on Positive Behavioral Interventions and Supports — tiered framework](https://www.pbis.org/tiered-framework)
- [Harvard — Center on the Developing Child](https://developingchild.harvard.edu)
