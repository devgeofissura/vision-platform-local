---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: civil-structures
description: Load calculations for beams, slabs and columns with reinforcement examples
category: construction
version: 0.1.0
author: devtiagoabreu
tags: [structures, beam, slab, column, loads, engineering]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Basic structural mechanics (moments, forces, stresses)
  - Understanding of characteristic loads and partial safety factors
provides:
  - Beam bending moment and reinforcement sizing examples
  - One-way and two-way slab load distribution examples
  - Column axial capacity check and steel ratio example
---

# Civil Structures

## Overview

This skill covers the elementary load calculations used when designing or
verifying reinforced concrete structures: simply supported beams, floor slabs,
and columns. It gives the formulas, worked numerical examples, and practical
rules of thumb so an engineer or student can size elements and cross-check
results against structural software output.

All examples use the metric system and typical characteristic loads for
residential buildings. Design values apply the Brazilian load combination
convention (1.4 x permanent load, 1.4 x live load) as a simplification.

## Prerequisites

- Solid understanding of statics: reactions, shear force, and bending moment
- Familiarity with stress, strain, and material properties of concrete and steel
- Ability to interpret a structural layout drawing

## Usage Instructions

### 1. Beam Load Calculation

A simply supported beam with a uniformly distributed load produces a parabolic
moment diagram. The maximum bending moment and the required reinforcement area
are obtained with the formulas below.

```text
Beam: span L = 5.00 m, width b = 0.20 m, height h = 0.50 m

Self weight = 0.20 x 0.50 x 25 kN/m³ = 2.50 kN/m
Permanent superimposed load (walls, floor) = 6.00 kN/m
Live load (residential) = 2.00 kN/m

Characteristic load  gk + qk = 2.50 + 6.00 + 2.00 = 10.50 kN/m
Design load  pd = 1.4 x 10.50 = 14.70 kN/m

Reactions:  R = pd x L / 2 = 14.70 x 5.00 / 2 = 36.75 kN

Max bending moment: M = pd x L² / 8
  M = 14.70 x 5.00² / 8 = 14.70 x 25 / 8 = 45.94 kN.m

Required steel area (simplified lever-arm method):
  d = h - cover - stirrup - bar/2 = 0.50 - 0.025 - 0.008 - 0.0125 = 0.4545 m
  fyd = 500 MPa / 1.15 = 434.78 MPa
  As = M / (0.9 x d x fyd) = 0.04594 / (0.9 x 0.4545 x 434780)
  As = 0.04594 / 177890 = 2.58 x 10⁻⁴ m² = 2.58 cm²

Choice: 3 bars of 12 mm (As = 3 x 1.131 = 3.39 cm²)  -> OK
```

### 2. Slab Load Distribution

A one-way slab spans across the shorter direction and transfers load to the
two supporting beams. A two-way slab (span ratio < 2) transfers load in both
directions, reducing the load per direction.

```text
One-way slab:  lx = 4.00 m (span), ly = 6.00 m (ratio ly/lx = 1.5 < 2
-> actually two-way, but keep ly long for comparison)

Check ratio: 6.00 / 4.00 = 1.5  ->  ratio < 2, so TWO-WAY slab

Two-way slab load distribution (approx, for ratio 1.5):
  Load in x direction:  qx = q x (ly⁴) / (lx⁴ + ly⁴)
  q = 0.12 m x 25 kN/m³ + 1.00 kN/m² finishes + 1.50 kN/m² live
  q = 3.00 + 1.00 + 1.50 = 5.50 kN/m²

  lx⁴ = 4.00⁴ = 256,  ly⁴ = 6.00⁴ = 1296
  qx = 5.50 x 1296 / (256 + 1296) = 5.50 x 0.835 = 4.59 kN/m²
  qy = 5.50 - 4.59 = 0.91 kN/m²

Reinforcement spacing example for x direction (steel 6.3 mm, d = 0.105 m):
  Mx = qx x lx² / 8 (simplified) = 4.59 x 4.00² / 8 = 9.18 kN.m/m
  Asx = 0.00918 / (0.9 x 0.105 x 434780) = 2.24 cm²/m
  Area per bar (6.3 mm) = 0.31 cm² -> spacing = 0.31 x 100 / 2.24 = 13.8 cm
  Adopt 6.3 mm c/ 12.5 cm
```

