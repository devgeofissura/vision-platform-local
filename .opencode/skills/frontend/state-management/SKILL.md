---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: state-management
description: Best practices for state management in frontend applications
category: frontend
version: 0.1.0
author: devtiagoabreu
tags: [state-management, react, redux, frontend]
compatible:
  - opencode
  - claude-code
  - cursor
---

# State Management Best Practices

## Overview

This skill provides best practices for state management in frontend applications, including local state, global state, and server state.

## Prerequisites

- Basic understanding of state management concepts
- React or similar framework knowledge

## Usage Instructions

### Step 1: Local State

Use local state for UI-specific data:

```javascript
function Modal({ isOpen, onClose, children }) {
  const [isVisible, setIsVisible] = useState(isOpen);
  
  useEffect(() => {
    setIsVisible(isOpen);
  }, [isOpen]);
  
  if (!isVisible) return null;
  
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        {children}
        <button onClick={onClose}>Close</button>
      </div>
    </div>
  );
}
```

### Step 2: Global State

Use global state for shared data:

```javascript
// Redux Toolkit slice
const userSlice = createSlice({
  name: 'user',
  initialState: {
    data: null,
    loading: false,
    error: null
  },
  reducers: {
    setUser: (state, action) => {
      state.data = action.payload;
    },
    setLoading: (state, action) => {
      state.loading = action.payload;
    },
    setError: (state, action) => {
      state.error = action.payload;
    }
  }
});

// Async thunk
const fetchUser = createAsyncThunk(
  'user/fetchUser',
  async (userId) => {
    const response = await fetch(`/api/users/${userId}`);
    return await response.json();
  }
);
```

### Step 3: Server State

Use React Query for server state:

```javascript
function UserProfile({ userId }) {
  const { data: user, isLoading, error } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
    staleTime: 5 * 60 * 1000, // 5 minutes
    cacheTime: 30 * 60 * 1000 // 30 minutes
  });
  
  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  
  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
    </div>
  );
}
```

### Step 4: URL State

Use URL for filter and pagination state:

```javascript
function ProductList() {
  const [searchParams, setSearchParams] = useSearchParams();
  
  const page = parseInt(searchParams.get('page') || '1');
  const category = searchParams.get('category');
  const sort = searchParams.get('sort');
  
  const handleFilterChange = (newCategory) => {
    setSearchParams({
      category: newCategory,
      page: '1'
    });
  };
  
  return (
    <div>
      <Filter value={category} onChange={handleFilterChange} />
      <Pagination page={page} />
    </div>
  );
}
```

## Examples

### Zustand Store

```javascript
import create from 'zustand';

const useStore = create((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
  decrement: () => set((state) => ({ count: state.count - 1 })),
  reset: () => set({ count: 0 })
}));

function Counter() {
  const { count, increment, decrement, reset } = useStore();
  
  return (
    <div>
      <button onClick={decrement}>-</button>
      <span>{count}</span>
      <button onClick={increment}>+</button>
      <button onClick={reset}>Reset</button>
    </div>
  );
}
```

## Best Practices

1. Use local state for UI-specific data
2. Use global state for shared data
3. Use React Query for server state
4. Use URL for filter and pagination state
5. Keep state as close to where it's used as possible
6. Normalize complex state

## References

- [React State Management](https://react.dev/learn/managing-state)
- [Redux Toolkit](https://redux-toolkit.js.org/)
- [React Query](https://tanstack.com/query/latest)