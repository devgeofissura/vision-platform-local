---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: react-patterns
description: Best practices for React component patterns and architecture
category: frontend
version: 0.1.0
author: devtiagoabreu
tags: [react, javascript, frontend, patterns]
compatible:
  - opencode
  - claude-code
  - cursor
---

# React Patterns Best Practices

## Overview

This skill provides best practices for React component patterns and architecture, including hooks, state management, and performance optimization.

## Prerequisites

- Basic understanding of React
- JavaScript knowledge

## Usage Instructions

### Step 1: Component Organization

Organize components by feature:

```
src/
├── features/
│   ├── auth/
│   │   ├── components/
│   │   │   ├── LoginForm.jsx
│   │   │   └── RegisterForm.jsx
│   │   ├── hooks/
│   │   │   └── useAuth.js
│   │   └── index.js
│   └── products/
│       ├── components/
│       ├── hooks/
│       └── index.js
└── shared/
    ├── components/
    └── hooks/
```

### Step 2: Custom Hooks

Extract logic into custom hooks:

```javascript
function useAuth() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    checkAuth().then(user => {
      setUser(user);
      setLoading(false);
    });
  }, []);
  
  const login = async (credentials) => {
    const user = await loginApi(credentials);
    setUser(user);
  };
  
  const logout = async () => {
    await logoutApi();
    setUser(null);
  };
  
  return { user, loading, login, logout };
}
```

### Step 3: Performance Optimization

Optimize re-renders:

```javascript
// Use React.memo for pure components
const PureChild = React.memo(({ data }) => {
  return <div>{data.name}</div>;
});

// Use useMemo for expensive calculations
const sortedData = useMemo(() => {
  return data.sort((a, b) => a.name.localeCompare(b.name));
}, [data]);

// Use useCallback for stable references
const handleClick = useCallback(() => {
  console.log('clicked');
}, []);
```

### Step 4: Error Boundaries

Implement error boundaries:

```javascript
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }
  
  static getDerivedStateFromError(error) {
    return { hasError: true };
  }
  
  componentDidCatch(error, errorInfo) {
    logErrorToService(error, errorInfo);
  }
  
  render() {
    if (this.state.hasError) {
      return <h1>Something went wrong.</h1>;
    }
    
    return this.props.children;
  }
}
```

## Examples

### Custom Hook

```javascript
function useLocalStorage(key, initialValue) {
  const [storedValue, setStoredValue] = useState(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      return initialValue;
    }
  });
  
  const setValue = value => {
    try {
      setStoredValue(value);
      window.localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      console.error(error);
    }
  };
  
  return [storedValue, setValue];
}
```

## Best Practices

1. Organize components by feature
2. Extract logic into custom hooks
3. Optimize re-renders
4. Implement error boundaries
5. Use TypeScript for type safety
6. Write unit tests

## References

- [React Documentation](https://react.dev/)
- [React Patterns](https://reactpatterns.com/)