---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: google-workspace-analytics
description: Build analytics on Google Workspace with Sheets formulas, Looker Studio dashboards, and Apps Script automation.
category: web
version: 0.1.0
author: devtiagoabreu
tags: [google-sheets, looker-studio, apps-script, analytics, dashboards, data]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - A Google Workspace or Gmail account
  - Access to Looker Studio (studio.google.com)
  - Basic spreadsheet and SQL concepts
provides:
  - Sheets formulas for cleaning and aggregation
  - Looker Studio data-source and dashboard setup
  - Apps Script automation patterns
  - Scheduled refresh and sharing practices
---

# google-workspace-analytics

## Overview

Google Workspace is a low-friction analytics stack: Google Sheets for
storage and formulas, Looker Studio for dashboards, and Apps Script for
automation. You can go from raw export to a refreshed executive
dashboard in an afternoon, without a data warehouse.

The sweet spot is operational reporting (sales, support tickets, finance
exports). When volumes grow past roughly 500k rows or you need SQL-level
joins, move upstream to BigQuery and keep Looker Studio pointing there.

## Prerequisites

- A Google account with Sheets, Drive, and Looker Studio access
- Source data in Sheets (CSV paste, export, or a form/API feed)
- Basic understanding of formulas and pivot concepts
- Apps Script editor access (Extensions > Apps Script)

## Usage Instructions

### 1. Cleaning and Aggregation Formulas

Normalize messy exports before building charts: trim whitespace, parse
dates, and classify values. `QUERY` is your SQL in Sheets:

```text
=QUERY(raw!A:E,
  "SELECT B, SUM(D)
   WHERE B IS NOT NULL AND C = 'closed'
   GROUP BY B
   ORDER BY SUM(D) DESC
   LABEL SUM(D) 'Revenue'",
  1)
```

Clean individual columns with `TRIM`, `PROPER`, and `REGEXEXTRACT`:

```text
=TRIM(raw!B2)
=REGEXEXTRACT(raw!C2, "([A-Z]{2,3})")
=DATEVALUE(TEXT(raw!D2, "yyyy-mm-dd"))
```

### 2. Pivot Tables for Exploration

Use Insert > Pivot table for ad-hoc slicing and point charts at the
pivot output. For live dashboards prefer a `QUERY`-based pivot so
appended rows flow through automatically:

```text
=QUERY(raw!A:E,
  "SELECT B, COUNT(D), SUM(D)
   GROUP BY B
   PIVOT C",
  1)
```

### 3. Looker Studio Setup

Connect Looker Studio to the Sheets file, define one data source per
granularity, and build charts off a shared date-range control.

```text
Data source: Google Sheets -> sheet "closed_deals"
Date field:  closed_date
Metrics:     SUM(revenue)
Dimensions:  region, product
```

Setup checklist: create a data source, add a date-range control, add
filters per page, and refresh the sheet before the scheduled report
delivery.

### 4. Apps Script Automation

Automate refresh, emailing, and light data transformations with Apps
Script. A daily rollup from a raw tab into a reporting tab:

```javascript
function rollupDaily() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const raw = ss.getSheetByName("raw");
  const data = raw.getDataRange().getValues();
  const byDate = {};
  for (let i = 1; i < data.length; i++) {
    const d = data[i][0].toISOString().slice(0, 10);
    byDate[d] = (byDate[d] || 0) + data[i][2];
  }
  const out = Object.entries(byDate).map(([d, v]) => [d, v]);
  out.sort((a, b) => (a[0] < b[0] ? -1 : 1));
  ss.getSheetByName("report").getRange(2, 1, out.length, 2)
    .setValues(out);
}
```

Schedule with a time-driven trigger:

```javascript
ScriptApp.newTrigger("rollupDaily")
  .timeBased().atHour(6).everyDays(1).create();
```

## Best Practices

- Keep one raw tab per source and never edit it; transform into other tabs.
- Name ranges and tabs exactly — Looker Studio binds to sheet names.
- Use `QUERY` with `LIMIT 100` while prototyping to avoid long runs.
- Pin dates to a control so all charts answer the same window.
- Test Apps Script against a copy before scheduling on shared sheets.

## Pitfalls / Common Mistakes

- Editing raw data and losing provenance, making the dashboard undebuggable.
- Using `SUMIF` loops over 50k rows instead of one `QUERY`.
- Looker Studio caching stale data; the sheet must refresh before the report.
- Hardcoding sheet names in Apps Script, breaking when renamed.
- Sharing the dashboard before removing formula columns from the data source.

## Examples

### Example 1: MTD revenue

```text
=SUMIFS(raw!D:D, raw!A:A, ">="&DATE(YEAR(TODAY()), MONTH(TODAY()), 1))
```

### Example 2: Unique customers

```text
=COUNTUNIQUE(IF(raw!C:C="closed", raw!B:B, ""))
```

## References

- [Google Sheets function list](https://support.google.com/docs/table/25273)
- [Looker Studio documentation](https://support.google.com/looker-studio/)
- [Apps Script reference](https://developers.google.com/apps-script/reference)
