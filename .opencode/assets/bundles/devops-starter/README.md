# DevOps Starter Bundle

The `devops-starter` bundle packages the assets needed to stand up a
reliable delivery pipeline and production observability for a project.

## Contents

### Skills

- `docker-best-practices` - Containerization best practices
- `ci-cd-pipeline` - Continuous integration and delivery pipelines
- `terraform-aws` - Infrastructure as code on AWS with Terraform
- `monitoring-observability` - Metrics, logs, and tracing for production

### Agents

- `devops-engineer` - DevOps Engineer for pipelines, infrastructure, and reliability

### Prompts

- `performance-review` - Analyze and improve system performance

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

- Load the `devops-engineer` agent to get a delivery-focused assistant.
- Invoke the `performance-review` prompt to find bottlenecks.
- Combine the bundled skills when containerizing, automating, and
  deploying to the cloud.
