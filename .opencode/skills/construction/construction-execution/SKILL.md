---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: construction-execution
description: Concrete mix design, measurement reports and site safety for construction execution
category: construction
version: 0.1.0
author: devtiagoabreu
tags: [construction, concrete, measurement, safety, site]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Basic knowledge of construction processes
  - Familiarity with metric units and material densities
provides:
  - Concrete mix ratio (traco) calculation
  - Measurement report template and quantity takeoff method
  - Site safety checklist aligned with NR-18
---

# Construction Execution

## Overview

This skill provides practical guidance for executing and managing construction
work on site: how to design a concrete mix ratio (traco), how to produce
accurate measurement reports (medições) for payment and control, and how to
plan site safety. It focuses on the day-to-day decisions a site engineer,
foreman, or small contractor makes.

The content uses metric units and Brazilian construction conventions (traco,
NR-18, diário de obra), but the underlying logic applies to any market.

## Prerequisites

- Basic understanding of construction processes and materials
- Ability to work with volumes, weights, and percentages
- Familiarity with metric units (kg, m³, MPa)
- Access to material suppliers' technical data sheets

## Usage Instructions

### 1. Designing a Concrete Mix Ratio (Traco)

The traco expresses the proportion of cement : fine aggregate : coarse
aggregate : water, in mass. A common structural mix is 1:2:3, but the correct
mix must be validated by a compressive strength test (fck). The water/cement
ratio (a/c) is the most important parameter for strength and durability.

```text
Concrete mix design (1 m³ of structural concrete, fck = 25 MPa)

Traco (mass):  cement : sand : gravel : water = 1 : 2.2 : 3.1 : 0.55

Cement needed: 350 kg
Sand  (fine) : 350 x 2.2  = 770 kg
Gravel (coarse): 350 x 3.1 = 1085 kg
Water       : 350 x 0.55 = 192.5 L

Unit densities (approx):
  Cement : 3150 kg/m³
  Sand   : 1800 kg/m³ (dry)
  Gravel : 1500 kg/m³ (dry)

Volume check (approx apparent volume):
  350/3150 + 770/1800 + 1085/1500 + 192.5/1000
  = 0.111 + 0.428 + 0.723 + 0.192 = 1.454 m³ (including voids)

Rule: always run a slump test (Abatimento) at 10 ± 2 cm for this mix,
and prepare at least 2 test cylinders per 10 m³ for the 28-day fck test.
```

### 2. Producing Measurement Reports (Medição)

A measurement report documents the quantities executed in a period so the
contractor can bill and the client can verify. It must reference the project's
bill of quantities (planilha orçamentária) and be signed on site.

```text
Measurement Report - February - Apartment Block A

Item | Description                       | Unit | Qty plan | Qty exec | Unit cost | Total
-----|-----------------------------------|------|----------|----------|-----------|--------
 01  | Concrete C25 foundation           | m³   |  120.00  |  118.40   |  R$ 780.00 | R$ 92,352.00
 02  | Rebar CA-50 (average)             | kg   | 18,000   | 17,650    | R$ 12.50   | R$ 220,625.00
 03  | Formwork (contact area)           | m²   |  1,500   |  1,492    | R$ 38.00   | R$ 56,696.00
 04  | Block masonry 9 cm                | m²   |  3,200   |  3,180    | R$ 85.00   | R$ 270,300.00
-----|-----------------------------------|------|----------|----------|-----------|--------
Total executed in the period                                        R$ 639,973.00

Summary:
  Executed value         : R$ 639,973.00
  Retained (5% holdback) : R$ 31,998.65
  Net payable            : R$ 607,974.35

Checklist before signature:
  [ ] Quantities match the as-built drawing and diario de obra
  [ ] Test results (fck) attached for concrete items
  [ ] Photos of the executed work saved in the project folder
  [ ] Signed by the site engineer and the client's inspector
```

### 3. Planning Site Safety (NR-18)

Safety on site is a legal requirement and a cost-control tool: one serious
accident can erase the profit of a small project. The plan must cover fall
protection, machinery, scaffolding, and personal protective equipment (PPE).

