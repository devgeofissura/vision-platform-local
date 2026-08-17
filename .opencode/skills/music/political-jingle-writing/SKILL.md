---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: political-jingle-writing
description: 'Craft catchy political jingles: hooks, lyric structure, rhythm, singability and emotional tone.'
category: music
version: 0.1.0
author: devtiagoabreu
tags: [jingles, songwriting, rhythm, hooks, lyrics, political-marketing]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Basic knowledge of melody, rhythm and Portuguese lyric writing
  - Access to the campaign message and platform before writing
  - Commitment to truthful, respectful, ethical content
provides:
  - A repeatable structure for jingles (hook, verse, chorus, close)
  - Lyric writing patterns with meter, rhyme and clear articulation
  - Rhythm and tempo guidance for Brazilian popular styles
  - Singability testing and ethical writing checklists
---

# Political Jingle Writing

## Overview

This skill explains how to write political jingles, short songs designed to be
memorable and easy to sing. A good jingle ("chiclete") is a hook that the
listener repeats: simple melody, clear words, a positive feeling, and a
message aligned with the campaign.

The skill is educational. All examples are fictional, and the content must
stay truthful and respectful. Never write lyrics that misinform, attack
opponents, or exploit emotions.

## Prerequisites

- Familiarity with basic music concepts (melody, tempo, bars)
- Comfort writing short Portuguese lyrics with regular meter
- The candidate's verified message and proof points to align with
- Understanding that the piece must respect electoral ethics

## Usage Instructions

### 1. Extract the Core Message First

Before writing a single line, capture the campaign's core message and proof
points. The jingle repeats that message, never invents new facts.

```text
Input (educational example):
- Core message: "mais resultados, menos promessas"
- Proof: metas públicas, relatórios de execução
- Tone: otimista e confiante
- Target: eleitorado geral
```

### 2. Build the Jingle Structure

Use a short, predictable structure so the listener can join in quickly:
an opening hook, one or two verses, a repeated chorus, and a strong closing
hook with the key message.

```text
Standard structure (roughly 30-45 seconds):
Abertura   -> melodic hook, 1 line
Verso 1    -> problem / situation in 2 lines
Refrão     -> the message, repeated, easy to sing
Verso 2    -> the change / hope in 2 lines
Refrão     -> repeat
Gancho final -> key line, ends with name/message
```

### 3. Write Lyrics for Singability

Choose short words, regular syllable counts per line, and strong rhyme at the
ends of phrases. Read the lines aloud: if you stumble, rewrite. Keep the vocal
range narrow so anyone can sing it.

```markdown
Lyric checklist:
- [ ] 7-11 syllables per line, consistent across the verse
- [ ] Rhymes at phrase endings (alternate or paired)
- [ ] Only easy-to-articulate words
- [ ] No double meanings that hurt the message
- [ ] Chorus shorter and simpler than verses
- [ ] Final line carries the core message
```

### 4. Choose Rhythm, Tempo, and Emotional Tone

Pick a rhythm the target audience knows. Marchinha and samba read as festive;
sertanejo reads as familiar; frevo reads as energetic. Set a brisk but
comfortable tempo and keep the melody stepwise (mostly adjacent notes).

```text
Reference mapping (educational):
Marchinha -> festivo, tradicional, ~120 bpm
Samba    -> caloroso, popular, ~100 bpm
Frevo    -> energético, carnavalesco, ~150 bpm
Sertanejo -> familiar, interiorano, ~90 bpm
Rule: match the tone to the message; joyful if the message is hope.
```

### 5. Test and Iterate Ethically

Sing the chorus three times in a row. Ask two people to repeat it after one
listen. If they cannot, simplify. Then verify the words against the platform
and remove anything exaggerated, offensive, or misleading.

```json
{
  "teste": "cantabilidade",
  "passos": [
    "cantar o refrao tres vezes seguidas",
    "ouvir a reproducao de outra pessoa",
    "conferir clareza de cada palavra",
    "medir duracao total do spot"
  ],
  "aprovacao": {
    "recall": "repetido apos uma audicao",
    "clareza": "todas as palavras claras",
    "duracao": "dentro do limite da veiculacao"
  },
  "etica": {
    "veracidade": "mensagem coerente com a plataforma",
    "respeito": "sem ataques ou desinformacao",
    "finalidade": "exemplo educacional ficticio"
  }
}
```

## Examples

### Example 1: Jingle skeleton (fictional)

```text
Title: "A Força da Cidade" (fictional, for study)

Abertura: "Ei, cidadão, chegou a hora de falar"
Verso 1:  "A cidade que a gente quer ver mudar"
Refrão:   "Com trabalho e união, a cidade vai em frente"
Verso 2:  "Meta clara, resultado pra todo mundo"
Refrão:   "Com trabalho e união, a cidade vai em frente"
Gancho:   "A gente acredita, a gente é presente"

Rhythm: marchinha, ~120 bpm, vocal range one octave and a half.
```

### Example 2: Singability rewrite

```text
First draft:  "implementaremos soluções de eficiência fiscal"
Problem:      words too long to sing clearly.
Rewrite:      "Menos promessa, mais resultado"
Why it works: short words, 7 syllables, message intact, easy to chant.
```

## References

- [Tribunal Superior Eleitoral (TSE) - Propaganda](https://www.tse.jus.br)
- [Justiça Eleitoral - Normas](https://www.justicaeleitoral.jus.br)
- [ECAD - Música e Licenças](https://www.ecad.org.br)
- [ABMI - Associação Brasileira da Música Independente](https://www.abmi.com.br)
- [Câmara dos Deputados - Legislação Eleitoral](https://www.camara.leg.br)
