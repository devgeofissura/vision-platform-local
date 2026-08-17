---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: free-llm-models
description: 'Guide to free reputable online LLMs: which models exist, free tiers, use cases, prompting and privacy caveats.'
category: ai
version: 0.1.0
author: devtiagoabreu
tags: [llm, ai, free-tier, deepseek, qwen, gemini, mistral, groq, perplexity, copilot, huggingface]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Internet access to the provider websites listed below
  - A provider account for services that require login
  - Basic knowledge of prompts and token limits
provides:
  - A curated list of free, reputable online LLMs
  - Free-tier limits and strengths for each provider
  - Guidance on when to use each model
  - Prompting considerations and data privacy warnings
---

# Free LLM Models Guide

## Overview

This skill is a practical guide to free, reputable online LLMs. It helps you
choose a model, understand free-tier limits, write effective prompts, and stay
safe with your data. The models below are well-known and frequently updated, so
always confirm details on the official websites.

This guide is informational only. Free tiers change often, and providers may
store or use conversations for training. Never send confidential or personal
data to a free service without reviewing its terms of use.

## Prerequisites

- Access to the internet and the official provider sites
- An account with providers that require one for the free tier
- Awareness that free-tier limits change and should be re-checked
- No expectation that a free tier is appropriate for sensitive data

## Usage Instructions

### 1. Choose a Model for the Task

Match the model to the task. Reasoning-heavy work benefits from strong
general-purpose models; fast coding completions benefit from code-focused
assistants; open-source research benefits from models you can inspect or host.

```text
Task categories:
- General writing and analysis: Gemini Flash, Mistral Small, DeepSeek
- Code assistance: GitHub Copilot Free, Groq-hosted models, Qwen Coder
- Fast experiments and math: Groq (high-speed inference)
- Research and citations: Perplexity (search-augmented answers)
- Open-weight models to inspect or self-host: Llama, Qwen, DeepSeek
```

### 2. Know the Free Tiers and Limits

Each provider offers a free tier with different limits. Understand the model
sizes, request quotas, and context windows before building on them.

```markdown
- DeepSeek: chat access and a free API tier with a daily token budget
- Qwen: free chat on the Qwen portal; open weights on Hugging Face
- Llama: open weights; access via Groq, Hugging Face, and GitHub Models
- Google Gemini: free tier with Gemini Flash on AI Studio
- Mistral: free tier on La Plateforme and chat on Le Chat
- Groq: fast inference with free quotas for hosted Llama and Qwen models
- Perplexity: free tier with a limited number of search queries
- GitHub Copilot Free: monthly quota of completions and premium requests
- Hugging Face Chat: chat with community-hosted open models
```

### 3. Write Effective Prompts

Keep prompts specific, structured, and within the model's context window.
Request reasoning steps, define the audience, and ask for uncertainty to be
stated. Test on small inputs before scaling up.

```text
Good prompt shape:
Role + task + input + constraints + output format.

Example:
"You are a technical writer. Summarize the text below in 5 bullets for a
developer audience. Do not invent facts. If unsure, say so.
Text: <paste here>"
```

### 4. Respect Privacy and Data Boundaries

Free tiers may use inputs for training, review, or product improvement. Treat
every free conversation as potentially visible. Never paste secrets, personal
data, client data, or internal documents.

```yaml
privacy_do:
  - "Check the provider terms of use before sending any data"
  - "Use anonymous, synthetic data for testing and demos"
  - "Prefer local or contract-based models for sensitive content"
privacy_dont:
  - "Never send passwords, keys, or tokens"
  - "Never send customer or personal data to free tiers"
  - "Never rely on a free tier for compliance-critical tasks"
```

### 5. Stay Current

Model names, quotas, and features change frequently. Re-verify the official
sites periodically and treat stale knowledge as a risk. When in doubt, choose a
model you can test with your own representative workload.

## Examples

### Example 1: Model selection for a small team

```json
{
  "goal": "Free AI assistant for internal docs summarization",
  "team": "5 developers, non-sensitive public docs",
  "options": [
    "Gemini Flash (free tier)",
    "Mistral Small (free tier)",
    "Groq + Llama 3.1 (free quota)"
  ],
  "recommendation": "Gemini Flash (free tier)",
  "reason": "Good quality and generous free quota for low-volume internal use",
  "warning": "Re-check limits; use synthetic data for anything internal"
}
```

### Example 2: Prompt for comparing models

```text
Compare the following free models for a Portuguese-language summarization
task: Gemini Flash, Mistral Small, and Llama 3.1 8B via Groq.

For each, report: typical quality, latency feel, free-tier limit, and privacy
notes. Recommend one and justify your choice. State assumptions clearly.
```

## References

- [DeepSeek](https://deepseek.com)
- [Qwen](https://qwen.ai)
- [Google AI for Developers](https://ai.google.dev)
- [Mistral AI](https://mistral.ai)
- [Groq](https://groq.com)
- [Perplexity](https://www.perplexity.ai)
- [Hugging Face](https://huggingface.co)
- [GitHub Copilot](https://github.com/features/copilot)
