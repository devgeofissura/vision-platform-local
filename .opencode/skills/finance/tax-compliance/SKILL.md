---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: tax-compliance
description: Simples Nacional DAS calculation, ICMS mechanics and Brazilian tax calendar
category: finance
version: 0.1.0
author: devtiagoabreu
tags: [tax, compliance, simpres, icms, das, brazil]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Basic understanding of revenue and invoices
  - Company registration data (CNAE, annual revenue, state UF)
provides:
  - Monthly DAS (Simples Nacional) calculation example
  - ICMS credit/debit mechanics with worked numbers
  - Tax calendar checklist and obligation dates
---

# Tax Compliance

## Overview

This skill explains how to comply with the main Brazilian tax obligations for
small and medium companies: the unified monthly payment under Simples Nacional
(DAS), the state ICMS on goods, and the calendar of returns and payments.
Getting these wrong causes fines, loss of the Simples benefit, and cash-flow
surprises.

The examples follow the 2025-2026 Simples Nacional annexes. Because the tables
change every year, always confirm the current figures on the official Simples
portal before making decisions.

## Prerequisites

- Company registration data: CNAE, UF, and last 12 months of revenue
- Access to the Simples Nacional revenue table for the current year
- Knowledge of which taxes apply to your CNAE and activity

## Usage Instructions

### 1. Calculating the Monthly DAS (Simples Nacional)

The DAS is a single monthly tax that replaces federal, state, and municipal
taxes. The rate depends on the revenue bracket (from the last 12 months -
RBT12) and the activity annex. The effective rate is progressive:

```text
Example: Retail company (Annex I), RBT12 = R$ 400,000.00
Monthly revenue in the period: R$ 45,000.00

Simplified calculation (single rate method):
  2015 law table (Annex I):
    - 1st bracket: up to R$ 180,000.00  -> 4.00%
    - 2nd bracket: R$ 180,000.01 to R$ 360,000.00 -> 7.30%
    - 3rd bracket: R$ 360,000.01 to R$ 720,000.00 -> 9.50%
    - 4th bracket: R$ 720,000.01 to R$ 1,800,000.00 -> 10.70%

Since RBT12 = 400,000 -> 3rd bracket
  DAS = 45,000.00 x 9.50% = R$ 4,275.00

Important: the 2015 law uses marginal single rate per bracket.
The Simples Nacional amendment (LC 123/2006 with changes) uses a
progressive effective rate: calculate each partial bracket, then
divide by RBT12:

Effective rate (progressive):
  (180000 x 4.00% + 180000 x 7.30% + 40000 x 9.50%) / 400000
  = (7200 + 13140 + 3800) / 400000 = 24140 / 400000 = 6.035%

  DAS = 45,000.00 x 6.035% = R$ 2,715.75

Always use the official calculator (PGDAS-D) for the definitive value.
```

### 2. Understanding ICMS Mechanics

ICMS is a state value-added tax on the circulation of goods. The tax is
non-cumulative: the company takes a credit on purchases and pays the debit on
sales, remitting the difference.

```text
Example: Commerce in SP (internal ICMS rate 18%)

1) Purchase R$ 10,000.00 of goods:
   Debit paid to supplier as credit:
   Credit ICMS = 10,000 x 18% = R$ 1,800.00

2) Sale of the goods for R$ 15,000.00:
   Debit ICMS = 15,000 x 18% = R$ 2,700.00

3) Amount to pay in the state return (GIA/EFD):
   ICMS due = Debits - Credits = 2,700 - 1,800 = R$ 900.00

4) Other rates to watch:
   - Interest on late payment: SELIC + 1% per month (verify current)
   - Inter-state sales (DIFAL) may add a complementary rate
   - ST (substituição tributária) applies to specific goods
     (e.g., cosmetics, electronics) with a MVA margin:

   Example of ICMS-ST:
   Base price R$ 100, MVA 45%, internal rate 18%:
   Base ST = 100 x (1 + 0.45) = R$ 145.00
   ICMS ST per unit = 145 x 18% - 100 x 18% = 26.10 - 18.00 = R$ 8.10
```

### 3. Following the Tax Calendar and Returns

