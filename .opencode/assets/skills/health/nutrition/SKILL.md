---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: nutrition
description: "Evidence-based nutrition education: food groups, dietary planning basics, macro/micronutrients and population adaptations"
category: health
version: 0.1.0
author: devtiagoabreu
tags: [nutrition, diet, food-groups, macronutrients, micronutrients, health]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Basic understanding of healthy eating concepts
  - A food composition table or reference for portion estimates
  - Access to the person's dietary restrictions (vegetarian, allergies, etc.)
provides:
  - Food group framework and MyPlate/Guiá Alimentar orientation
  - Macro and micronutrient basics with food sources
  - Dietary planning structure (breakfast, lunch, dinner, snacks)
  - Population adaptations (children, elderly, athletes, pregnancy)
  - Educational disclaimers about professional nutrition care
---

# Nutrition

## Overview

This skill provides evidence-based guidance for planning balanced, varied and
adequate diets. It is **educational only**: it does not diagnose, prescribe
diets, or treat diseases. Individualized nutrition requires a licensed
nutritionist or dietitian. Use this skill to build meal plans, food guides,
educational content and nutrition tracking structures that are safe and
aligned with public health recommendations (WHO, Guía Alimentar para a
População Brasileira).

## Prerequisites

- Knowledge of the person's food preferences, allergies and restrictions
- A clear goal: general health, weight management, sports performance, etc.
- Willingness to treat this as education, not as medical prescription

## Usage Instructions

### 1. Build the food-group foundation

Use the guiding principles: **natural or minimally processed foods** as the
base; oils, fats, salt and sugar used sparingly; ultra-processed foods
avoided. Organize meals around these groups:

- Cereals and tubers: rice, oats, pasta, potatoes, yuca
- Legumes: beans, lentils, chickpeas, soy
- Vegetables and fruits: varied colors and textures
- Milk and dairy (or fortified alternatives)
- Meat, eggs, fish (and plant protein sources)

### 2. Balance macronutrients

- **Carbohydrates:** main energy source; prefer whole grains
- **Proteins:** 1.0–1.6 g/kg/day for most adults (higher for athletes)
- **Fats:** 20–35% of daily energy; prefer unsaturated fats (olive oil,
  nuts, avocado, fish)

### 3. Cover micronutrients

Prioritize foods rich in iron (beans, red meat, dark greens), calcium
(dairy, fortified plant drinks, broccoli), vitamin D (fatty fish, egg yolk,
sun exposure) and fiber (fruits, vegetables, whole grains). In restrictive
diets (vegan, low-carb), point out nutrients at risk and recommend a
nutritionist's follow-up.

### 4. Structure the day

A typical daily structure with varied portions:

| Meal | Example |
|------|---------|
| Breakfast | Oat porridge with fruit and nuts |
| Morning snack | Fruit or yogurt |
| Lunch | Rice, beans, lean protein, salad, olive oil |
| Afternoon snack | Whole-grain toast with cheese or hummus |
| Dinner | Lighter meal: soup or grilled fish with vegetables |

Adjust portions to age, sex, activity level and health status.

### 5. Apply population adaptations

- **Children:** small frequent meals, exposure variety, no restrictive diets
- **Elderly:** protein at each meal, hydration, easy-to-chew textures
- **Athletes:** pre/post workout energy, adequate protein and hydration
- **Pregnancy:** folic acid, iron, iodine; avoid raw/unsafe foods

## Examples

### Example 1: Balanced weekly meal plan template

```markdown
# Semana equilibrada — modelo educacional

## Segunda
- Café: mingau de aveia com banana e canela
- Almoço: arroz integral, feijão, frango grelhado, salada de folhas
- Jantar: sopa de legumes com caldo de carne magra

## Terça
- Café: pão integral, ovo mexido, mamão
- Almoço: macarrão integral ao sugo com carne moída e brócolis
- Jantar: salmão assado, batata e salada verde

## Regra geral
- Água: 30-35 ml por kg de peso ao dia
- Sobremesa: fruta ou iogurte natural
- Lanches: oleaginosas, frutas, iogurte, pipoca integral
```

### Example 2: Educational content disclaimer

```markdown
> **Aviso importante:** este conteúdo é educativo e não substitui
> consulta com nutricionista ou médico. Não prescreva dietas para
> pessoas com doenças (diabetes, hipertensão, DRC) ou em condições
> especiais (gestação, lactação, transtornos alimentares) sem
> acompanhamento profissional. Ao construir produtos, inclua esse
> aviso na interface e recomende busca de profissional habilitado.
```

## References

- [WHO — Healthy diet](https://www.who.int/initiatives/behealthy/healthy-diet)
- [Guía Alimentar para a População Brasileira (Ministério da Saúde)](https://www.gov.br/saude/pt-br/assuntos/saude-brasil/alimentacao-saudavel)
- [FAO — Food-based dietary guidelines](https://www.fao.org/nutrition/education/food-dietary-guidelines/en/)