```text
Daily safety checklist (adapt to the task of the day):

1. Housekeeping
   [ ] Access routes clear and free of debris
   [ ] Materials stacked with stable bases
   [ ] Trenches and openings fenced or covered

2. Fall protection (most common cause of fatalities)
   [ ] Perimeter guardrails installed above 2.0 m
   [ ] Safety harness (cinto paraquedista) anchored on roofs/edges
   [ ] Scaffolding inspected and leveled before use

3. Machinery and tools
   [ ] Operator authorized and trained (NR-11 / NR-12)
   [ ] Concrete pump hoses and clamps checked
   [ ] Circular saw with blade guard and riving knife

4. PPE
   [ ] Helmet, boots, gloves, and safety glasses worn by everyone
   [ ] Ear protection near concrete mixers and vibrators
   [ ] Mask and gloves when handling cement and additives

5. Permits and communication
   [ ] Permit-to-work signed for hot work and confined space
   [ ] Toolbox talk (diálogo diário de segurança) logged in the
       diario de obra with the names of all attendees
```

## Examples

### Example 1: Converting a Traco to a 50 kg Bag Basis

```text
Mix 1:2.2:3.1:0.55 per bag of cement:

  Cement: 1 x 50 kg = 50 kg
  Sand  : 2.2 x 50  = 110 kg
  Gravel: 3.1 x 50  = 155 kg
  Water : 0.55 x 50 = 27.5 L

Approximate volumes per bag (using dry bulk density):
  Sand   : 110 / 1800 = 0.061 m³ = 1 wheelbarrow (approx.)
  Gravel : 155 / 1500 = 0.103 m³ = 2 wheelbarrows (approx.)

Yield per bag: total mass / 2350 kg/m³ (fresh concrete density)
  = (50+110+155+27.5) / 2350 = 342.5 / 2350 = 0.146 m³ per bag
```

### Example 2: Quantity Takeoff for Concrete

```text
Slab: 8.00 m x 6.00 m x 0.12 m thick
  Volume = 8 x 6 x 0.12 = 5.76 m³
  Add 5% waste and spillage: 5.76 x 1.05 = 6.05 m³

Cement at 350 kg/m³: 6.05 x 350 = 2117.5 kg  -> 43 bags (50 kg)
Sand : 6.05 x 770  = 4658.5 kg
Gravel: 6.05 x 1085 = 6564.25 kg
Water: 6.05 x 192.5 = 1164.6 L

Number of truck mixers (7 m³ capacity): 1 truck, or 2 if using a pump.
```

## Best Practices

- Validate every traco with a compressive strength test (fck at 28 days)
- Record weather and temperature on the measurement report and diario de obra
- Measure by executed quantity, not by planned quantity; reconcile monthly
- Keep a photographic log with timestamps for every significant activity
- Inspect formwork and rebar before pouring concrete, and log the release
- Perform a daily toolbox talk and record attendance
- Retain test cylinders: 2 per 10 m³ per the applicable standard

## Pitfalls / Common Mistakes

- Guessing the water/cement ratio and adding water on site to improve workability
- Measuring concrete by volume of materials dumped, ignoring the planned traco
- Billing quantities before the service is actually executed and inspected
- Using the planned quantities from the budget as the executed measurement
- Ignoring the vertical loads of stacked materials (e.g., bricks) on slabs
- Treating safety as an extra cost instead of a baseline requirement

## References

- [NR-18 Segurança no Trabalho na Construção Civil (Brazilian regulation)](https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/inspecao-do-trabalho/seguranca-e-saude/seguranca-e-saude-no-trabalho-normas-regulamentadoras)
- [ACI Concrete Mix Design Guidance](https://www.concrete.org/topicsinconcrete/topicdetail/mix%20design)
- [NBR 6118 Concrete Structures Design (ABNT)](https://www.abntcatalogo.com.br/norma.aspx?ID=344546)
- [Measurement of Construction Works (RICS guidance)](https://www.rics.org/profession-standards/rics-standards-and-guidance/sector-standards/quantity-surveying-standards)

## Notes

- Always confirm local standards: NBR (Brazil), ACI (USA), EN 206 (Europe)
- A traco is only valid for the specific aggregates tested; re-test on new supply
- The measurement report is a contractual document; keep a signed copy
