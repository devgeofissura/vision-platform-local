---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: accounting-basics
description: Double-entry bookkeeping, journal entries, chart of accounts and financial statements
category: finance
version: 0.1.0
author: devtiagoabreu
tags: [accounting, bookkeeping, journal, ledger, statements]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - No prior accounting knowledge, but basic math and finance intuition help
  - A spreadsheet or accounting software to practice the entries
provides:
  - Journal entry templates with debit/credit rules
  - A sample chart of accounts
  - Income statement and balance sheet reconciliation walkthrough
---

# Accounting Basics

## Overview

This skill introduces the core mechanics of financial accounting: the
double-entry system, journal entries, the chart of accounts, and how they flow
into the two main reports, the income statement (DRE) and the balance sheet.
It is aimed at entrepreneurs, developers, and analysts who need to read
accounts or record simple transactions correctly.

The golden rule of double entry is that every transaction debits one or more
accounts and credits one or more accounts, always with equal totals. This keeps
the accounting equation (Assets = Liabilities + Equity) in balance.

## Prerequisites

- Basic arithmetic and an understanding of what an asset, a liability, and
  equity are
- A spreadsheet editor to reproduce the examples
- Patience to trace every transaction through the ledger

## Usage Instructions

### 1. Journal Entries with the Double-Entry System

Every economic event is recorded first in the journal as a dated entry with a
debit and a credit side. Debits increase assets and expenses; credits increase
liabilities, equity, and revenue.

```text
Rule of thumb:
  DEBIT  increases:  Assets, Expenses
  CREDIT increases:  Liabilities, Equity, Revenue

Example 1 - Sale on credit (sale of R$ 1,000, cost R$ 600, stock R$ 600):

Date       Account                  Debit     Credit
01/03      Accounts Receivable      1,000.00
           Sales Revenue                      1,000.00
           (record revenue on sale on credit)

01/03      Cost of Goods Sold         600.00
           Inventory                          600.00
           (transfer cost of goods sold)

Example 2 - Paying a supplier invoice (R$ 400 cash):

01/03      Accounts Payable           400.00
           Cash                                400.00
           (settle supplier invoice in cash)

Example 3 - Monthly depreciation (asset R$ 12,000, life 5 years):

01/31      Depreciation Expense       200.00
           Accumulated Depreciation            200.00
           (12,000 / 60 months = 200/month)
```

### 2. Chart of Accounts (COA)

The COA is the numbered list of accounts used to classify every transaction.
A consistent COA makes reports reliable and comparable across periods. Use a
numerical hierarchy so accounts group naturally.

```text
Sample chart of accounts (Brazilian style, brief):

1   ATIVO (Assets)
1.1   Circulante (Current)
1.1.1   Caixa e Equivalentes
1.1.2   Contas a Receber
1.1.3   Estoques
1.2   Não Circulante
1.2.1   Imobilizado
1.2.1.1   Equipamentos
1.2.1.2   (-) Depreciação Acumulada

2   PASSIVO (Liabilities)
2.1   Circulante
2.1.1   Fornecedores
2.1.2   Empréstimos
2.2   Não Circulante
2.2.1   Financiamentos

3   PATRIMÔNIO LÍQUIDO (Equity)
3.1   Capital Social
3.2   Lucros Acumulados

4   RECEITAS (Revenue)
4.1   Vendas de Mercadorias
4.2   Receitas Financeiras

5   CUSTOS E DESPESAS (Costs and Expenses)
5.1   Custo das Mercadorias Vendidas
5.2   Despesas Operacionais
5.2.1   Salários
5.2.2   Aluguel
5.2.3   Depreciação

Rules:
  - Never create ad-hoc account names; add them to the COA first
  - Use negative sign for contra accounts (accumulated depreciation)
  - Keep the numbering stable between periods
```

### 3. Financial Statements: Income Statement and Balance Sheet

