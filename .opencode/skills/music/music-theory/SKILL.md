---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: music-theory
description: Learn music theory fundamentals covering notes, rhythm, scales, chords, intervals, and ear training
category: music
version: 0.1.0
author: devtiagoabreu
tags: [music-theory, notes, rhythm, scales, chords, intervals, ear-training, sight-reading]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - No prior music knowledge is required
  - An instrument or a piano/melody app for practice
  - 15 minutes of daily practice time
provides:
  - Note reading on treble and bass clefs
  - Rhythm counting for simple and compound meters
  - Scale and chord construction (major, minor, triads, sevenths)
  - Interval recognition and basic ear training routines
---

# Music Theory

## Overview

Music theory is the shared vocabulary musicians use to read, write, and create
music. This skill covers the essential building blocks: note names and clefs,
rhythm and meter, scales and key signatures, chords and harmony, and intervals.
Practical ear training keeps theory connected to real sound so the knowledge
becomes intuitive instead of abstract.

The goal is not to memorize facts but to recognize patterns: a scale on paper, a
chord in a progression, a rhythm in a song. Every concept here is paired with a
practice routine to develop fluent, usable understanding.

## Prerequisites

- No prior knowledge required; start at Step 1
- A piano, keyboard, or free digital instrument for pitch practice
- A metronome (physical or app) for rhythm work
- Paper and pencil for writing scales and chords

## Usage Instructions

### Step 1: Learn Note Names and Clefs

Notes repeat in octaves using the letters A through G. The treble clef places G on
the second line from the bottom; the bass clef places F on the fourth line:

```
Treble clef (lines): E G B D F  -> "Every Good Boy Does Fine"
Treble clef (spaces): F A C E
Bass clef (lines):   G B D F A
Bass clef (spaces):  A C E G
```

Practice naming random notes on both clefs for 5 minutes daily.

### Step 2: Count Rhythm in Simple Meter

Rhythm organizes time. In simple meter each beat divides into two. Use syllables to
sound rhythms out loud before clapping them:

```
Quarter note: "ta"  (1 beat)
Eighth notes: "ti-ti" (2 per beat)
Sixteenths:   "ta-ka-ti-ki" (4 per beat)
Dotted quarter: "ta-ah" (1.5 beats)
```

Practice each rhythm with a metronome, starting at 60 BPM.

### Step 3: Build Major and Minor Scales

A major scale follows the interval pattern whole, whole, half, whole, whole, whole,
half. A natural minor scale uses whole, half, whole, whole, half, whole, whole:

```
C major:    C D E F G A B C
A minor:    A B C D E F G A
G major:    G A B C D E F# G  (one sharp)
F major:    F G A Bb C D E F   (one flat)
```

Write one new scale per day, saying each note aloud.

### Step 4: Construct Chords

Triads stack notes in thirds. The major triad is root, major third, perfect fifth.
The minor triad lowers the third one semitone:

```
C major:     C E G
C minor:     C Eb G
C seventh:   C E G Bb
A minor 7:   A C E G
```

Practice building triads and seventh chords starting on every note of the chromatic
scale.

### Step 5: Identify Intervals by Ear

Intervals are distances between notes. Sing or play these anchors to internalize
them:

```
Perfect unison:  same note
Major second:    first two notes of "Happy Birthday"
Perfect fourth:  opening of "Here Comes the Bride"
Perfect fifth:   opening of "Twinkle Twinkle"
Octave:          jump to the same note name
```

Drill intervals daily with an app or a partner for 10 minutes.

### Step 6: Train Your Ears Daily

Ear training makes theory audible:

- Sing scales and intervals aloud before playing them
- Identify major vs minor quality of chords
- Transcribe short 4-note melodies from recordings
- Clap rhythms and check yourself against a metronome

Keep a log of what you practiced and which skills felt weak.

## Examples

### Example 1: Identify a Key from Its Key Signature

```
Two sharps (F# and C#)  -> D major / B minor
Three flats (Bb, Eb, Ab) -> Eb major / C minor

Trick: the major key is one half step above the last sharp,
or four steps below the last flat.
```

### Example 2: Harmonize a Melody in C Major

```python
chords = {
    "C": ["C", "E", "G"],
    "F": ["F", "A", "C"],
    "G": ["G", "B", "D"],
    "Am": ["A", "C", "E"],
}

def harmonize(melody_notes):
    harmonized = []
    for note in melody_notes:
        for name, chord in chords.items():
            if note in chord:
                harmonized.append(name)
                break
    return harmonized

melody = ["E", "G", "A", "C"]
print(harmonize(melody))
```

### Example 3: Daily Ear Training Routine

```
1. Sing the major scale (10 min)
2. Name 10 random intervals played by an app (10 min)
3. Classify 10 chords as major or minor (10 min)
4. Clap a rhythm from sheet music (5 min)
```

## References

- [MusicTheory.net](https://www.musictheory.net/)
- [Teoria.com](https://www.teoria.com/)
- [Khan Academy – Music](https://www.khanacademy.org/humanities/music)
- [Wikipedia – Music theory](https://en.wikipedia.org/wiki/Music_theory)
