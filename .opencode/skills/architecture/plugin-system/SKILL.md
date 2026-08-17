---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-15
name: plugin-system
description: Design plugin-based architectures with a stable module interface, plugin manager, SDK, and event-driven integration that keeps business logic out of the core
category: architecture
version: 0.1.0
author: devtiagoabreu
tags: [plugins, module-interface, architecture, extensibility, sdk, event-driven, cv]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Python 3.12 and FastAPI
  - Understanding of interfaces, decoupling, and event-driven design
  - A target host (the Vision Platform Core) to integrate with
provides:
  - Plugin interface and lifecycle definition
  - Plugin manager discovery, loading, and execution patterns
  - SDK shape so new modules need no Core changes
  - Event-based result integration with the platform
---

# Plugin System (Vision Platform)

## Overview

The Vision Platform is not an EPI detection system — EPI is only the first
plugin. The Core must never contain module business logic (VP-000 §2). Every
computer vision capability (EPI, Fissura, Tecidos, Estoque, Pessoas) is a
plugin installed on the platform. Plugins implement a stable interface, are
discovered and managed by a Plugin Manager, and communicate results through the
Event Bus. This skill defines that contract.

## Prerequisites

- The platform Core (FastAPI) and its Event Bus available
- Python 3.12+ with an understanding of ABCs and dataclasses
- A plugin package layout (see SDK docs)

## Usage Instructions

### Step 1: Define the plugin interface

Every plugin exposes the same lifecycle so the manager can treat them equally:

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


class ModulePlugin(ABC):
    key: str                       # e.g. "epi"
    version: str                   # e.g. "0.1.0"

    @abstractmethod
    async def initialize(self, config: dict): ...
    @abstractmethod
    async def process(self, input_data: dict) -> dict: ...
    @abstractmethod
    async def shutdown(self): ...
```

`initialize` loads models, `process` receives a frame + context and returns
detections, `shutdown` releases resources.

### Step 2: Plugin manifest

Each plugin ships a manifest describing it (module name, version, models,
inputs/outputs, permissions). The manager validates the manifest before load.

### Step 3: Plugin manager

Discovery and lifecycle:

```python
class PluginManager:
    def __init__(self):
        self._plugins: dict[str, ModulePlugin] = {}

    def register(self, plugin: ModulePlugin):
        self._plugins[plugin.key] = plugin

    async def initialize_all(self, configs: dict):
        for key, plugin in self._plugins.items():
            await plugin.initialize(configs.get(key, {}))

    async def execute(self, key: str, input_data: dict) -> dict:
        plugin = self._plugins[key]
        return await plugin.process(input_data)
```

### Step 4: Keep module logic out of the Core

The Core routes frames and persists results; it never knows about helmets or
fissures. A module result is an opaque JSON payload:

```python
{"module": "epi", "confidence": 0.92, "payload": {"person_id": 7, "ppes": []}}
```

### Step 5: Install new modules without Core changes

A new module = a new package implementing `ModulePlugin` + a manifest. The
manager discovers it, the Core API exposes it under `/api/v1/plugins`, and no
Core rebuild is required. The plugin SDK (VP-012) documents the packaging rules.

### Step 6: Scheduler and concurrency

The manager runs plugins on a scheduler (queues + worker pool). Frames from
many cameras are queued, and parallel workers execute plugin pipelines. Each
execution creates an `Execution` row with a status.

## Examples

### Example 1: EPI plugin skeleton

```python
class EpiPlugin(ModulePlugin):
    key = "epi"
    version = "0.1.0"

    async def initialize(self, config: dict):
        self.detector = load_onnx_model(config["model_path"])

    async def process(self, input_data: dict) -> dict:
        detections = self.detector.predict(input_data["frame"])
        return {"module": "epi", "payload": detections}

    async def shutdown(self):
        pass
```

### Example 2: Registering at startup

```python
manager = PluginManager()
manager.register(EpiPlugin())
await manager.initialize_all(load_plugin_configs())
```

## References

- [Vision Platform VP-003 Plugin System](docs/architecture/003-plugin-system.md)
- [Vision Platform VP-012 Plugin SDK](docs/architecture/012-plugin-sdk.md)
- [Python ABC](https://docs.python.org/3/library/abc.html)
- [Event Bus skill](assets/skills/architecture/event-driven-architecture/SKILL.md)

## Notes

- The Core must stay module-agnostic; no EPI/fissure/tecido logic in Core.
- Plugins never expose their own APIs — results flow through the Core API.
- Version every plugin and validate the manifest before loading.
- Run heavy work on the scheduler, never in request handlers.
- Goal: install a new module without modifying the Core (VP-000).
