---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: personal-training
description: Design training programs with the FITT principle, safe progression, warm-up and cool-down, and health screening.
category: sports
version: 0.1.0
author: devtiagoabreu
tags: [training, fitness, fitt, progression, programming]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Basic exercise terminology (sets, reps, cadence)
  - Understanding of effort scales such as RPE
  - Safety awareness and pre-participation screening basics
provides:
  - Program design using the FITT principle
  - Progressive overload planning with safe increments
  - Warm-up, cool-down, and session structure templates
  - Health screening and referral guidance
---

# Personal Training

## Overview

This skill covers the fundamentals of designing exercise programs
aligned with NSCA and ACSM standards: applying the FITT principle
(frequency, intensity, time, type), structuring sessions with warm-up,
main part, and cool-down, and progressing loads safely. It also covers
pre-participation screening so users start at an appropriate level.

This skill is educational. It does not diagnose injuries or medical
conditions. When a user reports pain, cardiovascular disease, recent
injury, or high-risk pregnancy, refer them to a physician or licensed
health professional before recommending exercise.

## Prerequisites

- Familiarity with basic exercise terminology
- Knowledge of effort scales (RPE, talk test)
- Understanding of the safety limits of remote guidance
- Access to NSCA or ACSM resources for deeper reference

## Usage Instructions

### 1. Apply the FITT principle

Adjust each variable to the user's goal and level.

```text
Frequency:  sessions per week (e.g., 2-3 for beginners)
Intensity:  effort level and load (e.g., RPE 5-7)
Time:       session duration (e.g., 40-50 minutes)
Type:       exercise selection (strength, cardio, mobility)
```

### 2. Design a session structure

Every session needs a warm-up, a main part, and a cool-down.

```text
Warm-up:     5-10 minutes of mobility and light activation
Main part:   exercises with sets, reps, and rest
Cool-down:   5 minutes of light activity and stretching
```

### 3. Plan progression safely

Increase load only when technique is consistent.

```text
Rule of thumb for beginners
- Start with 2-3 sets of 10-12 reps
- Add one rep per session when the last set is easy
- Increase load only after reaching the upper rep target
- Progress one variable at a time
```

### 4. Screen before starting

Collect basic health information and identify red flags.

```json
{
  "questions": [
    "Has a doctor ever said you have a heart condition?",
    "Do you feel chest pain during physical activity?",
    "Do you have joint problems that limit exercise?",
    "Do you take medication for blood pressure or the heart?"
  ],
  "red_flags": ["chest pain", "unexplained dizziness", "recent injury"],
  "action": "Refer to a physician when any red flag is present"
}
```

### 5. Choose exercises by level

Prefer bodyweight and controlled movements for beginners.

```text
Beginner:      bodyweight squat, push-up on bench, band row
Intermediate:  added load, single-leg variations
Advanced:      compound lifts, power and conditioning
```

## Examples

### Example 1: Beginner weekly program

```markdown
# Beginner Program (3 days per week)

## Day A - Strength
1. Bodyweight squat: 3 x 10-12
2. Push-up (on bench): 3 x 6-10
3. Band row: 3 x 10-12
4. Plank: 3 x 20-30s

## Day B - Strength
1. Reverse lunge: 3 x 8-10 per leg
2. Shoulder press (light): 3 x 8-12
3. Glute bridge: 3 x 12-15
4. Dead bug: 3 x 8 per side

## Day C - Conditioning
- 20 minutes moderate pace, effort 5-7 of 10
- Progress by 5 minutes per week as tolerated
```

### Example 2: Program data structure

```json
{
  "program": "beginner-strength",
  "days": [
    {
      "name": "Day A",
      "warmup_min": 10,
      "exercises": [
        { "name": "Squat", "sets": 3, "reps": "10-12", "rest_s": 90 },
        { "name": "Push-up", "sets": 3, "reps": "6-10", "rest_s": 90 }
      ],
      "cooldown_min": 5
    }
  ],
  "progression": "Add a rep per session; increase load at upper target",
  "safety_note": "Stop on sharp pain and consult a professional"
}
```

## References

- [NSCA — National Strength and Conditioning Association](https://www.nsca.com/)
- [ACSM — Guidelines for Exercise Testing and Prescription](https://www.acsm.org/education-resources/books/guidelines-for-exercise-testing-and-prescription)
- [WHO — Physical Activity Fact Sheet](https://www.who.int/news-room/fact-sheets/detail/physical-activity)
