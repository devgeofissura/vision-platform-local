---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: terraform-aws
description: Best practices for Terraform with AWS cloud infrastructure
category: devops
version: 0.1.0
author: devtiagoabreu
tags: [terraform, aws, infrastructure-as-code, cloud]
compatible:
  - opencode
  - claude-code
  - cursor
---

# Terraform AWS Best Practices

## Overview

This skill provides best practices for using Terraform with AWS cloud infrastructure, including module design, state management, and security.

## Prerequisites

- Terraform installed
- AWS CLI configured
- Basic understanding of AWS services

## Usage Instructions

### Step 1: Provider Configuration

Always pin provider versions:

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
  required_version = ">= 1.0"
}
```

### Step 2: State Management

Use remote state with locking:

```hcl
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
```

### Step 3: Module Design

Create reusable modules:

```hcl
module "vpc" {
  source = "./modules/vpc"
  
  cidr_block = "10.0.0.0/16"
  environment = "production"
  tags = {
    Environment = "production"
    ManagedBy   = "terraform"
  }
}
```

### Step 4: Security

Use IAM roles instead of access keys:

```hcl
resource "aws_iam_role" "example" {
  name = "example-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}
```

## Examples

### VPC Module

```hcl
module "vpc" {
  source = "./modules/vpc"
  
  cidr_block = "10.0.0.0/16"
  
  availability_zones = [
    "us-east-1a",
    "us-east-1b",
    "us-east-1c"
  ]
  
  public_subnets = [
    "10.0.1.0/24",
    "10.0.2.0/24",
    "10.0.3.0/24"
  ]
  
  private_subnets = [
    "10.0.4.0/24",
    "10.0.5.0/24",
    "10.0.6.0/24"
  ]
}
```

## Best Practices

1. Use remote state with locking
2. Pin provider versions
3. Use modules for reusability
4. Implement proper tagging
5. Use IAM roles instead of access keys
6. Enable encryption at rest and in transit

## References

- [Terraform AWS Provider Documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Terraform Best Practices](https://www.terraform-best-practices.com/)