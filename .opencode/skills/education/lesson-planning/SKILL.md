---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: lesson-planning
description: Plan lessons with backward design, measurable objectives, aligned assessments, and differentiation
category: education
version: 0.1.0
author: devtiagoabreu
tags: [lesson-planning, backward-design, objectives, assessment, differentiation, curriculum, pedagogy, planning]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - A defined topic, standard, or unit of study
  - Knowledge of the learners' current level
  - The class schedule (minutes per session, days per week)
  - Access to curriculum or standards documents
provides:
  - A backward design planning template
  - Measurable objective writing guidance
  - Assessment alignment checklists
  - Differentiation strategies for diverse learners
---

# Lesson Planning with Backward Design

## Overview

Lesson planning is the bridge between curriculum and classroom reality. The
backward design model (Wiggins and McTighe) starts with the end in mind: decide
what learners must know and do, design evidence that proves it, then plan the
activities that move learners from where they are to where they need to be.

The three stages are always the same order:

```
Stage 1: Identify desired results (objectives)
Stage 2: Determine acceptable evidence (assessments)
Stage 3: Plan learning experiences (activities)
```

Planning backward prevents the common trap of picking fun activities first and
only later discovering they teach nothing. This skill gives you a complete
template, objective formulas, alignment checks, and differentiation options so
your plans are concrete, measurable, and inclusive.

## Prerequisites

- A topic, standard, or learning outcome assigned to you
- A realistic sense of the learners' current knowledge
- The length and frequency of your class sessions
- Optional but useful: a copy of your curriculum map or standards list

## Usage Instructions

### Step 1: Write Measurable Objectives

Start by defining what a successful learner will know or do by the end. Use the
behavior-condition-criterion formula:

```
Verb (observable) + Content (what) + Condition (how) + Criterion (how well)

Example: After a 20-minute reading of "A Gotinha Viajante" (condition),
students will list (verb) at least three stages of the water cycle (content)
with 100% accuracy (criterion).
```

Avoid vague verbs like "understand" or "appreciate". Prefer: identify, list,
compare, explain, solve, demonstrate, construct, predict. Write one objective per
lesson, or a maximum of three for a double period.

### Step 2: Design Assessments Backward

Before choosing activities, decide the evidence. You need at least two sources:

```
Formative evidence: cold-call questions, exit tickets, mini-quizzes
Summative evidence: performance task, project, test, or written product

Ask: "If I had to grade this objective today, what would the learner hand me?"
```

Design the assessment at the same cognitive level as the objective. If the
objective says "explain," do not assess with only multiple-choice recall. A
well-aligned assessment can be pre-designed and shown to students as the
"big picture" target.

### Step 3: Plan Activities in a Logical Sequence

Build the lesson in phases that move from teacher modeling to independent
practice:

```
Warm-up (5 min):       activate prior knowledge, connect to today
Input (10 min):        teacher models or presents the key idea
Guided practice (15):  students try it with teacher support
Independent work (15): students apply it alone or in pairs
Closure (5 min):       check for understanding, preview next step
```

Each activity must map to the objective. If an activity does not move learners
toward the objective, cut it, however fun it is.

### Step 4: Plan Differentiation

One lesson, many entry points. Plan for the edges, not just the middle:

```
Support (struggling):  sentence frames, partner work, step-by-step checklists,
                       more time, visuals, native-language glossary
Extension (advanced):  open-ended prompts, leadership roles, deeper questions,
                       extra data or reading, mentor other students
Access (all):          clear instructions, wait time, choice of product
```

Write your differentiation into the plan before class, so it is deliberate
rather than improvised.

### Step 5: Write the Timing and Materials

Give every phase a realistic time budget and list every material. If the lesson
needs scissors, slides, a video, or printed texts, list them explicitly.

```
Materials: printed text, whiteboard markers, exit-ticket slips, timer,
           sentence-frame poster, 3 extra copies for late joiners
Timing note: total must equal the period length; plan 10% buffer
```

A complete plan fits one page and can be executed by another teacher without
asking you anything.

### Step 6: Close the Loop After the Lesson

Planning does not end at the bell. Note what worked and what did not:

```
Did learners meet the objective? What evidence shows it?
Which students need follow-up? Which need extension?
What will I do differently tomorrow?
```

Store these notes with the lesson so next year's plan starts from evidence, not
from memory.

## Examples

### Example 1: Completed One-Page Lesson Plan

```markdown
# Lesson Plan — The Water Cycle (grade 4)

Objective: After a 20-minute guided reading (condition), students will list
(verb) three stages of the water cycle (content) with 100% accuracy (criterion).

Stage 1 — Desired results: stages of the water cycle; evaporation, condensation,
precipitation; vocabulary in Portuguese and English.

Stage 2 — Evidence:
- Formative: exit ticket "name one stage and one example"
- Summative: labeled diagram of the cycle with all three stages

Stage 3 — Activities:
- Warm-up (5): brainstorm where rain comes from; record answers
- Input (10): read "A Gotinha Viajante"; model labeling stages
- Guided (15): pairs label a diagram; teacher circulates
- Independent (15): students draw and label their own cycle
- Closure (5): exit ticket + share one new fact

Differentiation:
- Support: sentence frames ("The water ... and becomes ...")
- Extension: write a short story from the droplet's point of view
- Materials: text, diagrams, colored pencils, exit slips

After-class notes:
- 3 students confused evaporation vs condensation; re-teach with a kettle demo.
```

### Example 2: Objective Alignment Checklist

```python
objectives = [
    {"objective": "Students will understand photosynthesis", "verb": "understand"},
    {"objective": "Students will list the inputs of photosynthesis", "verb": "list"},
    {"objective": "Students will explain why plants need sunlight", "verb": "explain"},
]

weak_verbs = {"understand", "know", "appreciate", "learn", "realize"}
for item in objectives:
    verb = item["verb"].lower()
    status = "REWRITE" if verb in weak_verbs else "OK"
    print(f"{status}: {item['objective']}")
```

### Example 3: Backward Design One-Line Template

```text
Objective -> Evidence -> Activity 1 -> Activity 2 -> Activity 3 -> Closure

Objective: [verb + content + condition + criterion]
Evidence:  [what students hand me]
Activity 1: [warm-up connecting to prior knowledge]
Activity 2: [teacher input and modeling]
Activity 3: [guided then independent practice]
Closure:   [quick check for understanding]
Differentiation: [support + extension + access]
Materials: [everything needed, listed]
```

## References

- [ASCD — Understanding by Design framework](https://www.ascd.org/el/articles/backward-design-the-basics)
- [Vanderbilt University — Backward Design](https://cft.vanderbilt.edu/guides-sub-pages/understanding-by-design/)
- [Edutopia — Lesson Planning articles](https://www.edutopia.org/topic/lesson-planning)
- [TeachThought — Objectives and assessment alignment](https://www.teachthought.com/pedagogy/backward-design/)
- [OECD — Teaching and learning resources](https://www.oecd.org/en/topics/teaching-and-learning.html)
