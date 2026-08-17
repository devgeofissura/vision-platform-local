---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: guitar
description: Learn guitar with chords, strumming, fingerpicking, scales, and tab reading
category: music
version: 0.1.0
author: devtiagoabreu
tags: [guitar, acoustic-guitar, chords, strumming, fingerpicking, scales, tab]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - A guitar in tune and a pick
  - Basic knowledge of chord names
  - Daily practice of 20-30 minutes
provides:
  - Open and barre chord vocabulary
  - Strumming patterns and rhythm control
  - Fingerpicking patterns and Travis picking
  - Scale shapes and tablature reading
---

# Guitar

## Overview

Guitar is a chord and melody instrument used across most popular music. This skill
takes a player from first chords to confident accompaniment: open chords, barre
chords, strumming with dynamics, fingerpicking patterns, pentatonic and major
scales, and fluent tablature reading.

The guitar rewards small daily habits: a clean chord change, a steady strum, one
new scale shape. Practicing at a slow tempo with a metronome builds a solid rhythm
sense that carries into real songs quickly.

## Prerequisites

- A tuned guitar (acoustic or electric) and a medium pick
- Comfort with basic chord diagrams and string numbers
- A metronome and 20-30 minutes of daily practice

## Usage Instructions

### Step 1: Learn Open Chords

Start with the essential open chords that cover thousands of songs:

```
C:   x32010
G:   320003
D:   xx0232
A:   x02220
Em:  022000
Am:  x02210
```

Press each chord, strum once, check every string rings cleanly, then move to the
next. Drill changes between chord pairs until each change takes under one second.

### Step 2: Strum with Rhythm and Dynamics

Strumming is more than hitting strings: it is time and dynamics. Count and strum
with a metronome, varying which beats get accented:

```
Pattern 1 (4/4): D D D D
Pattern 2:       D D U U D
Pattern 3:       D U D U D U
Accent variations: D d D d  then  d D d D
```

Start at 70 BPM and only speed up when the pattern stays steady.

### Step 3: Build Barre Chords

Barre chords let every chord move up the neck. The E-shape and A-shape are the two
main grips:

```
F barre (E-shape on fret 1): 133211
B barre (A-shape on fret 2): x24442

Trick: clamp with the side of the index finger,
keep the thumb low and the elbow close to the body.
```

Practice barre chords for short bursts to build finger strength without pain.

### Step 4: Fingerpicking Patterns

Fingerpicking frees the thumb to play bass notes while fingers cover higher strings:

```
PIMA assignment:
P (thumb) = bass strings (6, 5, or 4)
I = 3rd string, M = 2nd string, A = 1st string

Pattern: P I M A M I   (classic arpeggio)
Travis:  bass, I, bass, M   (alternating thumb bass)
```

Keep the thumb steady as a metronome while the fingers play the melody.

### Step 5: Learn Scale Shapes

The pentatonic scale unlocks soloing in any key. One shape moves up and down the
neck:

```
A minor pentatonic (5th position):
E |--5--8--
A |--5--7--
D |--5--7--
G |--5--7--
B |--5--8--
E |--5--8--
```

Add the major scale (CAGED shapes) later for full melodic control.

### Step 6: Read Tablature and Play Songs

Tabs show which fret to play on which string: numbers on the line of each string,
with symbols for slides (s), hammer-ons (h), pull-offs (p), and bends (b). Learn
one complete song per two weeks, combining chords, strumming, and an intro riff.

## Examples

### Example 1: 15-Minute Daily Routine

```
1. Tune and check posture (2 min)
2. Chord change drills C-G, D-A, Em-C (4 min)
3. Strumming patterns with metronome (4 min)
4. One scale shape, two octaves (3 min)
5. Play part of a song or riff (2 min)
```

### Example 2: Chord Chart for Common Progressions

```text
Campfire:  G - C - D - G
Pop:       C - G - Am - F
Rock:      E - A - B - A
Folk:      D - G - A - D
```

### Example 3: Convert a Progression to a Loop

```python
progressao = ["C", "G", "Am", "F"]
bpm = 90
tempo = 60 / bpm

for volta in range(4):
    for acorde in progressao:
        print(f"Tocar {acorde} por {tempo:.2f}s")
```

## References

- [Justin Guitar](https://www.justinguitar.com)
- [Ultimate Guitar Tabs](https://www.ultimate-guitar.com)
- [Guitar World Lessons](https://www.guitarworld.com/lessons)
- [Wikipedia – Guitar chord](https://en.wikipedia.org/wiki/Guitar_chord)