Compliance is mostly a matter of calendar discipline. Missing a deadline means
fines and interest. The most common monthly and annual obligations are listed
below.

```text
Monthly obligations (example for 2026):

Day 10    - DAS (Simples Nacional) payment of the previous month
Day 20    - INSS/GFIP or eSocial worker contributions
Day 25    - ICMS payment (SP) - with EFD filing (fiscal return)
Date per UF - ICMS-ST payment when applicable
Day 15    - ISS (municipal service tax) when outside Simples

Annual and periodic:

- PGDAS-D annual report (Simples) - confirming monthly revenues
- DASN-SIMEI (if MEI) - annual declaration of gross revenue
- ECD/ECF (accounting and fiscal books) - due in May/June
- DIRF (annual income tax return of source withholdings) - February
- RAIS/eSocial data - by the end of April
- CND (certificado de regularidade) renewal checks

Weekly reminder loop (put this in your calendar):
  Every Friday: confirm all DAS, ICMS, and payroll obligations
  for the next 10 working days are scheduled.
```

## Examples

### Example 1: DAS for a Service Company (Annex III)

```text
Annex III (services with deduction, e.g., software development)
RBT12 = R$ 250,000.00 -> 2nd bracket
  Marginal rate: 9.00%
  Deductible amount for the bracket: R$ 5,940.00

Progressive effective rate:
  (180000 x 6.00% + 70000 x 9.00% - 5940) / 250000
  = (10800 + 6300 - 5940) / 250000 = 11160 / 250000 = 4.464%

Monthly revenue R$ 30,000.00:
  DAS = 30,000 x 4.464% = R$ 1,339.20

Split of the DAS (approx, Annex III):
  CPP (social security): 33.50% of the tax
  CSLL: 10.00%
  PIS: 3.17%
  COFINS: 12.74%
  ISS (municipal): 40.59%
  (percentages vary by bracket - confirm on the official table)
```

### Example 2: Verifying a Supplier Invoice

```text
Invoice received: R$ 2,350.00
ICMS highlighted: R$ 423.00  (18%)
Check: 2350 x 0.18 = 423.00 -> consistent

Also verify:
  [ ] CNPJ and UF on the invoice match the supplier
  [ ] CFOP code correct for the operation (e.g., 5.102 internal purchase)
  [ ] ICMS-ST field filled only if applicable to the product
  [ ] CFOP and CST consistent with the tax regime
```

## Best Practices

- Pay DAS and ICMS on the due date; interest accrues immediately
- Reconcile the PGDAS-D calculation with your accounting monthly
- Keep an updated map of CFOP, CST, and ICMS rate per product
- Review the RBT12 monthly to detect bracket changes early
- Automate calendar alerts for every tax deadline
- Keep a tax provision account in cash: set aside ~10% of revenue
- Work with an accountant for annual returns (ECF, DIRF, RAIS)

## Pitfalls / Common Mistakes

- Using the marginal bracket rate instead of the progressive effective rate
- Forgetting the ICMS-ST (MVA) margin on controlled goods
- Confusing ISS (municipal) with ICMS (state) for service invoices
- Paying DAS with the wrong annex because the CNAE is misclassified
- Missing the DASN-SIMEI annual declaration for MEI
- Not reconciling the GIA/EFD with the PGDAS numbers

## References

- [Simples Nacional Portal (official simulator and tables)](https://www8.receita.fazenda.gov.br/SimplesNacional/)
- [Receita Federal - PGDAS-D](https://www.gov.br/receitafederal/pt-br/assuntos/orientacao-tributaria/pagamentos-e-parcelamentos/simples-nacional)
- [Portal do Simples Nacional (SEFAZ)](https://www.simplesnacional.com.br/)
- [SPED Fiscal (EFD) documentation](https://www.gov.br/receitafederal/pt-br/assuntos/orientacao-tributaria/sped)
- [Receita Federal Tax Calendar](https://www.gov.br/receitafederal/pt-br/assuntos/orientacao-tributaria/calendario)

## Notes

- Tax tables and annexes change annually; always validate with official sources
- This skill is educational and does not replace professional tax advice
- The DAS includes multiple taxes; know what each share pays for
