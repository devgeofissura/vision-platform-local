---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: plastics-industry-sales
description: "Technical selling of resins and polymers: grades, certifications, converters and pricing"
category: commercial
version: 0.1.0
author: devtiagoabreu
tags: [commercial, plastics, resins, polymers, b2b, technical-sales]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Resin catalog with technical data sheets (MFI, density, temperature)
  - Cost model per grade and per ton (with freight rule CIF/FOB)
  - Knowledge of the customer's process (injection, blow molding, film)
provides:
  - Resin family and grade classification knowledge (PE, PP, PET, PS, PVC)
  - How to read a technical data sheet and match grade to process
  - Cost-per-part calculation for price defense in negotiation
  - Homologation workflow from sample to standing order
  - Certifications and recycled content (regrind, PIR, PCR) guidance
---

# Plastics Industry Sales

## Overview

This skill covers technical selling of resins and polymers to converters
(injection molders, extruders, blow molders, film producers). Buyers in
this market are engineers and production managers: the sale is won on
data, not charm.

The core loop is homologation: the customer tests the grade on their own
machine before committing volume. This skill walks through resin families,
reading data sheets, calculating cost per part, running homologation, and
pricing per grade with freight and indexation rules.

## Prerequisites

- A catalog of resin grades with technical data sheets (TDS)
- Safety data sheets (FDS) available for every grade sold
- Cost structure per ton, including freight terms (CIF/FOB)
- Customer information: process type, machines, and applications
- Awareness of certifications relevant to the region (ABNT, ANVISA,
  INMETRO, food-contact standards)

## Usage Instructions

### 1. Knowing the Resin Families

Each family serves distinct applications. Match the family to the process
before discussing grades.

```text
Family  | Common grades           | Typical applications
--------|-------------------------|------------------------------------
PE      | HDPE, LDPE, LLDPE       | filmes, embalagens, tubos, garrafas
PP      | homopolímero, copolímero| injeção, tecido, utilidades, autopeças
PET     | bottle, film grade      | pré-formas, garrafas, laminados
PS      | crystal, high impact    | copos, embalagens rígidas, eletrodomésticos
PVC     | rigid, flexible         | perfis, tubos, mangueiras, películas
```

Inside a family, the grade is selected by processing needs: MFI controls
flow, density affects part weight, and impact/barrier properties decide
if the grade survives the application.

### 2. Reading the Technical Data Sheet

Four numbers usually decide the sale: MFI, density, melt temperature,
and impact or flexural properties.

```text
Key TDS fields:
  - MFI (Melt Flow Index) g/10 min: flow at a given load/temp
  - Density g/cm3: part weight and resin yield per kg
  - Melt temperature C: sets the processing window
  - Impact (Izod/Charpy): mechanical toughness
  - Tensile / flexural modulus: stiffness
  - Food contact / certification markings
  - Storage and handling notes

Quick guide:
  High MFI  -> thin parts, fast cycles (caps, thin-wall)
  Low MFI   -> blown film, big parts needing strength
  Low density -> lighter parts, more parts per kg
  High density -> stiffer, heavier parts
```

If the TDS is missing a property the customer asked about, say so and
get the value from the supplier before quoting.

### 3. Matching Grade to Process

Do not offer a grade; offer a solution for the customer's machine.

```text
Process      | Considerations
-------------|------------------------------------------------
Injection    | MFI and cycle time; mold temperature window
Blow molding | melt strength; parison stability; wall distribution
Extrusion    | melt stability; die swell; dimensional control
Film         | gel control; bubble stability; clarity/barrier

Match workflow:
1. Ask about machine (tonnage, screw, mold cavities)
2. Confirm the part (weight, dimensions, required properties)
3. Check operating window vs grade TDS
4. Propose a homologation plan with success criteria
```

Document the machine parameters used in the homologation: the next sale
to the same customer becomes much easier.

### 4. Cost per Part and Price Defense

Price is quoted per ton, but the buyer evaluates per part. Show them the
part cost, not just the ton price.

```text
Cost per part:
  Part weight      = 98 g
  Sucata (scrap)   = 2%    -> effective 100 g/part
  Ton price        = R$ 7.450,00
  Resin cost/part  = 0.100 kg * 7.450,00 = R$ 0,745
  Cycle + labor + energy per part = R$ 0,30
  Total cost       = R$ 1,045 per part

Yield comparison:
  Standard grade:  0,902 g/cm3  -> 1.000 kg = 10.207 parts of 98 g
  Alternate grade: 0,905 g/cm3  -> 1.000 kg = 10.173 parts of 98 g
  Use density to show the real economic difference, not just price.
```

