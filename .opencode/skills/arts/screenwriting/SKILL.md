---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: screenwriting
description: Screenwriting covering three-act structure, the Save the Cat beat sheet, character arcs and dialogue
category: arts
version: 0.1.0
author: devtiagoabreu
tags: [screenwriting, structure, dialogue, character, story]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - A story idea with a protagonist and a clear conflict
  - Knowledge of the target format and runtime
  - A consistent file format for scripts and documents
provides:
  - A three-act structure method with turning points
  - A Save the Cat beat sheet mapped to the story
  - A character arc framework with desire and flaw
  - Dialogue and scene-writing guidelines
---

# Screenwriting

## Overview

This skill explains how to write a screenplay from logline to a formatted
script. It covers the three-act structure, the Save the Cat beat sheet,
character arcs, and dialogue and scene craft. The guidance applies to film,
television and short-form video, always aiming for story told through
visible action rather than explanation.

## Prerequisites

- A story idea with a protagonist and a clear conflict
- A chosen format: feature, series episode or short
- A target runtime to size the structure
- A text editor or screenwriting tool for the draft

## Usage Instructions

### Step 1: Write the Logline

- One sentence with protagonist, goal and stakes.
- State what makes the story unique.
- Test it: does it raise curiosity about the outcome?

```markdown
Logline
A retired detective must solve a cold case
before the only witness dies,
but the case points to her own family.
```

### Step 2: Build the Three Acts

Structure the story around three acts.

- Act 1 - Setup: establish the world and the protagonist.
- Act 2 - Confrontation: rising obstacles and midpoint shift.
- Act 3 - Resolution: climax and change.

Place a turning point at the end of each act.

```markdown
Structure
Act 1: ordinary world, inciting incident, decision
Act 2: rising stakes, midpoint turn, all-is-lost
Act 3: final plan, climax, new normal
```

### Step 3: Map the Beat Sheet

Use the 15 beats of the Save the Cat method.

- Opening image, theme stated, setup.
- Catalyst, debate, break into two.
- Promise of the premise, B story, midpoint.
- Bad guys close in, all is lost, dark night.
- Break into three, finale, final image.

```yaml
beats:
  opening_image: 1
  theme_stated: 5
  catalyst: 10
  break_into_two: 12
  promise_premise: 20
  midpoint: 30
  all_is_lost: 50
  dark_night: 51
  break_into_three: 53
  finale: 57
  final_image: 60
```

### Step 4: Design the Character Arc

Give the protagonist a desire, a flaw and a change.

- Desire: what the character wants.
- Flaw: the belief that blocks the desire.
- Need: what the character must learn.
- Change: how the character is different at the end.

```json
{
  "character": "Clara",
  "desire": "escape the family business",
  "flaw": "believes leaving betrays her father",
  "need": "see loyalty as love, not obligation",
  "arc": "from silence to a declared choice"
}
```

### Step 5: Write Scenes That Turn

Every scene should change the state of the story.

- Enter late and leave early.
- Give each scene a goal for at least one character.
- Make the conflict visible through action.
- End the scene with a change in intention or information.

### Step 6: Write Dialogue with Subtext

- Give each character a distinct voice.
- Have characters say less than they mean.
- Use action between lines instead of explaining.
- Cut lines that repeat information already shown.

### Step 7: Format the Script

- Sluglines: INT./EXT. location - time of day.
- Action lines: present tense, visible action only.
- Dialogue: character name above the line.
- Parentheticals only when necessary.

```markdown
INT. COFFEE SHOP - DAY

CLARA looks at the letter and folds it twice.

CLARA
I'm leaving next week.

Pause. The father drinks without looking up.

FATHER
The shop needs you.

CLARA
The shop needs money, not me.
```

### Step 8: Revise Through Reading

- Read the script aloud to test the dialogue.
- Get feedback from readers, not only writers.
- Fix structure before polishing prose.
- Cut scenes that do not change the story state.

## Examples

### Example 1: Scene Card

```json
{
  "scene": 14,
  "slugline": "INT. KITCHEN - NIGHT",
  "goal": "Clara decides to resign",
  "conflict": "the father finds the letter",
  "start": "indecision",
  "end": "determination",
  "characters": ["Clara", "Father"],
  "estimated_seconds": 95
}
```

### Example 2: Beat Sheet Outline

```yaml
title: Working logline here
outline:
  act_1: pages 1-25
  catalyst: page 12
  act_2: pages 26-85
  midpoint: page 45
  all_is_lost: page 75
  act_3: pages 86-110
  climax: page 103
  final_image: page 110
```

## References

- [Save the Cat - Method and beat sheet](https://savethecat.com/)
- [Syd Field - Screenplay structure](https://www.sydfield.com/)
- [Writers Guild of America](https://www.wga.org/)
- [BBC Writersroom](https://www.bbc.co.uk/writersroom/)
- [Roteiro de Cinema - Screenwriting school](https://www.roteirodecinema.com.br/)

## Notes

- Write the logline before the treatment.
- Define the goal and conflict of every scene.
- Show emotion through action, not narration.
- Read the script aloud to test the dialogue.
- Review the beat sheet before rewriting the draft.
