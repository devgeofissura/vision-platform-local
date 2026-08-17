---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-15
name: event-driven-architecture
description: Design event-driven systems with an internal Event Bus, async queues, publishers/subscribers, and persistent event records
category: architecture
version: 0.1.0
author: devtiagoabreu
tags: [event-driven, event-bus, pubsub, messaging, decoupling, architecture, python]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Python 3.12 and asyncio
  - Understanding of decoupling and asynchronous systems
  - A target service (the Vision Platform Core) to integrate with
provides:
  - Event Bus design and message schema
  - Publisher/subscriber patterns with async queues
  - Event persistence and replay guidance
  - Integration with plugin results and storage
---

# Event-Driven Architecture (Event Bus)

## Overview

The Vision Platform prefers **event-driven** communication between services
(VP-000 §10). The Event Bus is the backbone: cameras produce frames, plugins
produce detections, the storage service persists evidence, and the Dashboard
consumes results — without direct coupling between any of them. An event has a
stable schema, a typed name, and a payload. Events can be persisted for audit
and replay.

## Prerequisites

- Python 3.12+ and `asyncio`
- Basic pub/sub knowledge
- The Vision Platform Core services (API, AI Engine, Storage) running

## Usage Instructions

### Step 1: Define the event schema

Every event carries a name, timestamp, tenant, and payload:

```python
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class Event:
    name: str
    tenant_id: str
    payload: dict
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    event_id: str | None = None
```

### Step 2: Build a simple in-process bus

For a single-server deployment, an async pub/sub bus is enough:

```python
import asyncio


class EventBus:
    def __init__(self):
        self._subs: dict[str, list] = {}

    def subscribe(self, name: str, handler):
        self._subs.setdefault(name, []).append(handler)

    async def publish(self, event: Event):
        for handler in self._subs.get(event.name, []):
            asyncio.create_task(handler(event))
```

### Step 3: Wire the pipeline

`Camera → Frame → Preprocess → Queue → Scheduler → Plugin → Event → Storage → Dashboard`:

```python
async def on_detection(event: Event):
    await storage.save_evidence(event.payload)   # JPEG + JSON
    await notify_dashboard(event)


bus = EventBus()
bus.subscribe("detection.created", on_detection)
```

### Step 4: Persist events for audit and replay

Store events in an `events` table (tenant-scoped) so the history endpoint and
audit trail work. Replaying means re-publishing stored events to subscribers.

### Step 5: Keep producers and consumers decoupled

A plugin publishes `detection.created`; it does not know about the Dashboard or
Storage. The Dashboard subscribes; Storage subscribes. Adding a consumer never
touches the producer.

### Step 6: Ordering and delivery guarantees

- A single in-process queue gives FIFO per publisher.
- For retries, use a small dead-letter queue per subscriber.
- Events reference an `Execution` id to group a batch (one detection run).

## Examples

### Example 1: Camera event flow

```python
await bus.publish(Event(
    name="camera.frame",
    tenant_id=tenant_id,
    payload={"camera_id": "cam-1", "frame": jpeg_bytes, "ts": now},
))
```

### Example 2: Plugin result consumed by storage

```python
bus.subscribe("detection.created", lambda e: persist_detection(e))
```

## References

- [Vision Platform VP-006 Event Bus](docs/architecture/006-event-bus.md)
- [asyncio documentation](https://docs.python.org/3/library/asyncio.html)
- [Plugin System skill](assets/skills/architecture/plugin-system/SKILL.md)

## Notes

- Event-driven is the preferred communication mode (VP-000); RPC only where it
  fits (auth, management).
- Events are tenant-scoped and persisted for audit.
- Keep payloads small (JPEG + JSON) to save bandwidth across the fleet.
- Use dead-letter queues for retries instead of blocking producers.
- Modules integrate through events — never direct Core-module calls.
