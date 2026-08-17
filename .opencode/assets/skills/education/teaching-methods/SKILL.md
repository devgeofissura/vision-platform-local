---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: teaching-methods
description: Apply core pedagogical methods from direct instruction to flipped classrooms and spaced practice
category: education
version: 0.1.0
author: devtiagoabreu
tags: [teaching-methods, pedagogy, direct-instruction, cooperative-learning, inquiry-based, flipped-classroom, spaced-practice]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - A topic or content unit to teach
  - A sense of the learners' prior knowledge
  - Class time and available technology
  - Willingness to match method to learning goal
provides:
  - A decision guide for choosing a teaching method
  - Protocols for five core pedagogical methods
  - Classroom sequences for each method
  - Common pitfalls and how to avoid them
---

# Teaching Methods

## Overview

No single method teaches everything. Direct instruction is best when learners
need a clear skill or procedure. Cooperative learning builds communication and
shared responsibility. Inquiry-based learning develops curiosity and
investigation skills. The flipped classroom moves direct teaching to homework so
class time is active. Spaced practice combats forgetting by returning to content
at growing intervals.

The professional move is to choose the method that matches the objective, not to
have one favorite. This skill gives you a simple decision rule and a practical
protocol for each of the five core methods, with timings and pitfalls.

```
Decision rule:
Needs a new skill or fact?  -> direct instruction
Needs discussion and depth? -> cooperative learning
Needs a question to answer? -> inquiry-based learning
Needs practice with support?-> flipped classroom
Needs long-term retention?  -> spaced practice
```

## Prerequisites

- A topic you know well enough to anticipate questions
- A clear idea of the learning objective (see lesson-planning skill)
- Basic class routines already established
- Technology access if you plan a flipped classroom

## Usage Instructions

### Step 1: Choose the Method by Objective

Match the method to what learners must be able to do:

```
Goal "recall or perform"      -> direct instruction
Goal "explain or collaborate" -> cooperative learning
Goal "investigate or create"  -> inquiry-based learning
Goal "apply with limited time"-> flipped classroom
Goal "retain over weeks"      -> spaced practice
```

If unsure, combine methods: direct instruction for the core concept, then
cooperative practice, then spaced retrieval in later lessons.

### Step 2: Use Direct Instruction for New Skills

Direct instruction is not lecture-only. It uses a fast cycle of model, guided,
independent:

```
I do:   model the task with think-aloud (5 min)
We do:  guided practice with immediate feedback (10 min)
You do: independent practice with a mastery check (10 min)
```

Keep explanations short, give worked examples, and check for understanding
every few minutes with quick questions.

### Step 3: Use Cooperative Learning for Depth

Cooperative learning requires positive interdependence: learners cannot finish
alone. Use structures with clear roles and a group product:

```
Jigsaw:      each expert teaches their piece to the group
Think-pair-share: think alone, discuss in pairs, share to the class
Group roles: leader, recorder, timekeeper, reporter
Success criteria: group product plus individual check
```

Assign roles explicitly, give each role a script, and end with an individual
assessment so no one hides in the group.

### Step 4: Use Inquiry-Based Learning for Questions

Inquiry starts from a question learners genuinely want to answer:

```
Hook:       present a surprising phenomenon or question (5 min)
Investigate:students gather data, experiment, or read (20 min)
Construct:  groups build an explanation (10 min)
Reflect:    share explanations, compare with the scientific answer (10 min)
```

The teacher is a facilitator: prompt with questions, never hand out the answer
too early. Provide scaffolds like observation sheets and question starters.

### Step 5: Use the Flipped Classroom for Practice Time

The flipped classroom gives direct instruction as homework and uses class time
for active practice:

```
At home:  learners watch a 5-10 minute video or read a short text, and answer
          2-3 comprehension questions
In class: entrance quiz on the video, then problem-solving, labs, or projects
          with the teacher available to coach
```

Protect the model: the homework must be short, the entrance quiz quick, and the
class activity genuinely active. If learners arrive unprepared, run the practice
in pairs so they can still participate.

### Step 6: Use Spaced Practice for Retention

Spaced practice returns to content on an expanding schedule and uses retrieval
instead of re-reading:

```
Day 1:  teach the content
Day 2:  quick retrieval quiz (5 min)
Day 7:  retrieval + application question
Day 21: cumulative review mixing old and new
```

Every return is a test, not a re-lecture. Retrieval practice (recalling from
memory) is far more effective for long-term memory than re-reading notes.

## Examples

### Example 1: Method Selection Table

```text
Objective                        Method              Why
Solve a two-step equation        direct instruction  clear procedure to model
Compare two historical accounts  cooperative         discussion and synthesis
Design a fair experiment         inquiry-based       open question to answer
Practice 20 physics problems     flipped classroom   more coaching time
Remember vocabulary in 1 month   spaced practice     retrieval beats re-reading
```

### Example 2: Flipped Classroom Lesson Script

```yaml
homework_video: "How a bill becomes a law (6 minutes)"
homework_questions:
  - "What are the three main stages?"
  - "Where can a bill be blocked?"
entrance_quiz: "4 multiple-choice items on the video, graded instantly"
class_activities:
  - "Pairs simulate a bill passing through two houses (15 min)"
  - "Groups identify where a real law got stuck (15 min)"
  - "Whole class: what slows a bill down? (10 min)"
teacher_role: "circulate, coach, collect misconceptions"
follow_up: "1 retrieval question on the bill process next week"
```

### Example 3: Spaced Practice Schedule Generator

```python
import datetime

def spaced_schedule(lesson_date, intervals_days=(1, 7, 21)):
    d = datetime.date.fromisoformat(lesson_date)
    return [str(d + datetime.timedelta(days=i)) for i in intervals_days]

print("Review dates:", spaced_schedule("2026-08-10"))
```

## References

- [Rosenshine's Principles of Instruction — American Educator](https://www.aft.org/sites/default/files/Rosenshine.pdf)
- [Visible Learning — John Hattie](https://visible-learning.org/hattie-ranking-influences-effect-sizes-learning-achievement/)
- [The Learning Scientists — retrieval and spacing](https://www.learningscientists.org)
- [Edutopia — Cooperative Learning strategies](https://www.edutopia.org/topic/cooperative-learning)
- [Center for Teaching Vanderbilt — Flipped classroom](https://cft.vanderbilt.edu/guides-sub-pages/flipping-the-classroom/)
- [inquirED — Inquiry-based learning](https://www.inquired.org)
