---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: vehicle-mechanics
description: Diagnose common faults, plan maintenance schedules, understand vehicle systems, and work safely.
category: automotive
version: 0.1.0
author: devtiagoabreu
tags: [mechanics, diagnostics, maintenance, safety, vehicles]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Basic knowledge of vehicle systems and components
  - Familiarity with OBD-II diagnostic codes
  - Safety awareness for workshop and roadside work
provides:
  - Systematic fault diagnosis guidance
  - Preventive maintenance scheduling
  - Systems overview: engine, brakes, suspension, electrics
  - Torque and safety practices
---

# Vehicle Mechanics

## Overview

This skill covers automotive maintenance and diagnostics for passenger
vehicles: interpreting symptoms and OBD-II codes, planning preventive
maintenance by mileage and time, understanding core systems (engine,
brakes, suspension, steering, electrics), and applying safety and
torque practices. The goal is practical, correct guidance that always
points to physical inspection when needed.

Remote guidance has limits. A code or symptom description suggests
likely causes; confirmation requires inspection in a shop. When
brakes, steering, or tires are compromised, advise stopping use and
seeking a qualified workshop.

## Prerequisites

- Familiarity with car systems and common parts names
- Ability to read OBD-II fault codes
- Understanding of workshop safety basics
- Access to vehicle service manuals or owner's manual

## Usage Instructions

### 1. Diagnose symptoms systematically

Gather symptoms, then narrow down systems before replacing parts.

```text
1. Confirm symptom: when does it happen? speed, load, temperature?
2. Check simple causes first: fluids, belts, filters, tire pressure
3. Read OBD-II codes when available
4. Test systems in isolation before replacing components
5. Confirm with inspection; do not guess-replace
```

### 2. Interpret common OBD-II codes

Use codes as starting points, not final answers.

```text
P0171    System too lean (air leak, fuel supply)
P0300    Random misfire (spark, fuel, compression)
P0420    Catalyst efficiency below threshold
P0562    System voltage low
```

### 3. Plan preventive maintenance

Base intervals on the manufacturer's schedule; never invent them.

```json
{
  "every_5000_km": ["check fluids", "check tire pressure"],
  "every_10000_km": ["oil and filter change", "brake pad inspection"],
  "every_20000_km": ["air filter", "cabin filter", "tire rotation"],
  "every_40000_km": ["brake fluid", "suspension check", "timing belt"],
  "note": "Confirm intervals in the owner's manual"
}
```

### 4. Apply torque correctly

Critical fasteners require calibrated torque.

```text
Rules
- Always use the manufacturer's torque specification
- Use a calibrated torque wrench for wheels and suspension
- Tighten in the sequence stated by the manual
- Never exceed torque to compensate for thread wear
```

### 5. Work safely

Protect the person before the part.

```text
- Lift and support the vehicle with rated stands
- Never work under a car held only by a jack
- Disconnect the battery when working on electrics
- Wear eye protection and gloves
- Dispose of oil, batteries, and parts correctly
```

## Examples

### Example 1: Diagnosis worksheet

```markdown
# Diagnosis Worksheet

## Symptom
Car vibrates when braking at 80 km/h

## Hypotheses
1. Worn or uneven brake rotors
2. Wheel balance or alignment
3. Suspension wear

## Checks (in order)
1. Visual pad and rotor inspection
2. Brake fluid level and color
3. Tire pressure and visual wear pattern
4. Wheel bearing play

## Outcome
Refer to workshop for rotor measurement if worn
```

### Example 2: Maintenance reminder data

```json
{
  "vehicle": { "model": "example", "year": 2019, "km": 48200 },
  "due_services": [
    { "name": "oil_and_filter", "due_km": 50000, "priority": "high" },
    { "name": "air_filter", "due_km": 60000, "priority": "medium" }
  ],
  "advisories": ["Check brake pads at next service"],
  "safety": "Do not drive if brake pedal feels low or spongy"
}
```

## References

- [Senatran — Transit and vehicles (gov.br)](https://www.gov.br/transportes/pt-br/assuntos/transito)
- [EPA — On-Board Diagnostics (OBD)](https://www.epa.gov/obd)
- [ANFAVEA — National Association of Vehicle Manufacturers](https://www.anfavea.com.br/)
