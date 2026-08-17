---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-15
name: route-optimization
description: Plan, geocode and optimize field routes with OpenRouteService/OSRM — provider abstraction, single-vehicle routing, distance/time calculation, and route persistence
category: logistics
version: 0.1.0
author: devtiagoabreu
tags: [routing, optimization, geocoding, openrouteservice, osrm, vrp, logistics, maps]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - A routing provider API key (OpenRouteService free tier)
  - Backend knowledge (this skill keeps API keys server-side)
  - OpenStreetMap/Leaflet for display
provides:
  - Provider-agnostic routing abstraction (geocode, calculateRoute, optimizeRoute)
  - Geocoding strategy and coordinate caching
  - Single-vehicle routing (SVRP) with origin = destination
  - Distance/time units and persistence of optimized stops
  - Error handling for external services and rate limits
---

# Route Optimization

## Overview

Route optimization turns a set of customer addresses into an efficient driving
sequence. For an MVP the correct approach is to delegate to a routing provider
instead of writing a VRP solver: **OpenRouteService** (or OSRM) exposes
geocoding, route calculation and optimization APIs. The frontend must never
call the provider directly — all calls go through the application backend,
which protects the API key, enforces tenant isolation, adds caching, logs
usage, and makes it trivial to swap providers (Google/Here/Mapbox/OSRM) later.

## Prerequisites

- An OpenRouteService API key (or OSRM self-hosted), set as `ORS_API_KEY`
- A backend layer (Next.js Route Handlers / Express) with tenant context
- A map component (Leaflet) to render markers and the optimized path

## Usage Instructions

### Step 1: Define the provider abstraction

```ts
export interface RoutingProvider {
  geocode(input: GeocodeInput): Promise<GeocodeResult>;
  calculateRoute(input: RouteCalculationInput): Promise<RouteCalculationResult>;
  optimizeRoute(input: RouteOptimizationInput): Promise<RouteOptimizationResult>;
}

export class OpenRouteServiceProvider implements RoutingProvider { ... }
```

Flow: `Frontend → App API → Routing Service → Routing Provider → OpenRouteService`.
Never leak `ORS_API_KEY` to the browser.

### Step 2: Geocode addresses on save

When a customer is created, geocode once and store lat/lng on the `Address`:

```ts
async function geocodeAddress(address: Address, provider: RoutingProvider) {
  if (address.latitude != null && address.longitude != null) return; // skip
  const { latitude, longitude } = await provider.geocode({ query: address.text });
  return { latitude, longitude };
}
```

- Do not geocode the same address repeatedly — cache coordinates.
- Allow manual marker drag as a fallback when geocoding fails.
- Map geocoding failures to a domain error (`CUSTOMER_INVALID_ADDRESS`).

### Step 3: Optimize a route (single vehicle)

MVP solves the Single Vehicle Routing Problem via the provider's optimization
API. Origin equals destination (the base):

```ts
const result = await provider.optimizeRoute({
  start: baseCoords,
  end: baseCoords,
  stops: selectedCustomers.map((c) => ({ id: c.id, location: c.address.coords })),
});
// result.stops: ordered [{ id, position, distanceFromStart, eta }]
```

Persist each stop as a snapshot (`RouteStop`) with lat/lng so historical routes
stay valid even if the customer's address changes later.

### Step 4: Allow manual reordering and recalc

Users must be able to reorder stops by drag-and-drop. After reordering:

1. Update the `RouteStop.position` sequence.
2. Re-request `calculateRoute` for the new order (keeps distance/time accurate).
3. Update the map polyline and the `RouteSummary` totals.

The planning screen keeps a single source of truth
(`RoutePlanningState`) that both the map and the stop list read from.

### Step 5: Store units consistently

- Distances in **meters** (Int), durations in **seconds** (Int).
- Keep the provider raw payload out of the domain; map to your own types.
- Store the provider + route version so re-runs with a new provider stay
  consistent.

### Step 6: Handle provider errors and limits

```ts
class ExternalServiceError extends Error { ... }

try {
  return await provider.optimizeRoute(...);
} catch (err) {
  // timeout (ROUTING_TIMEOUT_MS=15000), rate limit, quota exceeded
  throw new ExternalServiceError("routing provider unavailable", { cause: err });
}
```

- Never surface provider stack traces or keys to the client.
- Add a request timeout and a fallback message ("optimization failed, try again").
- Log provider calls with tenant + requestId for cost monitoring.

## Examples

### OpenRouteService optimization call (server side)

```ts
// services/routing.ts
const res = await fetch(`${ORS_BASE_URL}/v2/optimization`, {
  method: "POST",
  headers: {
    Authorization: process.env.ORS_API_KEY!,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    jobs: stops.map((s, i) => ({
      id: i,
      location: [s.location.longitude, s.location.latitude],
    })),
    vehicles: [{ start: [start.lng, start.lat], end: [end.lng, end.lat] }],
  }),
  signal: AbortSignal.timeout(15_000),
});
```

### Route stop snapshot (Prisma)

```prisma
model RouteStop {
  id        String  @id @default(cuid())
  routeId   String
  tenantId  String
  position  Int
  customerId String?
  latitude  Float
  longitude Float
  distanceMeters Int?
  etaSeconds Int?
  @@unique([routeId, position])
}
```

## Best Practices

- Keep the provider behind an interface; write provider tests with mocked HTTP.
- Validate inputs (coordinates bounds, tenant) before calling external APIs.
- Cache geocoding results; store snapshots for historical integrity.
- Enforce plan limits on routes/month in the backend before optimizing.

## References

- OpenRouteService API: <https://openrouteservice.org/dev/#/api-docs>
- OSRM: <https://project-osrm.org>
- RouteOS SaaS spec — Documento 13 (Arquitetura de Roteirização)
