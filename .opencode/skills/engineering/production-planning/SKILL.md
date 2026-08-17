---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: production-planning
description: Plan production with takt time, capacity calculations, and PCP formulas like OEE and batch sizing.
category: engineering
version: 0.1.0
author: devtiagoabreu
tags: [production, planning, takt-time, oee, capacity, scheduling, pcp]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Demand/forecast data for products and shifts
  - Cycle times and downtimes per machine
  - A spreadsheet or Python environment for calculations
provides:
  - Takt time and cycle time formulas
  - Capacity and OEE calculations
  - Workload balancing and batch-sizing patterns
  - Scheduling heuristics
---

# production-planning

## Overview

Production planning (PCP — Planejamento e Controle da Produção) decides
what to make, when, and on which machine, so output meets demand without
overbuilding or starving the line. The foundational numbers are takt time
(demand pacing) and cycle time (capability).

This skill gives you the formulas and a Python implementation to compute
takt time, required headcount, OEE, workload balancing, and batch sizing.
Plan at three horizons: long-term (capacity), medium-term (MPS), and
short-term (scheduling).

## Prerequisites

- Forecast or orders per period per product
- Cycle time, availability, and quality data per workstation
- Number of working days/hours and the shift structure
- Python 3 or a spreadsheet for the calculations

## Usage Instructions

### 1. Takt Time and Required Capacity

Takt time paces production to demand. Compare it with the bottleneck
cycle time to know whether the line can meet demand.

```python
work_seconds_per_day = 8 * 3600          # one shift
effective = work_seconds_per_day * 0.85  # 15% planned losses
demand_per_day = 960                     # units

takt = effective / demand_per_day
print(f"Takt time: {takt:.1f} s/unit")

bottleneck_cycle = 26.0                  # slowest station, s/unit
stations_needed = bottleneck_cycle / takt
print(f"Stations required at bottleneck: {stations_needed:.2f}")
```

### 2. OEE (Overall Equipment Effectiveness)

OEE = Availability x Performance x Quality. It exposes where losses
happen: downtime, slow running, or defects.

```python
planned_time = 8 * 3600
run_time = planned_time - 1800            # 30 min of downtime
ideal_cycle = 20.0
total_units = 1000
good_units = 930

availability = run_time / planned_time
performance = (total_units * ideal_cycle) / run_time
quality = good_units / total_units
oee = availability * performance * quality
print(f"OEE = {oee:.1%}")
```

### 3. Workload Balancing

Spread work so no station exceeds takt. Compute the balance efficiency
and reassign tasks until the bottleneck cycle drops below takt.

```python
tasks = {"A": 18, "B": 22, "C": 15, "D": 25, "E": 12}  # seconds
takt = 24.0

stations = []
for name, dur in sorted(tasks.items(), key=lambda x: -x[1]):
    placed = False
    for s in stations:
        if s["load"] + dur <= takt:
            s["load"] += dur
            s["tasks"].append(name)
            placed = True
            break
    if not placed:
        stations.append({"load": dur, "tasks": [name]})

balance = sum(tasks.values()) / (len(stations) * takt)
print(f"Stations: {len(stations)}, balance: {balance:.1%}")
```

### 4. Batch Sizing (EPQ)

Economic Production Quantity balances setup cost against inventory
holding cost. For a production rate `p` and demand rate `d`:

```python
import math

demand_rate = 2000          # units/year
setup_cost = 150            # per setup
holding_cost = 2.0          # per unit per year
prod_rate = 8000            # units/year

epq = math.sqrt(2 * demand_rate * setup_cost /
                (holding_cost * (1 - demand_rate / prod_rate)))
print(f"EPQ batch size: {epq:.0f} units")
```

## Best Practices

- Recompute takt whenever demand or shift structure changes; it drives everything.
- Track OEE at the bottleneck, not at every station — non-bottleneck OEE is misleading.
- Always plan with a loss factor (80-90% effectiveness), never 100%.
- Freeze a short scheduling horizon and replan exceptions rather than the whole MPS daily.
- Use ERP/MES data, but validate the numbers on the shop floor.

## Pitfalls / Common Mistakes

- Using theoretical cycle times instead of measured ones.
- Balancing the line without considering the bottleneck's quality losses.
- Ignoring changeover time when sizing batches, causing idle lines.
- Optimizing utilization of non-bottlenecks, which only creates inventory.
- Planning one shift of work but two shifts of demand.

## Examples

### Example 1: Mixed-model sequencing

```python
models = {"A": 40, "B": 30, "C": 20}   # daily demand
step = {}
for name, d in models.items():
    step[name] = 0.5 / d
seq = []
while len(seq) < sum(models.values()):
    nxt = min(step, key=step.get)
    seq.append(nxt)
    step[nxt] += 1.0 / models[nxt]
print(seq)
```

### Example 2: Required headcount

```python
import math

direct_seconds = 120.0                   # work content per unit
takt = 25.0
operators = math.ceil(direct_seconds / takt)
print(f"Operators needed: {operators}")
```

## References

- [Takt time](https://en.wikipedia.org/wiki/Takt_time)
- [Overall equipment effectiveness](https://en.wikipedia.org/wiki/Overall_equipment_effectiveness)
- [Economic production quantity](https://en.wikipedia.org/wiki/Economic_production_quantity)
