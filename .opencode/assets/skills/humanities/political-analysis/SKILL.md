---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: political-analysis
description: 'Balanced analysis of political systems, institutions and elections with evidence and plural perspectives.'
category: humanities
version: 0.1.0
author: devtiagoabreu
tags: [political-analysis, institutions, elections, public-policy, democracy]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Access to official sources (parliaments, electoral courts, statistics offices)
  - Basic knowledge of political systems and electoral concepts
  - Commitment to neutrality and to presenting multiple perspectives
provides:
  - A structured method to describe systems, institutions and elections
  - Guidance on balanced policy analysis across viewpoints
  - Templates for electoral data and policy-cycle summaries
  - Ethical rules separating facts, analysis, and opinion
---

# Political Analysis

## Overview

This skill offers a method for analyzing politics in a balanced and
evidence-based way. It covers political systems, institutions, elections, and
public policy, with a neutral, plural perspective applicable to Brazilian and
global contexts.

The material is educational and analytical. It never takes a partisan stance,
never advises who to vote for, and always flags uncertainty.

## Prerequisites

- Internet access to official and reputable sources
- Familiarity with basic concepts: regime, system of government, elections
- Readiness to present opposing views with equal rigor
- No expectation of definitive answers for contested issues

## Usage Instructions

### 1. Describe the Political System

Identify the regime type, form of government, and electoral system. Record how
power is distributed across levels of government and branches.

```text
System description (Brazil example):
- Form of government: federal presidential republic
- Legislative: bicameral (Chamber of Deputies, Federal Senate)
- Electoral system: proportional open list (legislative), majority two-round
  (executive)
- Federation: Union, states, municipalities
Note: verify the current law before asserting details.
```

### 2. Map Institutions and Decision Channels

List the institutions that decide and implement policy: parliaments,
executives, courts, regulatory agencies, and oversight bodies. For each, note
its powers, composition, and the channels for citizen participation.

```markdown
Institution | Powers | Composition | Oversight channel
Legislature | legislate, budget, oversight | elected members | public hearings
Executive | implement, decree, diplomacy | elected chief + ministries | transparency portals
Courts | constitutional review, disputes | appointed/selected judges | public sessions
Electoral court | runs and audits elections | selected members | published rulings
```

### 3. Analyze Elections Fairly

Analyze electoral processes with the same standard for all parties: rules,
campaign environment, results, and checks. Never promote or attack a
candidate; describe the process.

```json
{
  "election": "fictional_municipal",
  "rules": "proportional for council, majority two-round for mayor",
  "turnout_note": "report official figures only",
  "verification": "official results after audit by electoral court",
  "campaign_notes": "describe channels and tone neutrally",
  "analysis_limit": "interpret results without endorsing candidates"
}
```

### 4. Analyze Public Policy Across Viewpoints

For any policy, map the problem definition, actors, the policy cycle stage,
and the main arguments on all sides. Pair each position with evidence and
state the trade-offs.

```yaml
policy_analysis:
  topic: "reforma_educacional_ficticia"
  cycle_stage: "formulacao"
  actors: ["executivo", "legislativo", "entidades_de_classe", "pesquisa_academica"]
  perspectives:
    - argument: "expansao de acesso e modernizacao curricular"
      evidence: "relatorios publicos de desempenho"
    - argument: "riscos de implementacao e custo fiscal"
      evidence: "notas tecnicas de orcamento"
  trade_offs: ["cobertura vs custo", "velocidade vs qualidade"]
  verdict: "plural; decisao compete aos atores democraticos"
```

### 5. Write Balanced Conclusions

Separate facts, analysis, and opinion. Attribute every claim to a source,
present the strongest counterargument, and label uncertainty. Keep the tone
neutral and educational.

## Examples

### Example 1: Election result summary

```text
Summary for a fictional election:
- Turnout and valid votes: use official published figures
- Seat distribution: report numbers without commentary on parties
- Notable pattern: describe demographic or regional variation factually
Sources: official electoral court publications.
```

### Example 2: Institutional landscape checklist

```markdown
- [ ] Identify regime and form of government
- [ ] List branches and their powers
- [ ] Map oversight and transparency bodies
- [ ] Note electoral rules and calendar
- [ ] Collect sources for every claim
- [ ] Present at least two perspectives per contested point
```

## References

- [Câmara dos Deputados](https://www.camara.leg.br)
- [Senado Federal](https://www.senado.leg.br)
- [Tribunal Superior Eleitoral (TSE)](https://www.tse.jus.br)
- [IBGE](https://www.ibge.gov.br)
- [Inter-Parliamentary Union](https://www.ipu.org)
- [International IDEA - Elections and Democracy](https://www.idea.int)
