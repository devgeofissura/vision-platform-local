---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: fabric-mill-sales
description: "B2B selling for a flat-woven fabric mill: specs, sampling, MOQ, quoting, negotiation and CRM"
category: commercial
version: 0.1.0
author: devtiagoabreu
tags: [commercial, fabrics, textile, b2b, sales, crm, moq]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Access to the mill's product data (composition, grammage, width, finishes)
  - A CRM (Pipedrive, HubSpot, RD Station) or spreadsheet for the pipeline
  - Cost and production capacity data from the weaving department
provides:
  - Technical specification sheets and fabric classification knowledge
  - Sampling and MOQ management workflows
  - Quotation templates with price per meter and volume discounts
  - Negotiation and follow-up cadences for B2B textile sales
  - A CRM pipeline structure for the textile sales team
---

# Fabric Mill Sales

## Overview

This skill covers the complete B2B sales workflow of a flat-woven fabric
mill selling to garment makers (confeccoes) and furniture makers. It goes
from reading a fabric technical spec sheet to closing the deal and
managing the customer in the CRM.

Fabrics are a commodity-like product, so the sales edge comes from
technical credibility and process discipline: knowing the spec, quoting
fast, managing samples correctly, and following up without annoying the
buyer. This skill gives you the templates and checklists to run that
process consistently.

## Prerequisites

- Product master data: composition, grammage (g/m2), width, finishes
- Production data: loom capacity, MOQ, standard lead time
- Cost data: yarn cost, weaving cost, finishing cost per meter
- A CRM with pipeline stages, or a spreadsheet you can maintain
- Access to the Brazilian buyer context (confecções, vestuário)

## Usage Instructions

### 1. Reading and Building the Technical Spec Sheet

Every quote starts from the spec sheet. Standardize how the product is
described so production and sales speak the same language.

```text
Spec sheet fields:

  Reference      - internal code (e.g. SARJA_PE_DIAGONAL)
  Composition    - cotton, polyester, viscose, elastane + %
  Weave / tie    - plain (tela), twill (sarja), satin (cetim), jacquard
  Grammage       - g/m2 (e.g. 185)
  Useful width   - meters (e.g. 1.50; 1.60)
  Density        - ends/cm and picks/cm (urdume/trama)
  Finish         - dyeing, printing, softening, water repellency
  Shrinkage      - expected % after washing
  Color fastness - standard used (e.g. ABNT)
  MOQ            - minimum meters per item
  Lead time      - days after sample approval
```

Rules: never quote without composition and grammage; always confirm the
width because price per meter assumes a given width; record shrinkage and
fastness because they are the top complaint sources.

### 2. Sampling and MOQ Management

B2B fabric buyers approve a sample before buying volume. Treat sampling as
a controlled sales step, not a favor.

```text
Sample workflow:

1. Register the sample request in the CRM (date, product, quantity)
2. Send 1 m per item, free, freight paid by customer
3. Track delivery and confirm receipt within 3 days
4. Log the customer's technical approval or rejection
5. If rejected, capture the reason and adjust the spec or price
6. Move the deal to quotation only after approval

MOQ policy example:
  - Standard MOQ: 1,200 m per item
  - Below MOQ: +10% surcharge, subject to loom schedule
  - Above 20,000 m: discount band applies (see pricing)
```

Track the sample-to-approval conversion rate: if it drops below 30%, the
spec or the price is wrong, not the customer.

### 3. Quoting and Pricing

Price per meter is the standard unit, but you must know the cost per
square meter and per kg to defend the price in negotiation.

```text
Cost build-up per linear meter:

  Yarn cost        R$ 5.20
  Weaving cost     R$ 2.10
  Finishing cost   R$ 1.40
  = Production     R$ 8.70
  + 12% waste      R$ 1.04  -> R$ 9.74
  + 8% SG&A        R$ 0.78  -> R$ 10.52
  + 25% margin     R$ 2.63  -> R$ 13.15  (base price/m)

Discount bands by volume:
  Up to 5,000 m            list price
  5,001 - 20,000 m         -4%
  Above 20,000 m           -8% (always check capacity first)

Quote fields:
  - Item, fabric ref, grammage, width, price/m, qty
  - Subtotal, freight (CIF/FOB), payment terms, validity
  - MOQ and lead time per item, sample note
```

Rules: price in Reais per meter; freight rule stated up front (CIF above
10,000 m is common in Brazil); quote validity of 10-15 days.

