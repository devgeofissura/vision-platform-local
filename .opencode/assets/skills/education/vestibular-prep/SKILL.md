---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: vestibular-prep
description: Prepare students for Brazilian university entrance exams with ENEM, FUVEST, and VUNESP structures and study plans
category: education
version: 0.1.0
author: devtiagoabreu
tags: [vestibular, ENEM, FUVEST, VUNESP, redacao, study-planning, brazil, ensino-medio, college-prep]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - A student in the last years of ensino médio or a pre-vestibular course
  - The target exam (ENEM, FUVEST, VUNESP, or a mix)
  - Realistic study time (usually 1-4 hours per day)
  - Official documents and past exams from the exam boards
provides:
  - Exam structure breakdowns for ENEM, FUVEST, and VUNESP
  - A redação (essay) writing protocol aligned with ENEM's 5 competências
  - A weekly study plan template with time blocks
  - Simulado (mock exam) strategy and analysis guidance
---

# Vestibular Preparation (ENEM, FUVEST, VUNESP)

## Overview

Brazilian university entrance exams are high-stakes marathons with very
specific formats. ENEM is a national exam used by SISU for federal universities
and by many private programs. FUVEST is the entrance exam of the University of
São Paulo (USP). VUNESP is the foundation that runs admission exams for many
state universities in São Paulo, including the famous UNESP vestibular.

Each exam rewards different preparation:

```
ENEM:   180 objective questions over 2 days + redação (essay)
FUVEST: 90 questions over 2 phases, with a famous first phase and
        subject-specific second phase + redação
VUNESP: UNESP's exam has 90 questions, a redação, and sometimes
        second-phase discipline exams depending on the course
```

The winning strategy is the same for all three: know the format, master the
redação competências, and study with a plan based on your own weak points, not
on what is comfortable.

## Prerequisites

- Determine the target exam(s) before anything else
- Access to past exams (provas anteriores) from each board
- The official ENEM redação reference matrix (Matriz de Referência)
- A reliable place to study for at least 1 hour daily, 5-6 days a week

## Usage Instructions

### Step 1: Learn the Format of Your Target Exam

Study the exact structure so no question surprises you:

```
ENEM (2 days):
  Day 1: 45 Linguagens, 45 Ciências Humanas + redação (5h30)
  Day 2: 45 Matemática, 45 Ciências da Natureza (5h)
  Scoring: TRI (Item Response Theory) weights question quality, so
           consistency beats guessing; each area counts 1000 points
  Redação: 1 dissertativo-argumentativo text, scored 0-1000 by 5 competências

FUVEST:
  Phase 1: 90 questions of multiple choice, all disciplines (4h30)
  Phase 2: discipline-specific questions + redação, two days
  Score: each phase filtered; the redação is decisive in many courses

VUNESP (UNESP):
  90 objective questions in one day (4h30) covering all disciplines
  Redação on the same day for most courses
  Some courses add a second phase with subject exams
```

Check the official site of each board every year, because formats can change.

### Step 2: Master the ENEM Redação's 5 Competências

The ENEM redação is scored 0-200 per competência, totaling 1000. Teach and
practice each one explicitly:

```
C1: Portuguese language correctness (spelling, grammar, norms)
C2: Comprehend the proposal and write a dissertativo-argumentativo text
C3: Select, relate, and organize arguments with information and facts
C4: Use cohesion and connection mechanisms between sentences and paragraphs
C5: Propose an intervention (solução) respecting human rights, with agent,
    action, means, and purpose
```

A zero in any competência can void the essay. The classic winning structure:

```
Introdução (1 para): thesis + the problem stated
Desenvolvimento (2-3 paras): 2 arguments with data, authors, or events
Conclusão (1 para): proposal of intervention with agent, action, means,
                    and purpose (5 elements)
```

### Step 3: Build a Weekly Study Plan by Weak Points

The plan must come from your own diagnostic, not a generic schedule:

```
Diagnose: take 1 past exam (simulado) and list which subjects you lost
          the most points in; rank from worst to best
Prioritize: spend 50% of time on your 2 worst subjects, 30% on your
            strongest subjects (to keep them sharp), 20% on the redação
Time blocks: 25-50 minute study blocks with 5-10 minute breaks
Weekly rhythm:
  Mon-Fri: 2 blocks of content study + 1 block of questions
  Sat:    1 redação + 1 full review of the week's weak points
  Sun:    1 simulado or a full rest day (rest is part of the plan)
```

Use active study: solve questions and write, do not just re-read theory.

