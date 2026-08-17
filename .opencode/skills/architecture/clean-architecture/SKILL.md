---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: clean-architecture
description: Design maintainable applications with Clean and Hexagonal Architecture patterns
category: architecture
version: 0.1.0
author: devtiagoabreu
tags: [clean-architecture, hexagonal, domain-driven, layered, solid]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Object-oriented or functional programming experience
  - Basic understanding of dependency injection
  - Familiarity with at least one backend framework
provides:
  - Layered project structure templates
  - Dependency rule enforcement patterns
  - Use case and domain model design guidance
  - Ports-and-adapters (hexagonal) implementation examples
---

# Clean and Hexagonal Architecture

## Overview

Clean Architecture separates a system into concentric layers so that the business
domain stays independent of frameworks, databases, and UI. The dependency rule states
that source code dependencies must point inward, from the outermost infrastructure
layers toward the innermost domain core. Hexagonal (ports and adapters) Architecture
achieves the same goal by defining explicit ports as application boundaries and
adapters as the concrete integrations (HTTP, database, message queues). The result is
a codebase that is testable in isolation, where frameworks are pluggable and business
logic is expressed in plain, framework-free code.

## Prerequisites

- Experience structuring a non-trivial application in your language of choice
- Working knowledge of dependency injection and interfaces/abstract types
- Basic familiarity with a web framework and an ORM or database driver

## Usage Instructions

### Step 1: Draw the Dependency Circles

Define the four layers from innermost to outermost:

```
entities/            # Enterprise-wide business rules (no dependencies)
  +-- Customer.ts
usecases/            # Application-specific business rules
  +-- CreateOrder.ts
interface-adapters/  # Controllers, presenters, serializers
  +-- rest/
infrastructure/      # Frameworks, DB drivers, HTTP clients
  +-- persistence/
  +-- http/
```

Enforce the dependency rule: inner layers never import outer layers, never know about
HTTP, SQL, or a framework, and never see concrete infrastructure classes.

### Step 2: Model the Domain Core

Keep entities free of annotations, base classes, and framework imports:

```typescript
// entities/Customer.ts - no framework imports allowed
export class Customer {
  private constructor(private readonly id: string, private email: string) {}

  static register(id: string, email: string): Customer {
    if (!email.includes("@")) throw new Error("invalid email");
    return new Customer(id, email);
  }

  changeEmail(newEmail: string): void {
    if (!newEmail.includes("@")) throw new Error("invalid email");
    this.email = newEmail;
  }

  getEmail(): string {
    return this.email;
  }
}
```

### Step 3: Define Ports (Hexagonal Boundaries)

An application port is an interface that the use case needs but that only the outer
world can provide. The use case depends on the port, never on the concrete adapter:

```typescript
// usecases/ports/CustomerRepository.ts
export interface CustomerRepository {
  findById(id: string): Promise<Customer | null>;
  save(customer: Customer): Promise<void>;
}
```

```typescript
// usecases/CreateCustomer.ts
export class CreateCustomer {
  constructor(private readonly customers: CustomerRepository) {}

  async execute(id: string, email: string): Promise<Customer> {
    const customer = Customer.register(id, email);
    await this.customers.save(customer);
    return customer;
  }
}
```

### Step 4: Implement Adapters in Infrastructure

Adapters live in the outer layer and translate between infrastructure and the domain:

```typescript
// infrastructure/persistence/SqlCustomerRepository.ts
import { Customer } from "../../entities/Customer";
import { CustomerRepository } from "../../usecases/ports/CustomerRepository";
import { db } from "./db";

export class SqlCustomerRepository implements CustomerRepository {
  async findById(id: string): Promise<Customer | null> {
    const row = await db.query("SELECT * FROM customers WHERE id = $1", [id]);
    if (!row) return null;
    return Customer.register(row.id, row.email);
  }

  async save(customer: Customer): Promise<void> {
    await db.query(
      "INSERT INTO customers (id, email) VALUES ($1, $2) ON CONFLICT (id) DO UPDATE SET email = $2",
      [customer.getId(), customer.getEmail()]
    );
  }
}
```

### Step 5: Compose at the Composition Root

Wire everything together in one place, typically main or an application entry point.
Infrastructure creates adapters, which are injected into use cases, which are passed
to controllers:

```typescript
// main.ts
const customers: CustomerRepository = new SqlCustomerRepository();
const createCustomer = new CreateCustomer(customers);
const controller = new CustomerController(createCustomer);
```

## Examples

### Example 1: Testing a Use Case with a Fake Adapter

```typescript
class InMemoryCustomerRepository implements CustomerRepository {
  private store = new Map<string, Customer>();

  async findById(id: string): Promise<Customer | null> {
    return this.store.get(id) ?? null;
  }

  async save(customer: Customer): Promise<void> {
    this.store.set(customer.getId(), customer);
  }
}

it("registers a customer without a real database", async () => {
  const useCase = new CreateCustomer(new InMemoryCustomerRepository());
  const customer = await useCase.execute("c1", "ada@example.com");
  expect(customer.getEmail()).toBe("ada@example.com");
});
```

### Example 2: Swapping a Database Adapter

Because the use case only knows the `CustomerRepository` port, migrating from SQL to
MongoDB only requires a new adapter, with zero changes to domain or use cases:

```typescript
// infrastructure/persistence/MongoCustomerRepository.ts
import { CustomerRepository } from "../../usecases/ports/CustomerRepository";

export class MongoCustomerRepository implements CustomerRepository {
  async findById(id: string): Promise<Customer | null> {
    const doc = await mongo.collection("customers").findOne({ _id: id });
    return doc ? Customer.register(doc._id, doc.email) : null;
  }

  async save(customer: Customer): Promise<void> {
    await mongo
      .collection("customers")
      .updateOne({ _id: customer.getId() }, { $set: { email: customer.getEmail() } }, { upsert: true });
  }
}
```

## References

- [The Clean Architecture - Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Alistair Cockburn - Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/)
- [Microsoft Architecture Guide - Clean Architecture](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures)
- [Architecture Patterns with Python (Cosmic Python)](https://www.cosmicpython.com/book/preface.html)

## Notes

- Keep the domain layer free of any dependency; if you need a framework in an entity,
  the layering is wrong.
- Make ports match domain language, not infrastructure language (e.g. `save`,
  not `persistToPostgres`).
- Start with the use cases; they reveal which ports the application really needs.
- Do not over-engineer small CRUD apps; adopt layers when business rules or framework
  lock-in are a real concern.
- Run tests that exercise use cases with fake adapters so the domain is verified
  without network or database access.