### 4. Negotiation and Follow-Up Cadence

Negotiation in textiles is about volume and payment terms, not unit
discounts. Trade discounts for commitment.

```text
Concessions in order of preference:
  1. Payment terms (30/60/90 days) for a standing order
  2. Volume commitment (x meters per month, 6 months)
  3. Exclusivity of an item/color for a season
  4. Only last: unit price discount

Follow-up cadence:
  Day 0   - send quote
  Day 3   - confirm receipt + answer technical questions
  Day 7   - ask for decision / approval status
  Day 14  - quote expires or extend with new offer
  After   - if won: onboarding; if lost: capture reason
```

Never call a buyer daily. Space the follow-up and always add value:
send a new finish, a capacity slot, or a market note.

### 5. CRM Pipeline Structure

Keep the pipeline readable by the whole team. Every deal gets the same
fields so reports and forecasts are reliable.

```text
Pipeline stages:
  1. Prospecting      - new confecção identified
  2. Sampled          - sample sent, awaiting approval
  3. Quotation        - quote sent, awaiting decision
  4. Negotiation      - terms being discussed
  5. Won / Lost

Deal fields:
  - customer, contact, phone, email
  - fabric ref, grammage, width, quantity (m)
  - unit price, total value, currency
  - expected close date, source (indication, event, cold call)
  - last touch date, next action date
```

Keep the next action field mandatory: a deal without a next action is a
dead deal.

## Examples

### Example 1: Full Quotation for a Confecção

```text
Proposta #PT-2026-0412
Cliente: Confecção Veste Bem LTDA
Contato: (11) 99999-1234 | compras@vestebem.com.br

Item | Tecido          | Gramatura | Largura | Preço/m  | Qtde (m)
1    | Sarja Diagonal  | 185 g/m²  | 1,50 m  | R$ 11,90 | 8.000
2    | Tela Algodão    | 120 g/m²  | 1,60 m  | R$ 9,80  | 5.000

Subtotal: R$ 144.200,00
Frete: CIF São Paulo, incluso acima de 10.000 m
Condição: 30/60 dias | Validade: 15 dias
MOQ: 1.200 m/item | Prazo: 25 dias úteis após amostra
Amostra: 1 m por item, grátis, frete por conta do cliente
```

### Example 2: CRM Deal Entry (JSON)

```json
{
  "deal": "D-2026-0901",
  "stage": "quotation",
  "customer": "Confecção Veste Bem LTDA",
  "contact": { "name": "Ana Souza", "phone": "5511999991234" },
  "product": {
    "ref": "SARJA_PE_DIAGONAL",
    "grammage_g_m2": 185,
    "width_m": 1.5,
    "quantity_m": 8000,
    "unit_price": 11.9,
    "total": 95200.0
  },
  "timeline": {
    "sample_sent": "2026-07-20",
    "sample_approved": "2026-07-28",
    "quote_sent": "2026-07-30"
  },
  "expected_close": "2026-08-14",
  "next_action": "call buyer on 2026-08-05 for decision"
}
```

## Best Practices

- Quote from an approved spec sheet, never from memory
- Sample fast: approval is the gate to quotation
- State freight terms and payment conditions in every quote
- Trade discounts for volume or payment commitments
- Track sample-to-approval and quote-to-close conversion rates
- Keep one mandatory "next action" per CRM deal
- Update loom capacity regularly so you never overpromise lead time

## Pitfalls / Common Mistakes

- Quoting without width and grammage (prices become incomparable)
- Giving unit discounts instead of volume or terms concessions
- Following up every day and burning the relationship
- Overpromising lead time without checking loom capacity
- Ignoring shrinkage and fastness complaints after delivery
- Letting deals sit in the CRM without a next action

## References

- [SEBRAE - mercado de vestuário e confecção](https://www.sebrae.com.br)
- [ABIT - Associação Brasileira da Indústria Têxtil](https://www.abit.org.br)
- [CNI - Portal da Indústria](https://www.portaldaindustria.com.br)
- [ABNT - normas técnicas têxteis](https://www.abnt.org.br)
- [Pipedrive - pipeline de vendas](https://www.pipedrive.com)

## Notes

- Prices in the examples are illustrative; use your own cost structure
- Brazilian buyers commonly expect CIF quotes on large volumes
- Benchmark sample-to-approval conversion against your own history
