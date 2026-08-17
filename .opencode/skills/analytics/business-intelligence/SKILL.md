---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: business-intelligence
description: "Design BI dashboards and analytics: KPIs, metrics, data modeling, ETL, charts and reports. Use when building dashboards, KPI cards, trend/geographic/ABC analysis, forecasting, reading spreadsheets (Google Sheets/Excel), data warehousing, or when users mention BI, dashboard, indicadores, métricas, relatório, gráfico, KPI or previsão de vendas."
category: analytics
version: 0.1.0
author: devtiagoabreu
tags: [bi, analytics, dashboards, kpi, data-warehouse, etl, reporting, abc-curve]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - A data source (SQL database, Google Sheets, CSV, API)
  - A charting/BI stack (Recharts/ECharts in-app, Metabase, Power BI, or simple tables)
  - Understanding of SQL aggregation (GROUP BY, window functions)
provides:
  - KPI definition and metric design
  - Dashboard layout patterns (cards, trends, geo, ABC curve)
  - Data modeling and ETL patterns (cache, incremental load)
  - SQL aggregation and window function recipes
  - Forecast and segmentation techniques
  - Reporting export patterns (CSV, Excel, PDF)
difficulty: intermediate
frameworks: [recharts, metabase, power-bi, sql]
languages: [sql, typescript, python]
---

# Business Intelligence

## Overview

BI turns raw operational data into decisions. The pipeline is
`Source → ETL/Model → Storage → Metrics → Dashboards → Decisions`. Most BI
projects fail on **data quality and metric definition**, not on charts.

## Prerequisites

- A data source (SQL database, Google Sheets, CSV, API)
- A charting/BI stack (Recharts/ECharts in-app, Metabase, Power BI, or simple tables)
- Understanding of SQL aggregation (GROUP BY, window functions)

## 1. Metric Design (define before you code)

Every metric needs a precise, agreed definition:

| Metric | Definition must state |
|--------|------------------------|
| Revenue | Gross/net? Including taxes? Currency? Timezone? |
| Active customers | Customer, contact, or company? Active in what window? |
| Conversion | Which step → which step? Attribution window? |
| Avg ticket | Revenue / orders, or per invoice line? |

Write definitions next to the code/query that computes them (comments or a
`metrics.md`). Two dashboards showing "the same" KPI with different numbers is
a trust killer.

## 2. ETL / Data Loading

### Patterns

| Pattern | When |
|---------|------|
| Direct query on operational DB | Small data, live freshness needed |
| Materialized tables + cache (TTL) | Repeated heavy aggregations |
| Incremental load (append since last max date) | Large append-only events |
| ELT (load raw, transform in warehouse) | Lake/warehouse setups |

### Cache in Postgres pattern

```sql
CREATE TABLE bi_sheets (
    id         BIGSERIAL PRIMARY KEY,
    source_key TEXT NOT NULL UNIQUE,   -- ex.: 'sheet:ID' or 'metric:abc'
    payload    JSONB NOT NULL,
    loaded_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

```sql
-- read with TTL (e.g. 10 minutes)
SELECT payload
FROM bi_sheets
WHERE source_key = :key
  AND loaded_at > now() - interval '10 minutes';
```

### Reading Google Sheets

Load **all tabs** with their real GIDs (spreadsheet IDs change between tabs).
Normalize column names, detect the date column, and cast types. Never assume a
fixed sheet layout — make the loader tolerant to extra/renamed columns.

## 3. SQL Recipes

### Period comparison (monthly trend)

```sql
SELECT
    date_trunc('month', data_movto) AS mes,
    count(DISTINCT cliente_id)      AS clientes,
    sum(valor)                      AS receita
