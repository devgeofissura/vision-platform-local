# Backend Starter Bundle

The `backend-starter` bundle packages everything needed to start a new
backend project with strong API, data, and testing foundations.

## Contents

### Skills

- `api-design` - Complete guide for RESTful API design
- `rest-api-design` - REST API design patterns and best practices
- `database-design` - Data modeling and schema design
- `unit-testing` - Unit testing and test-driven development

### Agents

- `backend-developer` - Backend Developer specialized in APIs and distributed systems

### Prompts

- `code-review-checklist` - Review backend implementation against a comprehensive checklist

## Installation

The bundle is installed by copying its assets into the kit and
regenerating the registry index:

```bash
# 1. Make sure all referenced assets exist in the kit
#    (skills, agents, and prompts from the Contents section above)

# 2. Regenerate the registry indexes
./core/registry/generate.sh

# 3. Validate the registry
./core/registry/validate.sh
```

## Usage

With the bundle registered, you can use the bundled assets directly:

- Load the `backend-developer` agent to get a backend-focused assistant.
- Invoke the `code-review-checklist` prompt to review backend changes.
- Combine the bundled skills when designing APIs, models, and tests.
