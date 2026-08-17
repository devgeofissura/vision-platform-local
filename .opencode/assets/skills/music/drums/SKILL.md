---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: drums
description: Learn drums with grip, rudiments, independence, groove, and timekeeping
category: music
version: 0.1.0
author: devtiagoabreu
tags: [drums, drum-set, rudiments, independence, groove, timekeeping, metronome]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - A drum set, practice pad, or sturdy surface
  - Drumsticks and a metronome
  - Daily practice of 20-30 minutes
provides:
  - Matched and traditional grip fundamentals
  - Core rudiment vocabulary and sticking
  - Four-limb independence exercises
  - Groove and timekeeping patterns with metronome
---

# Drums

## Overview

Drums anchor the time and feel of a band. This skill builds the essentials: correct
grip and stroke, the core rudiments that build hand technique, independence between
limbs, and steady grooves with solid timekeeping. Every drummer, from beginner to
pro, returns to these fundamentals daily.

Drumming is physical: relaxed grip, efficient strokes, and breathing prevent injury
and let speed develop naturally. Practice slow and even with a metronome; speed is a
byproduct of control, not of forcing.

## Prerequisites

- A drum set, practice pad, or a quiet, stable surface
- Drumsticks and a metronome (app is fine)
- 20-30 minutes of daily practice time

## Usage Instructions

### Step 1: Master the Grip

Matched grip is the standard: hold both sticks the same way. The fulcrum sits
between thumb and index finger, with the other fingers wrapping loosely:

```
Matched grip: palms down, thumbs on top, sticks at 90 degrees
Relaxed wrist: pivot from the wrist, not the arm
Fulcrum check: the stick bounces freely when tapped
```

Strike the pad with rebound, letting the stick bounce rather than pressing down.

### Step 2: Learn the Core Rudiments

Rudiments are the alphabet of drumming. Start with single stroke, double stroke,
and paradiddle:

```
Single stroke:  RLRL RLRL RLRL RLRL
Double stroke:  RRLL RRLL RRLL RRLL
Paradiddle:     RLRR LRLL RLRR LRLL
Flame:          lR lR lR lR  (soft grace note + main hit)
```

Run each rudiment with a metronome, starting at 60 BPM and adding 5 BPM as it
stays clean. Aim for even volume between hands.

### Step 3: Build Four-Limb Independence

Independence lets each limb keep its own rhythm. Start with feet as the timekeeper
and add hands over them:

```
Pattern 1: Bass on 1 and 3, hi-hat 8th notes
Pattern 2: Bass on 1 and 3, snare on 2 and 4, hats 8ths
Pattern 3: Bass 1, hats offbeat, snare 2 and 4
```

Add one element at a time and isolate any limb that drifts off the click.

### Step 4: Play Basic Grooves

The rock beat is the gateway to most popular music:

```
Count:   1 e & a  2 e & a  3 e & a  4 e & a
Hi-hat:  x x x x  x x x x  x x x x  x x x x
Snare:               o                  o
Bass:    o                            o

Variation: add bass on the "&" of beat 3
```

Lock the groove at 70 BPM, then explore jazz, funk, and Latin patterns once the
rock beat feels automatic.

### Step 5: Train Timekeeping and Feel

Timekeeping is the drummer's first job. Practice with the metronome as a partner:

- Play a groove for 5 minutes without stopping
- Remove the click for 30 seconds and play the same tempo
- Bring the click back and check whether you drifted
- Practice playing slightly behind the beat (laid back) and on top (pushing)

### Step 6: Build Independence Combinations

Combine rudiments and grooves: play a paradiddle across snare and hi-hat while the
feet keep a steady beat, then trade hands between snare, tom, and hi-hat. Record
yourself weekly to hear where time and consistency break down.

## Examples

### Example 1: 20-Minute Daily Routine

```
1. Warm-up singles and doubles at 60-80 BPM (5 min)
2. Paradiddle around the kit (5 min)
3. Rock beat with variations, feet patterns (5 min)
4. Free time: play along with a metronome only (5 min)
```

### Example 2: Groove Variations Over One Rock Beat

```text
Bass variation A:  1 . . .  3 . . .  (straight 8ths)
Bass variation B:  1 . . .  & . . 4 . (syncopated)
Hat variation C:   1 & 2 & 3 & 4 &  (straight)
Hat variation D:   . & . & . & . &  (offbeat "ska")
```

### Example 3: Track Practice Progress

```python
practice = {
    "rudimento": "paradiddle",
    "bpm_inicial": 60,
    "bpm_atual": 95,
    "meta": 120,
    "dias": 30,
}

aumento_por_dia = 2
print("Em 10 dias chegamos a", practice["bpm_atual"] + 10 * aumento_por_dia)
```

## References

- [Vic Firth Rudiment Library](https://vicfirth.zildjian.com/education/40-international-drum-rudiments.html)
- [Drummerworld](https://www.drummerworld.com)
- [Drumeo](https://www.drumeo.com)
- [Wikipedia – Drum rudiment](https://en.wikipedia.org/wiki/Drum_rudiment)
