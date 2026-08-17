# Full-Stack Team Composition

The `full-stack-team` composition groups the agents needed to deliver a
complete feature across the entire stack, from API to UI to quality.

## Members

| Agent | Role |
|-------|------|
| `backend-developer` | Lead - APIs, databases, and services |
| `frontend-developer` | UI implementation and integration |
| `qa-engineer` | Test strategy, execution, and release quality |

## Workflow

The team follows a linear delivery flow:

```
plan -> implement -> review -> test
```

1. **Plan** - The lead structures the feature into tasks.
2. **Implement** - Backend and frontend agents build their layers.
3. **Review** - Implementation is cross-reviewed for quality.
4. **Test** - The QA engineer validates behavior and coverage.

## Usage

Load the individual agents and orchestrate them through the workflow, or
drive the whole flow with the lead agent:

```bash
# The lead agent coordinates the composition
backend-developer: "Coordinate the full-stack-team for: <feature>"
```

## Related Assets

- Agent definitions live in `assets/agents/`.
- Use the `feature-delivery` prompt chain to drive the whole workflow:
  `assets/prompt-chains/feature-delivery/chain.json`.
