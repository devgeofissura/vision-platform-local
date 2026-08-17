---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-15
name: onpremise-deployment
description: Deploy multi-service Python stacks on customer hardware with Docker Compose, CPU-first sizing, resource limits, persistence, and backup
category: devops
version: 0.1.0
author: devtiagoabreu
tags: [docker, docker-compose, on-premise, deployment, deployment-onpremise, cpu, debian, backup]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Docker and Docker Compose on the target host (Debian Stable recommended)
  - A multi-service application image set (Core API, AI Engine, DB)
  - Basic sysadmin knowledge (systemd, networking, disks)
provides:
  - Compose stack layout for the Vision Platform services
  - CPU-first resource sizing for weak hardware
  - Persistent volumes for DB, evidence, and model storage
  - Backup/restore and update workflow
---

# On-Premise Deployment

## Overview

The Vision Platform is deployed on-premise per customer (VP-013): each tenant
has its own server, and the Core never depends on the Internet to operate.
Reference hardware is modest (i5 2nd gen, 4GB RAM, SSD, 8GB swap), so CPU-first
sizing is a first-class requirement. Everything runs in Docker Compose with a
clean separation between services, volumes, and configuration.

## Prerequisites

- Debian Stable Minimal host with Docker + Compose installed
- SSD storage for PostgreSQL and evidence files
- Build/registry access for the platform images (or a local build path)

## Usage Instructions

### Step 1: Compose stack layout

Separate services by responsibility: Core API (FastAPI), AI Engine, and
PostgreSQL. Put model files and evidence on volumes:

```yaml
services:
  api:
    image: vision-platform/api:latest
    env_file: .env
    ports: ["8080:80"]
    depends_on: [db]
    volumes:
      - models:/models:ro

  ai-engine:
    image: vision-platform/ai-engine:latest
    env_file: .env
    depends_on: [db]
    volumes:
      - models:/models:ro
      - evidence:/evidence

  db:
    image: postgres:16
    env_file: .env
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
  models:
  evidence:
```

### Step 2: CPU-first sizing

Reference hardware (4GB RAM) is tight — plan around it:

- Cap each service with `deploy.resources.limits` (e.g., `memory: 2g` for AI).
- ONNX Runtime on CPU is the standard; keep model sizes small (YOLO Nano).
- Prefer swap over OOM kills on 4GB boxes; add 8GB swap in provisioning.
- Use JPEG + JSON evidence to keep disk growth bounded.

### Step 3: Configuration via env files

Secrets (DB password, JWT secret, API keys) live in `.env`, not in images:

```env
POSTGRES_PASSWORD=change-me
JWT_SECRET=change-me
AI_ENGINE_CONCURRENCY=2
```

### Step 4: Persistence and backup

- PostgreSQL data, evidence, and models must live on persistent volumes.
- Back up `pgdata` and the `evidence` volume; exclude `models` (re-downloadable).
- Use `pg_dump` on a schedule and copy the dump off-box.

### Step 5: Deploy and update

```bash
docker compose up -d
docker compose pull && docker compose up -d   # rolling update
docker compose logs -f api
```

### Step 6: Health and systemd

Wrap Compose in a systemd unit for auto-start on boot:

```ini
[Unit]
Description=Vision Platform
Requires=docker.service
After=docker.service

[Service]
ExecStart=/usr/bin/docker compose -f /opt/vision-platform/compose.yml up
ExecStop=/usr/bin/docker compose -f /opt/vision-platform/compose.yml down
Restart=on-failure
```

## Examples

### Example 1: Minimal single-node compose

See Step 1. Add `restart: unless-stopped` to each service for resilience.

### Example 2: Backup snapshot script

```bash
docker compose exec -T db pg_dump -U vision vision > backup_$(date +%F).sql
```

## References

- [Vision Platform VP-013 Deployment](docs/architecture/013-deployment.md)
- [Vision Platform VP-019 Backup/DR](docs/architecture/019-backup-disaster-recovery.md)
- [Docker Compose reference](https://docs.docker.com/compose/)
- [ONNX Runtime CPU](https://onnxruntime.ai/)

## Notes

- On-premise per customer; the Core never requires Internet access.
- CPU-first is non-negotiable: size for the 4GB reference hardware.
- Everything persistent (DB, evidence) goes on volumes; models are read-only.
- Automate backups and test restores regularly.
- Use systemd to keep the stack alive across reboots.
