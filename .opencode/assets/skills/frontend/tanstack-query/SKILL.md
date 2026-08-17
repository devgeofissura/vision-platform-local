---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-15
name: tanstack-query
description: Manage server state in React with TanStack Query — queries, mutations, cache invalidation, optimistic updates, and infinite lists for data-heavy SaaS screens
category: frontend
version: 0.1.0
author: devtiagoabreu
tags: [tanstack-query, react-query, server-state, cache, mutations, optimistic-update]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - React 18+ and a fetch/http client (fetch, axios)
  - A REST API to consume
provides:
  - QueryClient setup and provider wiring
  - useQuery/useMutation patterns with typing
  - Cache key design and invalidation strategies
  - Optimistic updates and error rollback
  - Pagination and refetch policies
---

# TanStack Query

## Overview

TanStack Query (formerly React Query) manages **server state** in React: data
fetched from an API is cached, deduplicated, retried, and revalidated
automatically. UI state (modals, form inputs, toggles) stays in React state;
server state lives in the query cache keyed by stable query keys. The library
dramatically reduces boilerplate for loading/error states and keeps screens in
sync after mutations by invalidating queries. It is the recommended server-state
layer for SaaS dashboards (alongside Zustand/Context for UI state).

## Prerequisites

- `npm i @tanstack/react-query`
- A root `QueryClientProvider` wrapping the app
- An API that returns predictable shapes (e.g. `{ success, data, meta }`)

## Usage Instructions

### Step 1: Set up the client

```tsx
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const queryClient = new QueryClient({
  defaultOptions: { queries: { staleTime: 60_000, retry: 1, refetchOnWindowFocus: false } },
});

export function Providers({ children }: { children: React.ReactNode }) {
  return <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>;
}
```

### Step 2: Fetch with useQuery

Design query keys from (entity, filters, page) — the key IS the cache identity:

```tsx
export function useCustomers(params: CustomerParams) {
  return useQuery({
    queryKey: ["customers", params],
    queryFn: () => api.get<CustomerPage>("/api/v1/customers", { params }),
    select: (res) => res.data,
  });
}

// usage
const { data, isLoading, isError, error } = useCustomers({ page, pageSize, search });
```

Load `loading.tsx`/`Skeleton` while `isLoading`, show empty states, and
translate `error` into a user-facing message.

### Step 3: Mutate with useMutation and invalidate

```tsx
const queryClient = useQueryClient();

const createCustomer = useMutation({
  mutationFn: (input: CustomerInput) => api.post("/api/v1/customers", input),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ["customers"] });
    toast.success("Cliente criado");
  },
  onError: (err) => toast.error(message(err)),
});
```

- Invalidate the broadest key affected by the mutation.
- Handle `onError` — never let a failed request leave the UI stale silently.

### Step 4: Optimistic updates (reorder stops, toggles)

For drag-and-drop route reordering, update the cache before the server round-trip:

```tsx
const reorder = useMutation({
  mutationFn: (order: string[]) => api.patch("/api/v1/routes/reorder", { order }),
  onMutate: async (order) => {
    await queryClient.cancelQueries({ queryKey: ["route", routeId] });
    const prev = queryClient.getQueryData(["route", routeId]);
    queryClient.setQueryData(["route", routeId], (old: Route) => ({ ...old, stopOrder: order }));
    return { prev }; // context for rollback
  },
  onError: (_e, _v, ctx) => queryClient.setQueryData(["route", routeId], ctx?.prev),
  onSettled: () => queryClient.invalidateQueries({ queryKey: ["route", routeId] }),
});
```

### Step 5: Pagination and search

Use `useQuery` keys that include the page/filter params; keep filters debounced:

```tsx
const [params, setParams] = useState({ page: 1, pageSize: 20, search: "" });
const { data } = useCustomers(params);
// DataTable reads data.items + data.meta.totalPages
```

For infinite scroll use `useInfiniteQuery` with `getNextPageParam` reading
`meta.nextPage`.

### Step 6: Route optimization flow (map + list sync)

The planning screen holds a single source of truth (`RoutePlanningState`) and
the optimization is a mutation:

```tsx
const optimize = useMutation({
  mutationFn: (payload: OptimizeInput) => api.post("/api/v1/routes/optimize", payload),
  onSuccess: (res) => setPlanningState((s) => ({ ...s, optimizedStops: res.data.stops })),
});
```

After success the map and stop list re-render from the same state; `isLoading`
shows the "otimizando rota…" indicator.

## Best Practices

- Treat query keys as a contract; name them `[entity, filter, page]`.
- Prefer `staleTime` over aggressive refetching for slow-changing lists.
- Keep mutations server-authoritative; use optimistic updates only where UX
  demands it and always roll back on error.
- Put `onError` handling in one place (toast helper) to avoid repetition.
- Never cache tenant-crossing data under a shared key — scope keys with
  `tenantId` when relevant.

## References

- TanStack Query docs: <https://tanstack.com/query/latest>
- RouteOS SaaS spec — Documento 08 (Arquitetura Frontend)
