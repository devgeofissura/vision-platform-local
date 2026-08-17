---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: supply-chain-management
description: Optimize supply chains with EOQ, safety stock, ABC classification, and WMS-driven warehouse flows.
category: logistics
version: 0.1.0
author: devtiagoabreu
tags: [supply-chain, inventory, eoq, safety-stock, abc, wms, logistics]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Item demand history and supplier lead times
  - Cost data: holding, ordering, and stock-out penalties
  - Knowledge of your WMS capabilities and warehouse layout
provides:
  - EOQ and reorder-point calculations
  - Safety stock and service-level formulas
  - ABC/XYZ classification patterns
  - WMS inbound/outbound flow design
---

# supply-chain-management

## Overview

Supply chain management coordinates material from suppliers through
warehouses to customers. The core trade-off is inventory: too much ties
up capital, too little breaks service. This skill covers the quantitative
tools — EOQ, reorder points, safety stock, ABC classification — and the
operational flows in a WMS.

Good inventory decisions need three inputs you must collect before
calculating: demand distribution, supplier lead time, and cost structure.

## Prerequisites

- Demand history per SKU (at least 12 months) and lead time per supplier
- Holding cost, ordering/setup cost, and unit cost per item
- Knowledge of your WMS: bins, lot tracking, putaway, and picking rules
- Python 3 or a spreadsheet for the calculations

## Usage Instructions

### 1. EOQ and Reorder Point

The Economic Order Quantity balances ordering cost against holding cost.
The reorder point adds lead-time demand plus safety stock.

```python
import math

annual_demand = 12000
order_cost = 80            # per order
holding_cost = 3.5         # per unit per year
lead_time_days = 7

eoq = math.sqrt(2 * annual_demand * order_cost / holding_cost)
daily_demand = annual_demand / 365
rop = daily_demand * lead_time_days          # before safety stock
print(f"EOQ: {eoq:.0f} units, ROP: {rop:.0f} units")
```

### 2. Safety Stock for a Target Service Level

Safety stock covers lead-time demand variability. For normally
distributed demand, the Z factor encodes the target service level.

```python
import statistics, math

lead_demand = [98, 110, 104, 130, 96, 118]   # units over past lead times
z = 1.65                                     # 95% service level

mu = statistics.mean(lead_demand)
sigma = statistics.pstdev(lead_demand)
safety = z * sigma
print(f"Mean lead-time demand {mu:.0f}, safety stock {safety:.0f}")
```

### 3. ABC Classification

Pareto-classify items by annual usage value so you apply tight control
(A) where it pays and loose control (C) where it does not.

```python
items = {"SKU1": 120000, "SKU2": 30000, "SKU3": 8000, "SKU4": 2000}
total = sum(items.values())
cum = 0.0
for name, value in sorted(items.items(), key=lambda x: -x[1]):
    cum += value / total
    cls = "A" if cum <= 0.80 else "B" if cum <= 0.95 else "C"
    print(f"{name}: {value/total:.1%} cumulative {cum:.0%} -> {cls}")
```

### 4. WMS Inbound and Outbound Flow

A WMS codifies warehouse movements. Design flows around the two
transactions that drive everything else: receiving (putaway) and
picking (shipping). Keep units of measure explicit to avoid UoM errors.

```json
{
  "inbound": [
    { "step": "receive", "verify": "PO match", "field": "lot" },
    { "step": "quality_hold", "condition": "random_inspect", "field": "hold_flag" },
    { "step": "putaway", "rule": "directed_to_bin_by_class", "field": "bin" }
  ],
  "outbound": [
    { "step": "allocate", "rule": "fifo_by_expiry", "field": "lot" },
    { "step": "pick", "method": "zone_batch", "field": "qty_picked" },
    { "step": "pack_verify", "rule": "scan_each", "field": "serial" }
  ]
}
```

## Best Practices

- Separate counting and cycle counting by ABC class: A weekly, B monthly, C quarterly.
- Keep master data clean: one unit of measure, one bin, one owner per item.
- Base reorder points on measured lead-time demand, not guesswork.
- Pick FEFO by expiry for perishables; FEFO beats FIFO for shelf life.
- Measure service level, fill rate, and inventory turns as key metrics.

## Pitfalls / Common Mistakes

- Using one safety-stock policy for all items regardless of ABC class.
- Treating EOQ as a fixed order quantity without reviewing demand changes.
- Ignoring supplier lead-time variability, so reorder points are too low.
- Letting WMS overrides (manual bin assignments) silently accumulate.
- Measuring turns with average stock that includes obsolete items.

## Examples

### Example 1: Fill-rate service level

```python
orders = [{"ordered": 10, "shipped": 10}, {"ordered": 8, "shipped": 6}]
total_ordered = sum(o["ordered"] for o in orders)
total_shipped = sum(o["shipped"] for o in orders)
print(f"Fill rate: {total_shipped / total_ordered:.1%}")
```

### Example 2: Inventory turnover

```python
cogs = 2_400_000
avg_inventory = 600_000
print(f"Turns: {cogs / avg_inventory:.1f} /year")
```

## References

- [Economic order quantity](https://en.wikipedia.org/wiki/Economic_order_quantity)
- [ABC analysis](https://en.wikipedia.org/wiki/ABC_analysis)
- [Warehouse management system](https://en.wikipedia.org/wiki/Warehouse_management_system)