### 3. Column Axial Capacity Check

Short columns are checked against the ultimate axial load, applying the
strength reduction factor for the combined concrete and steel contribution.

```text
Column: 0.20 m x 0.40 m, height 3.00 m, concrete C25, steel CA-50

Area of concrete Ac = 0.20 x 0.40 = 0.08 m²
Steel ratio (assume 2%) As = 0.02 x 0.08 = 0.0016 m² = 16 cm²
-> 8 bars of 16 mm (As = 8 x 2.01 = 16.08 cm²)

Axial capacity (simplified):
  Nrd = 0.85 x fcd x Ac + fyd x As
  fcd = 25 MPa / 1.4 = 17.86 MPa = 17,860 kN/m²
  fyd = 500 / 1.15 = 434.78 MPa = 434,780 kN/m²

  Nrd = 0.85 x 17860 x 0.08 + 434780 x 0.001608
  Nrd = 1214.48 + 699.13 = 1913.61 kN

Check slenderness:  lambda = (2 x 3.00) / 0.115 (r = b/sqrt(12))
  r = 0.20 / 3.464 = 0.0577 m   lambda = 6.00 / 0.0577 = 104
  lambda > 40  ->  second order effects must be considered, increase
  section or add ties; this check is only preliminary.
```

## Examples

### Example 1: Verifying a Beam Shear

```text
Same beam, Vmax = R = 36.75 kN

Shear stress:  tau = V / (b x d) = 0.03675 / (0.20 x 0.4545) = 0.404 MPa
Concrete shear strength (C25, no stirrup design):
  tau0 = 0.6 x sqrt(fck) = 0.6 x 5 = 3.0 MPa -> concrete carries alone

Required stirrup (if needed): 
  Asw = V x 100 / (0.9 x d x fyd) per meter
  = 36.75 x 100 / (0.9 x 0.4545 x 43478) = 0.207 cm²/m
  Minimum (6.3 mm, two legs) = 2 x 0.31 = 0.62 cm²/m
  Adopt stirrups 6.3 mm c/ 20 cm (governs minimum requirement)
```

### Example 2: Serviceability Deflection Check (rule of thumb)

```text
Simple beam, span 5.00 m, h = L/10 = 0.50 m (adopted height)

Deflection estimate:  delta = (5/384) x (w x L⁴) / (E x I)
  E = 26 GPa (C25), I = b x h³/12 = 0.20 x 0.125 / 12 = 0.002083 m⁴
  w (service) = 10.50 kN/m

  delta = 0.01302 x (10500 x 625) / (26e9 x 0.002083)
  delta = 0.01302 x 6562500 / 54166666 = 0.00158 m = 1.58 mm

Limit L/250 = 20 mm -> OK
```

## Best Practices

- Always separate characteristic loads (gk, qk) from design loads (pd)
- Use the correct support condition: never treat continuous beams as simply supported
- Add minimum reinforcement, even when the calculation gives zero
- Consider second-order effects for slender columns (lambda > 40)
- Check both bending and shear for every beam
- Cross-check every hand calculation with software output
- Round reinforcement up and verify the bar spacing fits the section

## Pitfalls / Common Mistakes

- Confusing the moment coefficient: M = wL²/8 is only for simply supported
- Forgetting the self-weight of the structural element itself
- Using characteristic instead of design loads in capacity formulas
- Oversizing sections with hand rules and never validating with software
- Ignoring span/depth limits, causing excessive deflection and cracking
- Reinforcing only the bottom of a continuous beam (needs top steel at supports)

## References

- [Eurocode 2: Design of Concrete Structures](https://www.phd.eng.br/wp-content/uploads/2015/12/en.1992.1.1.2004.pdf)
- [NBR 6118 - Structural Concrete Design (ABNT)](https://www.abntcatalogo.com.br/norma.aspx?ID=344546)
- [ACI 318 Building Code Requirements](https://www.concrete.org/topicsinconcrete/topicdetail/building%20code%20requirements%20for%20structural%20concrete)
- [Simply Supported Beam Calculator (Omni)](https://www.omnicalculator.com/physics/beam-load)

## Notes

- These examples are simplifications; always check against local codes
- Structural design requires licensed professional review
- Live loads depend on occupancy; verify the applicable load table
