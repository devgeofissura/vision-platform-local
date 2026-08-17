---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: customer-relationship
description: "Customer relationship team playbook: pre-sales, onboarding, support tiers, NPS/CSAT and retention"
category: commercial
version: 0.1.0
author: devtiagoabreu
tags: [commercial, relationship, crm, support, nps, csat, retention, omnichannel]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - A CRM with ticket and contact history
  - Multichannel access: WhatsApp, email, phone, chat
  - Defined SLAs per severity and support tier
provides:
  - Pre-sales qualification and expectation-setting workflow
  - Onboarding playbook (30/60/90 days) for B2B and ecommerce
  - Support tier structure (N1/N2/N3) with SLA defaults
  - NPS and CSAT calculation and interpretation
  - Escalation matrix and retention playbooks
  - Omnichannel operating rules for the relationship team
---

# Customer Relationship

## Overview

This skill is the operating playbook of a customer relationship team. It
covers the full lifecycle: pre-sales qualification, onboarding, support
tiers, satisfaction metrics (NPS/CSAT), escalation, retention, and
omnichannel handling.

The team's job is to turn every interaction into loyalty. That requires
discipline: SLAs, documented history, and playbooks that anyone in the
team can follow. This skill provides the templates, formulas and rules to
run that process for both B2B (factory customers) and B2C (ecommerce).

## Prerequisites

- CRM with tickets, contacts and interaction history
- Messaging channels configured (WhatsApp, email, phone, chat)
- Product knowledge base for N2/N3 support
- Defined team structure: who owns N1, N2 and N3
- Management buy-in on the SLA commitments

## Usage Instructions

### 1. Pre-Sales Qualification and Expectations

The relationship starts before the sale. Quality the lead and set
realistic expectations to avoid refunds and churn later.

```text
Pre-sales checklist:
  - Confirm the buyer's application (product, volume, season)
  - Validate the spec fits the product line (no overpromising)
  - Share MOQ, lead time and freight rules in writing
  - Answer technical questions within 4 business hours
  - Set expectations: sample timing, production, delivery
  - Pass the qualified lead to sales with full context

Handoff fields for the sales team:
  - customer, contact, phone, channel of origin
  - product interest, volume, timeline
  - objections raised and answers given
  - next action and owner
```

Never promise a deadline the operation cannot meet; it creates a
support ticket before the first order exists.

### 2. Onboarding (30/60/90 Days)

Onboarding defines whether the customer stays. Follow a phased plan and
track completion.

```text
Onboarding plan (B2B factory customer):

Days 0-7 (Activation)
  [ ] Account created with catalog access
  [ ] Samples sent and tracked
  [ ] Kickoff call with commercial + production
  [ ] Guide sent: how to order, lead times, contacts

Days 8-30 (First order)
  [ ] First quotation and pilot order
  [ ] Production of the first batch followed
  [ ] Feedback collected on the spec sheet

Days 31-60 (Stabilization)
  [ ] Quality review with the customer (shrinkage, color)
  [ ] Rebuy program proposed (quarterly calendar)
  [ ] Preferences for color and finish registered

Days 61-90 (Consolidation)
  [ ] First NPS survey
  [ ] Volume review and annual order calendar
  [ ] Upsell/cross-sell analysis presented
```

Track activation rate (customers reaching day 30) and time to first
repeat order.

### 3. Support Tiers and SLA

Structure support so simple issues resolve fast and hard issues reach
the right specialist.

```text
Tier structure:
  N1 - Triagem and common questions (returns, shipping, docs)
  N2 - Technical issues (spec, quality, homologation follow-up)
  N3 - Specialist/escalation (process or system changes)

SLA defaults (per severity):
  Severity | Examples                | 1st response | Resolution
  Baixa    | information, docs      | 8h           | 3 business days
  Média    | returns, payment       | 4h           | 2 business days
  Alta     | defective batch, stop  | 2h           | 24h
  Crítica  | safety, recall         | 30 min       | 4h
```

Escalate by the clock, not by mood: when an SLA is near, raise the ticket
to N2/N3 automatically.

### 4. NPS and CSAT

Measure experience systematically. NPS measures loyalty; CSAT measures a
specific interaction.

```text
NPS question: "De 0 a 10, quanto você recomendaria a empresa?"
  Promoters  (9-10)  - loyal, generate referrals
  Neutrals   (7-8)   - satisfied but not loyal
  Detractors (0-6)   - at risk, act immediately

NPS formula:
  NPS = ((Promoters - Detractors) / Total) x 100

Example: 120 promoters, 40 neutrals, 25 detractors
  NPS = ((120 - 25) / 185) x 100 = 51.4

CSAT: 1-5 scale on a single interaction (support, delivery)
  CSAT % = (answers 4-5 / total answers) x 100

When to survey:
  - NPS: after 90 days, then quarterly
  - CSAT: after each support resolution and each delivery
```

A high NPS with a low response rate is not reliable; chase the detractors
first, in person or by phone.

### 5. Escalation Matrix

Define who is reached when, before the crisis happens.

