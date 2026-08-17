---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: lean-methodology
description: Apply lean methodology with 5S, Kaizen, and value stream mapping to eliminate waste and improve flow.
category: management
version: 0.1.0
author: devtiagoabreu
tags: [lean, kaizen, 5s, vsm, waste, continuous-improvement, kanban]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - A process or workflow to improve (production, office, or dev)
  - Data on cycle times, WIP, and defects
  - Management support for experiment-based changes
provides:
  - 5S audit checklists
  - Kaizen/PDCA experiment templates
  - Value stream mapping (current and future state)
  - Waste identification patterns (7 wastes)
---

# lean-methodology

## Overview

Lean is a management philosophy built on eliminating waste (muda),
improving flow, and letting employees improve their own work. Its three
pillars: value defined by the customer, flow without stops, and
continuous improvement through small experiments (Kaizen).

This skill gives you the three most practical tools — 5S for workplace
organization, Kaizen for structured experiments, and Value Stream
Mapping (VSM) for seeing where waste lives — plus the formulas to make
decisions from real data.

## Prerequisites

- Access to the actual work area or process (walk the gemba)
- Cycle times, changeover times, WIP, and defect data
- A whiteboard or tool to draw current-state maps
- Leadership willing to fund small improvements and kill waste

## Usage Instructions

### 1. 5S Workplace Organization

5S = Sort, Set in order, Shine, Standardize, Sustain. Run it as a
cycle, not a one-off. Score each area with a simple checklist and
track the trend:

```python
areas = {
    "Assembly line 2": {"sort": 3, "set": 2, "shine": 3,
                        "standardize": 2, "sustain": 1},
}
for area, scores in areas.items():
    total = sum(scores.values()) / 25
    weakest = min(scores, key=scores.get)
    print(f"{area}: {total:.0%} — focus on {weakest}")
```

### 2. Kaizen and PDCA Experiments

Kaizen = incremental, employee-driven improvement. Formalize with the
PDCA cycle (Plan, Do, Check, Act). Every change is a small experiment
with a measurable hypothesis:

```markdown
## Kaizen sheet — Line 4 changeover
PLAN    : Move tool trays to the line side (timebox 1 week)
Hypothesis: changeover < 45 min with zero new defects
Metrics : changeover time, defect rate, safety incidents
DO      : [implement, log daily results]
CHECK   : compare vs baseline chart
ACT     : standardize if proven, else revert and record learning
```

### 3. Value Stream Mapping

VSM maps the flow from raw material to customer, stacking up cycle time
(CT), changeover (CO), WIP, and uptime at each step to expose the
value-added ratio:

```python
steps = [
    {"name": "Receiving",  "ct": 10, "va": 5,  "wip": 40},
    {"name": "Machining",  "ct": 25, "va": 25, "wip": 120},
    {"name": "Assembly",   "ct": 18, "va": 18, "wip": 60},
    {"name": "Inspection", "ct": 8,  "va": 4,  "wip": 30},
]

va_total = sum(s["va"] for s in steps)
lead_time = sum(s["wip"] for s in steps)   # simplified WIP-based LT
print(f"Value-added ratio: {va_total/lead_time:.1%}")
```

### 4. Seven Wastes Checklist

When mapping, tag every step with the waste it carries:

```python
W = {
    "overproduction": 0, "waiting": 0, "transport": 0,
    "overprocessing": 0, "inventory": 0, "motion": 0, "defects": 0,
}
observations = ["waiting", "waiting", "transport", "defects"]
for o in observations:
    W[o] += 1
print(max(W, key=W.get), "is your dominant waste")
```

## Best Practices

- Walk the gemba; data alone hides the physical reality of flow.
- Make improvements visible: 5S scoreboards and Kaizen boards in the area.
- Keep PDCA experiments small, time-boxed, and reversible.
- Measure the value-added ratio before and after a future-state map.
- Sustain is the hardest S — schedule audits; do not just declare it.

## Pitfalls / Common Mistakes

- Treating 5S as a cleanup day instead of a sustained management system.
- Mapping a future state nobody can staff or fund.
- Kaizen events that "improve" one metric while shifting defects elsewhere.
- Measuring WIP in items but cycle time in hours, corrupting the ratio.
- Blaming workers instead of the process; lean directs attention to the system.

## Examples

### Example 1: Takt vs pitch board for a cell

```python
takt = 30.0
batch = 10
pitch = takt * batch
print(f"Pitch: {pitch/60:.0f} min for {batch} units")
```

### Example 2: Continuous-flow cell rule

```python
cycle = {"lathe": 24, "mill": 21, "deb": 6}
line_takt = 25
bottleneck = max(cycle.values())
print("one-piece flow OK" if bottleneck <= line_takt
      else "add a parallel station")
```

## References

- [Toyota Production System](https://en.wikipedia.org/wiki/Toyota_Production_System)
- [Value stream mapping](https://en.wikipedia.org/wiki/Value_stream_mapping)
- [Kaizen](https://en.wikipedia.org/wiki/Kaizen)
