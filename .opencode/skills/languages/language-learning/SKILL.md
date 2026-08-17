---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: language-learning
description: Learn languages with CEFR levels, spaced repetition, comprehensible input, and active recall
category: languages
version: 0.1.0
author: devtiagoabreu
tags: [language-learning, cefr, spaced-repetition, comprehensible-input, active-recall, vocabulary]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - A target language and 30-60 minutes of daily time
  - Access to graded input (podcasts, readers, or videos)
  - A flashcard app or spaced repetition schedule
provides:
  - CEFR level mapping and goal setting (A1-C2)
  - Spaced repetition scheduling for vocabulary
  - Comprehensible input routines for listening and reading
  - Active recall and speaking practice patterns
---

# Language Learning

## Overview

Language learning is a habit problem more than a talent problem. The most effective
methods share three ingredients: comprehensible input (listening and reading
slightly above your level), spaced repetition (reviewing vocabulary at growing
intervals), and active recall (pulling information out of memory instead of
re-reading it). The CEFR (Common European Framework of Reference) gives a clear
roadmap from A1 to C2 with measurable goals at each level.

This skill combines those ingredients into a daily routine you can run for months:
set a CEFR target, schedule reviews, consume input daily, and practice active
recall through speaking and writing. Consistency beats intensity.

## Prerequisites

- A clear target language and a reason to learn it
- 30-60 minutes per day, including 10 minutes of reviews
- A flashcard app (Anki, Quizlet, or similar)
- Graded materials: podcasts, graded readers, or native content with subtitles

## Usage Instructions

### Step 1: Set a CEFR Goal

Map where you are and where you want to go with the CEFR:

```
A1: basic phrases, introductions
A2: routine tasks, simple conversations
B1: describe experiences, handle travel situations
B2: argue, understand complex texts
C1: fluent and flexible use
C2: near-native comprehension
```

Set one level as a target and choose materials for the level just below it.

### Step 2: Build a Spaced Repetition Routine

Spaced repetition schedules reviews at growing intervals so memory becomes
long-term. Add new words every day and let the algorithm schedule reviews:

```json
{
  "intervalos": [1, 3, 7, 15, 30, 90],
  "novas_por_dia": 10,
  "revisoes_por_dia": 50,
  "regra": "acertou avança, errou recomeça"
}
```

Ten minutes of reviews daily beats two hours once a week.

### Step 3: Consume Comprehensible Input Daily

Input is where real language lives. Choose content you understand about 80% of:

```
Listening: podcasts and videos at your level, 20 min/day
Reading: graded readers and news, 15 min/day
Rule of thumb: if you need a dictionary on every line,
                the material is too hard for now
```

Understand the main idea first; look up words only when they block meaning.

### Step 4: Practice Active Recall

Passive recognition fades; producing the language cements it:

```
1. Cover the answer side of flashcards and say the word aloud
2. Write 3 sentences with each new word the same day
3. Shadow audio: repeat after the speaker with the same rhythm
4. Summarize a listened segment aloud or in writing
```

Speaking practice can happen alone at first; it still builds the skill.

### Step 5: Track Progress by CEFR Can-Dos

Measure progress with concrete can-do statements instead of vague feelings:

```
A2: "I can order food and ask for the bill"
B1: "I can describe my weekend plans"
B2: "I can discuss a news article and defend an opinion"
```

Record a short audio or writing sample monthly to see improvement.

### Step 6: Make It a Daily Loop

The routine only works if it fits your life. A minimum viable daily loop:

```
1. 10 min of spaced repetition reviews
2. 20 min of listening input (commute, chores, gym)
3. 10 min of reading or shadowing
4. 1-2 sentences written in a journal or chat
```

On busy days, keep only step 1 and the streak alive.

## Examples

### Example 1: 12-Week Plan to Reach B1

```text
Weeks 1-4:  podcasts at A2, 20 min/day + 10 words/day
Weeks 5-8:  graded reader + speaking shadowing
Weeks 9-12: news articles, journal entries, mock dialogue
```

### Example 2: Spaced Repetition Schedule in Code

```python
intervalos = [1, 3, 7, 15, 30, 90]

def proxima_revisao(acertos, hoje):
    indice = min(acertos, len(intervalos) - 1)
    return hoje + intervalos[indice]

print("Palavra 'casa':", proxima_revisao(2, "2026-08-08"))
```

### Example 3: Input Triage Decision

```text
Can I follow 80% of the audio?      -> keep listening
Can I read 3 pages without help?    -> keep reading
Do I stop to translate every word?  -> go easier, do not translate
Am I bored?                          -> raise the level one step
```

## References

- [Common European Framework of Reference (CEFR)](https://www.coe.int/en/web/common-european-framework-reference-languages)
- [Stephen Krashen – Comprehensible Input](https://www.sdkrashen.com)
- [Language Learning Spaced Repetition Agent Skill](https://github.com/dungnotnull/language-learning-spaced-repetition-agent-skill)
- [Anki – Spaced Repetition Software](https://apps.ankiweb.net)
