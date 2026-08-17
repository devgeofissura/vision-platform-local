---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: google-cloud-architecture
description: Architect scalable Google Cloud solutions with gcloud, VPC networking, GKE, and IAM security best practices.
category: cloud
version: 0.1.0
author: devtiagoabreu
tags: [gcp, gcloud, gke, kubernetes, vpc, iam, google-cloud]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - A Google Cloud project with billing enabled
  - gcloud CLI installed and authenticated
  - Docker and kubectl for GKE work
  - Basic networking concepts (CIDR, subnets, load balancers)
provides:
  - gcloud project and resource hierarchy patterns
  - VPC and firewall design guidance
  - GKE cluster deployment with kubectl
  - IAM and service-account best practices
---

# google-cloud-architecture

## Overview

Google Cloud (GCP) organizes resources in a hierarchy: organization ->
folders -> projects -> resources. Everything is governed by IAM, and
networking is defined by VPCs and firewall rules. This skill covers the
three layers you will touch daily — `gcloud` operations, VPC networking,
and GKE (Kubernetes) — with an IAM-first mindset.

Design for least privilege from project one: service accounts for
machines, groups for humans, and no orphaned `Owner` keys. Prefer
managed services (Cloud Run, GKE) over raw compute VMs unless you need
bare metal.

## Prerequisites

- A Google Cloud project (billing enabled) and an IAM role you can expand
- `gcloud` CLI: `gcloud auth login && gcloud auth application-default login`
- `kubectl` and `docker` installed for the GKE section
- Comfort with CIDR blocks, subnetting, and firewall rules

## Usage Instructions

### 1. Project and IAM Setup

Create a project and grant the smallest role that does the job. Use
groups and service accounts; never hand out user `Owner` rights by
default.

```bash
PROJECT=my-app-prod
gcloud projects create $PROJECT --name="My App (prod)"
gcloud config set project $PROJECT

gcloud iam service-accounts create app-runner \
  --display-name="App Runner SA"

gcloud projects add-iam-policy-binding $PROJECT \
  --member="serviceAccount:app-runner@$PROJECT.iam.gserviceaccount.com" \
  --role="roles/run.invoker"
```

### 2. VPC and Firewall Design

Put backends in private subnets and expose only through load balancers
or Cloud Run ingress. Default deny applies to firewall rules unless you
create an allow rule:

```bash
gcloud compute networks create my-vpc --subnet-mode=custom

gcloud compute networks subnets create app-subnet \
  --network=my-vpc --region=us-central1 \
  --range=10.10.0.0/24 \
  --private-ip-google-access

# Only the LB and health checks may reach the app
gcloud compute firewall-rules create allow-lb-to-app \
  --network=my-vpc \
  --direction=INGRESS --action=ALLOW \
  --rules=tcp:8080 \
  --source-ranges=130.211.0.0/22,35.191.0.0/16
```

### 3. GKE Cluster and Deployment

Provision a cluster, configure `kubectl`, and deploy a workload. Use
private nodes and workload identity so pods authenticate without keys:

```bash
gcloud container clusters create app-cluster \
  --region us-central1 --num-nodes 3 \
  --network my-vpc --subnetwork app-subnet \
  --enable-private-nodes --release-channel regular

gcloud container clusters get-credentials app-cluster \
  --region us-central1
```

```yaml
apiVersion: apps/v1
kind: Deployment
metadata: { name: web }
spec:
  replicas: 3
  selector: { matchLabels: { app: web } }
  template:
    metadata: { labels: { app: web } }
    spec:
      containers:
        - name: web
          image: gcr.io/my-app-prod/web:latest
          ports: [{ containerPort: 8080 }]
```

Expose it:

```bash
kubectl apply -f deployment.yaml
kubectl expose deployment web --type=LoadBalancer --port=80 --target-port=8080
kubectl get svc web   # -> EXTERNAL-IP
```

### 4. Audit and Cost Hygiene

Review IAM and spend regularly; orphaned resources are the usual leak:

```bash
gcloud projects get-iam-policy $PROJECT --format=json

gcloud billing projects describe $PROJECT
gcloud services list --enabled
```

## Best Practices

- Organize by folders and projects per environment; tag resources for cost.
- Use service accounts + Workload Identity for anything that talks to GCP APIs.
- Prefer private subnets with Cloud NAT for egress; avoid public compute.
- Scope firewalls to load balancer ranges and health checks only.
- Enable audit logs and review the security dashboard quarterly.

## Pitfalls / Common Mistakes

- Running nodes on the default network with public IPs and wide-open 0.0.0.0/0.
- Embedding service-account JSON keys in images or git — use Workload Identity.
- Forgetting to update the `kubectl` context and deploying to the wrong cluster.
- Creating firewall allows wider than needed, defeating default-deny.
- Scaling a cluster to zero and being surprised by costs from static IPs or disks.

## Examples

### Example 1: Cloud Run one-liner deploy

```bash
gcloud run deploy web \
  --image gcr.io/my-app-prod/web:latest \
  --region us-central1 --allow-unauthenticated \
  --cpu-boost
```

### Example 2: Inspect cluster nodes

```bash
kubectl get nodes -o wide
kubectl top nodes
gcloud container clusters list
```

## References

- [gcloud CLI reference](https://cloud.google.com/sdk/gcloud/reference)
- [VPC networking on Google Cloud](https://cloud.google.com/vpc/docs)
- [Google Kubernetes Engine docs](https://cloud.google.com/kubernetes-engine/docs)
