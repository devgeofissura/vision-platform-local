# Platform Team Composition

The `platform-team` composition groups the agents responsible for keeping
the delivery platform reliable, observable, and secure.

## Members

| Agent | Role |
|-------|------|
| `devops-engineer` | Lead - pipelines, infrastructure, and delivery |
| `site-reliability-engineer` | Reliability, monitoring, and incident response |
| `security-engineer` | Security posture, audits, and vulnerability handling |

## Workflow

The team follows a platform-focused flow:

```
plan -> build -> secure -> operate
```

1. **Plan** - The lead designs the infrastructure and delivery changes.
2. **Build** - Infrastructure and automation are implemented.
3. **Secure** - The security engineer reviews the platform posture.
4. **Operate** - The SRE validates reliability and observability.

## Usage

Load the individual agents and orchestrate them through the workflow, or
drive the whole flow with the lead agent:

```bash
# The lead agent coordinates the composition
devops-engineer: "Coordinate the platform-team for: <initiative>"
```

## Related Assets

- Agent definitions live in `assets/agents/`.
- Use the `incident-response` prompt chain for operational runbooks:
  `assets/prompt-chains/incident-response/chain.json`.
