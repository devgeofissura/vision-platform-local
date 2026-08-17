---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: labor-law
description: "Educational basics of Brazilian labor law (CLT): contracts, rights, dismissal and overtime."
category: humanities
version: 0.1.0
author: devtiagoabreu
tags: [labor-law, clt, brazil, employment, contracts, dismissal, overtime]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - A general understanding of Brazilian employment vocabulary
  - Willingness to treat all content as educational, not legal advice
  - Access to official sources for verification (planalto.gov.br, tst.jus.br)
provides:
  - A map of core CLT rights and obligations
  - Checklist guidance for employment contracts and dismissal
  - Educational calculation patterns for overtime and severance
  - Clear references to official Brazilian law sources
---

# Labor Law (CLT) Basics

## Overview

This skill is a structured, educational overview of Brazilian labor law as
consolidated in the CLT (Consolidação das Leis do Trabalho). It covers the
employment contract, core employee rights, overtime rules, and dismissal
procedures so you can reason correctly about labor topics in products,
documents, and conversations.

This skill is informational and educational only. It does not provide legal
advice for a specific case and never replaces a lawyer licensed with the
Brazilian Bar Association (OAB). Laws and collective agreements change, so
always verify against official sources.

## Prerequisites

- Basic knowledge of Portuguese legal vocabulary (CLT, FGTS, 13th salary)
- Internet access to official sources for verification
- Clear understanding that this is educational material, not legal advice
- No expectation of a guaranteed legal outcome from these patterns

## Usage Instructions

### 1. Map the Employment Contract

The CLT defines the employment relationship by four elements: personal service,
ongoing subordination, remuneration, and non-eventuality (not occasional).
Identify these elements before reasoning about rights or obligations.

```text
Employment relationship (CLT) requires:
1. Personal work (performed by the worker)
2. Subordination (direction from the employer)
3. Remuneration (payment in exchange for work)
4. Non-eventuality (regular, recurring work)
```

### 2. Apply Core Employee Rights

Brazilian workers enjoy a set of guaranteed rights that usually cannot be
waived. Keep this checklist in mind when modeling HR rules.

```markdown
- [ ] Written or digital work card (CTPS) registration
- [ ] Minimum wage guarantee
- [ ] 8-hour day / 44-hour week limits
- [ ] Overtime paid with at least 50% surcharge
- [ ] Weekly rest, ideally on Sundays
- [ ] Annual paid vacation with 1/3 extra (terço constitucional)
- [ ] 13th salary (décimo terceiro)
- [ ] Monthly FGTS deposit of 8% of salary
```

### 3. Handle Overtime and Additional Pay

Overtime is the norm under article 59 of the CLT: at least 50% surcharge on the
normal hour, with higher rates possible via collective agreements. Sundays and
holidays commonly reach 100%. Some roles carry additional risk allowances:
insalubridade (unhealthy conditions) at 10/20/40% and periculosidade
(dangerous conditions) at 30%.

```text
Monthly hours base: 220h
Salary: R$ 2.200,00 -> hourly value R$ 10,00
Overtime (50%): R$ 15,00 per hour
Extra night hours or risk allowances add further surcharges
```

### 4. Reason About Dismissal and Severance

Dismissal without just cause triggers a package of severance payments: notice
period (aviso prévio), proportional vacation and 13th salary, salary balance,
and FGTS deposit plus a 40% penalty on the balance. Dismissal for just cause
(justa causa) removes most of these benefits. Treat any amount as educational
until a licensed professional calculates it.

```json
{
  "dismissal_type": "without_just_cause",
  "severance_items": [
    "notice period (worked or paid)",
    "salary balance for worked days",
    "accrued and proportional vacation + 1/3",
    "proportional 13th salary",
    "FGTS for the month plus 40% penalty"
  ],
  "disclaimer": "Educational summary. Verify each item with official sources and a licensed OAB lawyer."
}
```

### 5. Apply Safely

Always separate general knowledge from a concrete case. Never assert a right or
an amount as definitive; recommend consulting a lawyer registered with the OAB
for real disputes, contracts, or dismissals.

## Examples

### Example 1: Educational overtime calculation

```text
Input:
  Monthly hours base: 220
  Monthly salary: R$ 2.200,00
  Hours worked: 12 overtime hours in the month

Steps:
  Hourly value = 2.200,00 / 220 = R$ 10,00
  Overtime value = 10,00 * 1.5 = R$ 15,00
  Total overtime = 12 * 15,00 = R$ 180,00

Result:
  Add R$ 180,00 to the month's pay as overtime.

Note: percentages may change under a collective agreement.
This is an educational example, not a payroll calculation.
```

### Example 2: Contract analysis prompt

```text
You are studying the CLT for educational purposes. Given this fictional
employment contract summary, list the clauses that touch on:
- hours and overtime
- vacation and 13th salary
- insalubridade or periculosidade
- dismissal and severance

Fictional contract: 8h/day, 44h/week, R$ 2.500,00/month, office role,
overtime at 50%, standard vacation and 13th salary.

Then explain the key rights involved and remind the user to consult a
licensed lawyer before making any decision.
```

## References

- [CLT - Decreto-Lei 5.452/1943 (planalto.gov.br)](https://www.planalto.gov.br/ccivil_03/decreto-lei/del5452.htm)
- [Tribunal Superior do Trabalho (TST)](https://www.tst.jus.br)
- [Ministério do Trabalho e Emprego](https://www.gov.br/trabalho-e-emprego)
- [Ordem dos Advogados do Brasil (OAB)](https://www.oab.org.br)
