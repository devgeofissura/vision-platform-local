---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: ecommerce-commerce
description: "Ecommerce commercial operations: catalog, SKU, pricing, channels, funnel, returns and omnichannel"
category: commercial
version: 0.1.0
author: devtiagoabreu
tags: [commercial, ecommerce, catalog, sku, pricing, marketplace, omnichannel]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Product master data (attributes, images, NCM, cost)
  - A storefront or marketplace account and order data
  - Cost, freight and tax structure for the product line
provides:
  - Catalog structure and SKU naming conventions
  - Pricing model with margin, freight and channel fees
  - Marketplace and channel management checklist
  - Stock control formulas (reorder point, safety stock)
  - Order funnel metrics and returns policy templates
  - Omnichannel operating rules for one inventory
---

# Ecommerce Commerce

## Overview

This skill covers the commercial side of running an ecommerce operation:
how to structure the catalog and SKUs, how to price with margin, how to
manage sales channels (own store, marketplaces), how to control stock,
how to measure the order funnel, and how to define returns and omnichannel
rules.

The guiding principle is that price must cover cost, freight, channel
fees, taxes and returns — while still leaving margin. Every section below
gives you a template or a formula you can adapt to your catalog.

## Prerequisites

- Product data: name, attributes, images, NCM, unit of sale
- Cost structure: product cost, average freight, channel fees
- Access to sales data: visits, orders, conversion, stock levels
- Defined returns policy before scaling paid traffic

## Usage Instructions

### 1. Structuring the Catalog and SKUs

A clean catalog makes everything else possible: filtering, inventory,
marketplace feeds and reporting.

```text
SKU naming rule:
  [CATEGORY]-[PRODUCT]-[ATTRIBUTES]-[VARIANT]
  Example: TEC-SARJA-PE-185-0150-AZUL
           (tecido, sarja, poliéster, 185 g/m2, 1,50 m, azul)

Catalog rules:
  - One SKU per variation (color, size, grammage)
  - Standard attribute set: composition, measures, weight, finish
  - Unique EAN/UPC for every sellable variant
  - NCM per product line (taxes depend on it)
  - Photos and descriptions mandatory before activating the SKU
  - Block SKUs with no inventory instead of letting them show "sold out"
```

Never reuse SKUs across products; a wrong SKU corrupts stock and tax
reporting.

### 2. Pricing with Margin

Price is not a guess. Build it from cost plus freight plus channel fees
plus target margin, then sanity-check against the market.

```text
Price build-up:
  Product cost         R$ 8.90
  Average freight      R$ 1.20
  Channel fees (taxa)  R$ 0.45
  = Cost before margin R$ 10.55
  Target margin 25%:   price = 10.55 / (1 - 0.25) = R$ 14.07
  Round to market      R$ 14.20

Channel effect (same product):
  Own store   price 14.20, fee 0%     -> margin 25.7%
  Marketplace price 15.90, fee 16%    -> net 13.36, margin 20.9%
  Marketplace with free shipping: raise price to cover freight

Review triggers:
  - Any change in product cost or freight
  - Exchange rate moves for imported inputs
  - Competitor repositioning (check weekly, not daily)
```

Always recompute margin when a channel changes its fee structure.

### 3. Managing Channels and Marketplaces

Different channels have different economics. Keep the product strategy
but adapt price, logistics and content per channel.

```text
Channel setup checklist:
  - Catalog feed synced (name, EAN, price, stock)
  - Price rule per channel (fee and freight differ)
  - Logistics: fulfilled by us vs marketplace (FBA-like)
  - Reputation metrics: delivery time, cancellation, review score
  - Return policy adapted to each channel's rules

Channel economics:
  - Own store: control, no fee, but you pay for traffic
  - Marketplaces: traffic included, but fee + reputation pressure
  - Social commerce: high engagement, smaller average order
```

Protect marketplace reputation: a canceled order hurts ranking more than
a slightly higher price.

### 4. Controlling Stock

Stock out costs sales and ranking; excess stock burns cash. Use reorder
point and safety stock formulas.

```text
Reorder point = daily demand x lead time + safety stock

Example:
  Daily demand       = 120 units
  Supplier lead time = 12 days
  Safety stock       = 500 units (covers demand variability)
  Reorder point      = (120 x 12) + 500 = 1.940 units

Stock rules:
  - Never sell from negative stock: sync channels
  - Safety stock sized by demand variability, not a fixed week
  - Review slow movers quarterly: discount or delist
  - Keep one physical inventory for all channels (omnichannel)
```