A higher-priced grade that reduces scrap or cycles can be the cheaper
solution. Prepare that argument before the negotiation.

### 5. Homologation Workflow

Make homologation a controlled, documented process so the deal moves from
sample to standing order.

```text
Homologation steps:
1. Register the request: customer, machine, application
2. Send 2 samples of 25 kg (free or at cost, defined in policy)
3. Define success criteria with the customer (impact, cycle, color)
4. Follow up during the test and record the machine settings
5. Capture the result: approved, conditional, rejected
6. If approved, convert to a standing order with monthly volume
7. If rejected, capture the reason and adjust grade or price

Standing order:
  - Volume per month and schedule
  - Price per ton valid for N days, indexation clause if imported
  - Minimum order and freight terms
  - Blend allowances (regrind/PCR) documented per application
```

### 6. Certifications and Recycled Content

Certifications unlock markets; recycled content is a growing requirement.
Know what applies to each grade and application.

```text
Common certifications:
  - Food contact (ANVISA / EU / FDA)
  - INMETRO for regulated products
  - ABNT standards for pipes and profiles
  - Resin producer certificates of analysis (CoA) per lot

Recycled content:
  - Regrind: internal scrap, usually up to X% in blend
  - PIR (post-industrial): production scrap from industry
  - PCR (post-consumer): from collected and sorted waste
  - Always state the PCR/PIR content and its limits per application
  - Document traceability: lot, supplier, recycling origin
```

Never claim a certification the grade does not have; that ends accounts.

## Examples

### Example 1: Price Table by Grade (JSON)

```json
{
  "familia": "polipropileno",
  "moeda": "BRL",
  "unidade": "tonelada",
  "atualizado_em": "2026-08-08",
  "graus": [
    {
      "codigo": "PP-HOM-500",
      "aplicacao": "injeção de utilidades domésticas",
      "mfi_g_10min": 12,
      "densidade_g_cm3": 0.905,
      "preco": 6850.00,
      "condicao": "CIF São Paulo, 5 ton mín."
    },
    {
      "codigo": "PP-COP-900",
      "aplicacao": "peças de impacto e autopeças",
      "mfi_g_10min": 8,
      "densidade_g_cm3": 0.902,
      "preco": 7450.00,
      "condicao": "CIF São Paulo, 5 ton mín."
    }
  ]
}
```

### Example 2: Homologation Proposal with Cost per Part

```text
Grau: PP-COP-900 (copolímero de impacto)
Aplicação: painel de porta, injeção 450 t, molde 2 cavidades

Propriedades-alvo:
  - MFI 230°C/2,16 kg: 8 g/10 min
  - Densidade: 0,902 g/cm3
  - Impacto Izod 23°C: 55 J/m
  - Temperatura de injeção: 200-230°C

Homologação: 2 amostras de 25 kg, custo R$ 0,00
Ciclo estimado: 42 s | Sucata alvo: < 2%
Custo por peça: R$ 0,47 (peso 98 g)
Preço: R$ 7.450,00/ton CIF | Volume mínimo: 5 ton/mês
Condição: 28 dias | Validade: 30 dias

Status: amostra enviada em 48h úteis, acompanhamento no dia 3.
```

## Best Practices

- Homologate before selling volume: it protects both sides
- Record machine settings and results of every homologation
- Quote per ton with clear freight (CIF/FOB) and minimum order
- Add an indexation clause for imported resin price swings
- Always attach the CoA and FDS to the first order
- State recycled content limits per application in writing
- Keep the grade catalog updated as suppliers change grades

## Pitfalls / Common Mistakes

- Selling on ton price alone while ignoring part cost
- Promising a property not confirmed on the TDS
- Skipping homologation and taking returns on the first truck
- Mixing CIF and FOB prices in the same comparison
- Not documenting PCR/PIR content and losing certified accounts
- Ignoring MFI when recommending a grade for a specific machine

## References

- [ABIPLAST - Associação Brasileira da Indústria do Plástico](https://www.abiplast.org.br)
- [Braskem - catálogo de resinas](https://www.braskem.com.br)
- [ABNT - normas técnicas para plásticos](https://www.abnt.org.br)
- [SEBRAE - reciclagem e indústria do plástico](https://www.sebrae.com.br)
- [CNI - Portal da Indústria](https://www.portaldaindustria.com.br)

## Notes

- Prices and properties are illustrative; always confirm on the TDS
- Homologation is the standard entry point in the Brazilian market
- Compare grades using yield (parts per ton), not only price
