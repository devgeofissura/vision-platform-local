---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: evidence-based-teaching
description: Apply research-backed teaching practices and interpret effect sizes to decide what to do in class
category: education
version: 0.1.0
author: devtiagoabreu
tags: [evidence-based-teaching, research, effect-sizes, teaching, retrieval-practice, education-science, hattie]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - A willingness to compare your current practice with research findings
  - Access to research summaries (The Learning Scientists, Meta-Analysis)
  - A class where you can try one practice at a time
  - A simple way to measure outcomes before and after
provides:
  - A ranked guide to high-impact teaching practices
  - Effect size interpretation guidance
  - A single-practice trial protocol
  - Research literacy tools for reading studies
---

# Evidence-Based Teaching

## Overview

Evidence-based teaching means choosing practices because research shows they
work, not because they are fashionable or familiar. The field of education
synthesizes hundreds of studies into effect sizes: a number that says how much a
practice moves learning forward. Practices like retrieval practice, spaced
practice, worked examples, and feedback consistently outperform lectures and
re-reading.

Use a simple rule of thumb for effect sizes:

```
Effect size 0.00-0.19:  weak or negligible effect
Effect size 0.20-0.39:  small but noticeable
Effect size 0.40-0.59:  medium, worth serious attention
Effect size 0.60+:      large, adopt if feasible
```

This skill gives you the highest-impact practices, how to read the numbers, and
a trial protocol so you can test one practice in your own classroom and measure
whether it works for your students.

## Prerequisites

- A topic or skill you teach regularly
- A class group you can observe before and after a change
- Access to research summaries (the references in this skill)
- Discipline to change one practice at a time

## Usage Instructions

### Step 1: Know the High-Impact Practices

These practices have consistent, large-to-medium effects across meta-analyses:

```
Retrieval practice:   test recall frequently; d = 0.5-0.7
Spaced practice:      review on expanding intervals; d = 0.6+
Worked examples:      show solved examples before practice; d = 0.5
Feedback:             task-focused, specific comments; d = 0.7
Teacher clarity:      explicit objectives and explanations; d = 0.75
Metacognitive prompts:ask students to plan, monitor, evaluate; d = 0.6
```

Prefer combinations that reinforce each other, such as retrieval followed by
feedback.

### Step 2: Read Effect Sizes Correctly

An effect size is not a guarantee; it is an average across studies.

```
Read the source: meta-analysis is stronger than a single small study
Check the context: who were the learners, what was the subject?
Compare to a baseline: an effect of 0.4 means improvement relative to
                       business as usual
Ask about cost: two practices with d = 0.4 may have very different effort
```

A practice with a smaller effect but trivial cost (like a quick retrieval quiz)
can be worth more in practice than a large-effect practice that needs huge
training.

### Step 3: Trial One Practice at a Time

Test changes like a scientist, not a fashion-follower:

```
Baseline (2 weeks):   teach as usual, record a simple measure (quiz scores,
                      completion rates, time on task)
Intervention (4 weeks): add ONE practice, e.g., a 5-minute retrieval quiz
                       at the start of every lesson
Measurement (weekly):  keep the same measure, record weekly
Compare:               did the measure improve? by how much?
```

Keep the same class and the same content type so the comparison is fair. If the
improvement is meaningful, keep the practice; if not, adjust or try another.

### Step 4: Embed Retrieval and Spacing First

These two are the cheapest high-effect changes:

```
Retrieval: 5-minute start-of-lesson quiz on last week's content, no grade
Spacing:    return to topics on days 1, 7, and 21 (see teaching-methods)
Mixing:     interleave different topics in the same review quiz
```

Retrieval causes the learning; it is not just a check. Let students see that
"forgetting then recalling" builds memory.

### Step 5: Use Worked Examples Before Independent Practice

Do not send students to practice before they have seen how the task is done:

```
Example 1: fully solved, teacher explains the thinking
Example 2: partially solved, students complete the missing step
Example 3: students solve a similar problem with support
Then:      independent practice
```

Fading the help step by step builds confidence and reduces early error rates.

### Step 6: Build Research Literacy

Evaluate new claims before adopting them:

```
Ask: who ran the study, with how many students, for how long?
Ask: was there a control group and random assignment?
Ask: what does the effect size really measure?
Prefer: systematic reviews and meta-analyses over single testimonials
```

Use respected sources that translate research into practice, and always
interpret results for your own students.

## Examples

### Example 1: Effect Size Decision Sheet

```markdown
| Practice          | Effect size | Cost in class time | Verdict        |
|-------------------|-------------|--------------------|----------------|
| Retrieval quiz    | 0.50        | 5 min per lesson   | adopt now      |
| Spaced review     | 0.60        | 5 min per week     | adopt now      |
| Worked examples   | 0.50        | replaces some practice | adopt now  |
| Learning styles   | ~0.10       | moderate           | drop           |
| Re-reading notes  | ~0.20       | low                | replace with retrieval |
```

### Example 2: Six-Week Trial Protocol

```yaml
goal: "Improve retention of vocabulary from week to week"
baseline:
  weeks: 2
  measure: "average score on Monday vocabulary quiz"
intervention:
  weeks: 4
  practice: "start every lesson with a 5-min retrieval quiz (old words)"
  materials: "printed 10-item quiz per lesson"
measurement:
  weekly: "record quiz average and completion rate"
decision:
  keep: "if the weekly average rises by 15% or more"
  adjust: "otherwise vary the quiz format and try again"
```

### Example 3: Effect Size Calculation from Your Own Data

```python
import statistics

def effect_size(pre, post):
    mean_diff = statistics.mean(post) - statistics.mean(pre)
    pooled_sd = statistics.pstdev(pre + post) or 1
    return round(mean_diff / pooled_sd, 2)

before = [62, 64, 60, 65, 61]
after = [70, 74, 72, 71, 76]
print("Observed effect size:", effect_size(before, after))
```

## References

- [Visible Learning — John Hattie effect size list](https://visible-learning.org/hattie-ranking-influences-effect-sizes-learning-achievement/)
- [The Learning Scientists — retrieval and spacing research](https://www.learningscientists.org)
- [Education Endowment Foundation — teaching and learning toolkit](https://educationendowmentfoundation.org.uk/education-evidence/teaching-learning-toolkit)
- [education-agent-skills — Gareth Manning](https://github.com/GarethManning/education-agent-skills)
- [IES What Works Clearinghouse](https://ies.ed.gov/ncee/wwc)