```text
Escalation matrix:
  Level | Trigger                    | Action
  L1    | SLA response breached      | N2 takes over within 1h
  L2    | Resolution SLA breached    | Manager + production on the call
  L3    | Customer threatens churn   | CS director + account owner
  L4    | Legal / safety risk        | Legal + compliance, documented

Escalation record:
  - ticket, severity, timeline of actions
  - customer contact, decision owner
  - resolution and follow-up actions
  - communication to the customer with clear dates
```

Every escalation must end with a written plan to the customer and an
internal root-cause note.

### 6. Retention Playbooks and Churn

Retention is cheaper than acquisition. Use churn signals to trigger
playbooks before the customer leaves.

```text
Churn signals:
  - No purchases in 60 days (ecommerce)
  - Two tickets without resolution in a month
  - NPS detractor with no follow-up
  - Price sensitivity or competitor mention

Retention playbook (medium/high risk):
  1. Personalized contact by the account owner
  2. Diagnose the root cause (price, quality, service)
  3. Offer concrete remedy: credit, rework, better terms
  4. Propose a retention plan (standing order, rebuy program)
  5. Track recovery: repurchase within 30 days

Retention metrics:
  - Churn rate = customers lost / customers at start
  - Repeat purchase rate (share of customers buying again)
  - Health score per account (activity, tickets, NPS)
```

Score each account monthly (health score) so churn is predicted, not
discovered.

### 7. Omnichannel Rules

The customer should be able to continue a conversation across channels
without repeating themselves.

```text
Omnichannel operating rules:
  - One unified customer history in the CRM
  - WhatsApp, email, phone and chat share the same ticket
  - Channel switching keeps the same ticket and context
  - Storefront and marketplace tickets unified for B2C
  - SLA applies to the ticket, not per channel
  - Automatic replies confirm receipt within the SLA
```

Never make the customer repeat their story after switching from email to
WhatsApp.

## Examples

### Example 1: Onboarding Playbook (30/60/90)

```text
ONBOARDING CLIENTE B2B - CONFECÇÃO

Dia 0 a 7  (Ativação)
  [ ] Conta criada no portal com acesso ao catálogo
  [ ] Amostras enviadas e rastreadas
  [ ] Reunião de kickoff com comercial e produção
  [ ] Guia de como pedir e prazos enviado

Dia 8 a 30 (Primeiro pedido)
  [ ] Primeira cotação e pedido-piloto
  [ ] Acompanhar produção do primeiro lote
  [ ] Coletar feedback sobre a ficha técnica

Dia 31 a 60 (Estabilização)
  [ ] Revisar qualidade e encolhimento com o cliente
  [ ] Propor programa de recompra trimestral
  [ ] Registrar preferências de cor e acabamento

Dia 61 a 90 (Consolidação)
  [ ] Pesquisa NPS (primeira medição)
  [ ] Revisar volume e calendário de pedidos
  [ ] Apresentar análise de preço e upsell
```

### Example 2: Support Ticket (JSON)

```json
{
  "ticket": "TKT-2026-8831",
  "canal": "whatsapp",
  "cliente": "Confecção Veste Bem LTDA",
  "severidade": "alta",
  "categoria": "qualidade_tecidos",
  "assunto": "Rolo com defeito de tingimento no lote 1047",
  "sla": { "resposta_horas": 4, "resolucao_dias": 5 },
  "nivel": "N2",
  "acionamentos": ["producao", "qualidade"],
  "status": "em_atendimento",
  "resolucao": "Troca do rolo agendada + coleta do defeituoso",
  "cliente_respondido_em_horas": 2
}
```

### Example 3: NPS Calculation (Python)

```python
promotores = 120
neutros = 40
detratores = 25
total = promotores + neutros + detratores

nps = ((promotores - detratores) / total) * 100
print(f"NPS: {nps:.1f}")  # NPS = 51,4
```

## Best Practices

- Answer pre-sales within 4 business hours
- Onboard with a tracked 30/60/90 plan, not ad hoc
- Escalate by the clock, never by mood
- Survey NPS after 90 days and CSAT after each resolution
- Chase detractors first; ignore them and they leave
- Score account health monthly to predict churn
- Keep one ticket and one history across all channels

## Pitfalls / Common Mistakes

- Promising deadlines the operation cannot meet
- Sending NPS surveys nobody reads and nobody acts on
- Letting tickets sit past SLA without escalation
- Restarting the conversation when the channel changes
- Treating every lost customer as unavoidable
- Surveying without a follow-up loop for detractors

## References

- [SEBRAE - atendimento e relacionamento com o cliente](https://www.sebrae.com.br)
- [Reclame Aqui - reputação de atendimento](https://www.reclameaqui.com.br)
- [Consumidor.gov.br - plataforma oficial de solução de conflitos](https://www.consumidor.gov.br)
- [Zendesk - guia de atendimento ao cliente](https://www.zendesk.com.br)
- [HubSpot - customer success e retenção](https://www.hubspot.com.br)

## Notes

- SLA and survey cadence are defaults; adapt to your reality
- NPS and CSAT only help if there is an action loop behind them
- A relationship team is judged by retention, not ticket volume
