---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: literacy-teaching
description: Teach literacy with the alphabetic principle, phonemic awareness, and adult literacy contexts
category: education
version: 0.1.0
author: devtiagoabreu
tags: [literacy, teaching, phonics, phonemic-awareness, alphabetic-principle, adult-literacy, EJA]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - A learner (child or adult) beginning to read and write
  - Assessment of the learner's current literacy level
  - Daily sessions of 30-60 minutes
provides:
  - Alphabetic principle teaching sequences
  - Phonemic awareness activity frameworks
  - Adult literacy lesson plans with real-life themes
  - Assessment and progress tracking methods
---

# Literacy Teaching

## Overview

Literacy teaching turns spoken language into written language. The strongest
foundation is the alphabetic principle: written letters represent speech sounds in
a predictable way. Learners need phonemic awareness (hearing the individual sounds
in words), explicit phonics (linking letters to those sounds), and plenty of
practice decoding and reading real texts. Adult learners also need content grounded
in their lives, work, and community, following the critical tradition of educators
like Paulo Freire.

This skill covers the sequence from phonemic awareness to fluent reading, and how
to adapt the same principles to adults and to children. Assessment comes first:
understand where the learner is, then teach the next small step.

## Prerequisites

- A learner ready to start literacy work
- A diagnostic of the learner's current level (letter knowledge, phoneme
  awareness, writing level)
- Simple materials: letters, word cards, short texts, paper
- 30-60 minutes per session, 3-5 days per week

## Usage Instructions

### Step 1: Assess the Starting Level

Before teaching, find out what the learner already knows:

```
1. Can they identify letter names and sounds?
2. Can they isolate the first sound of a word?
3. How do they write a simple word like "casa"?
4. Can they read any short word or sentence aloud?
```

Use the results to choose the first teaching step.

### Step 2: Develop Phonemic Awareness

Phonemic awareness is hearing sounds in words, without letters yet:

```
Rhyme: which words rhyme with "sol"? (sol, gol, farol)
First sound: what sound does "mão" start with? (/m/)
Counting: how many sounds in "pé"? (2: /p/ and /e/)
Blending: /c/ + /a/ + /s/ + /a/ -> "casa"
```

Play these as games before and alongside letter teaching.

### Step 3: Teach the Alphabetic Principle

Connect sounds to letters explicitly, a few per week, always with words:

```
Week 1: m, a -> "ma", "am", "mama"
Week 2: s, p -> "sapo", "pia"
Week 3: l, o -> "lua", "sol"
Pattern: sound, letter, syllable, word, sentence
```

Use the learner's own speech sounds as the starting point for letters.

### Step 4: Build Decoding and Writing

Move from sounding out to automatic word reading and spelling:

```
Decoding: /s/ /o/ /l/ -> "sol"
Writing: say the word slowly, write the sounds heard
Dictation: teacher says a word, learner writes it
Reading: short sentences using words already mastered
```

Write daily, even one or two words, to reinforce the sound-letter link.

### Step 5: Adapt to Adult Learners

Adults learn literacy through meaning and dignity. Center the lessons on their
reality, following the Freirean principle of reading the world before reading the
word:

```
Theme: work, land, home, rights, money
Generative words: words from their own vocabulary
Dialogues: start from what learners already know and say
Purpose: reading contracts, medicine labels, children's notes
```

Never make an adult feel childish; start from their knowledge and experience.

### Step 6: Assess Progress Continuously

Track learning to plan the next step and celebrate growth:

```
Weekly: can the learner read 5 new words? write them?
Monthly: read a short text and answer simple questions
Keep a learner portfolio of writing samples and dictations
```

Assessment is formative: it tells the teacher what to teach next, not whether the
learner is "good" or "bad".

## Examples

### Example 1: Weekly Sequence for Early Child Literacy

```text
Monday:   phoneme games (first sound isolation)
Tuesday:  letters m, a + word building "mama"
Wednesday:decode "sapo", "pia" with new letters s, p
Thursday: dictation of known words
Friday:   read a short text and draw its meaning
```

### Example 2: Adult Literacy Lesson on a Generative Word

```yaml
tema: trabalho
palavra: TRABALHO
fluxo:
  - conversa sobre o trabalho dos participantes
  - leitura da palavra em cartaz
  - decomposição em sílabas e fonemas
  - formação de novas palavras com as famílias silábicas
  - leitura de texto coletivo produzido pelo grupo
```

### Example 3: Track Writing Level

```python
niveis = ["pré-silábico", "silábico", "silábico-alfabético", "alfabético"]

def registrar_escrita(palavra):
    if palavra == "casa":
        return "alfabético"
    if len(palavra) == 2:
        return "silábico"
    return "silábico-alfabético"

print("Nível:", registrar_escrita("csa"))
```

## References

- [Ministério da Educação – Alfabetização](https://www.gov.br/mec)
- [UNESCO – Literacy](https://www.unesco.org)
- [National Institute for Literacy (NIFL)](https://lines.ed.gov)
- [The Reading League](https://www.thereadingleague.org)
