---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: chemistry-basics
description: Balancing chemical equations, molarity and stoichiometry with examples
category: science
version: 0.1.0
author: devtiagoabreu
tags: [chemistry, reactions, balancing, molarity, stoichiometry]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Basic understanding of atoms, molecules, and the periodic table
  - Comfort with simple algebraic equations for balancing
provides:
  - Step-by-step method for balancing chemical equations
  - Molarity and dilution calculations
  - Mole-based stoichiometry with limiting reagent examples
---

# Chemistry Basics

## Overview

This skill covers the essential quantitative and symbolic work of chemistry:
writing and balancing chemical equations, calculating concentrations as
molarity, and converting between moles, masses, and amounts in reactions
(stoichiometry). These are the skills needed in laboratories, formulation work,
and industrial production.

All examples are fully worked with units shown at every step, because unit
errors are the most common source of wrong answers in chemistry calculations.

## Prerequisites

- Familiarity with chemical symbols and the periodic table
- Understanding of the mole concept and Avogadro's number
- Ability to use atomic masses from the periodic table (approx values)
- Basic algebra for solving ratio problems

## Usage Instructions

### 1. Balancing Chemical Equations

Balancing requires equal numbers of each atom on both sides of the reaction.
Use coefficient fractions first if needed, then multiply to whole numbers.
Balance elements one at a time, leaving hydrogen and oxygen for last.

```text
Example: combustion of propane
  C3H8 + O2 -> CO2 + H2O

Step 1 - Balance carbon:    C3H8 + O2 -> 3 CO2 + 4 H2O
Step 2 - Balance hydrogen:  C3H8 + O2 -> 3 CO2 + 4 H2O  (8 H = 8 H, done)
Step 3 - Balance oxygen:    3 x 2 + 4 x 1 = 10 O on the right
  -> 10/2 = 5 O2
Balanced: C3H8 + 5 O2 -> 3 CO2 + 4 H2O

Check atoms:
  C: 3 = 3
  H: 8 = 8
  O: 10 = 3x2 + 4x1 = 10  OK

Example: neutralization
  H3PO4 + NaOH -> Na3PO4 + H2O
  Na: need 3 -> H3PO4 + 3 NaOH -> Na3PO4 + H2O
  H: 3 + 3 = 6 -> 3 H2O
Balanced: H3PO4 + 3 NaOH -> Na3PO4 + 3 H2O
```

### 2. Molarity and Dilution

Molarity is moles of solute per liter of solution: M = n/V. The dilution
equation M1 V1 = M2 V2 keeps the amount of solute constant when adding solvent.

```text
Molarity:
  Molar mass of NaCl = 23.0 + 35.5 = 58.5 g/mol
  n = 58.5 g / 58.5 g/mol = 1.00 mol
  Dissolved in 0.250 L:
  M = 1.00 / 0.250 = 4.0 mol/L

Preparing 0.500 L of 0.200 mol/L NaCl:
  n = M x V = 0.200 x 0.500 = 0.100 mol
  mass = 0.100 x 58.5 = 5.85 g
  Weigh 5.85 g, dissolve, and fill to 0.500 L mark.

Dilution:
  Have 2.0 mol/L stock, need 1.0 L of 0.50 mol/L:
  M1 V1 = M2 V2
  2.0 x V1 = 0.50 x 1.0  ->  V1 = 0.25 L
  Take 250 mL of stock, add solvent to 1.0 L total.

Hydrates reminder:
  CuSO4·5H2O molar mass includes 5 water molecules:
  63.5 + 32 + 64 + 5 x 18 = 249.5 g/mol
```

### 3. Stoichiometry with the Mole Method

Convert the given quantity to moles, apply the mole ratio from the balanced
equation, then convert to the wanted quantity. Identify the limiting reagent
when more than one reactant amount is given.

