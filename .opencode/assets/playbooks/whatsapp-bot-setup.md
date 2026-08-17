---
name: whatsapp-bot-setup
description: Set up a WhatsApp bot end-to-end (Evolution API instance, webhook, state machine, AI replies)
version: 0.1.0
author: devtiagoabreu
tags: [whatsapp, evolution-api, bot, ai, webhook, n8n]
compatible:
  - opencode
  - claude-code
  - cursor
steps:
  - title: Start Evolution API
    description: Run Evolution API (Docker) with a Postgres backend
    commands:
      - docker compose up -d evolution-api
  - title: Create Instance
    description: Create an instance and connect the WhatsApp number via QR code
    commands:
      - curl -X POST "$BASE_URL/instance/create" -H "apikey: $API_KEY" -d '{"instanceName":"bot","integration":"WHATSAPP-BAILEYS","qrcode":true}'
      - curl "$BASE_URL/instance/connect/bot" -H "apikey: $API_KEY"
  - title: Configure Webhook
    description: Point Evolution webhook events to your backend or n8n
    commands:
      - curl -X POST "$BASE_URL/webhook/instance" -H "apikey: $API_KEY" -d '{"url":"https://api.example.com/webhook/evolution/bot","events":["MESSAGES_UPSERT","CONNECTION_UPDATE"]}'
  - title: Implement Message Handler
    description: Normalize messages, filter fromMe, run state machine, reply with retry queue
    commands: []
  - title: Connect AI (optional)
    description: Route intents to an LLM with a RAG context and multi-provider fallback
    commands: []
  - title: Test and Monitor
    description: Test happy path + failure path, monitor CONNECTION_UPDATE and send failures
    commands: []
---

# WhatsApp Bot Setup

## Objective

Ship a production-ready WhatsApp bot: instance connected, webhook wired,
messages answered (optionally with AI), and failures monitored.

## Instructions

### Context

You are an automation engineer. Follow the `evolution-api` skill for exact
endpoints. Keep the backend stateless: webhook events drive a per-sender state
machine persisted in the database.

### Task

1. Start Evolution API (Docker) and verify `GET /instance/fetchInstances`
2. Create + connect the instance; capture the QR and display it to pair the number
3. Configure the webhook with `MESSAGES_UPSERT` + `CONNECTION_UPDATE`
4. Implement the handler: extract text, ignore `fromMe`, load state, reply
5. Add a retry queue for sends and a convo-abandon timer
6. Add monitoring: connection state alerts and send-failure logging

### Criteria

1. **No loops:** the bot never replies to its own messages
2. **Survives restarts:** state lives in the DB, not in memory
3. **Safe:** instance keys stored server-side, never in the client
4. **Observable:** every send/state transition is logged

## Usage Example

```
Set up a WhatsApp bot that:
- answers product catalog questions with AI (using our RAG over the catalog)
- forwards new leads to the CRM as contacts
- escalates to a human when confidence is low

Use Evolution API + our backend webhook. Show the docker-compose, the instance
creation commands, the webhook handler skeleton, and the state machine design.
```

## Variations

### Variation 1: n8n-first

```
Do the same but with n8n as the orchestrator: webhook node -> IF node (fromMe
filter) -> HTTP nodes to Evolution API and the CRM, with Try/Catch + error
notification.
```

### Variation 2: Human handoff

```
Design the conversation state machine with an ESCALATED state: when the AI
can't answer (low similarity or repeated confusion), tag the chat for a human
and notify the team via WhatsApp group message.
```

## References

- [Evolution API skill](../skills/ai/evolution-api/SKILL.md)
- [n8n skill](../skills/automation/n8n-workflow-automation/SKILL.md)
- [RAG skill](../skills/ai/rag-llm/SKILL.md)
- [Evolution API Docs](https://doc.evolution-api.com/)
