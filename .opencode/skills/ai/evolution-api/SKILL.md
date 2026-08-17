---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: evolution-api
description: "Integrate WhatsApp bots with Evolution API (Baileys/Meta Cloud): sending messages/media, handling webhooks, managing instances, chat/group operations."
category: ai
version: 0.1.0
author: devtiagoabreu
tags: [whatsapp, evolution-api, bot, webhook, baileys, messaging]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - An Evolution API server (Docker) or the hosted API
  - An instance created and connected via QR code
  - '`apikey` header for authenticated calls'
  - A webhook URL reachable from the server (https recommended)
provides:
  - Instance lifecycle management (create, connect, QR, restart, logout)
  - Message sending (text, media, buttons, lists, templates)
  - Webhook configuration and event handling
  - Chat, contact and group operations
  - WhatsApp bot architecture patterns (state machine + retry queue)
difficulty: intermediate
frameworks: [evolution-api, whatsapp, node, python]
languages: [python, typescript, javascript]
---

# Evolution API (WhatsApp)

## Overview

Evolution API exposes a REST API for building WhatsApp bots. Instances are
created per WhatsApp number; a webhook delivers events to your backend. Keep
the **backend stateless** and let the webhook events drive a state machine —
this is the pattern that survives restarts and retries.

## Prerequisites

- An Evolution API server (Docker) or the hosted API
- An instance created and connected via QR code
- `apikey` header for authenticated calls
- A webhook URL reachable from the server (https recommended)

## Instance Lifecycle

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/instance/create` | Create instance |
| GET | `/instance/connect/{name}` | Get QR code |
| GET | `/instance/connectionState/{name}` | open/close/connecting |
| GET | `/instance/fetchInstances` | List instances |
| POST | `/instance/restart/{name}` | Restart |
| DELETE | `/instance/logout/{name}` | Disconnect number |
| DELETE | `/instance/delete/{name}` | Delete instance |
| POST | `/instance/setPresence/{name}` | online/typing... |

Create with webhook enabled from the start:

```json
{
  "instanceName": "comercial",
  "integration": "WHATSAPP-BAILEYS",
  "qrcode": true,
  "webhook": {
    "enabled": true,
    "url": "https://api.example.com/webhook/evolution/comercial",
    "events": ["MESSAGES_UPSERT", "CONNECTION_UPDATE"]
  }
}
```

**Tips:** store instance name + API token per tenant; log `CONNECTION_UPDATE`
events (they tell you when the number disconnects); keep one webhook URL per
instance so you can route by `instance`.

## Sending Messages

Base URL `http://<server>:8080`, header `apikey: <token>`.

### Text

```json
POST /message/sendText/{instanceName}
{
  "number": "5511999999999",
  "textMessage": { "text": "Olá! Recebemos sua mensagem." },
  "delay": 1000,
  "linkPreview": true
}
```

### Media (multipart/form-data)

Fields: `number`, `mediatype` (`image`|`video`|`audio`|`document`), `media` (file),
`caption`, `fileName`.

### Interactive (buttons / list)

```json
POST /message/sendButtons/{instanceName}
{
  "number": "5511999999999",
  "text": "Escolha uma opção:",
  "footerText": "Atendimento",
  "buttons": [
    { "buttonId": "1", "buttonText": { "text": "Sim" } },
    { "buttonId": "2", "buttonText": { "text": "Não" } }
  ]
}
```

```json
POST /message/sendList/{instanceName}
{
  "number": "5511999999999",
  "title": "Menu",
  "description": "O que deseja?",
  "buttonText": "Ver opções",
  "sections": [
    { "title": "Produtos", "rows": [{ "title": "Tecidos", "rowId": "1" }] }
  ]
}
```

Other senders: `sendLocation`, `sendContact`, `sendPoll`, `sendReaction`,
`sendTemplate` (WhatsApp Business templates).

## Receiving Messages (Webhooks)

Configure once via `/webhook/instance`:

```json
{
  "url": "https://api.example.com/webhook/evolution/comercial",
  "webhook_by_events": false,
  "webhook_base64": false,
  "events": ["QRCODE_UPDATED", "MESSAGES_UPSERT", "CONNECTION_UPDATE"]
}
```

### Important events

| Event | Meaning |
|-------|---------|
| `QRCODE_UPDATED` | QR base64 to display for pairing |
| `CONNECTION_UPDATE` | `state` open/close — alert when closed |
| `MESSAGES_UPSERT` | New incoming message (this drives your bot) |
| `MESSAGES_UPDATE` | Edited message |
| `SEND_MESSAGE` | Your bot sent a message (ignore it or log it) |
| `GROUPS_UPSERT` | Group created |

