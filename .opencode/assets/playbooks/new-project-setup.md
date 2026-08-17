---
name: new-project-setup
description: Complete guide for setting up a new project with best practices
version: 0.1.0
author: devtiagoabreu
tags: [project-setup, initialization, best-practices]
compatible:
  - opencode
  - claude-code
  - cursor
steps:
  - title: Initialize Git Repository
    description: Create a new Git repository with proper configuration
    commands:
      - git init
      - git config user.name "Your Name"
      - git config user.email "your.email@example.com"
  - title: Create Project Structure
    description: Set up the basic project directory structure
    commands:
      - mkdir -p src tests docs
      - touch README.md .gitignore LICENSE
  - title: Set Up Package Manager
    description: Initialize package manager (npm/yarn/pip)
    commands:
      - npm init -y  # For Node.js projects
      - pip install -r requirements.txt  # For Python projects
  - title: Configure Linting
    description: Set up linting and formatting tools
    commands:
      - npm install --save-dev eslint prettier  # For Node.js
      - pip install flake8 black  # For Python
  - title: Set Up Testing
    description: Configure testing framework
    commands:
      - npm install --save-dev jest  # For Node.js
      - pip install pytest  # For Python
  - title: Create CI/CD Pipeline
    description: Set up GitHub Actions or similar CI/CD
    commands:
      - mkdir -p .github/workflows
estimatedTime: 30 minutes
difficulty: beginner
---

# New Project Setup Playbook

## Overview

This playbook guides you through setting up a new project with industry best practices.

## Prerequisites

- Git installed
- Node.js or Python installed
- Code editor installed

## Steps

### Step 1: Initialize Git Repository

```bash
git init
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

### Step 2: Create Project Structure

```bash
mkdir -p src tests docs
touch README.md .gitignore LICENSE
```

### Step 3: Set Up Package Manager

For Node.js:
```bash
npm init -y
```

For Python:
```bash
pip install -r requirements.txt
```

### Step 4: Configure Linting

For Node.js:
```bash
npm install --save-dev eslint prettier
```

For Python:
```bash
pip install flake8 black
```

### Step 5: Set Up Testing

For Node.js:
```bash
npm install --save-dev jest
```

For Python:
```bash
pip install pytest
```

### Step 6: Create CI/CD Pipeline

```bash
mkdir -p .github/workflows
```

## Expected Outcome

- Initialized Git repository
- Clean project structure
- Configured linting and testing
- Basic CI/CD pipeline