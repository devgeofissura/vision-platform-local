---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: assessment-and-feedback
description: Design formative and summative assessment, build rubrics, and run effective feedback loops
category: education
version: 0.1.0
author: devtiagoabreu
tags: [assessment, feedback, formative, summative, rubrics, grading, feedback-loops, teaching]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - A learning objective or standard to assess
  - Learners who will receive the assessment
  - A way to record results (gradebook, sheet, or tracker)
  - Time to review and return work promptly
provides:
  - Formative and summative assessment design guidance
  - Rubric building templates and examples
  - A feedback loop protocol for learning cycles
  - Grading and analysis checklists
---

# Assessment and Feedback

## Overview

Assessment is the process of collecting evidence of learning, and feedback is
how that evidence travels back to the learner. Formative assessment happens
during learning and drives the next teaching decision; summative assessment
judges learning after the fact. Rubrics make judgments transparent, and
feedback loops turn single grades into cycles of try, receive, revise.

The highest-impact feedback is specific, timely, and focused on the task, not
the person. Generic "good work" changes nothing. A grade without a comment is a
score, not feedback.

This skill covers how to design both assessment types, how to build rubrics that
students can actually use, and how to run feedback loops that end in improvement.

## Prerequisites

- At least one clear learning objective (see the lesson-planning skill)
- A class or set of learners being assessed
- A simple record-keeping tool (paper gradebook, spreadsheet, or LMS)
- A turnaround commitment (return work within one week, ideally less)

## Usage Instructions

### Step 1: Plan Formative Assessment Continuously

Formative assessment happens often, is low-stakes, and its only job is to tell
you and the learner what to do next:

```
During the lesson:  thumbs up/down, cold calls, mini-whiteboards
End of the lesson:  exit tickets with one key question
Between lessons:    short quizzes, one-minute essays, misconception checks
```

Ask two questions after each formative check: "Who has not learned this yet?"
and "What do they need next?" Use the answer to adjust your next session.

### Step 2: Design Summative Assessment Aligned to Objectives

Summative assessment samples the full objective, at the same cognitive level:

```
Match: recall objectives get recall items; explain objectives get
explain tasks; apply objectives get performance tasks
Blueprint: map every item or task to the objective it measures
Coverage: check the assessment actually tests all stated objectives
Fairness: allow all learners to show the learning (clear language, time)
```

Write the rubric or answer key at the same time you write the test, and review
both against the objective list.

### Step 3: Build Rubrics That Learners Can Use

A good rubric names levels of performance with observable descriptors. Use four
levels and criteria that match your objectives:

```
Levels:     1 (not yet) -> 2 (developing) -> 3 (proficient) -> 4 (exemplary)
Criteria:   one row per skill the task requires (e.g., thesis, evidence,
            organization, language)
Descriptors: describe what the work looks like at each level, concretely
```

Give the rubric to learners before they start the task, and use it when giving
feedback so comments match the criteria. This turns the rubric into a learning
tool, not just a grading tool.

### Step 4: Deliver Feedback That Moves the Learner Forward

Feedback should answer three questions for the learner:

```
Where am I going?      (the target, from the rubric)
How am I doing?        (what the work shows, against criteria)
What is the next step? (one specific action to improve)
```

Write feedback as specific, actionable comments tied to criteria. Limit the
number of comments per piece (2-3 priorities) so the learner can act on them.

### Step 5: Close the Loop with Revision Cycles

Feedback that never returns to the learner is wasted. Build revision into the
cycle:

```
Round 1: learner submits draft
Round 2: teacher gives 2-3 rubric-based comments (no grade yet)
Round 3: learner revises and resubmits
Round 4: teacher grades the improved version
```

The grade rewards the growth, and the learner experiences improvement as a
skill, not a talent.

### Step 6: Analyze Results to Improve Teaching

Assessment data has a second job: improving instruction.

```
Error patterns: which items failed, and why? (gap, confusion, wording?)
Class trends:   which objectives need re-teaching, and to whom?
Teaching moves: adjust pacing, method, or examples for the next cycle
Item quality:   drop or fix items nobody understood
```

Review the same data after the unit to confirm the fixes worked.

## Examples

### Example 1: Exit Ticket Design

```markdown
# Exit Ticket — "Why does the shadow move?"

1. Draw the sun, the object, and the shadow at 9am and at 3pm.
2. Write one sentence: what makes the shadow change?

Use:
- 3 who draw both correctly: ready for the summative task
- 5 who only draw one: small-group re-teach with a flashlight
- 2 who draw nothing: individual support with a concrete model
```

### Example 2: Four-Level Rubric for an Explanatory Essay

```markdown
| Criterion | 1 Not yet | 2 Developing | 3 Proficient | 4 Exemplary |
|-----------|-----------|--------------|--------------|-------------|
| Thesis    | missing   | vague        | clear claim  | clear, nuanced claim |
| Evidence  | none      | one weak example | 2+ relevant examples | varied, well-chosen evidence |
| Organization | confusing | partly ordered | logical sequence | cohesive, purposeful flow |
| Mechanics | errors block meaning | some errors | few errors | polished, no blocking errors |
```

### Example 3: Feedback Comment Builder

```python
def feedback(target, current, next_step):
    return (
        f"Target: {target}\n"
        f"You are: {current}\n"
        f"Next: {next_step}\n"
    )

print(feedback(
    "a clear claim supported by two examples",
    "your claim is stated, but the examples are not connected",
    "add one sentence linking each example to your claim",
))
```

## References

- [National Center for the Improvement of Educational Assessment](https://www.nciea.org)
- [Dylan Wiliam — Formative assessment](https://www.dylanwiliam.org)
- [John Hattie — Visible Learning on feedback](https://visible-learning.org/2016/06/john-hattie-feedback-to-learners-better-than-anyone/)
- [Cornell — Center for Teaching Innovation on rubrics](https://teaching.cornell.edu/teaching-resources/assessment-evaluation/rubric-design)
- [Edutopia — Assessment](https://www.edutopia.org/topic/assessment)
