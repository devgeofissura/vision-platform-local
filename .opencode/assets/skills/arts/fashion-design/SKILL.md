---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: fashion-design
description: Fashion design covering fabric types, flat sketches, pattern basics and collection structure
category: arts
version: 0.1.0
author: devtiagoabreu
tags: [fashion, design, fabrics, pattern, collection]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - A collection concept with target market and season
  - Real fabric references with composition and width
  - A size range with base measurements
provides:
  - A method for planning a collection
  - Guidance for flat sketches and technical sheets
  - Fabric behavior knowledge for design choices
  - Pattern and grading basics for production
---

# Fashion Design

## Overview

This skill explains how to design a clothing collection from concept to
technical sheet. It covers fabric selection by behavior, flat sketching,
basic pattern and grading, and the structure that keeps a collection
coherent. The guidance applies to apparel for daily wear, occasions and
seasonal releases, always balancing creativity with production feasibility.

## Prerequisites

- A defined theme, target market and season
- Real fabric swatches with composition and width data
- A base size range (for example P to GG)
- An understanding of cost and production limits

## Usage Instructions

### Step 1: Define the Collection Concept

Start with a clear concept before the first sketch.

- Write the theme and the story of the collection.
- Choose a color palette with three to six tones.
- Define the silhouette direction: fitted, straight or wide.
- Set the target price and the number of pieces.

```markdown
Collection concept
Name: Urban Roots
Season: Winter 2027
Theme: Nature found in the city
Palette: moss green, terracotta, sand, graphite
Silhouettes: straight, flared, wide
Price target: BRL 120-260
```

### Step 2: Choose Fabrics by Behavior

Select materials by how they behave on the body.

- Fluid fabrics: viscose, silk, crepe for movement.
- Structured fabrics: wool suiting, canvas for shape.
- Stretch fabrics: jersey, knits with elastane for fit.
- Sheer fabrics: chiffon, organza for layering.

Record composition, width, consumption and care for each piece.

```markdown
Fabric card
Material: wool blend suiting
Composition: 80% wool, 20% polyester
Width: 150 cm
Consumption: 1.6 m per blazer
Care: dry clean
```

### Step 3: Draw Flat Sketches

Draw technical flats for every piece.

- Show front and back views at the same scale.
- Add side seams, darts, pockets and closures.
- Mark button placement and stitch lines.
- Indicate where each fabric and trim is used.

Keep the drawing clean enough for a pattern maker to follow.

### Step 4: Write the Technical Sheet

Produce a technical sheet per piece.

- List the SKU, name and model reference.
- Add fabric, lining and trims with suppliers.
- Include measurements per size.
- Describe finishing: hem, seams, neckline binding.

```json
{
  "sku": "BLAZER-2027-003",
  "fabric": { "material": "wool suiting", "width_cm": 150, "consumption_m": 1.6 },
  "trims": ["lining viscose", "buttons horn 2 cm", "thread polyester"],
  "sizes": ["P", "M", "G", "GG"],
  "measurements_cm": { "P": { "bust": 88, "hip": 94 }, "GG": { "bust": 116, "hip": 122 } }
}
```

### Step 5: Apply Pattern Basics

Build the pattern from the base block.

- Draft the base block per product type and size.
- Add ease according to fit and fabric.
- Mark grainlines, notches and seam allowances.
- Cut a pilot in inexpensive fabric to test the fit.

### Step 6: Build the Size Grade

Grade the base pattern to the full size range.

- Use consistent grade rules per measurement point.
- Check that grade increments follow the size chart.
- Verify the graded set in a fit sample.

### Step 7: Structure the Collection

Organize the pieces into groups.

- Group by category: tops, bottoms, outerwear and dresses.
- Balance looks across the palette and silhouettes.
- Plan quantities by bestseller potential.
- Define the release order and deadlines per group.

## Examples

### Example 1: Collection Plan

```yaml
collection:
  name: Urban Roots
  season: Winter 2027
  groups:
    tops: 8
    bottoms: 6
    outerwear: 4
    dresses: 3
  total_pieces: 21
  palette: [moss green, terracotta, sand, graphite]
  fit_tests: 3 rounds per piece
```

### Example 2: Flat Sketch Checklist

```markdown
Flat sketch checklist
- [ ] Front and back views
- [ ] Same scale for all views
- [ ] Seams and darts marked
- [ ] Pockets and closures positioned
- [ ] Fabric and trim labels per area
```

## References

- [SENAI - Fashion courses in Brazil](https://www.portaldaindustria.com.br/senai/)
- [SEBRAE - Fashion business management](https://www.sebrae.com.br/)
- [Business of Fashion - Trends](https://www.businessoffashion.com/)
- [Fashion Revolution - Ethical fashion](https://www.fashionrevolution.org/)
- [GOTS - Global organic textile standard](https://global-standard.org/)

## Notes

- Always prototype in cheap fabric before final cutting.
- Validate fabric with a pilot garment before bulk buying.
- Keep technical sheets in a single source of truth.
- Respect labeling rules for composition and care.