At the end of the period, ledger balances are summarized. The income statement
shows performance (revenues - expenses = net profit). The balance sheet shows
the financial position (Assets = Liabilities + Equity), updated with the net
profit.

```text
Income Statement (DRE) - March
  Revenue (sales)                 R$ 10,000.00
  (-) Cost of goods sold          R$ (6,000.00)
  = Gross profit                  R$  4,000.00
  (-) Operating expenses
      Salaries        (1,200.00)
      Rent            (800.00)
      Depreciation    (200.00)
      Other           (300.00)
  = Net profit before tax         R$  1,500.00

Balance Sheet - 31 March
  Assets                           Liabilities + Equity
  Cash            2,000.00         Accounts Payable   800.00
  A/R             1,000.00         Loans            1,000.00
  Inventory       1,400.00         Capital          3,000.00
  Equipment      12,000.00         Net profit        1,500.00
  (-) Accum. dep.  (700.00)        Retained earnings  400.00
  ---------------------------      ---------------------------
  Total          15,700.00         Total           15,700.00

Check: Assets = Liabilities + Equity  ->  15,700 = 15,700  OK
```

## Examples

### Example 1: Full Cycle for a Sale on Credit

```text
1) Sale on credit of R$ 2,000 (stock cost R$ 1,200)
   Dr Accounts Receivable  2,000 | Cr Sales Revenue  2,000
   Dr COGS 1,200               | Cr Inventory       1,200

2) Customer pays R$ 1,000 in advance of the invoice
   Dr Cash 1,000 | Cr Accounts Receivable 1,000

3) Remaining R$ 1,000 written off as bad debt
   Dr Bad Debt Expense 1,000 | Cr Accounts Receivable 1,000

Net effect on equity: +2,000 (revenue) -1,200 (cogs) -1,000 (bad debt)
                      = -200 from this customer
Lesson: always provision for doubtful accounts before the write-off.
```

### Example 2: Trial Balance of All Entries

```text
Trial balance after posting all entries of the month:

Account                     Debit       Credit
Cash                        1,000.00
Accounts Receivable         1,000.00
Inventory                   1,400.00
Equipment                  12,000.00
Accumulated Depreciation                700.00
Accounts Payable                         800.00
Loans                                   1,000.00
Capital                                 3,000.00
Sales Revenue                         12,000.00
COGS                        7,200.00
Salaries                    1,200.00
Rent                          800.00
Bad Debt                    1,000.00
------------------          --------    --------
Total                      25,600.00   25,600.00
Both columns equal -> posting is consistent
```

## Best Practices

- Post entries on the date the economic event occurs, not when cash moves
- Reconcile the trial balance before closing the period
- Separate personal and business transactions completely
- Keep supporting documents (invoices, receipts) for every entry
- Use accrual basis once the business exceeds a minimal size
- Review the balance sheet equation after every batch of entries
- Automate recurring entries (depreciation, rent, salaries)

## Pitfalls / Common Mistakes

- Posting both sides to the same side (breaking the double-entry rule)
- Recording revenue when money arrives instead of when it is earned
- Ignoring accruals: expenses of the period not yet paid
- Using the same cash account for personal and business money
- Writing off bad debt without an allowance account
- Closing the books without a trial balance check

## References

- [IAS 1 - Presentation of Financial Statements](https://www.ifrs.org/issued-standards/list-of-standards/ias-1-presentation-of-financial-statements/)
- [AccountingCoach: Debits and Credits Explained](https://www.accountingcoach.com/debits-and-credits/explanation)
- [CPA Exam Double Entry System (AICPA)](https://www.aicpa-cima.com/)
- [IFRS Standards Portal](https://www.ifrs.org/issued-standards/)

## Notes

- Brazilian GAAP uses the plan of accounts structure above; other countries
  follow the same logic with local numbering
- For public companies, always follow the applicable accounting standards
- This skill teaches principles; consult a licensed accountant for filing
