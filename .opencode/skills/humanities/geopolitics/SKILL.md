---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: geopolitics
description: 'Frameworks for analyzing global power, regions, resources and alliances in an evidence-based way.'
category: humanities
version: 0.1.0
author: devtiagoabreu
tags: [geopolitics, international-relations, energy, alliances, trade, regional-stability]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Access to reliable sources (UN, IMF, World Bank, government portals)
  - Basic knowledge of geography and international relations vocabulary
  - Commitment to factual, neutral, educational analysis
provides:
  - A structured framework for geopolitical scenario analysis
  - Guidance on actors, resources, routes and alliances mapping
  - Templates for risk assessment and regional stability checks
  - Ethical rules for impartial and source-based analysis
---

# Geopolitics

## Overview

This skill provides a repeatable framework for analyzing global power,
regions, resources and alliances. It helps you move from news headlines to a
structured picture: who the actors are, what they want, which resources and
routes matter, and how institutions channel conflict and cooperation.

The output is educational and analytical. It is not advocacy for any country,
bloc, or company, and it never substitutes for professional risk advice.

## Prerequisites

- Internet access to official and multilateral sources for verification
- Familiarity with basic concepts: sovereignty, power, trade blocs, sanctions
- Willingness to separate facts, interpretation, and projections
- No expectation that a projection is a prediction

## Usage Instructions

### 1. Map the Actors and Interests

Start by listing the states, blocs, institutions, and non-state actors in the
scenario. For each one, record its stated interests, capabilities, and the
constraints it faces. A table keeps the analysis comparable.

```text
Actor | Type | Main interests | Capabilities | Constraints
Brazil | state | agriculture exports, energy autonomy | large agribusiness, renewables | infrastructure gaps
Mercosur | bloc | regional trade integration | common external tariff | internal divergences
OPEC+ | cartel | stable oil revenues | output decisions | demand volatility
```

### 2. Map Resources, Routes, and Infrastructure

Identify the physical and economic foundations of power in the region:
energy, minerals, food, water, and the corridors that move them. Chokepoints
(straits, ports, pipelines) deserve special attention.

```markdown
Checklist:
- [ ] Energy: oil, gas, renewables, critical minerals
- [ ] Trade corridors: maritime routes, straits, ports, railways
- [ ] Food and water security exposure
- [ ] Infrastructure: pipelines, grids, data cables
- [ ] Dependencies: who depends on whom for supply and transit
```

### 3. Analyze Alliances and Institutions

Evaluate how alliances and multilateral bodies manage or amplify tensions.
Record the institutional channels available (UN, trade blocs, arbitration),
their reach, and their limits.

```text
Channel | Reach | Typical instruments | Limits
UN Security Council | global | sanctions, resolutions, peacekeeping | veto power
Regional bloc | regional | tariff agreements, dispute courts | enforcement gaps
Bilateral treaty | two states | defense pacts, trade deals | scope limited to signatories
```

### 4. Assess Conflict Risk and Regional Stability

Combine the actor, resource, and institutional layers into a stability
assessment. Use explicit risk levels and always cite the basis for each
judgment.

```yaml
risk_matrix:
  escalation_trigger: "disputa por rota ou recurso compartilhado"
  probability: "low"
  impact: "high"
  watch_indicators:
    - "mudancas em acordos de transito"
    - "movimentacao militar incomum"
    - "retorica oficial escalada"
  mitigating_factors:
    - "mecanismos multilaterais ativos"
    - "interdependencia comercial elevada"
  note: "Projecao condicionada; revisar com novos dados."
```

### 5. Write the Output Ethically

Present the analysis neutrally, distinguish facts from interpretation, cite
sources for every data point, and state uncertainty explicitly. Treat all
content as educational and analytical.

## Examples

### Example 1: Scenario brief

```text
Scenario: increased tension around a strategic strait.
Actors: coastal state, transit users, multilateral body.
Resources: oil, gas, containerized goods.
Assessment:
  - Disruption probability: medium
  - Impact on regional supply chains: high
  - Mitigation: diplomatic channels and alternative routes in operation
Sources: UN data, IMF projections, government statements.
Disclaimer: educational analysis, not a forecast or advice.
```

### Example 2: Regional stability snapshot

```json
{
  "region": "latin_america",
  "assessment_year": 2026,
  "indicators": {
    "trade_integration": "moderate",
    "energy_interdependence": "high",
    "institutional_density": "medium",
    "dispute_management": "functional"
  },
  "verdict": "stable with monitored risks",
  "sources": ["UN", "IMF", "World Bank", "regional bloc secretariat"],
  "method_note": "Qualitative scoring based on cited public data."
}
```

## References

- [United Nations](https://www.un.org)
- [International Monetary Fund (IMF)](https://www.imf.org)
- [World Bank](https://www.worldbank.org)
- [International Energy Agency (IEA)](https://www.iea.org)
- [Crisis Group](https://www.crisisgroup.org)
- [World Trade Organization (WTO)](https://www.wto.org)
