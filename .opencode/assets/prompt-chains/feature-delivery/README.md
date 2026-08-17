# Feature Delivery Chain

The `feature-delivery` chain drives a feature from an idea through a
planned, reviewed, and tested delivery.

## Steps

| Step | Prompt | Purpose |
|------|--------|---------|
| 1 | `feature-planning` | Plan the feature (scope, tasks, acceptance criteria) |
| 2 | `code-review-checklist` | Review the implementation systematically |
| 3 | `test-strategy` | Define test coverage and quality gates |

## Usage

Run the steps in order, feeding the output of each step into the next:

```bash
# Step 1: Plan the feature
#   prompt: feature-planning
#   inputs: feature_name, requirements
#   output: implementation plan + acceptance criteria

# Step 2: Review the implementation
#   prompt: code-review-checklist
#   inputs: code, language
#   output: structured review feedback

# Step 3: Define test coverage
#   prompt: test-strategy
#   inputs: project, testing_goals
#   output: layered test strategy and coverage targets
```

## Related Assets

- Prompts live in `assets/prompts/`.
- Pair with the `full-stack-team` composition to staff the delivery:
  `assets/compositions/full-stack-team/composition.json`.
