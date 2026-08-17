---
name: react-project-setup
description: Complete recipe for setting up a modern React project
version: 0.1.0
author: devtiagoabreu
tags: [react, javascript, frontend, project-setup]
category: project-setup
ingredients:
  - type: skill
    name: react-patterns
    version: 0.1.0
  - type: skill
    name: css-best-practices
    version: 0.1.0
  - type: skill
    name: testing
    version: 0.1.0
steps:
  - description: Initialize React project with Vite
    commands:
      - npm create vite@latest my-react-app -- --template react-ts
      - cd my-react-app
      - npm install
  - description: Install development dependencies
    commands:
      - npm install -D eslint prettier @typescript-eslint/eslint-plugin
      - npm install -D @testing-library/react @testing-library/jest-dom
  - description: Configure ESLint and Prettier
    commands:
      - npx eslint --init
  - description: Set up project structure
    commands:
      - mkdir -p src/components src/hooks src/utils src/types
  - description: Create basic components
    commands: []
  - description: Write tests
    commands: []
outcome: A fully configured React project with TypeScript, testing, and linting
difficulty: intermediate
---

# React Project Setup Recipe

## Overview

This recipe guides you through setting up a modern React project with TypeScript, testing, and best practices.

## Prerequisites

- Node.js 18+ installed
- npm or yarn installed
- Code editor (VS Code recommended)

## Ingredients

- **react-patterns**: React best practices and patterns
- **css-best-practices**: CSS architecture and styling
- **testing**: Unit and integration testing

## Steps

### Step 1: Initialize React Project

```bash
npm create vite@latest my-react-app -- --template react-ts
cd my-react-app
npm install
```

### Step 2: Install Development Dependencies

```bash
npm install -D eslint prettier @typescript-eslint/eslint-plugin
npm install -D @testing-library/react @testing-library/jest-dom
```

### Step 3: Configure ESLint and Prettier

```bash
npx eslint --init
```

### Step 4: Set Up Project Structure

```bash
mkdir -p src/components src/hooks src/utils src/types
```

### Step 5: Create Basic Components

Create your first component:

```typescript
// src/components/Hello.tsx
import React from 'react';

interface HelloProps {
  name: string;
}

export const Hello: React.FC<HelloProps> = ({ name }) => {
  return <h1>Hello, {name}!</h1>;
};
```

### Step 6: Write Tests

```typescript
// src/components/Hello.test.tsx
import { render, screen } from '@testing-library/react';
import { Hello } from './Hello';

test('renders hello message', () => {
  render(<Hello name="World" />);
  expect(screen.getByText('Hello, World!')).toBeInTheDocument();
});
```

## Expected Outcome

- Modern React project with TypeScript
- Configured linting and formatting
- Basic testing setup
- Clean project structure

## References

- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [Testing Library](https://testing-library.com/)