---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: political-campaign-marketing
description: 'Ethical campaign strategy: positioning, message discipline, segmentation, channels and budget allocation.'
category: marketing
version: 0.1.0
author: devtiagoabreu
tags: [political-marketing, campaigns, positioning, segmentation, message-discipline, ethics]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Familiarity with marketing basics (funnel, channels, metrics)
  - Access to official electoral rules (TSE) and reliable polling data
  - Commitment to factual communication and electoral ethics
provides:
  - A campaign planning workflow from positioning to calendar
  - Voter segmentation and message matrix templates
  - Media budget allocation and measurement guidance
  - Ethical guardrails: truthfulness, identification, no hate speech
---

# Political Campaign Marketing

## Overview

This skill provides a structured, ethical approach to political campaign
marketing: strategy, positioning, message discipline, voter segmentation,
budget allocation, and digital plus offline integration. It is designed for
educational use and for professionals who want a repeatable planning method.

Everything here is educational. Campaign work must always respect electoral
law and democratic values: truthful information, transparency, and respect
for voters and opponents.

## Prerequisites

- Basic knowledge of marketing, media buying, and metrics
- Access to the official electoral rules for the relevant jurisdiction
- Reliable data: official statistics and reputable polling
- Willingness to apply strict ethical limits in all materials

## Usage Instructions

### 1. Define Positioning and Core Message

Positioning is the one idea the campaign owns. The core message expresses it
simply and repeatedly. Every channel repeats it, every proof point supports it.

```text
Positioning formula:
  Para <público>, <candidatura/causa> é a melhor escolha porque <diferença>
Core message: short, honest, repeatable sentence.
Proof points: 3 to 5 verifiable facts that support the message.

Example (educational, fictional):
  Positioning: para a cidade, gestão transparente com foco em resultados.
  Core message: "Mais resultados, menos promessas."
  Proof: metas públicas, relatórios de execução, dados abertos.
```

### 2. Segment the Electorate

Segment by geography, demographics, issues, and behavior. Prioritize groups
with highest leverage: undecided voters and low-turnout groups that a message
can realistically move.

```markdown
Segment | Profile | Main concern | Message angle | Channel
Young | 16-24, first vote | jobs, climate | concrete plans | social video
Workers | 30-50, private sector | income, costs | practical wins | radio + WhatsApp
Seniors | 60+, retired | health, safety | trust, continuity | TV + printed
```

### 3. Build the Message Matrix

For each segment, define the core message, the proof, the emotional tone, and
the call to action. Keep the candidate's platform and the core message
identical everywhere; only the angle changes.

```json
{
  "segment": "jovens_primeiro_voto",
  "dor": "falta de oportunidades",
  "mensagem": "mais educação técnica e primeiro emprego",
  "prova": "dados públicos de empregabilidade",
  "tom": "otimista e direto",
  "call_to_action": "ver o plano completo e compartilhar",
  "etica": "sem promessas irrealistas, sem ataque a opositores"
}
```

### 4. Allocate Budget Across Digital and Offline

Start from the segments and goals, not from habit. Reserve part of the budget
for tests, and reallocate based on measured response. Always follow the rules
for paid boosting and campaign financing.

```text
Example allocation (educational):
Digital: 60% (social video 30%, search 10%, tests 20%)
Offline: 40% (radio 20%, printed 15%, street 5%)
Rule: test small first, scale what proves effective.
Compliance: verify financing and boosting rules with the electoral court.
```

### 5. Enforce Message Discipline and Ethics

Keep every piece on-message and truthful. Identify paid content as required
by law, check every fact, avoid hate speech and personal attacks, and remove
anything misleading immediately.

```yaml
ethics_do:
  - "checar fatos e numeros em fontes oficiais"
  - "identificar publicidade conforme a lei"
  - "tratar adversarios com respeito"
  - "manter a mensagem coerente com a plataforma"
ethics_dont:
  - "nunca publicar desinformacao"
  - "nunca fazer discurso de odio"
  - "nunca explorar medo de forma enganosa"
  - "nunca prometer o que nao pode cumprir"
```

## Examples

### Example 1: One-week campaign calendar

```text
Seg | Launch positioning video + proof page
Ter | Segment-specific post (young voters) + test
Qua | Radio spot; retarget to engaged audiences
Qui | Live Q&A on local issues (fact-checked)
Sex | Printed material distribution in key regions
Sáb | Engagement report review; reallocate tests
Dom | Rest; plan next cycle from measured results
```

### Example 2: Message discipline checklist

```markdown
- [ ] Core message appears in every piece
- [ ] One angle per segment, same platform underneath
- [ ] Every number sourced and verified
- [ ] Paid content identified as required
- [ ] No attacks, no hate speech, no disinformation
- [ ] Educational disclaimer where applicable
```

## References

- [Tribunal Superior Eleitoral (TSE)](https://www.tse.jus.br)
- [Justiça Eleitoral](https://www.justicaeleitoral.jus.br)
- [Câmara dos Deputados - Legislação](https://www.camara.leg.br)
- [LGPD - Lei Geral de Proteção de Dados](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm)
- [International Foundation for Electoral Systems (IFES)](https://www.ifes.org)
- [Meta Business Help Center](https://www.facebook.com/business/help)
