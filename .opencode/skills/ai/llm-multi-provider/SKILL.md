---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: llm-multi-provider
description: Integrate multiple LLM providers (OpenAI, Anthropic, Groq, Gemini, DeepSeek) with automatic fallback, priority and key management. Use when building apps that call chat models, need provider redundancy, key rotation, fallback on failure, cost control, or when users mention LLM keys, providers, fallback, Groq, DeepSeek, OpenAI, Anthropic or Gemini integration.
category: ai
version: 0.1.0
author: devtiagoabreu
tags: [llm, multi-provider, fallback, openai, anthropic, groq, gemini, deepseek]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - API keys for at least one LLM provider
  - Server-side storage for keys (never expose on the client)
  - A `fetch`/HTTP-capable runtime (Node 18+, Python 3.9+)
provides:
  - Provider abstraction with OpenAI-compatible endpoints
  - Priority-ordered fallback with failure counting
  - Key management (multiple keys per provider, test connection)
  - Streaming and timeouts per provider
  - Usage/cost logging hooks
difficulty: intermediate
frameworks: [openai, anthropic, groq, gemini, deepseek]
languages: [typescript, javascript, python]
---

# LLM Multi-Provider Integration

## Overview

A thin layer in front of chat-model providers that gives you **one API**,
**automatic fallback**, and **key rotation**. Most providers (OpenAI, Groq,
DeepSeek, Together, and many local gateways) expose an OpenAI-compatible
`/v1/chat/completions` endpoint — implement the OpenAI shape once and reuse it.

## Prerequisites

- API keys for at least one LLM provider
- Server-side storage for keys (never expose on the client)
- A `fetch`/HTTP-capable runtime (Node 18+, Python 3.9+)

## Core Design

- **Keys live on the server** (env or DB), never in the client bundle.
- **Providers ordered by priority.** Try in order; on failure move to the next.
- **Per-key failure counter.** Disable keys after repeated failures; re-enable after a cooldown.
- **Timeout + retry** at the transport level so one dead key doesn't hang the request.

## Provider Abstractions

### OpenAI-compatible endpoint (covers OpenAI, Groq, DeepSeek, Together)

```python
import httpx

def chat(provider: dict, messages: list[dict], **kwargs):
    """provider = {"base_url": ..., "api_key": ..., "model": ...}"""
    resp = httpx.post(
        f"{provider['base_url']}/chat/completions",
        headers={"Authorization": f"Bearer {provider['api_key']}"},
        json={"model": provider["model"], "messages": messages, **kwargs},
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]
```

Base URLs:

| Provider | `base_url` | Notes |
|----------|------------|-------|
| OpenAI | `https://api.openai.com/v1` | `model: gpt-4o-mini` |
| Groq | `https://api.groq.com/openai/v1` | `model: llama-3.3-70b-versatile` |
| DeepSeek | `https://api.deepseek.com/v1` | `model: deepseek-chat` |
| Together / others | per vendor | OpenAI-compatible |

### Anthropic (separate shape)

Anthropic uses a different API (`/v1/messages`, `x-api-key`). Wrap it behind
the same interface so callers don't care:

```python
def chat_anthropic(provider, messages, **kwargs):
    resp = httpx.post(
        f"{provider['base_url']}/v1/messages",
        headers={"x-api-key": provider["api_key"], "anthropic-version": "2023-06-01"},
        json={"model": provider["model"], "max_tokens": kwargs.get("max_tokens", 1024),
              "messages": [m for m in messages if m["role"] != "system"],
              "system": next((m["content"] for m in messages if m["role"] == "system"), None)},
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()["content"][0]["text"]
```

## Fallback Orchestrator

```python
class LLMRouter:
    def __init__(self, providers):
        self.providers = providers  # ordered by priority, each with a failure count

    def chat(self, messages, **kwargs):
        last_error = None
        for provider in self.providers:
            if provider.get("disabled"):
                continue
            try:
                text = call_provider(provider, messages, **kwargs)
                provider["failures"] = 0
                return text
            except Exception as e:  # timeouts, 4xx/5xx, rate limits
                provider["failures"] = provider.get("failures", 0) + 1
                if provider["failures"] >= provider.get("max_failures", 3):
                    provider["disabled"] = True
                last_error = e
        raise RuntimeError(f"all providers failed: {last_error}")
```

