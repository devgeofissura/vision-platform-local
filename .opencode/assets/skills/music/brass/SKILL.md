---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: brass
description: Learn trumpet and trombone fundamentals with embouchure, breathing, and articulation
category: music
version: 0.1.0
author: devtiagoabreu
tags: [brass, trumpet, trombone, embouchure, breathing, articulation, range]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - A trumpet or trombone in working condition
  - Valve or slide oil and a mouthpiece
  - 15-25 minutes of daily practice
provides:
  - Embouchure setup and mouthpiece buzzing routines
  - Diaphragmatic breathing and air support exercises
  - Articulation patterns (legato, staccato, accents)
  - Long tones, flexibility, and range development
---

# Brass

## Overview

Brass playing (trumpet, trombone, and others) depends on the wind: air creates the
sound, and the lips (embouchure) control pitch. This skill covers the three
pillars of brass technique: a stable embouchure, strong diaphragmatic breathing,
and clean articulation. Long tones and mouthpiece buzzing are the daily medicine
that keeps the sound centered and the range reliable.

Brass is a game of gentle consistency. Pressing the mouthpiece harder never helps;
letting the air flow freely always does. Build endurance slowly and listen to
recordings to refine tone.

## Prerequisites

- A trumpet or trombone with valves/slide working and oiled
- A practice mute or a quiet, resonant space
- A metronome and 15-25 minutes of daily practice

## Usage Instructions

### Step 1: Set the Embouchure

Place the mouthpiece in the center of the lips, slightly above center for
trumpet. Corners firm, center relaxed, with the teeth apart as if saying "em":

```
Trumpet: 1/3 upper lip, 2/3 lower in the rim
Trombone: centered, slightly tilted to the lower lip
Signs of tension: red marks, buzzing the teeth, puffed cheeks
```

Buzz on the mouthpiece alone before playing to build the lip signal.

### Step 2: Breathe with the Diaphragm

The air column is the sound engine. Breathe low and relaxed so the belly expands
outward, keeping shoulders still:

```
Inhale 4 counts, exhale 4 counts with a hiss (repeat)
Then: 4 in, 8 out, 4 in, 12 out
Breathe before you feel you need to; never let the air run out
```

Keep the throat open and the tongue low, as if starting a yawn.

### Step 3: Play Long Tones Daily

Long tones stabilize pitch, tone, and breath control. Start on a comfortable
middle note and play each one as long and steady as possible:

```
Play C (trumpet) / Bb (trombone) for 8-16 counts at 60 BPM
Crescendo then decrescendo, keeping pitch centered
Repeat on neighboring notes downward and upward
```

Do not let the note waver; record yourself to hear intonation drift.

### Step 4: Articulate Cleanly

Articulation begins with the tongue touching behind the top teeth, releasing air
into the mouthpiece:

```
Ta = normal attack,  Da = legato attack,  Ka = detached (double tongue)
Scale articulation: ta-ta-ta-ta up and down
Double tongue: ta-ka-ta-ka for fast passages
```

Keep articulation light; the tongue interrupts air, it does not stop it.

### Step 5: Develop Flexibility and Range

Flexibility exercises move the lips across partials without tongue interruption:

```
Lip slurs (trumpet): C-G-C, C-E-G-C, then downward
Lip slurs (trombone): slide position with slur across partials
Add one chromatic step of range per week, no force
```

If the sound cracks or the lips feel tired, rest as long as you played.

### Step 6: Build Endurance Slowly

Endurance comes from rest periods and gradual exposure:

- Practice in 15-25 minute blocks with breaks
- Never play to the point of a wobbly sound or red lips
- Alternate hard passages with soft long tones
- Increase range work by 5% per week

## Examples

### Example 1: Ten-Minute Daily Warm-Up

```
1. Mouthpiece buzzing, 5 pitches (2 min)
2. Long tones, 8 counts each, 4 notes (3 min)
3. Articulation: ta-ta-ta on a scale (2 min)
4. Lip slur exercises, comfortable range (3 min)
```

### Example 2: Lip Slur Routine

```text
Trumpet (C major partials, no valves):
C - G - C, G - E - G, C - E - G - C
Trombone (slide 1st position):
Bb - F - Bb, F - D - F, Bb - D - F - Bb
```

### Example 3: Breathing Gauge

```python
capacidade = 100

def sopro(notas_por_folego):
    global capacidade
    capacidade = max(0, capacidade - notas_por_folego * 5)
    return capacidade

print("Restam", sopro(6), "unidades de fôlego")
print("Regra: descansar mais do que tocar nos primeiros meses")
```

## References

- [International Trumpet Guild](https://www.trumpetguild.org)
- [American Trombone Guild](https://www.trombone.net)
- [Trumpet Studio Resources](https://www.trumpetstudio.com)
- [Wikipedia – Embouchure](https://en.wikipedia.org/wiki/Embouchure)