### Message payload essentials

```json
{
  "event": "MESSAGES_UPSERT",
  "instance": "comercial",
  "data": {
    "key": { "remoteJid": "5511999999999@s.whatsapp.net", "fromMe": false },
    "message": { "conversation": "Oi" },
    "messageType": "conversation"
  }
}
```

**Never reply to `fromMe: true`** (would loop). Extract sender from
`key.remoteJid`. Handle message types: `conversation`/`extendedTextMessage`
(text), `imageMessage`, `audioMessage` (ptt), `documentMessage`, and buttons
payloads.

## Bot Architecture (the pattern that scales)

1. **Webhook handler** → normalizes the message → looks up the conversation state.
2. **State machine** (per sender) drives the flow: `START → MAIN_MENU → FLOW_X`.
3. **Persist state** (DB/Redis), not in-memory — instances restart.
4. **Reply queue** with retry for `rate_limit`/timeout errors (Evolution can drop sends under load).
5. **Abandon control:** close conversations after N minutes of inactivity.

```python
# Exemplo (FastAPI): roteamento por estado
@app.post("/webhook/evolution/{instance}")
async def webhook(instance: str, payload: dict):
    if payload.get("event") != "MESSAGES_UPSERT":
        return {"ok": True}
    data = payload["data"]
    if data["key"].get("fromMe"):
        return {"ok": True}
    sender = data["key"]["remoteJid"].split("@")[0]
    text = extract_text(data.get("message"))
    state = get_state(instance, sender)          # do banco
    reply = handle_state(instance, sender, state, text)
    if reply:
        enqueue_send(instance, sender, reply)     # fila com retry
    return {"ok": True}
```

## Chat, Contacts and Groups

| Action | Endpoint |
|--------|----------|
| Mark as read | `POST /chat/markMessageAsRead/{instance}` |
| Check numbers exist | `POST /chat/whatsappNumbers/{instance}` |
| Find chats / contacts / messages | `POST /chat/findChats|findContacts|findMessages/{instance}` |
| Create group | `POST /group/create/{instance}` |
| Group participants | `POST /group/updateParticipant/{instance}` (`add`/`remove`/`promote`/`demote`) |

Number validation:

```json
POST /chat/whatsappNumbers/{instance}
{ "numbers": ["5511999999999"] }
```

Returns `exists: true/false` per number — use this before sending to non-registered numbers.

## Error Handling

Standard error envelope:

```json
{
  "success": false,
  "error": { "code": "BAD_REQUEST", "message": "..." },
  "meta": { "timestamp": "...", "path": "/message/sendText/...", "method": "POST" }
}
```

Common codes: `UNAUTHORIZED` (bad apikey), `NOT_FOUND` (instance missing),
`BAD_REQUEST` (malformed payload). Add retry with backoff for 429/5xx and for
instance reconnect windows.

## Examples

### Example 1: Node.js sender helper

```js
export async function sendText(instance, number, text, baseUrl, apiKey) {
  const res = await fetch(`${baseUrl}/message/sendText/${instance}`, {
    method: "POST",
    headers: { apikey: apiKey, "Content-Type": "application/json" },
    body: JSON.stringify({ number, textMessage: { text } }),
  });
  if (!res.ok) throw new Error(`Evolution send failed: ${res.status}`);
  return res.json();
}
```

### Example 2: Docker Compose (Evolution API)

```yaml
services:
  evolution-api:
    image: atendai/evolution-api:latest
    ports: ["8080:8080"]
    environment:
      AUTHENTICATION_API_KEY: ${EVOLUTION_API_KEY}
      DATABASE_ENABLED: "true"
      DATABASE_PROVIDER: postgresql
      DATABASE_CONNECTION_URI: ${DATABASE_URL}
      CACHE_REDIS_ENABLED: "false"
```

## Notes

- Keep instance secrets (API keys) out of the client; never expose them in `NEXT_PUBLIC_*`.
- A single WhatsApp number = one instance; don't share instances across tenants.
- Validate numbers with `whatsappNumbers` before sending to avoid bans.
- For AI-powered replies, pair this skill with `rag-llm` and `llm-multi-provider`.

## References

- [Evolution API Docs](https://doc.evolution-api.com/)
- [Evolution API on GitHub](https://github.com/EvolutionAPI/evolution-api)
- [WhatsApp Business API docs](https://developers.facebook.com/docs/whatsapp)

