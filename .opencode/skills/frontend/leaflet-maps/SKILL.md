---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-15
name: leaflet-maps
description: Render interactive maps with Leaflet + React Leaflet and OpenStreetMap — markers, polylines, custom icons, tile handling, and map state synced to app state
category: frontend
version: 0.1.0
author: devtiagoabreu
tags: [leaflet, react-leaflet, openstreetmap, maps, markers, polyline, gis]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - React and a bundler (Next.js/Vite)
  - A tile source (OpenStreetMap is free; heavy usage should use a provider)
provides:
  - Map setup with React Leaflet + OSM tiles
  - Marker/polyline rendering with custom icons
  - Map as a view over application state (not a source of truth)
  - Zoom/fit-bounds and drag-marker interactions
  - Next.js SSR-safe mounting and performance tips
---

# Leaflet Maps

## Overview

Leaflet is a lightweight open-source map library; React Leaflet wraps it with
React components. Combined with OpenStreetMap tiles it gives you free,
dependency-light maps for web apps. The key architectural rule: **the map is a
view, not the source of truth**. All map data (selected customers, optimized
stops, polyline) lives in application state; the map renders that state and
emits user gestures (drag marker, click) back into it. This makes the map easy
to test and keeps it in sync with the rest of the UI.

## Prerequisites

- `npm i leaflet react-leaflet`
- Import Leaflet CSS: `import "leaflet/dist/leaflet.css"`
- In Next.js, load map components dynamically (SSR-safe), see below.

## Usage Instructions

### Step 1: Mount the map SSR-safe (Next.js)

Leaflet accesses `window` at import time, so it must not render on the server:

```tsx
"use client";
import dynamic from "next/dynamic";

const MapView = dynamic(() => import("@/components/maps/RouteMap").then((m) => m.RouteMap), {
  ssr: false,
  loading: () => <div className="h-[400px] bg-muted" />,
});

export function RouteMapPage() {
  return <MapView center={[-15.78, -47.93]} zoom={5} />;
}
```

### Step 2: Render map container with markers and polyline

```tsx
import { MapContainer, TileLayer, Marker, Popup, Polyline } from "react-leaflet";

export function RouteMap({ stops, path }: { stops: Stop[]; path: [number, number][] }) {
  return (
    <MapContainer center={stops[0]?.coords ?? [-15.78, -47.93]} zoom={13} className="h-full w-full">
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        url="https://tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {stops.map((s, i) => (
        <Marker key={s.id} position={s.coords}>
          <Popup>
            <b>{i + 1}. {s.name}</b>
          </Popup>
        </Marker>
      ))}
      {path.length > 1 && <Polyline positions={path} pathOptions={{ color: "#2563eb", weight: 4 }} />}
    </MapContainer>
  );
}
```

### Step 3: Fix default marker icon (known pitfall)

Default Leaflet marker icons break under bundlers. Provide your own:

```tsx
import L from "leaflet";
const pin = L.icon({
  iconUrl: "/icons/pin.svg",
  iconSize: [32, 42],
  iconAnchor: [16, 42],
  popupAnchor: [0, -42],
});
<Marker position={coords} icon={pin} />
```

For reorderable stops use numbered badges (`divIcon`) so users can see the
optimized sequence.

### Step 4: Sync map with state and fit bounds

```tsx
import { useMap } from "react-leaflet";
import { useEffect } from "react";

function FitBounds({ stops }: { stops: Stop[] }) {
  const map = useMap();
  useEffect(() => {
    if (!stops.length) return;
    map.fitBounds(stops.map((s) => s.coords), { padding: [40, 40] });
  }, [stops, map]);
  return null;
}
```

When the route is optimized, the polyline updates because the map re-renders
from state — no manual imperative updates needed.

### Step 5: Draggable markers (geocoding fallback)

```tsx
<Marker position={coords} draggable
  eventHandlers={{ dragend: (e) => onMove(e.target.getLatLng()) }}
/>
```

Users can drag a marker to correct a bad geocode; the new coordinates are
persisted via the app API.

## Examples

### Optimized route with ordered markers and polyline

```tsx
export function OptimizedRouteMap({ stops, path }: Props) {
  return (
    <MapContainer center={stops[0].coords} zoom={14} className="h-[500px] w-full rounded-lg border">
      <TileLayer url="https://tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; OpenStreetMap contributors' />
      {stops.map((s, i) => (
        <Marker key={s.id} position={s.coords} icon={numberedIcon(i + 1)}>
          <Popup>
            {i + 1}. {s.name} — {s.distanceLabel} · {s.etaLabel}
          </Popup>
        </Marker>
      ))}
      <Polyline positions={path} pathOptions={{ color: "#16a34a", weight: 4, dashArray: "8 6" }} />
      <FitBounds stops={stops} />
    </MapContainer>
  );
}
```

## Best Practices

- Keep `center`/`zoom` in state or a ref; never re-create the map on every
  render (memoize children).
- Load maps only on client (SSR-safe) to avoid hydration errors.
- Don't put heavy components inside the map container; keep popups light.
- Use a tile provider with attribution when traffic grows; OSM tile policy
  discourages heavy production use without a cache/provider.
- Store coordinates as `[lat, lng]` consistently (Leaflet order) and convert
  once at the API boundary.

## References

- Leaflet: <https://leafletjs.com>
- React Leaflet: <https://react-leaflet.js.org>
- OpenStreetMap tile usage policy: <https://operations.osmfoundation.org/policies/tiles/>
- RouteOS SaaS spec — Documento 13 (Arquitetura de Roteirização)
