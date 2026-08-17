---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: aircraft-mechanics
description: Understand airworthiness, inspection processes, maintenance records, and FAA-H-8083 references.
category: automotive
version: 0.1.0
author: devtiagoabreu
tags: [aviation, airworthiness, inspection, maintenance, safety]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Basic aviation terminology
  - Awareness that maintenance is regulated and certified
  - Understanding of documentation discipline
provides:
  - Airworthiness concepts and continued airworthiness
  - Inspection process and maintenance check structure
  - Maintenance records, logs, and forms guidance
  - FAA-H-8083 and ANAC reference mapping
---

# Aircraft Mechanics

## Overview

This skill provides an educational foundation in aircraft maintenance
following FAA AMT and ANAC standards. It covers airworthiness
concepts, inspection processes, maintenance records and logs, and the
reference handbooks (FAA-H-8083 series) plus Brazilian regulations
(RBAC). The safety culture is absolute: no work without qualification,
no release without authorization, no entry without records.

This skill is educational. It does not authorize anyone to perform or
release maintenance. Releasing an aircraft to service is restricted to
certified mechanics and certified maintenance organizations under the
applicable authority (FAA or ANAC).

## Prerequisites

- Basic aviation and aircraft systems vocabulary
- Willingness to follow checklists and manuals without improvisation
- Understanding of certification and regulatory limits
- Access to FAA-H-8083 handbooks and applicable RBAC texts

## Usage Instructions

### 1. Apply airworthiness concepts

Airworthiness is the aircraft's fitness for safe flight, maintained
continuously between inspections and repairs.

```text
Airworthiness principles
- The aircraft must conform to its approved type design
- It must be in condition for safe operation
- Continued airworthiness depends on scheduled maintenance
- Any modification requires approved data and authorization
```

### 2. Understand inspection processes

Inspections are planned by flight hours, cycles, and calendar time.

```text
Common check structure (educational)
- Preflight: daily checks by flight crew
- Periodic: scheduled inspections (e.g., 100-hour, annual)
- Progressive: inspections spread over a cycle
- Heavy maintenance: deeper structural checks
```

### 3. Keep accurate records

Everything performed is recorded; the log is the memory of the
aircraft.

```text
Record content
- Aircraft registration and total hours and cycles
- Description of work performed
- Parts installed with part and serial numbers
- Reference to approved manual or task
- Result of inspection and release signature
```

### 4. Map references correctly

Use the FAA-H-8083 series for fundamentals and ANAC RBAC for Brazilian
requirements.

```text
FAA-H-8083-30  General (safety, forms, materials)
FAA-H-8083-31  Airframe (structures, systems)
FAA-H-8083-32  Powerplant (engines, propellers)
RBAC (ANAC)    Brazilian regulations for maintenance
```

### 5. Enforce the safety culture

Safety over schedule, always.

```text
Safety rules
- Never release an aircraft in doubtful condition
- Stop and ask when a manual step is unclear
- Report discrepancies without fear of reprisal
- Verify the validity of licenses and certificates
- Use approved data only; never improvise
```

## Examples

### Example 1: Maintenance record template

```markdown
# Maintenance Record (Educational Template)

## Header
- Registration: PR-XXX
- Date and time: YYYY-MM-DD HH:MM
- Total flight hours: 1842
- Total cycles: 980

## Work performed
- Inspected flight control linkage per manufacturer Rev 14
- Replaced brake pads, P/N 12345, S/N 67890
- Lubricated nose gear per task card

## Completion
- Inspection result: approved
- Certified mechanic: [name and certificate number]
- Organization: [certified MRO name]
```

### Example 2: Work order data structure

```json
{
  "work_order": "EX-2026-0001",
  "aircraft": { "registration": "PR-XXX", "hours": 1842, "cycles": 980 },
  "service": "Periodic inspection",
  "reference": { "manual": "Manufacturer Mx Manual", "revision": "Rev 14" },
  "tasks": [
    { "task": "Inspect landing gear", "result": "approved" },
    { "task": "Check flight controls", "result": "approved" }
  ],
  "parts": [],
  "status": "pending certified release"
}
```

## References

- [FAA — Federal Aviation Administration](https://www.faa.gov/)
- [FAA — Aviation Maintenance Technician Handbooks](https://www.faa.gov/regulations_policies/handbooks_manuals/aviation/)
- [ANAC — National Civil Aviation Agency](https://www.gov.br/anac/pt-br)
- [ANAC — Brazilian Civil Aviation Regulations (RBAC)](https://www.anac.gov.br/assuntos/legislacao/legislacao-1/rbha-e-rbac/rbac)