FROM movimentos
WHERE data_movto >= :inicio AND data_movto <= :fim
GROUP BY 1
ORDER BY 1;
```

### Curva ABC (80/20) — Pareto por cliente

```sql
WITH base AS (
    SELECT cliente_id, sum(valor) AS total
    FROM movimentos
    WHERE data_movto BETWEEN :inicio AND :fim
    GROUP BY cliente_id
),
acumulado AS (
    SELECT
        cliente_id,
        total,
        sum(total) OVER (ORDER BY total DESC) AS acumulado,
        sum(total) OVER ()                    AS total_geral,
        row_number() OVER (ORDER BY total DESC) AS rn
    FROM base
)
SELECT
    cliente_id,
    total,
    round(100.0 * acumulado / total_geral, 2) AS pct_acumulado,
    CASE WHEN acumulado <= 0.80 * total_geral THEN 'A'
         WHEN acumulado <= 0.95 * total_geral THEN 'B'
         ELSE 'C' END                          AS classe
FROM acumulado
ORDER BY rn;
```

### Last purchase per customer (for reactivation lists)

```sql
SELECT DISTINCT ON (cliente_id) cliente_id, data_movto AS ultima_compra
FROM movimentos
ORDER BY cliente_id, data_movto DESC;
```

## 4. Dashboard Design

### Layout hierarchy

```
Page title + period selector + export button
├─ KPI cards row (value + delta vs previous period + sparkline)
├─ Trend chart (monthly/quarterly)
├─ Geographic distribution (map or top states)
├─ ABC curve / customer concentration
└─ Top-N tables (products, customers, reps) with drill-down
```

### Rules

- **One number per KPI card**, with the comparison period explicit ("vs mês anterior").
- Default period smartly (current month) with quick shortcuts: mês atual, passado, trimestre, semestre, 12 meses.
- Sort tables and allow export (CSV/Excel/PDF) — users will always want raw data.
- **Performance:** aggregate server-side; return small JSON; load async with skeletons. A dashboard that takes 10s is abandoned.
- Cache heavy aggregations (see §2) instead of computing on every page load.

## 5. Forecasting (simple)

Start with a baseline trend before any ML:

- **Moving average** (3/6/12 months) — good default.
- **Year-over-year** growth applied to recent run-rate.
- **Seasonality:** compare same month last year, not just previous month.
- Only escalate to regression/time-series (Prophet/ARIMA) when trend is noisy.

Present forecasts with explicit assumptions ("baseado nos últimos 12 meses,
sem sazonalidade de fim de ano") — never as a black box.

## 6. Export and Sharing

- CSV/Excel: streams; Excel with `jspdf-autotable`/`xlsx` libs for formatted exports.
- PDF: paginated, with date filters in the header and a "gerado em" stamp for auditability.
- Scheduled reports: n8n schedule → query → send (see `n8n-workflow-automation`).

## Examples

### Example 1: KPI cards with delta

```
Receita:     R$ 1.234.567  ▲ +12% vs mês anterior
Clientes:    890           ▼ -3% vs mês anterior
Ticket médio: R$ 1.387     ▲ +4%
```

### Example 2: React + Recharts dashboard snippet

```tsx
import { Card, CardHeader, CardTitle } from "@/components/ui/card"
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts"

export function TrendCard({ data }: { data: { mes: string; receita: number }[] }) {
  return (
    <Card>
      <CardHeader><CardTitle>Evolução da Receita</CardTitle></CardHeader>
      <ResponsiveContainer width="100%" height={220}>
        <LineChart data={data}>
          <XAxis dataKey="mes" />
          <YAxis tickFormatter={(v) => `R$ ${(v / 1000).toFixed(0)}k`} />
          <Tooltip formatter={(v) => `R$ ${Number(v).toLocaleString("pt-BR")}`} />
          <Line type="monotone" dataKey="receita" stroke="#3b82f6" />
        </LineChart>
      </ResponsiveContainer>
    </Card>
  )
}
```

## Notes

- Define metrics precisely; undefined metrics produce arguments, not insights.
- Cache aggressively; a BI screen must load in < 2s.
- Offer exports always — dashboards complement spreadsheets, they don't replace them.
- Pair with `rag-llm` to answer "why did sales drop" questions over the data, and with `n8n-workflow-automation` for scheduled reports.

## References

- [Recharts](https://recharts.org/)
- [Metabase](https://www.metabase.com/)
- [KPI definition guide](https://www.briantracy.com/blog/define-kpi)
- [Pareto / ABC analysis](https://www.investopedia.com/terms/p/paretoprinciple.asp)
