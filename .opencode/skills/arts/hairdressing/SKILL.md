---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: hairdressing
description: Hairdressing covering hair structure, coloring chemistry, cutting techniques and treatments
category: arts
version: 0.1.0
author: devtiagoabreu
tags: [hair, coloring, cutting, treatments, chemistry]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - A consultation on hair history, habits and expectations
  - Real products with manufacturer instructions
  - Patch test and strand test routines before chemical work
provides:
  - A consultation and analysis method
  - Color chemistry knowledge including developers and tones
  - Cutting technique guidance by hair type
  - A treatment and maintenance framework
---

# Hairdressing

## Overview

This skill explains how to deliver professional hair services safely:
consultation, strand and hair analysis, cutting, coloring, and treatment.
It covers the chemistry of color and lightening, the tone scale, and the
procedures that protect the fiber and the scalp. The guidance applies to
salons and freelance work, always using real products and following
manufacturer instructions.

## Prerequisites

- A consultation about history, habits and expectations
- Real products with legible labels and valid registration
- A patch test and a strand test before chemical work
- Clean tools: combs, clips, brushes and towels

## Usage Instructions

### Step 1: Consult the Client

Start with a structured consultation.

- Ask about previous color, chemical and treatments.
- Ask about home care and styling habits.
- Check the scalp for irritation, flaking or injury.
- Define the expectation and the limits of the result.

```markdown
Consultation card
Hair type: wavy thick
Scalp: normal
History: color 6 months ago, no straightening
Current color: medium brown
Target: light brown with highlights
```

### Step 2: Analyze the Hair

Assess fiber and scalp before any procedure.

- Determine porosity by observing the fiber.
- Determine elasticity and resistance to tension.
- Note damage: split ends, breakage or over-processing.
- Decide if the requested procedure is safe for the fiber.

### Step 3: Cut with the Hair Type

Choose the cut technique by structure and styling goal.

- Straight cut for clean, blunt shapes.
- Layered cut for volume and movement.
- Graduation for soft transitions in the neck.
- Face-framing layers to balance the face.

```markdown
Cut plan
Type: long layers
Dry or wet: wet cut
Points: split ends only, protect length
Finish: air dry or blow-dry by texture
```

### Step 4: Apply Color Chemistry

Use the tone scale and developer logic.

- Scale: level 1 (black) to level 10 (light blonde).
- Developer: 10 volumes for depositing, 20 for base, 30 for lightening.
- Mix tint and developer in the manufacturer's proportion.
- Neutralize unwanted tones: orange, yellow and red.

```markdown
Color formula
Current: medium brown (level 5)
Target: light chestnut with highlights
Highlights: 20 volume developer
Neutralizer: ash toner over the lightened strands
```

### Step 5: Follow Safe Chemical Rules

- Do a patch test 24 to 48 hours before the service.
- Do a strand test to preview result and timing.
- Section the hair and protect the scalp in foil work.
- Respect the manufacturer's processing time exactly.
- Rinse thoroughly and apply a neutral shampoo.

### Step 6: Apply Treatments

Choose the treatment by the fiber's need.

- Hydration: water-based masks for dryness.
- Nutrition: oil-based masks for loss of lipids.
- Reconstruction: protein masks for weakened fibers.
- Build a schedule that alternates the three stages.

```json
{
  "schedule": [
    { "week": 1, "treatment": "hydration" },
    { "week": 2, "treatment": "nutrition" },
    { "week": 3, "treatment": "reconstruction" },
    { "week": 4, "treatment": "hydration" }
  ],
  "alert": "Stop and refer to a dermatologist on unusual hair loss or scalp irritation."
}
```

### Step 7: Advise Maintenance

- Recommend home care matched to hair type and treatments.
- Schedule the return for color or retouch.
- Advise heat protection before styling tools.
- Instruct how to react to irritation: stop use and seek help.

## Examples

### Example 1: Blonding Formula Card

```markdown
Service: balayage lightening
Developer: 20 volume
Processing time: 35 minutes (per strand test)
Neutralizing: toner with violet pigment
Aftercare: purple shampoo twice a week
Return: 60 days
```

### Example 2: Treatment Session Plan

```yaml
session:
  purpose: reconstruction after lightening
  steps:
    - wash with neutral shampoo
    - apply protein mask 15 min
    - rinse and apply leave-in conditioner
    - finish with heat protectant and low-heat dry
  home_care: weekly hydration mask
```

## References

- [Anvisa - Cosmetics and safe use](https://www.gov.br/anvisa/pt-br/assuntos/cosmeticos)
- [Brazilian Society of Dermatology](https://www.sbd.org.br/)
- [Senac - Beauty courses](https://www.senac.br/)
- [ABIHPEC - Personal care industry](https://abihpec.org.br/)
- [MEC - Vocational education](https://www.gov.br/mec/pt-br)

## Notes

- This skill covers cosmetics, never medical procedures.
- Always run a patch test and a strand test first.
- Follow manufacturer proportions and timing exactly.
- Cite only real products registered with Anvisa.
- Refer scalp or hair concerns to a dermatologist.
