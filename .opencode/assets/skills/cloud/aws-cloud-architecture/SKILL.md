---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: aws-cloud-architecture
description: Architect serverless AWS solutions with SAM templates, IAM, VPCs, and the AWS CLI for repeatable deployments.
category: cloud
version: 0.1.0
author: devtiagoabreu
tags: [aws, serverless, sam, lambda, iam, vpc, cloudformation]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - An AWS account with appropriate IAM permissions
  - AWS CLI installed and configured (aws configure)
  - A Node.js/Python runtime for Lambda development
  - Basic networking concepts (subnets, CIDR, security groups)
provides:
  - SAM/serverless YAML templates
  - IAM least-privilege patterns
  - VPC and subnet design guidance
  - CLI deployment and CI/CD workflows
---

# aws-cloud-architecture

## Overview

AWS solutions combine compute, storage, and networking behind strict
security boundaries. Serverless-first with the Serverless Application
Model (SAM) keeps infrastructure as code, deployable in one command,
while IAM policies and VPCs control who can reach what.

This skill covers the architecture loop: template -> build/test locally ->
deploy -> verify with the CLI. Start small and boring (Lambda + S3 +
DynamoDB), and only add services that solve a demonstrated need.

## Prerequisites

- An AWS account and an IAM user with keys scoped to your project
- `aws` CLI configured (`aws configure` or an SSO profile)
- `sam` CLI installed (`pip install aws-sam-cli`)
- Docker (optional) for local Lambda testing
- Comfort with YAML and basic CIDR math

## Usage Instructions

### 1. SAM Serverless Template

SAM extends CloudFormation. A minimal HTTP API backed by Lambda and a
table shows the shape:

```yaml
AWSTemplateFormatVersion: "2010-09-09"
Transform: AWS::Serverless-2016-10-31

Globals:
  Function:
    Runtime: python3.11
    Timeout: 10
    MemorySize: 256
    Tracing: Active

Resources:
  ItemsTable:
    Type: AWS::DynamoDB::Table
    Properties:
      BillingMode: PAY_PER_REQUEST
      KeySchema: [{ AttributeName: id, KeyType: HASH }]
      AttributeDefinitions: [{ AttributeName: id, AttributeType: S }]

  ApiFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: src/
      Handler: app.handler
      Policies:
        - Statement:
            - Effect: Allow
              Action: [dynamodb:GetItem, dynamodb:PutItem]
              Resource: !GetAtt ItemsTable.Arn
      Events:
        Api:
          Type: Api
          Properties: { Path: /items/{id}, Method: ANY }
```

### 2. IAM Least Privilege

Scope policies to the resource ARN, never `"Action": "*"` on core
services. Separate roles for Lambda, CI, and humans:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject"],
      "Resource": ["arn:aws:s3:::my-bucket/uploads/*"]
    }
  ]
}
```

Validate before deploying with `simulate-principal-policy`:

```bash
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::123456789012:role/my-role \
  --action-names s3:GetObject s3:DeleteObject
```

### 3. VPC Design

Use private subnets for compute that touches databases, NAT for outbound
only, and security groups as the primary firewall. A minimal VPC:

```yaml
Resources:
  Vpc:
    Type: AWS::EC2::VPC
    Properties: { CidrBlock: 10.0.0.0/16 }
  PrivateSubnetA:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref Vpc
      CidrBlock: 10.0.1.0/24
      AvailabilityZone: !Select [0, !GetAZs ""]
  AppSg:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: app access
      VpcId: !Ref Vpc
      SecurityGroupIngress:
        - { IpProtocol: tcp, FromPort: 443, ToPort: 443,
            CidrIp: 10.0.0.0/16 }
```

Lambda in a VPC needs a NAT for internet egress — or use VPC endpoints
for AWS services to avoid NAT costs.

### 4. Local Build, Test, and Deploy

Develop and deploy with the SAM CLI loop:

```bash
sam build --use-container
sam local start-api            # test HTTP locally
sam validate
sam deploy --guided \
  --capabilities CAPABILITY_IAM
```

## Best Practices

- Infrastructure as code with SAM/CloudFormation; never click-deploy prod.
- Least privilege on IAM, audited via CloudTrail and Access Advisor.
- Separate private subnets from public ones; security groups over NACLs.
- Enable managed tracing (X-Ray) and structured JSON logs from day one.
- Tag everything (`CostCenter`, `Env`) for cost attribution and cleanups.

## Pitfalls / Common Mistakes

- Granting `"Action": "*"` on S3/DynamoDB and widening the blast radius.
- Lambda in a VPC with no NAT and no endpoints — it silently times out on egress.
- Hardcoding account IDs/regions in templates instead of pseudo-parameters.
- Deploying with `aws lambda update-function-code`, bypassing SAM state.
- Ignoring cold starts on synchronous user-facing APIs; keep Lambdas warm or short.

## Examples

### Example 1: Bucket policy for public read of one folder

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::cdn-example/public/*"
  }]
}
```

### Example 2: List resources via CLI

```bash
aws cloudformation describe-stacks \
  --stack-name my-app --query "Stacks[0].Outputs"
aws s3 ls s3://my-bucket/uploads/ --recursive --human-readable
```

## References

- [AWS Serverless Application Model](https://docs.aws.amazon.com/serverless-application-model/)
- [AWS IAM documentation](https://docs.aws.amazon.com/iam/)
- [Amazon VPC documentation](https://docs.aws.amazon.com/vpc/)