**Disable + cooldown:** store `disabled_until = now + 300s` instead of a hard
flag, and re-check on each call. Reset failures after a successful call.

## Streaming

Stream from the first working provider; hide provider selection from the UI:

```ts
export async function* streamChat(router, messages) {
  for (const provider of router.providers) {
    if (provider.disabled) continue;
    try {
      const res = await fetch(`${provider.baseUrl}/chat/completions`, {
        method: "POST",
        headers: { Authorization: `Bearer ${provider.apiKey}` },
        body: JSON.stringify({
          model: provider.model, messages,
          stream: true,
        }),
      });
      if (!res.ok || !res.body) throw new Error(`HTTP ${res.status}`);
      // parse SSE lines: "data: {...}" chunks; yield delta.content
      yield* parseSSE(res.body);
      return;
    } catch (e) {
      continue; // try next provider
    }
  }
  throw new Error("no provider available");
}
```

## Key Management

- Store keys per provider, multiple keys allowed (rotation on failure).
- `POST /api/keys/test` calls the provider with a tiny prompt to validate a key before saving.
- Never log the key; log only provider id + model + token usage.
- Rotate: on repeated `401`/`429`, move to the next key for that provider.

### Test-connection helper

```python
def test_key(base_url, api_key, model="gpt-4o-mini"):
    try:
        return chat({"base_url": base_url, "api_key": api_key, "model": model},
                    [{"role": "user", "content": "ping"}]) is not None
    except Exception:
        return False
```

## Usage/Cost Logging

Record per call: `provider`, `model`, `prompt_tokens`, `completion_tokens`,
`duration_ms`, `success`. This powers dashboards and tells you which provider
to promote in priority.

## Security Notes

- Treat keys as secrets: server-side env or encrypted DB, restricted to the API layer.
- Validate that requests to `/api/keys` are admin-only and never return full keys.
- Don't interpolate raw user input into prompts without sanitization when the prompt is built server-side.
- If the app is client-heavy, keep the router behind a server route — never expose provider list with keys.

## Examples

### Example 1: JS key provider config

```js
// providers ordered by priority; each may hold multiple keys
const providers = [
  { id: "groq", baseUrl: "https://api.groq.com/openai/v1", model: "llama-3.3-70b-versatile", keys: [GROQ_KEY], failures: 0 },
  { id: "openai", baseUrl: "https://api.openai.com/v1", model: "gpt-4o-mini", keys: [OPENAI_KEY], failures: 0 },
];
```

### Example 2: SQL schema for key management

```sql
CREATE TABLE llm_keys (
    id          SERIAL PRIMARY KEY,
    provider    TEXT NOT NULL,          -- openai | anthropic | groq | gemini | deepseek
    name        TEXT NOT NULL,
    key_value   TEXT NOT NULL,          -- criptografe em produção
    priority    INT NOT NULL DEFAULT 10, -- menor = mais usado
    enabled     BOOLEAN NOT NULL DEFAULT true,
    failures    INT NOT NULL DEFAULT 0,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

## Notes

- Most providers are OpenAI-compatible; only Anthropic needs a dedicated wrapper (Gemini can be wrapped too).
- A 429/rate-limit counts as failure but is usually transient — back off 5–30s before disabling.
- Test keys on save so users catch typos immediately.
- Combine with `rag-llm` and `evolution-api` for AI chatbots, and with `business-intelligence` for usage dashboards.

## References

- [OpenAI API reference](https://platform.openai.com/docs/api-reference)
- [Anthropic Messages API](https://docs.anthropic.com/en/api/messages)
- [Groq API docs](https://console.groq.com/docs)
- [DeepSeek API docs](https://api-docs.deepseek.com/)
- [Gemini API docs](https://ai.google.dev/gemini-api/docs)