```text
Reaction: N2 + 3 H2 -> 2 NH3

How many grams of NH3 from 28.0 g of N2 (excess H2)?
  Moles N2 = 28.0 / 28.0 = 1.00 mol
  Mole ratio NH3 : N2 = 2 : 1 -> 2.00 mol NH3
  Molar mass NH3 = 14.0 + 3 x 1.0 = 17.0 g/mol
  Mass = 2.00 x 17.0 = 34.0 g NH3

Limiting reagent example:
  Given 28.0 g N2 (1.00 mol) and 6.00 g H2 (6.00/2.0 = 3.00 mol)
  Required H2 for 1.00 mol N2: 3.00 mol -> exactly enough
  -> no limiting reagent, both fully consumed
  Product: 34.0 g NH3

If only 4.00 g H2 (2.00 mol):
  Required 3.00 mol H2 -> H2 is the limiting reagent
  NH3 produced = 2.00 mol H2 x (2/3) = 1.333 mol
  Mass = 1.333 x 17.0 = 22.7 g NH3
```

## Examples

### Example 1: Percent Yield

```text
Reaction produced 25.0 g of product; theoretical is 32.0 g
  Yield = (actual / theoretical) x 100
        = (25.0 / 32.0) x 100 = 78.1%

Common yield loss causes: incomplete reaction, side reactions,
loss during purification, measurement error.
```

### Example 2: Preparing a Dilute Solution Series

```text
Stock H2SO4 18.0 mol/L. Prepare 100 mL of each:

  For 0.50 mol/L:  M1 V1 = M2 V2
    18.0 x V1 = 0.50 x 0.100 -> V1 = 2.78 mL stock in 100 mL
  For 0.10 mol/L:
    18.0 x V1 = 0.10 x 0.100 -> V1 = 0.556 mL stock in 100 mL

Safety rule: ALWAYS add acid to water, never water to acid.
Use a volumetric flask; add acid slowly, cool, then complete to mark.
```

### Example 3: Gas from a Reaction (Ideal Gas Law)

```text
Decompose 24.5 g of KClO3:  2 KClO3 -> 2 KCl + 3 O2
  Moles KClO3 = 24.5 / 122.5 = 0.200 mol
  O2 produced = 0.200 x (3/2) = 0.300 mol
  Volume at 25°C (298 K), 1 atm:
  V = nRT / P = 0.300 x 0.0821 x 298 / 1.00
  V = 7.34 L of O2
```

## Best Practices

- Balance by inspection, then verify atom counts for every element
- Carry units through every calculation; cancel them at each step
- Use molar masses consistent with the periodic table you rely on
- Always convert to moles before comparing amounts of different substances
- Identify the limiting reagent whenever two amounts are given
- Record temperature, volume, and concentration in the lab notebook
- Use the dilution formula only when the solute amount is unchanged

## Pitfalls / Common Mistakes

- Balancing by changing chemical formulas (subscripts) instead of coefficients
- Forgetting water molecules in hydrates when computing molar mass
- Using M1V1 = M2V2 with volumes that are not in the same units
- Comparing masses directly instead of moles to find the limiting reagent
- Pouring water into concentrated acid (can splash violently)
- Neglecting significant figures in molar mass and volumes

## References

- [Khan Academy - Chemical Reactions and Stoichiometry](https://www.khanacademy.org/science/chemistry)
- [Purdue Chemcollective - Stoichiometry Tutorials](https://chemcollective.org/stoich)
- [IUPAC - Nomenclature and Molar Mass Definitions](https://iupac.org/)
- [PubChem - Molar Mass Lookup](https://pubchem.ncbi.nlm.nih.gov/)
- [Sigma-Aldrich - Dilution Calculator](https://www.sigmaaldrich.com/BR/pt/support/calculators-and-apps)

## Notes

- Atomic masses are averages; use the periodic table provided in your context
- Always cite the source of molar masses in professional reports
- Lab work requires appropriate PPE; acids and bases are corrosive
