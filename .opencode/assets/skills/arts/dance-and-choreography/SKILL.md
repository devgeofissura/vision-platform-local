---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: dance-and-choreography
description: Choreographic composition, staging for stage and video, and a structured rehearsal process
category: arts
version: 0.1.0
author: devtiagoabreu
tags: [dance, choreography, staging, composition, rehearsal]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - A concept and a dramatic intention for the piece
  - Music with a clear meter and phrase structure
  - Rehearsal space, time and performers at a known level
provides:
  - A composition method from concept to phrase
  - A framework for space and music relationship
  - Staging guidance for stage and camera
  - A rehearsal process with milestones and checks
---

# Dance and Choreography

## Overview

This skill explains how to create and deliver choreography for stage and
video. It covers composition from concept to movement phrases, the
relationship between music and movement, spatial design, and staging for
stage or camera. It ends with a rehearsal process that takes the piece from
montage to a reviewed performance.

## Prerequisites

- A clear concept and a dramatic intention
- Music with a defined tempo and phrase structure
- Performers at a known technical level
- A rehearsal space that matches the final venue

## Usage Instructions

### Step 1: Define the Concept

- Write the theme and the emotional arc of the piece.
- Define the tone: playful, dramatic, abstract or narrative.
- Decide the length and the number of performers.
- Collect references: images, videos, music and movement.

```markdown
Concept
Theme: departure and return
Arc: leaving, distance, remembering, returning
Length: 3 minutes
Performers: 5 dancers
Tone: introspective, warm
```

### Step 2: Build Movement Material

Create a base of movement phrases.

- Use the eight-count phrase as a unit.
- Vary each phrase by level, direction and speed.
- Repeat or invert phrases for development.
- Connect phrases into a full sequence.

```markdown
Phrase A (8 counts)
1-2 step forward
3-4 arm extension diagonal
5-6 full turn
7-8 slow drop and rise
```

### Step 3: Relate Music and Movement

Sync the movement to the music.

- Divide the music into bars and phrases.
- Map phrases of movement to musical phrases.
- Choose moments of rest for musical accents.
- Change dynamics to match sections of the music.

```json
{
  "music": { "track": "opening section", "bpm": 108 },
  "map": {
    "1-16": "entrance and formation",
    "17-32": "phrase A in canon",
    "33-48": "soloist in center",
    "49-64": "group unison peak",
    "65-80": "slow decrescendo and exit"
  }
}
```

### Step 4: Design the Space

Plan the use of the stage.

- Use levels: low, middle and high.
- Use directions: front, back, diagonals and sides.
- Vary formations: line, circle, scatter and solo.
- Control pathways to keep the stage balanced.

### Step 5: Stage for Stage or Camera

Adapt the staging to the presentation format.

- For stage: check visibility, light zones and exits.
- For video: plan shots, framing and coverage of detail.
- Mark the piece in a notation sheet for the team.
- Test the piece in the real space or set.

```markdown
Staging sheet
Section 1: diagonal entrance, wide shot
Section 2: center formation, medium shot
Section 3: soloist, close-up on hands
Section 4: group peak, wide shot
```

### Step 6: Run the Rehearsal Process

Structure rehearsals from montage to performance.

- Phase 1 - Montage: teach the phrases step by step.
- Phase 2 - Clean: correct alignment, timing and spacing.
- Phase 3 - Polish: refine dynamics and expression.
- Phase 4 - Run: full runs with music and feedback.
- Record rehearsals and review formations.

### Step 7: Protect the Body

- Warm up 15 to 20 minutes before every rehearsal.
- Cool down and stretch after each session.
- Stop the dancer at the first sign of injury.
- Refer persistent pain to a professional.

## Examples

### Example 1: Eight-Count Marking Sheet

```yaml
section: chorus
counts:
  - beats: "1-2"
    movement: step forward
    level: middle
    direction: left diagonal
  - beats: "3-4"
    movement: arm extension
    level: middle
    direction: right diagonal
  - beats: "5-6"
    movement: full turn
    level: high
    direction: front
  - beats: "7-8"
    movement: drop and rise
    level: low
    direction: center
```

### Example 2: Rehearsal Milestones

```markdown
Week 1: montage of all phrases
Week 2: full sequence linked to music
Week 3: clean spacing and alignment
Week 4: full run + recording review
Week 5: dress rehearsal in the venue
```

## References

- [Rudolf Laban - Movement analysis](https://www.rudolflaban.net/)
- [Imperial Society of Teachers of Dancing](https://www.istd.org/)
- [World Dance Alliance](https://www.wda.global/)
- [MEC - Arts education in Brazil](https://www.gov.br/mec/pt-br)
- [Itaú Cultural - Dance](https://www.itaucultural.org.br/)

## Notes

- Define the concept before creating the first step.
- Divide the music into countable blocks.
- Record rehearsals to review formations.
- Always test the piece in the final space or set.
- Never train through persistent pain.