A reorder point of zero is a promise to run out of stock.

### 5. Measuring the Order Funnel

The funnel shows where money is lost: traffic, product page, checkout or
payment.

```text
Funnel and reference conversion rates (ecommerce):
  Visits          100%      (baseline)
  Product views   70-85%    of visits
  Add to cart      8-15%    of product views
  Checkout started 50-70%   of add-to-cart
  Purchase (paid)  60-75%   of checkout started
  Overall CR       2-4%     healthy for general retail

Example (10,000 visits):
  Product views  8,000
  Add to cart      800
  Checkout         500
  Paid orders      350
  CR = 350 / 10,000 = 3.5%

Diagnosis:
  Low add-to-cart -> offer, price or product page
  Low checkout -> shipping surprise, registration wall
  Low paid rate -> payment methods or antifraud
```

Track the funnel per channel and per product family.

### 6. Returns and Omnichannel

A clear returns policy protects margin and trust. Omnichannel means the
customer flows freely between channels, with one inventory.

```text
Returns policy template:
  - Exchange window: 7 days for fabrics (sealed, unwashed)
  - Defect: full refund or exchange, freight paid by us
  - Change of mind: accepted, customer pays return freight
  - Steps: request by ticket -> code/QR for return -> inspect -> refund
  - Refund in 5 business days after inspection

Omnichannel rules:
  - One stock level across store, marketplaces and physical shop
  - Buy online, pick up in store (retirada na loja)
  - Returns accepted in any physical point
  - Customer history unified in the CRM
```

Track return reasons; a high return rate on a SKU usually means a spec
or photo problem, not a customer problem.

## Examples

### Example 1: SKU Registration (JSON)

```json
{
  "sku": "TEC-SARJA-PE-185-0150-AZUL",
  "nome": "Sarja Diagonal Poliéster 185 g/m² Azul",
  "variacao": { "cor": "azul", "gramatura_g_m2": 185, "largura_m": 1.5 },
  "atributos": {
    "composicao": "100% poliéster",
    "ligamento": "sarja 3x1",
    "acabamentos": ["tingimento", "amaciamento"]
  },
  "preco": {
    "custo": 8.9,
    "frete_medio": 1.2,
    "taxas": 0.45,
    "margem_alvo": 0.25,
    "preco_venda": 14.2
  },
  "estoque": {
    "disponivel": 3200,
    "ponto_pedido": 1940,
    "seguranca": 500
  },
  "ncm": "5514.21.00",
  "status": "ativo"
}
```

### Example 2: Channel Pricing Comparison

```text
Produto: Tecido Sarja 185 g/m² (rolo de 50 m)
Custo por rolo: R$ 445,00 | Frete médio: R$ 60,00

Canal         | Preço  | Comissão | Receita líquida | Margem
Loja própria  | 710,00 |   0,0%   | 710,00          | 24,9%
Mercado Livre | 749,00 |  16,0%   | 629,16          | 15,3%
Shopee        | 729,00 |  18,0%   | 597,78          | 10,9%

Decisão: loja própria com preço cheio; marketplaces com preço
maior para absorver comissão e frete grátis.
```

## Best Practices

- One SKU per variant, with EAN and NCM standardized
- Recompute price whenever cost, freight or fees change
- Sync stock in real time across channels to avoid negative stock
- Measure the funnel per channel, not only overall
- Publish a clear returns policy before scaling traffic
- Keep one unified inventory for omnichannel operations
- Review slow movers quarterly and delist or discount them

## Pitfalls / Common Mistakes

- Pricing without freight or channel fees (margin illusion)
- Reusing SKUs and corrupting stock and tax data
- Letting marketplaces show out-of-stock or wrong-stock items
- Checking competitor prices daily and repricing on noise
- Ignoring return reasons and keeping a defective SKU active
- Running separate inventories per channel and overselling

## References

- [SEBRAE - ecommerce para pequenos negócios](https://www.sebrae.com.br)
- [E-commerce Brasil](https://www.ecommercebrasil.com.br)
- [Receita Federal - NCM e tributos](https://www.gov.br/receitafederal)
- [Mercado Livre - central de vendedores](https://www.mercadolivre.com.br)
- [Shopify - recursos de ecommerce](https://www.shopify.com.br)

## Notes

- Conversion benchmarks vary by vertical and ticket size
- Brazilian marketplaces charge fee plus payment processing; read the
  contract before setting the channel price
- Always calculate margin after all fees, never before
