---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-15
name: fastapi-development
description: Build async Python REST backends with FastAPI, Pydantic schemas, dependency injection, router layering, and OpenAPI-first design
category: backend
version: 0.1.0
author: devtiagoabreu
tags: [fastapi, python, rest-api, pydantic, asyncio, openapi, backend]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Python 3.12 or newer
  - FastAPI and Uvicorn installed (`pip install fastapi uvicorn pydantic`)
  - Basic knowledge of asyncio and REST APIs
provides:
  - App factory and router layering patterns
  - Pydantic schemas for request/response contracts
  - Dependency injection for auth, DB sessions, and tenant context
  - OpenAPI-first design with versioned `/api/v1/` routes
---

# FastAPI Development

## Overview

FastAPI is the standard backend framework for the Vision Platform (CVaaS): a
multi-tenant, plugin-based computer vision SaaS. This skill covers building
async Python REST backends that are OpenAPI-first, type-safe, and easily
testable. FastAPI generates OpenAPI 3.1 documentation automatically from
Pydantic schemas, so the schema *is* the contract. The Core API is the single
entry point for all clients — modules never expose their own routes, so this
skill applies to the platform Core, not to plugins.

## Prerequisites

- Python 3.12+ and `pip`
- `fastapi`, `uvicorn[standard]`, `pydantic` installed
- Familiarity with REST conventions (paths, verbs, status codes, pagination)

## Usage Instructions

### Step 1: App factory and layering

Structure the application as a factory so tests and multiple deployments
(dev/staging/prod) share one code path:

```python
# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.v1.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup: open DB pools, start scheduler, discover plugins
    yield
    # shutdown: close pools, flush queues, persist state


def create_app() -> FastAPI:
    app = FastAPI(title="Vision Platform API", version="1.0.0", lifespan=lifespan)
    app.include_router(api_router, prefix="/api/v1")
    return app
```

### Step 2: Router layering

Keep routers thin. A router only maps paths to handlers; business logic lives
in services:

```
app/
  main.py          # create_app()
  api/
    v1/
      router.py    # aggregates sub-routers
      auth.py, cameras.py, executions.py, events.py, evidences.py
  core/
    config.py, db.py, security.py, tenant.py, eventbus.py
  services/        # business logic
  schemas/         # Pydantic request/response models
  models/          # SQLAlchemy models
```

### Step 3: Pydantic schemas are the contract

Define a schema per request and response. Use `model_config = ConfigDict(from_attributes=True)` to serialize ORM objects:

```python
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class ExecutionCreate(BaseModel):
    plugin_id: str
    camera_id: str
    params: dict = Field(default_factory=dict)


class ExecutionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    status: str
    started_at: datetime
    finished_at: datetime | None
```

Never return raw ORM objects from routes; always go through response schemas.

### Step 4: Dependency injection

Use `Depends` for authentication, DB sessions, and tenant context so every
route is explicit about what it needs:

```python
from fastapi import Depends, HTTPException, status
from app.core.tenant import get_tenant_context


async def require_tenant(ctx: TenantContext = Depends(get_tenant_context)):
    if not ctx.tenant_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Tenant required")
    return ctx


@app.get("/api/v1/cameras")
async def list_cameras(
    tenant: TenantContext = Depends(require_tenant),
    session: AsyncSession = Depends(get_db_session),
):
    ...
```

### Step 5: Uniform response envelope

Return a consistent envelope so clients parse one shape everywhere:

```python
class ApiResponse(BaseModel):
    success: bool
    data: dict | list | None = None
    message: str | None = None
    errors: list[dict] | None = None
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
```

### Step 6: Async-first route handlers

Prefer `async def` routes and async SQLAlchemy sessions. Never call blocking
OpenCV or ONNX work inside a route — dispatch heavy work to the AI Engine
(plugin scheduler) and return `202 Accepted` with the execution id:

```python
@app.post("/api/v1/executions", status_code=202)
async def start_execution(payload: ExecutionCreate, tenant: TenantContext = Depends(require_tenant)):
    execution = await service.start(tenant.tenant_id, payload)  # enqueues, returns id
    return ApiResponse(success=True, data={"id": execution.id, "status": "queued"})
```

### Step 7: Exception handling and validation errors

Register global handlers that translate domain exceptions into the envelope
format, and keep FastAPI's automatic 422 for Pydantic validation failures.

## Examples

### Example 1: Minimal versioned app

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/api/v1/health")
async def health():
    return {"status": "ok"}
```

### Example 2: Authenticated, paginated listing

```python
from fastapi import Depends, Query


@app.get("/api/v1/events")
async def list_events(
    tenant: TenantContext = Depends(require_tenant),
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=200),
    session: AsyncSession = Depends(get_db_session),
):
    rows, total = await event_service.list(tenant.tenant_id, page=page, size=size)
    return ApiResponse(success=True, data={
        "items": rows,
        "page": page,
        "size": size,
        "total": total,
    })
```

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [FastAPI Dependency Injection](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [Pydantic v2](https://docs.pydantic.dev/latest/)
- [SQLAlchemy 2.0 + asyncio](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [OpenAPI 3.1](https://spec.openapis.org/oas/v3.1.0.html)

## Notes

- Keep routers thin: routing in `api/`, logic in `services/`, data in `models/`.
- Version the API from day one (`/api/v1/`); breaking changes become `/api/v2/`.
- Modules/plugins never add their own routes — everything goes through the Core API.
- Heavy CV work belongs in the AI Engine queue, not in route handlers.
- Use response models to guarantee the OpenAPI contract stays truthful.
