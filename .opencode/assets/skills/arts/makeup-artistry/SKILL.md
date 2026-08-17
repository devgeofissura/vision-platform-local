---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: makeup-artistry
description: Professional makeup artistry covering skin analysis, the color wheel, techniques for base, contour, eyes and lips, and hygiene
category: arts
version: 0.1.0
author: devtiagoabreu
tags: [makeup, skin, color-theory, beauty, techniques]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - A client interview covering skin type, undertone and allergies
  - Real cosmetics available in the market with manufacturer instructions
  - Clean brushes, sponges and a patch-test routine
provides:
  - A step-by-step skin analysis method
  - A color wheel approach for correcting and neutralizing
  - Techniques for base, contour, eyes and lips
  - A hygiene and safety checklist for makeup sessions
---

# Makeup Artistry

## Overview

This skill explains how to perform professional makeup from start to finish:
analyzing the skin, preparing it, choosing colors with the color wheel, and
applying base, contour, eye and lip techniques. It also covers the hygiene
and safety rules that protect both the artist and the client. The guidance
applies to social, editorial and bridal work, always using real products and
respecting manufacturer instructions.

## Prerequisites

- A clean, well-lit workspace with mirrors
- Brushes, sponges and disposables for hygiene
- Real cosmetics with valid registration and legible labels
- Knowledge of the client's skin type, undertone and allergies

## Usage Instructions

### Step 1: Analyze the Skin

Assess the client before choosing any product.

- Identify the skin type: oily, dry, combination or normal.
- Identify the undertone: warm, cool, neutral or olive.
- Check visible conditions such as dark circles and spots.
- Ask about allergies and current skin care routine.

Document the result before proceeding.

```markdown
Skin analysis card
Type: combination
Undertone: warm (amber)
Concerns: dark circles, slight redness on cheeks
Allergies: none declared
```

### Step 2: Use the Color Wheel

Use complementary colors to correct and neutralize.

- Redness is neutralized with green.
- Dark circles with purple or blue tint are corrected with peach or orange.
- Sallow tone is balanced with a light lavender corrector.

Then choose base and concealers that match the undertone.

```markdown
Correction guide
Redness   -> green corrector
Purple circles -> peach/orange corrector
Yellow cast -> lavender corrector
```

### Step 3: Prepare the Skin

Follow the order: cleanse, tone, moisturize, protect, then makeup.

- Cleanse with a gentle product suitable for the skin type.
- Apply moisturizer matched to oiliness or dryness.
- Apply sunscreen whenever the look is worn in daylight.
- Apply primer in the targeted zones (pores, lines, shine).

### Step 4: Build the Base

Apply foundation in thin, even layers and spot-conceal.

- Start at the center of the face and blend outward.
- Build coverage with thin layers instead of one thick one.
- Set with powder only where you need less shine.
- Choose finish: matte, natural or dewy by occasion.

### Step 5: Contour and Highlight

Sculpt with contour, blush and highlight by face shape.

- Contour under the cheekbone, jawline and hairline.
- Blush on the apples or the high cheek, by preference.
- Highlight on cheekbones, brow bone and cupid's bow.

```markdown
Contour map
Shadow: temples, under cheekbones, jawline
Color: blush on the upper cheek
Light: cheekbones, brow bone, inner corner
```

### Step 6: Design the Eyes

Build eye looks from base shadow to definition.

- Apply an eye primer or base shadow first.
- Set the crease with a transition shade.
- Deepen the outer corner for dimension.
- Add shimmer on the lid and highlight the inner corner.
- Finish with liner and mascara as requested.

### Step 7: Paint the Lips

Prepare and define the lips.

- Exfoliate gently and apply lip balm first.
- Line the lips to correct or define the shape.
- Apply the chosen lipstick or gloss in thin layers.
- Blot between layers for longer wear.

### Step 8: Follow the Hygiene Checklist

- Wash brushes with gentle soap and dry them tilted.
- Use a new disposable applicator for each client when needed.
- Replace products that are expired or smell different.
- Never share products that touch skin directly.
- Check that all products carry manufacturer instructions.

## Examples

### Example 1: Bridal Look Plan

```yaml
look: classic bridal
skin: { prep: serum + primer, base: semi-matte, finish: natural }
eyes: { shadow: neutral pearl, liner: thin, mascara: waterproof }
lips: { tone: soft rose, finish: transparent gloss }
fixing: { spray: setting mist, touchups: every 3 hours }
test: { performed: true, photos: true, date: 7 days before }
```

### Example 2: Evening Social Look

```yaml
look: social night
skin: { type: combination, base: long-wear matte }
eyes: { style: smoky with defined crease }
lips: { tone: muted red, finish: satin }
focus: eyes
wear_time_h: 8
```

## References

- [Anvisa - Cosmetics safety](https://www.gov.br/anvisa/pt-br/assuntos/cosmeticos)
- [ABIHPEC - Brazilian personal care industry](https://abihpec.org.br/)
- [Brazilian Society of Dermatology](https://www.sbd.org.br/)
- [Senac - Beauty courses](https://www.senac.br/)

## Notes

- Patch test new products before full use.
- This skill covers cosmetics, never medical procedures.
- Refer clients with skin conditions to a dermatologist.
- Cite only real products with manufacturer instructions.
