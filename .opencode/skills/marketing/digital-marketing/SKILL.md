---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: digital-marketing
description: Campaign structure, marketing funnel and core metrics like ROAS and CAC
category: marketing
version: 0.1.0
author: devtiagoabreu
tags: [marketing, campaigns, funnel, metrics, roas, cac]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - A marketing channel account (Meta, Google) or access to campaign data
  - Basic spreadsheet skills for calculating metrics
provides:
  - Campaign architecture and naming convention templates
  - Funnel stages with conversion rate benchmarks
  - ROAS, CAC, and LTV calculations with worked examples
---

# Digital Marketing

## Overview

This skill covers the fundamentals of running digital marketing campaigns that
can be measured and improved: how to structure an account (campaigns, ad
groups, ads), how to map the sales funnel, and how to compute the metrics that
matter (ROAS, CAC, LTV, conversion rate). It applies to Meta Ads, Google Ads,
TikTok, and most programmatic channels.

The goal is not just to spend budget, but to spend it profitably. Every
decision should be grounded in the numbers, so a reporting routine is part of
the workflow.

## Prerequisites

- An active ads account or access to past campaign performance data
- A conversion event installed (Meta pixel / Google tag) to measure results
- A spreadsheet or BI dashboard to consolidate metrics
- Basic understanding of revenue and cost

## Usage Instructions

### 1. Structuring Campaigns and Ad Groups

A clean account structure makes optimization possible. One campaign per
objective and per budget, with ad groups separating audiences, creatives, and
placements. Use a consistent naming convention so anyone can read the account.

```text
Naming convention:
  [Channel]_[Country]_[Objective]_[Audience]_[Creative]_[Date]
  Example: FB_BR_Purchase_Retargeting_Video_v1_20260801

Account structure (Meta Ads example):

Campaign: FB_BR_Purchase_Retargeting
  Ad Set: FB_BR_Retargeting_Visitors30d
    - Audience: website visitors last 30 days
    - Placement: Feed + Reels + Stories
    - Bid: Lowest cost with cap R$ 25 CPM
    Ad: FB_BR_Retargeting_Video_v1
    Ad: FB_BR_Retargeting_Carousel_v1

Campaign: FB_BR_Purchase_Prospecting
  Ad Set: FB_BR_Prospecting_Lookalike2%
    - Audience: Lookalike of buyers, 2%
    - Placement: Feed only
    Ad: FB_BR_Prospecting_Static_v1

Rules:
  - Max 3-4 ad sets per campaign, 2-3 ads per ad set
  - Group by audience and by message, not by random split
  - Start with one conversion objective per campaign
```

### 2. Mapping the Marketing Funnel

The funnel organizes the journey from awareness to purchase. Define each stage,
the expected conversion rates, and the content that moves people forward. This
makes it possible to diagnose where the leak is.

```text
Funnel stages and reference conversion rates (e-commerce):

  STAGE              ACTION                    CONV RATE (ref)
  Awareness          Impressions / reach        -
  Interest           Clicks / visits            CTR 1.0-2.5%
  Consideration      Add to cart / signup       2.0-6.0%
  Intent             Checkout started            1.5-3.0%
  Purchase           Conversion (sale)           1.0-3.0%
  Retention          Repeat purchase            15-30% (within 90d)

Example funnel (1,000,000 impressions):

  Impressions      1,000,000
  Clicks (2%)          20,000
  Sessions                18,000
  Add to cart (3%)           540
  Purchase (40% of cart)     216
  CR overall = 216 / 18,000 = 1.2%

Diagnosis: if cart-to-purchase is 40% the bottleneck is traffic
quality; if it is 5%, the problem is the checkout or the offer.
```

### 3. Calculating the Core Metrics

ROAS, CAC, and LTV are the numbers that tell you if the channel pays for
itself. Define the calculation window consistently and build a weekly report.

```text
Definitions and formulas:

ROAS (Return On Ad Spend) = Revenue from ads / Ad spend
CAC (Customer Acquisition Cost) = Ad spend / New customers
LTV (Lifetime Value) = Average ticket x Purchase frequency x Margin
LTV/CAC ratio: target >= 3.0 for healthy unit economics

Worked example (month):

  Ad spend:            R$ 8,000.00
  Revenue from ads:    R$ 28,000.00
  New customers:            140

  ROAS = 28,000 / 8,000 = 3.5
  CAC  = 8,000 / 140    = R$ 57.14

  Average ticket       = R$ 200.00
  Avg purchases/year   = 2.5
  Gross margin         = 40%
  LTV = 200 x 2.5 x 0.40 = R$ 200.00

  LTV/CAC = 200 / 57.14 = 3.50 -> healthy

Sensitivity: if CAC rises to R$ 90, LTV/CAC = 2.2 < 3.0
-> stop scaling, fix offer or audience first.
```

## Examples

### Example 1: Building a Weekly Performance Report

```text
Week | Spend     | Revenue   | ROAS  | New Cx | CAC    | Conv. rate
01   | R$ 1,500  | R$ 5,100  | 3.40  |   26   | R$ 57.7 | 1.4%
02   | R$ 2,000  | R$ 6,400  | 3.20  |   31   | R$ 64.5 | 1.3%
03   | R$ 2,500  | R$ 9,000  | 3.60  |   40   | R$ 62.5 | 1.6%
04   | R$ 3,000  | R$ 10,800 | 3.60  |   49   | R$ 61.2 | 1.7%

Trend: ROAS stable, CAC slightly up but controlled, conv. rate improving.
Decision: keep scaling spend +15% per week while ROAS >= 3.0.
```

### Example 2: Allocating Budget Across Channels

```text
Channel   | Spend  | Revenue  | ROAS | CAC    | Notes
Facebook  | R$ 5,000 | R$ 17,500 | 3.50 | R$ 62 | Retargeting strong
Google    | R$ 3,000 | R$ 10,200 | 3.40 | R$ 55 | Search converts fast
TikTok    | R$ 1,000 | R$  2,400 | 2.40 | R$ 90 | Testing phase

Reallocation proposal:
  Facebook: +10% (R$ 5,500)  - proven ROAS
  Google  : +10% (R$ 3,300)  - steady
  TikTok  : -20% (R$ 800)    - below target, test new angle first
```

## Best Practices

- Define one primary conversion event per campaign and track it consistently
- Review metrics weekly, not daily, to avoid noise-driven decisions
- Use attribution windows consistently across all channels
- Always segment reporting by campaign and by audience
- Test one variable at a time: creative, audience, or bid
- Combine ROAS with CAC and LTV for the full picture
- Document the funnel assumptions so the team argues with data

## Pitfalls / Common Mistakes

- Optimizing for clicks instead of purchases (vanity metrics)
- Scaling spend before the funnel converts profitably
- Using different attribution windows in the same report
- Ignoring returning customers when computing CAC
- Judging performance on a single day of data
- Changing creatives, audiences, and bids in the same experiment

## References

- [Google Marketing Platform: Measurement Guide](https://marketingplatform.google.com/intl/en/about/resources/)
- [Meta Business Help Center](https://www.facebook.com/business/help)
- [Google Ads Help](https://support.google.com/google-ads)
- [Kotler: Marketing Management - Funnel Concepts](https://www.pearson.com/en-us/subject-catalog/p/marketing-management.html)

## Notes

- Benchmarks vary by vertical; always compare to your own historical data
- ROAS should be computed against contribution margin for profit decisions
- Attribution is imperfect; use the same model for all comparisons
