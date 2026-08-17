---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: microservices-design
description: Design scalable microservices with bounded contexts, events, and saga orchestration
category: architecture
version: 0.1.0
author: devtiagoabreu
tags: [microservices, bounded-context, ddd, event-driven, saga, distributed-systems]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Distributed systems fundamentals
  - Understanding of REST or message queue basics
  - Familiarity with domain-driven design concepts
provides:
  - Service decomposition guidance via bounded contexts
  - Event-driven and CQRS pattern templates
  - Saga coordination patterns for distributed transactions
  - Contract and versioning strategies for service APIs
---

# Microservices Design

## Overview

Microservices decompose a system into small, independently deployable services that
own their data and communicate over the network. Good designs start from bounded
contexts, which are the natural language and rules boundaries of the business, and
treat each context as the root of one service. Because services no longer share
databases, cross-service business flows must be coordinated with asynchronous events
or saga patterns instead of ACID transactions. The goal is autonomy: each team can
deploy, scale, and evolve its service without coordinated releases.

## Prerequisites

- Experience operating a deployed application
- Basic knowledge of HTTP, JSON, and messaging concepts
- Understanding of eventual consistency and its trade-offs

## Usage Instructions

### Step 1: Decompose by Bounded Contexts

Group responsibilities using Domain-Driven Design boundaries. Two services should
never own the same data and should communicate only through published contracts:

```
+-------------------+     +-------------------+
| Ordering Service  |     | Inventory Service |
| owns orders       |     | owns stock levels |
+--------+----------+     +---------+---------+
         |                          |
         +------- events --------> +
```

Model every noun (order, customer, shipment) in exactly one context, and extract a
shared "definition of done" from the business so ambiguous terms do not leak across
boundaries.

### Step 2: Choose Communication Style

Prefer asynchronous events for integration, and synchronous requests only for queries
that genuinely need an immediate answer:

```yaml
# event contract (Avro) - inventory-availability
{
  "type": "record",
  "name": "StockReserved",
  "fields": [
    { "name": "orderId", "type": "string" },
    { "name": "productId", "type": "string" },
    { "name": "quantity", "type": "int" }
  ]
}
```

Publish events to a broker such as Kafka or RabbitMQ; consumer services subscribe to
topics by their own read model rather than coupling to the producer's schema internals.

### Step 3: Design Sagas for Distributed Transactions

A saga is a sequence of local transactions with compensating actions. Use choreography
(each service reacts to events and emits the next) for simple flows, or orchestration
(a central coordinator instructs each service) for complex flows:

```javascript
// OrderService orchestrator (saga) - abbreviated pseudo-code
async function placeOrder(orderId, items) {
  try {
    await reserveStock(orderId, items);      // step 1
    await chargePayment(orderId, items);     // step 2
    await confirmShipment(orderId, items);   // step 3
  } catch (err) {
    await cancelShipment(orderId, items);    // compensate 3
    await refundPayment(orderId, items);     // compensate 2
    await releaseStock(orderId, items);      // compensate 1
  }
}
```

Every saga state must be persisted so an interrupted saga can be resumed or rolled back
after a crash.

### Step 4: Own Data Per Service

Each service owns its database and exposes no direct schema access to others. If
another service needs data, either expose a narrow API or replicate data through events
into a local read model. This is what makes independent scaling and deployment possible.

### Step 5: Version and Evolve Contracts

Make breaking changes safely by versioning contracts and supporting backward
compatibility during transitions:

```
/v1/orders          # current stable
/v2/orders          # future breaking version
order.events.v1      # Kafka topic namespace
order.events.v2      # old and new topics run in parallel
```

Prefer additive changes (new optional fields, new event types) and run both old and new
versions until all consumers migrate.

## Examples

### Example 1: Event-Driven Inventory Sync

```javascript
// InventoryService consumer - subscribe to order events and update stock
const { Kafka } = require("kafkajs");

const kafka = new Kafka({ clientId: "inventory", brokers: ["kafka:9092"] });
const consumer = kafka.consumer({ groupId: "inventory-service" });

await consumer.subscribe({ topic: "order.events.v1" });
await consumer.run({
  eachMessage: async ({ message }) => {
    const event = JSON.parse(message.value.toString());
    if (event.type === "OrderPlaced") {
      await reserveStock(event.orderId, event.items); // local DB write
    }
  },
});
```

### Example 2: Choreographed Saga

```javascript
// PaymentService publishes when payment succeeds
if (paymentApproved) {
  await producer.send({
    topic: "payment.events.v1",
    messages: [{ value: JSON.stringify({ type: "PaymentApproved", orderId }) }],
  });
}

// ShipmentService listens and continues the flow
if (event.type === "PaymentApproved") {
  await createShipment(event.orderId); // then emits ShipmentCreated
}
```

## References

- [Martin Fowler - Bounded Context](https://martinfowler.com/bliki/BoundedContext.html)
- [Martin Fowler - Saga](https://microservices.io/patterns/data/saga.html)
- [Microservices.io - Patterns](https://microservices.io/)
- [Amazon AWS - Microservices](https://aws.amazon.com/microservices/)
- [Confluent - Event-Driven Microservices](https://www.confluent.io/learn/event-driven-microservices/)

## Notes

- Start with one monolith; split services only when the boundary is clear and the cost
  of a shared deployment hurts.
- Never share a database across services; this silently removes the autonomy you built.
- Sagas must handle out-of-order events and be idempotent on retries.
- Add observability (tracing, logs, metrics) before going to production, since calls
  now cross process boundaries.
- Model eventual consistency explicitly; users must see a consistent view, not an
  instantly consistent one.
