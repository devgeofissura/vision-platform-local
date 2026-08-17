---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: criminal-law
description: "Educational basics of Brazilian criminal procedure (CPP): rights of the accused and procedural stages."
category: humanities
version: 0.1.0
author: devtiagoabreu
tags: [criminal-law, cpp, brazil, due-process, habeas-corpus, defense]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Basic familiarity with legal concepts such as rights and due process
  - Willingness to treat all content as educational, not legal advice
  - Access to official sources for verification (planalto.gov.br, cnj.jus.br)
provides:
  - A map of fundamental rights of the accused
  - An overview of criminal procedure stages
  - Educational guidance on habeas corpus and remedies
  - Clear references to official Brazilian law sources
---

# Criminal Law (CPP) Basics

## Overview

This skill is a structured, educational overview of Brazilian criminal
procedure, anchored in the Constitution, the Código Penal (CP), and the Código
de Processo Penal (CPP). It covers the rights of the accused, the main stages
of a criminal case, and the role of instruments such as habeas corpus.

This skill is informational and educational only. It does not provide legal
advice for a specific case and never replaces a criminal defense lawyer
licensed with the Brazilian Bar Association (OAB). Anyone facing an
investigation, arrest, or trial should contact a lawyer or the public
defender's office immediately.

## Prerequisites

- Understanding that legal content can be nuanced and change over time
- Access to official sources for verification
- Awareness that this material never substitutes professional defense
- No expectation of legal guarantees from these educational patterns

## Usage Instructions

### 1. Know the Rights of the Accused

The Constitution establishes the baseline protections. Reason about any
criminal topic with these rights in mind.

```markdown
- [ ] Presumption of innocence until final judgment (art. 5, LVII, CF)
- [ ] Full defense and adversarial procedure (art. 5, LV, CF)
- [ ] Right to silence and not to self-incriminate
- [ ] Right to a lawyer at every stage
- [ ] Public, justified decisions by competent courts
- [ ] Habeas corpus for unlawful restriction of movement (art. 5, LXVIII, CF)
```

### 2. Understand the Criminal Investigation

The police investigation (inquérito policial) is an inquisitorial,
pre-trial phase led by the police. It collects evidence to support either a
charge or an archiving request. Even at this stage the person investigated has
rights, including representation by a lawyer.

```text
Investigation stage:
- Police gather evidence and statements
- Reports are collected into a record (relatório)
- Ministry or the police decide whether there is support for a charge
- The person investigated may remain silent and have legal assistance
```

### 3. Follow the Criminal Action and Trial

The criminal action begins with a charge (denúncia) filed by the public
prosecutor or, in private cases, a complaint (queixa). The accused is summoned,
answers the accusation, and the case proceeds to evidence, closing arguments,
and judgment. Appeals follow at the end.

```text
Main stages:
1. Charge (denúncia or queixa)
2. Summons and written defense
3. Hearing and evidence production
4. Closing arguments
5. Judgment (sentença)
6. Appeals (apelação, recurso em sentido estrito, revisão criminal)
```

### 4. Reason About Habeas Corpus and Remedies

Habeas corpus protects freedom of movement against unlawful acts or abuse of
power. It can be preventive or liberatory. Other remedies, such as appeals and
criminal review (revisão criminal), correct errors after decisions. Describe
these instruments with precision and never draft real petitions.

```json
{
  "instrument": "habeas_corpus",
  "object": "freedom of movement (art. 5, LXVIII, CF)",
  "parties": ["impetrante (petitioner)", "paciente (person)", "coator (authority)"],
  "types": ["liberatory", "preventive"],
  "disclaimer": "Educational description only. Real filings require a licensed OAB lawyer."
}
```

### 5. Apply Safely

Treat every explanation as general knowledge. Never suggest outcomes for real
cases, never assume facts, and always direct people to a criminal defense
lawyer or the public defender's office when a real matter arises.

## Examples

### Example 1: Educational analysis of a procedural stage

```text
Scenario: a person is under investigation. The police ask for a statement.

Educational answer:
- The person has the right to remain silent (art. 5, LXIII, CF).
- A lawyer may attend and assist.
- Silence cannot be treated as proof of guilt.
- After investigation, the prosecutor decides whether to charge.

This is a general explanation. In any real case, contact a licensed OAB lawyer.
```

### Example 2: Structured rights checklist prompt

```json
{
  "task": "Summarize the rights of the accused during trial",
  "sections": [
    "presumption of innocence",
    "full defense and adversarial procedure",
    "right to silence",
    "right to legal assistance",
    "habeas corpus"
  ],
  "tone": "educational",
  "disclaimer": "Include a reminder that this is not legal advice and that a licensed OAB lawyer should be consulted."
}
```

## References

- [Código Penal - Decreto-Lei 2.848/1940](https://www.planalto.gov.br/ccivil_03/decreto-lei/del2848compilado.htm)
- [Código de Processo Penal - Decreto-Lei 3.689/1941](https://www.planalto.gov.br/ccivil_03/decreto-lei/del3689compilado.htm)
- [Conselho Nacional de Justiça (CNJ)](https://www.cnj.jus.br)
- [Ordem dos Advogados do Brasil (OAB)](https://www.oab.org.br)