### Step 4: Train with Simulados and Analyze

Mock exams train pacing and reveal gaps:

```
Month 1-2: 1 simulado per month, untimed, to learn the format
Month 3-4: 1 simulado per month, timed, in exam conditions
Month 5+:  1 simulado every 2 weeks, timed, with full redação
After every simulado: correct everything, record errors by subject and
                     competência, and update the weak-point list
```

Time strategy differs by exam: in ENEM with TRI, answer what you know first,
return to hard questions, and never leave a question blank.

### Step 5: Track Redação Progress Against Competências

The redação is the highest-leverage skill because it weighs heavily:

```
Write 1 redação per week, timed (the ENEM gives 5h30 for both days, plan
about 1h-1h30 for the essay)
Have each essay scored by competência (teacher, course, or self-check with
the official matrix)
Keep a log: date, theme, score per competência, and 1 specific fix for next
week (e.g., "use more cohesive connectors", "add a data point to C3")
```

Target 900+ by focusing on the two competências you lose most points in.

### Step 6: Manage the Week of the Exam

The last week is for consolidation and rest, not new content:

```
Day -6 to -3: review your weak-point summaries, re-read your best redações
Day -2:       pack the materials (documento com foto, caneta preta de
              material transparente, água, lanche simples)
Day -1:       travel check to the location, sleep early, no new content
Exam day:     arrive 1h early, keep the redação structure card in memory
```

Never start studying new topics in the final week; confidence and rest beat a
cram on unfamiliar material.

## Examples

### Example 1: Weekly Study Plan Template

```markdown
# Week of [date] — Target: ENEM

Goal this week: Matemática (trigonometry) + redação C3 (argument data)

| Day     | Block 1 (50min)          | Block 2 (50min)       | Block 3 (25min)     |
|---------|--------------------------|-----------------------|---------------------|
| Mon     | Trigonometry theory      | 15 trig questions     | 10 Language questions |
| Tue     | Reading: argument texts  | Extract arguments     | 10 History questions  |
| Wed     | Redação C3 drill         | 15 math questions     | 10 Chemistry questions|
| Thu     | Trigonometry review      | 15 questions mixed    | Vocabulary log        |
| Fri     | Past ENEM math questions | Review errors         | 10 Geography questions|
| Sat     | Full redação (timed)     | Self-score 5 competências | Light review       |
| Sun     | Rest                     | Rest                  | Rest                  |
```

### Example 2: ENEM Redação Outline Generator

```markdown
Tema: [write the proposal topic]

Introdução: context (1-2 lines) + thesis (1 line) + problem statement
  - Context: [current event, data, or historical reference]
  - Thesis:  [the position you will defend]

Desenvolvimento 1 (argument 1): 
  - Claim:   [idea that supports the thesis]
  - Evidence: [data, author, law, or event]
  - Link:    [connect the evidence to the thesis]

Desenvolvimento 2 (argument 2):
  - Claim:   [second supporting idea]
  - Evidence: [different kind of evidence]
  - Link:    [connect to thesis]

Conclusão (proposal of intervention):
  - Agent:   [who acts, e.g., government, school, society]
  - Action:  [what exactly they do]
  - Means:   [how they do it]
  - Purpose: [what they achieve]
  - Rights:  [respecting human rights, stated implicitly]
```

### Example 3: Study Planner Score Tracker

```python
from collections import defaultdict

def make_tracker():
    return {"subjects": defaultdict(float), "redacao": {"C1": 0, "C2": 0,
            "C3": 0, "C4": 0, "C5": 0}}

def record_errors(tracker, subject, lost_points):
    tracker["subjects"][subject] += lost_points

def log_redacao(tracker, c_scores):
    for c, score in c_scores.items():
        tracker["redacao"][c] = score

t = make_tracker()
record_errors(t, "Matemática", 12)
log_redacao(t, {"C1": 160, "C2": 180, "C3": 120, "C4": 160, "C5": 180})
print("Weakest subjects:", sorted(t["subjects"], key=t["subjects"].get))
print("Total redação:", sum(t["redacao"].values()))
```

## References

- [INEP — ENEM official information](https://www.gov.br/inep)
- [Ministério da Educação (MEC)](https://www.gov.br/mec)
- [FUVEST — entrance exam of USP](https://www.fuvest.br)
- [VUNESP — vestibular and exam foundation](https://www.vunesp.com.br)
- [SISU — Sistema de Seleção Unificada](https://sisu.mec.gov.br)
