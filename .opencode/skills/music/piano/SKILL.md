---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: piano
description: Learn piano fundamentals with posture, technique, scales, sight reading, and repertoire
category: music
version: 0.1.0
author: devtiagoabreu
tags: [piano, keyboard, technique, scales, sight-reading, repertoire, practice]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - A piano or 61+ key keyboard
  - A metronome and a comfortable bench
  - 20-30 minutes of daily practice
provides:
  - Correct posture and hand position routines
  - Finger independence and articulation exercises
  - Major and minor scale practice patterns
  - Sight reading drills and repertoire progression
---

# Piano

## Overview

Piano is one of the most direct instruments for learning music because pitch is
laid out linearly: black and white keys show scales and intervals visually. This
skill covers the foundations needed to play real music safely and musically:
posture, relaxed technique, finger independence, scales, chord playing, sight
reading, and a progressive repertoire list.

Progress comes from short, consistent practice with clear goals. Every session
should include technique, a new piece or passage, and sight reading. Playing slowly
and correctly beats playing fast and sloppy every time.

## Prerequisites

- A piano or keyboard with at least 61 full-size keys
- A stable bench that lets your elbows sit slightly above the keys
- A metronome (app is fine) and sheet music or a method book
- Daily practice time of 20-30 minutes

## Usage Instructions

### Step 1: Set Up Posture and Hand Position

Sit at the edge of the bench, feet flat, back straight but relaxed. Curl your
fingers so the fingertips touch the keys, with wrists level with the forearms:

```
Incorrect: flat wrists, collapsed knuckles
Correct:   rounded fingers, floating thumb, relaxed shoulders
```

Play slow five-finger patterns (C D E F G) watching for tension in the wrists.

### Step 2: Build Finger Independence

The hardest habit is keeping fingers relaxed while others move. Practice these
patterns hands separately at 60 BPM:

```
C major five-finger pattern:
1 2 3 4 5 4 3 2 1  (smooth, legato)
1 3 2 4 3 5 4 2 1  (isolation drill)
```

Use legato (connected) touch, then staccato, then accents on different fingers.

### Step 3: Learn Major Scales

Scales build technique and mapping. Start with C, G, D, A, E, F, Bb major. Use the
standard fingering: thumbs cross under, and 3-4-3 crossover for the right hand:

```
C major (right hand): 1 2 3 1 2 3 4 5
C major (left hand):  5 4 3 2 1 3 2 1
```

Practice two octaves, hands separately first, then together, with a metronome.

### Step 4: Play Chords and Accompaniment Patterns

Root-position triads under the right hand with a solid bass in the left hand let
you accompany songs quickly:

```
C major: C E G  (right), C (left, octave below)
F major: F A C
G major: G B D
Am:      A C E

Pattern: root-octave bass + broken chord
```

Learn chord progressions like C - G - Am - F for instant repertoire.

### Step 5: Sight Reading Drills

Sight reading improves fastest with easy, unfamiliar material read daily:

- Read 5 minutes per day from a method book at a slow tempo
- Look ahead at rhythm and key signature before playing
- Do not stop to correct: keep the pulse moving
- Use a metronome at a tempo slightly below comfortable

### Step 6: Build a Progressive Repertoire

Choose pieces you can play accurately at 80% of the target tempo. A balanced
repertoire includes a scale piece, an expressive piece, and a rhythmically active
piece. Learn each in layers: read hands separately, then slowly together, then
memorize and add dynamics.

## Examples

### Example 1: Ten-Minute Daily Warm-Up

```
1. Posture check and five-finger pattern (2 min)
2. C and G major scales, hands separately (3 min)
3. C - G - Am - F broken chord pattern (3 min)
4. Sight reading one short unknown piece (2 min)
```

### Example 2: Chord Progression Practice Sheet

```text
C  ->  G  ->  Am ->  F
RH: CEG  GBG  ACE  FAC
LH: C    G    A    F
Swing the rhythm: ta-ti-ta-ti
```

### Example 3: Plan a 4-Week Repertoire Cycle

```python
semana = {
    "tecnica": ["escala de G", "arpejos de Am"],
    "peca_principal": "Minueto em G (Pezold)",
    "leitura": "2 exercícios novos por dia",
    "meta": "80% do andamento sem parar",
}

print("Foco da semana:", list(semana.values()))
```

## References

- [Piano Street – Sheet Music Library](https://www.pianostreet.com)
- [IMSLP – Piano Scores](https://imslp.org/wiki/Category:Scores_featuring_the_piano)
- [Hoffman Academy](https://www.hoffmanacademy.com)
- [Wikipedia – Piano technique](https://en.wikipedia.org/wiki/Piano_technique)
