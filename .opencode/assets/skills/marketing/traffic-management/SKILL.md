---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: traffic-management
description: Meta Ads and Google Ads budget, bidding and audience segmentation config
category: marketing
version: 0.1.0
author: devtiagoabreu
tags: [traffic, meta-ads, google-ads, budget, bidding, segmentation]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - An active Meta Business and Google Ads account
  - Conversion tracking installed (Meta pixel / Google tag)
  - Monthly budget defined and marketing objectives clear
provides:
  - Meta Ads campaign setup with budget and targeting config
  - Google Ads campaign with bidding strategy and keywords
  - UTM tagging and reporting checklist
---

# Traffic Management

## Overview

This skill explains how to configure and manage paid traffic on Meta Ads
(Facebook/Instagram) and Google Ads: choosing campaign objectives, setting
budgets, configuring bids, and building the right audience segmentation. The
focus is operational: exact fields, realistic values, and a workflow to launch,
monitor, and optimize campaigns.

Traffic management is about control: knowing where each dollar goes, how the
auction behaves, and when to scale or pause.

## Prerequisites

- Access to Meta Business Suite and Google Ads account
- Conversion events active (Pixel, CAPI, or Google tag) for at least 1 week
- A defined monthly budget and a target CPA or ROAS
- Basic understanding of audiences and keywords

## Usage Instructions

### 1. Configuring a Meta Ads Campaign

For conversion campaigns, the objective and the audience are the most
important decisions. Start with a broad audience and let the algorithm learn,
then narrow based on data.

```text
Meta Ads campaign setup - Purchase objective

Campaign:
  Objective          : Sales (conversion)
  Special ad category: None (general products)
  Budget (CBO)       : R$ 50.00/day lifetime or daily
  Scheduling         : Run always
  Attribution        : 7-day click / 1-day view

Ad Set:
  Optimization event : Purchase
  Bid strategy       : Lowest cost (no cap) at launch
  Daily budget share : 100% of campaign budget

  Audience:
    Location      : Brazil, radius none
    Age           : 25-45
    Gender        : All
    Interests     : None (broad) for prospecting
    Exclude       : Website visitors of last 180 days (retargeting)
    Placements    : Advantage+ placements

Ad:
  Format       : 1:1 video (9:16 for stories is auto-cropped)
  Primary text : benefit + 1 CTA + scarcity
  Link         : URL with UTM parameters
  CTA button   : "Comprar agora" / "Shop Now"

Note: for retargeting campaigns use:
  Audience: Custom audience of website visitors 30 days
  Advantage+ placements, same optimization event
```

### 2. Configuring a Google Ads Search Campaign

Search intent is high, so the campaign should be tightly organized around
commercial keywords with negative keywords to protect spend.

```text
Google Ads setup - Search campaign

Campaign:
  Type         : Search
  Goal         : Sales
  Budget       : R$ 30.00/day
  Bidding      : Maximize conversions with target CPA R$ 25
  Network      : Search only (uncheck display partners)

Ad Group: "tênis de corrida masculino"
  Keywords (exact + phrase):
    [tenis de corrida masculino]
    "tenis corrida masculino preço"
    [tênis corrida masculino 42]
  Negative keywords:
    -gratuito  -pdf  -frete grátis site:job  -curso  -meia  -usado

Ad copy:
  Headline 1: Tênis de Corrida Masculino
  Headline 2: Frete Grátis | Parcele em 12x
  Headline 3: Modelo 2026 em até 3x sem juros
  Description: Envio imediato, troca grátis em 30 dias.

Extensions: sitelinks, callouts, structured snippets, prices.

Suggestion keywords (phrase) for later:
  "tênis corrida feminino" , "tênis corrida pronador" , "tênis corrida amortecedor"
```

### 3. Budget Management and Optimization Routine

Budget is a lever, not a setting: adjust it weekly based on performance, and
scale only when CPA/ROAS are on target. Never double the budget in one day.

```text
Weekly optimization routine:

Monday:
  - Export performance from both platforms into the report sheet
  - Flag campaigns with ROAS < 2.0 or CPA > target +20%
  - Check frequency on Meta (target < 3) and search terms on Google

Wednesday:
  - Pause non-converting ad sets/ads (spend > 1x CPA without results)
  - Add irrelevant search terms as negatives in Google
  - Refresh creative on ads with frequency > 4 (Meta)

Friday:
  - Scale winners: +15-20% budget, only if ROAS >= target
  - Never scale more than one variable at a time
  - Document decisions in the campaign log

Budget model (R$ 3,000/month example):
  Prospecting (Meta): R$ 1,200
  Retargeting (Meta): R$ 600
  Google Search:      R$ 1,000
  Google Shopping:    R$ 200
  Total:              R$ 3,000

Rule: shift budget between lines only after 14 days of data.
```

## Examples

### Example 1: UTM Tagging Standard

```text
UTM structure:
  https://seulink.com.br/produto?utm_source=facebook
    &utm_medium=cpc&utm_campaign=retarg_purchase
    &utm_content=video_v1&utm_term=visitors30d

Preset UTM values:
  source: facebook | google | instagram | tiktok | newsletter
  medium: cpc | cpm | email | organic | referral
  campaign: objective_audience (e.g., retarg_purchase)
  content: ad id or creative name
  term: keyword or audience segment

Audit: monthly check that every ad link contains the 5 UTM fields.
```

### Example 2: Launch Checklist for Both Platforms

```text
[ ] Conversions verified in Events Manager (Meta) / Conversions (Google)
[ ] Budget per campaign defined and consistent with monthly cap
[ ] Bid strategy selected (lowest cost on launch, tCPA after 30 conv.)
[ ] Audience excludes existing customers if retargeting is separate
[ ] UTM tags on every destination URL
[ ] Landing page loads fast (Lighthouse mobile score >= 60)
[ ] Pixel/tag fires on the thank-you page
[ ] Daily budget cap in place (no blank check campaigns)
[ ] Alerts configured: spend > 2x budget or 0 conversions in 5 days
```

## Best Practices

- Use a single conversion objective per campaign; consolidate data
- Launch with broad audiences and let the algorithm gather signal
- Let campaigns accumulate 30-50 conversions before changing bids
- Scale budget in steps of 15-20%, not 2x
- Keep creative refresh schedule: video weekly, static bi-weekly
- Use negative keywords lists and exclusions aggressively
- Centralize reporting with consistent UTM and naming

## Pitfalls / Common Mistakes

- Launching conversion campaigns before tracking is verified (wasted spend)
- Changing bidding strategy too often and resetting the learning phase
- Using daily budgets on both campaign and ad set level (double counting)
- Cutting spend on a campaign after 2 days of low results
- Forgetting to exclude buyers from prospecting audiences
- Scaling budget faster than the funnel can convert

## References

- [Meta Ads Manager Help Center](https://www.facebook.com/business/help)
- [Google Ads Help - Bidding Strategies](https://support.google.com/google-ads/answer/2472725)
- [Google Ads - Negative Keywords](https://support.google.com/google-ads/answer/2453972)
- [Meta Business Suite - Advantage+ Placements](https://www.facebook.com/business/help/2405092116183307)
- [Google Campaign Manager 360 - UTM Builder](https://ga-dev-tools.google/campaign-url-builder/)

## Notes

- Account learning phase (Meta) resets on major changes; keep it stable
- Target CPA should be based on your margin, not on the platform suggestion
- Budget allocation is an ongoing decision; review monthly with the P&L
