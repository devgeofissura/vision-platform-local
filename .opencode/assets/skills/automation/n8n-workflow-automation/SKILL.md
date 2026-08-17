---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: n8n-workflow-automation
description: Build, debug and maintain n8n automation workflows. Use when creating or fixing n8n workflows, webhooks, integrations between apps (WhatsApp, CRM, sheets, HTTP APIs), scheduling, error handling in workflows, or when users mention n8n, workflow, webhook, node, trigger or automation.
category: automation
version: 0.1.0
author: devtiagoabreu
tags: [n8n, automation, workflow, webhook, integration, no-code]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - An n8n instance (self-hosted Docker or n8n.cloud)
  - Credentials for the services you connect
  - Understanding of JSON data flow between nodes
provides:
  - Workflow design patterns (trigger → process → act → notify)
  - Webhook trigger and response patterns
  - HTTP Request node usage for custom APIs
  - Error handling, retries and idempotency
  - WhatsApp/Evolution and CRM integration patterns
  - Workflow import/export best practices
difficulty: beginner
frameworks: [n8n]
languages: [json, typescript]
---

# n8n Workflow Automation

## Overview

n8n is a node-based automation platform. Workflows are **JSON**, so version them
in git and review them like code. Design every workflow as
`Trigger → Process → Transform → Act → Notify`, and assume nodes will fail.

## Prerequisites

- An n8n instance (self-hosted Docker or n8n.cloud)
- Credentials for the services you connect
- Understanding of JSON data flow between nodes

## 1. Core Concepts

- **Trigger node** starts the flow: Webhook, Schedule, Event (WhatsApp, CRM, forms...).
- **Action node** does work: HTTP Request, Send Email, database write, app-specific nodes.
- **Data flows** as arrays of JSON items; most nodes process one item at a time.
- **Expressions** (`{{ $json.field }}`) reference item data. Use them in node parameters.
- **Execute once per item vs once for all items**: configure via node "Execute" options — often the root cause of "it ran N times / only once".

## 2. Workflow Design Patterns

### Pattern: Webhook → validate → process → reply

```
Webhook (POST /whatsapp) → HTTP Request (chatbot API) → Set (reply) → Respond to Webhook
```

- Validate the payload shape early (a failed parse should not 500 the caller).
- Reply to the webhook **synchronously** when the caller waits for a response; otherwise fire-and-forget.
- Keep timeouts in mind: if downstream can be slow, return `202` immediately and process async.

### Pattern: Schedule → batch job → notify

```
Schedule (daily 06:00) → HTTP Request (fetch data) → Merge/Filter → Spreadsheet (append) → Email/Slack notify
```

- Add an IF node for "no data → skip notification" to avoid noisy empty reports.

## 3. HTTP Request Node (talk to any API)

Use it for APIs without a dedicated node (e.g. custom backends, Evolution API).

| Config | Recommendation |
|--------|----------------|
| Method / URL | explicit per environment (n8n vars or expressions) |
| Auth | credential or header expression `{{ $env.API_KEY }}` — never hardcode |
| Response format | JSON by default; use "Response" tab options for binary/raw |
| Timeout | set a sensible one (defaults can hang) |
| Retry | enabled with backoff for transient 5xx/429 |

### Example: POST JSON to your API

```
Method: POST
URL: {{ $env.BACKEND_URL }}/api/leads
Headers: Authorization: Bearer {{ $env.BACKEND_TOKEN }}
Body (JSON):
{
  "name": "{{ $json.contactName }}",
  "phone": "{{ $json.phone }}",
  "source": "whatsapp-bot"
}
```

**Note on n8n data:** the input of an HTTP node is an array of items. If the
body must be a single object, use `Set` (Mode: JSON, Keep existing fields) or
`{{ $json }}` and set "Send Body" appropriately. This is the most common bug —
the API receives an array when it expects an object (or vice-versa).

## 4. Error Handling and Reliability

- Wrap risky branches in **Error Trigger** + `Try/Catch` nodes so failures notify instead of silently dying.
- Prefer **idempotent** actions: before creating a record, check it doesn't exist (dedupe by external id).
- For retries use the node's retry settings or an external queue — don't rely on manual replay.
- Log key fields (`error.message`, `$json`, run id) to a spreadsheet/DB for audit.
- Test the **failure path**, not just the happy path: what happens when the API is down?

## 5. Webhook Responses

```json
// Webhook node config
{
  "httpMethod": "POST",
  "path": "whatsapp",
  "responseMode": "responseNode" // or "onReceived" for immediate 200
}
```

Use "Respond to Webhook" node to control the reply. For platforms like
Evolution API that expect a fast ack, respond immediately with `{"ok": true}`.

## 6. WhatsApp / Evolution Integration

- **Trigger:** Evolution API webhook → n8n Webhook node (`/webhook/evolution`).
- **Act:** HTTP Request node → Evolution `POST /message/sendText/{instance}` with `apikey` header.
- Route by intent: IF node on message text → different workflows (product catalog, attendance, CRM lead creation).
- Never reply to messages sent by the bot (`fromMe: true`) — filter in an early IF node.

See the `evolution-api` skill for the exact endpoints and payloads.

## 7. CRM Integration Pattern

From a WhatsApp/new lead event to CRM:

```
Webhook → IF (message has phone) → HTTP (search CRM contact by phone)
                                     ├─ exists → Update contact / add note
                                     └─ not exists → HTTP (create lead) → notify
```

Store external IDs (WhatsApp JID ↔ CRM id) so repeated events update instead of duplicating records.

## 8. Import/Export and Versioning

- Export workflows as JSON and commit them to git. Review diffs like code.
- Use **n8n environment variables** (`$env.X`) for secrets and per-environment URLs — never hardcode.
- Put **expressions for variable params** so the same workflow works in dev/prod.
- Prefer a few focused workflows over one giant graph; each workflow should have one responsibility.

## Examples

### Example 1: Minimal webhook → HTTP → respond

```
1. Webhook (POST /ingest)                # receives JSON { id, qty }
2. Set (Fields to set)                   # enrich: receivedAt = {{ $now }}
3. HTTP Request (POST backend/api/orders)
4. Respond to Webhook (JSON { ok: true })
```

### Example 2: IF + Try/Catch skeleton

```
Webhook
└─ Try (IF phone != "")
     ├─ yes → HTTP (create lead) → Respond
     └─ no  → Respond (400: phone missing)
└─ Catch → HTTP (notify #errors) → Respond (500)
```

### Example 3: Expression reference

```json
{
  "name": "{{ $json.name }}",
  "phone": "{{ $json.phone.replace(' ', '') }}",
  "total": "{{ Number($json.price) * Number($json.qty) }}"
}
```

## Notes

- Simpler workflow > clever workflow. Each extra node is a failure point.
- Always test with the **real payload shape** (export a sample from the platform).
- Use `$json`, `$now`, `$env` and `$item(0)` deliberately; check expression results in the node's "Output data".
- Pair with `business-intelligence` for reporting workflows and `evolution-api` for WhatsApp bots.

## References

- [n8n Docs](https://docs.n8n.io/)
- [n8n Expressions](https://docs.n8n.io/code/builtin/overview/)
- [Webhook node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.webhook/)
- [HTTP Request node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/)
