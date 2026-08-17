# Incident Response Chain

The `incident-response` chain guides an operator from first report to a
diagnosed and security-assessed incident.

## Steps

| Step | Prompt | Purpose |
|------|--------|---------|
| 1 | `debug-analysis` | Diagnose the root cause of the failure |
| 2 | `security-audit` | Assess security impact and exposure |

## Usage

Run the steps in order, feeding the output of each step into the next:

```bash
# Step 1: Diagnose the incident
#   prompt: debug-analysis
#   inputs: error_message, code_context
#   output: root cause + proposed solution + prevention

# Step 2: Assess security impact
#   prompt: security-audit
#   inputs: application, scope
#   output: ranked findings + remediation steps
```

## Related Assets

- Prompts live in `assets/prompts/`.
- Pair with the `platform-team` composition to staff the response:
  `assets/compositions/platform-team/composition.json`.
