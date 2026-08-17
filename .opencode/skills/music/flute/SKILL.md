---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: flute
description: Learn flute fundamentals with embouchure, breathing, tone, and articulation
category: music
version: 0.1.0
author: devtiagoabreu
tags: [flute, transverse-flute, embouchure, breathing, tone, articulation, vibrato]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - A flute (transverse or a practice headjoint)
  - Cleaning cloth and a music stand
  - 15-25 minutes of daily practice
provides:
  - Embouchure setup and tone production routines
  - Diaphragmatic breathing and air speed control
  - Articulation patterns (legato, staccato, accents)
  - Vibrato and phrasing development
---

# Flute

## Overview

The flute produces sound when air moves across the lip plate, splitting against the
edge. Everything good about flute playing flows from that air: tone, pitch, range,
and articulation. This skill builds a correct embouchure, strong breathing, a clear
tone on every register, clean articulation, and expressive vibrato.

The flute responds to subtlety. Small changes in lip shape, air speed, and angle
produce big changes in sound, so listening is the most important skill. Practice
long tones, harmonics, and scales daily to make the tone consistent from the low
register to the high notes.

## Prerequisites

- A flute or flute headjoint in working condition
- A cleaning cloth and a stand to hold the flute
- A quiet room and 15-25 minutes of daily practice

## Usage Instructions

### Step 1: Form the Embouchure

Roll the flute toward you and place the lip plate on the lower lip. Smile flat
across the lips, corners slightly down, and aim the air stream downward across the
hole:

```
Correct:   air splits on the far edge, relaxed lips
Incorrect: puffed cheeks, strained corners, hissing air
Test:      blow across the top of a bottle to feel the edge
```

Start by producing sound on just the headjoint before assembling the flute.

### Step 2: Breathe Deeply and Support

The flute uses a lot of air, so support matters. Breathe low into the belly and
keep the shoulders relaxed:

```
Inhale 4 counts, exhale 4 counts with a hiss
Inhale 4, exhale 8; inhale 4, exhale 12
Use faster air for high notes, slower air for low notes
```

The abdominal wall supports the column of air gently and steadily.

### Step 3: Build a Consistent Tone

Play long tones on every note of the low register, then middle, then high:

```
Start with G (all keys open) for 8-16 counts at 60 BPM
Match pitch with a tuner or a reference recording
Crescendo, decrescendo, then try vibrato after the tone is steady
```

Keep the tone centered; a bright, focused sound projects further than a loud one.

### Step 4: Articulate Clearly

Articulation on flute is subtle: the tongue brushes behind the top teeth to
release air:

```
Tu = standard articulation, Du = legato, Ku = detached (double tonguing)
Practice: tu-tu-tu-tu on repeated notes
Legato scales: du-du-du with no break in the air
```

Keep articulation light; the air never fully stops between notes.

### Step 5: Explore the Registers

Each register needs different air speed and lip angle:

```
Low register: slower air, more open lip
Middle: natural, relaxed embouchure
High register: faster air, smaller aperture, slightly forward
Exercise: octave slurs C1-C2, D1-D2, E1-E2
```

Play harmonics by overblowing low fingerings to train the high register without
forcing.

### Step 6: Add Vibrato and Phrasing

Once the tone is steady, vibrato comes from gentle pulsing of the air, not the
throat:

```
Start at 4 pulses per beat at 60 BPM, then 5, then 6
Breathe deeply before phrases and shape dynamics across them
End phrases softly with a controlled release
```

Record yourself to hear the difference between supported vibrato and wobble.

## Examples

### Example 1: Ten-Minute Daily Warm-Up

```
1. Headjoint tone production and harmonics (3 min)
2. Long tones low/middle/high, 8 counts each (4 min)
3. Articulation tu/du on a scale (2 min)
4. Octave slurs and a short phrase (1 min)
```

### Example 2: Register Exercise

```text
Low:    C - B - A - G (slow air)
Middle: G - A - B - C
High:   C - D - E - F (fast air)
Loop each with a metronome at 60 BPM.
```

### Example 3: Track Tone Consistency

```python
sessoes = [4.5, 5.0, 4.8, 5.5, 6.0, 5.8]

def progresso(tempos):
    media = sum(tempos) / len(tempos)
    return f"Tempo médio de longas: {media:.1f} segundos"

print(progresso(sessoes))
```

## References

- [Flute Society of Washington](https://www.fswdc.org)
- [The Flutist Quarterly](https://www.nga.net/classical-flute-magazine)
- [Jenny Nizer Flute Studio](https://www.jennynizer.com)
- [Wikipedia – Western concert flute](https://en.wikipedia.org/wiki/Western_concert_flute)
