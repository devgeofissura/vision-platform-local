---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: e2e-testing
description: Best practices for end-to-end testing and browser automation
category: testing
version: 0.1.0
author: devtiagoabreu
tags: [e2e-testing, browser-automation, cypress, testing]
compatible:
  - opencode
  - claude-code
  - cursor
---

# End-to-End Testing Best Practices

## Overview

This skill provides best practices for end-to-end testing and browser automation, including test strategy, page objects, and CI/CD integration.

## Prerequisites

- Basic understanding of E2E testing
- Browser automation tool knowledge (Cypress, Playwright, etc.)

## Usage Instructions

### Step 1: Test Strategy

Focus on critical user journeys:

```javascript
describe('User Authentication', () => {
  it('should allow user to login', () => {
    cy.visit('/login');
    cy.get('[data-testid="email"]').type('user@example.com');
    cy.get('[data-testid="password"]').type('password123');
    cy.get('[data-testid="submit"]').click();
    cy.url().should('include', '/dashboard');
  });
});
```

### Step 2: Page Objects

Use Page Object pattern:

```javascript
class LoginPage {
  constructor() {
    this.emailInput = '[data-testid="email"]';
    this.passwordInput = '[data-testid="password"]';
    this.submitButton = '[data-testid="submit"]';
  }
  
  visit() {
    cy.visit('/login');
    return this;
  }
  
  login(email, password) {
    cy.get(this.emailInput).type(email);
    cy.get(this.passwordInput).type(password);
    cy.get(this.submitButton).click();
    return new DashboardPage();
  }
}

// Usage
const loginPage = new LoginPage();
const dashboard = loginPage.visit().login('user@example.com', 'password123');
```

### Step 3: Test Data

Manage test data properly:

```javascript
beforeEach(() => {
  // Seed database
  cy.task('seedDatabase');
  
  // Create test user
  cy.task('createUser', {
    email: 'test@example.com',
    password: 'password123'
  });
});

afterEach(() => {
  // Clean up
  cy.task('cleanDatabase');
});
```

### Step 4: CI/CD Integration

Run tests in CI/CD:

```yaml
# GitHub Actions
name: E2E Tests
on: [push, pull_request]
jobs:
  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install dependencies
        run: npm ci
      - name: Run E2E tests
        run: npm run test:e2e
```

## Examples

### Cypress Test Suite

```javascript
describe('Shopping Cart', () => {
  beforeEach(() => {
    cy.visit('/products');
  });
  
  it('should add item to cart', () => {
    cy.get('[data-testid="product-1"]').click();
    cy.get('[data-testid="add-to-cart"]').click();
    cy.get('[data-testid="cart-count"]').should('contain', '1');
  });
  
  it('should update quantity', () => {
    cy.get('[data-testid="product-1"]').click();
    cy.get('[data-testid="add-to-cart"]').click();
    cy.get('[data-testid="cart"]').click();
    cy.get('[data-testid="quantity"]').clear().type('3');
    cy.get('[data-testid="update"]').click();
    cy.get('[data-testid="total"]').should('contain', '$30');
  });
  
  it('should remove item from cart', () => {
    cy.get('[data-testid="product-1"]').click();
    cy.get('[data-testid="add-to-cart"]').click();
    cy.get('[data-testid="cart"]').click();
    cy.get('[data-testid="remove"]').click();
    cy.get('[data-testid="cart-count"]').should('contain', '0');
  });
});
```

## Best Practices

1. Focus on critical user journeys
2. Use Page Object pattern
3. Manage test data properly
4. Integrate with CI/CD
5. Use data-testid attributes
6. Handle async operations properly

## References

- [Cypress Documentation](https://docs.cypress.io/)
- [Playwright Documentation](https://playwright.dev/)