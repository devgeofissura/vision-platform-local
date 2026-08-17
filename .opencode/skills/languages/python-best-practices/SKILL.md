---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: python-best-practices
description: Python best practices covering typing, packaging, virtual environments, and code style
category: languages
version: 0.1.0
author: devtiagoabreu
tags: [python, typing, packaging, venv, pep8, style]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Python 3.9 or newer
  - pip and venv available
  - Basic familiarity with Python syntax
provides:
  - Guidelines for static typing with PEP 484 annotations
  - Workflow for virtual environments and dependency pinning
  - Project packaging setup with pyproject.toml
  - Code style and linting conventions (PEP 8, ruff, black)
---

# Python Best Practices

## Overview

This skill provides a practical guide to writing clean, maintainable, and
well-packaged Python code. It covers static typing with type annotations,
isolated dependency management with virtual environments, modern packaging
through `pyproject.toml`, and consistent code style following PEP 8. Following
these practices makes code easier to read, safer to refactor, and simpler to
ship as a reusable library. The guidance applies to libraries, CLI tools, and
application code alike.

## Prerequisites

- Python 3.9+ installed and available on `PATH`
- `python3 -m pip --version` returns a working pip
- Git for versioning your project (recommended)

## Usage Instructions

### Step 1: Create and Activate a Virtual Environment

Always isolate project dependencies with a virtual environment:

```bash
mkdir myproject && cd myproject
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

Add `.venv/` to `.gitignore`. On Windows activate with `.venv\Scripts\activate`.

### Step 2: Pin and Freeze Dependencies

Record exact dependency versions for reproducible builds:

```bash
pip install requests==2.32.0
pip freeze > requirements.txt
cat requirements.txt
```

For libraries, list top-level dependencies in `pyproject.toml` instead, and
avoid committing `requirements.txt` lockfiles unless building applications.

### Step 3: Add Type Annotations

Annotate function signatures and data structures to make intent explicit:

```python
from typing import Any, Iterable

def average(numbers: Iterable[float]) -> float:
    """Return the arithmetic mean of a non-empty iterable."""
    values = list(numbers)
    if not values:
        raise ValueError("cannot average an empty sequence")
    return sum(values) / len(values)

def handle_event(payload: dict[str, Any]) -> None:
    ...
```

Prefer built-in generics (`list[str]`, `dict[str, int]`) on Python 3.9+ and
reserve `typing.List` / `typing.Dict` for legacy codebases.

### Step 4: Configure Linting and Formatting

Standardize on `ruff` for linting and `black` for formatting:

```bash
python -m pip install ruff black
ruff check .
black .
```

Add a `pyproject.toml` section to keep settings shared across the team:

```toml
[tool.ruff]
target-version = "py39"
line-length = 88

[tool.black]
line-length = 88
```

### Step 5: Verify Types with mypy

Run `mypy` in strict mode to catch type errors before they reach production:

```bash
python -m pip install mypy
mypy --strict src/
```

Keep `py.typed` inside the package directory so downstream users can rely on
your type hints.

### Step 6: Package with pyproject.toml

Use the modern PEP 621 layout with a build backend:

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "myproject"
version = "0.1.0"
description = "A short summary of the project"
readme = "README.md"
requires-python = ">=3.9"
dependencies = ["requests>=2.32"]

[project.optional-dependencies]
dev = ["ruff", "black", "mypy", "pytest"]

[tool.setuptools.packages.find]
include = ["myproject*"]
```

Install the package in editable mode for development:

```bash
python -m pip install -e ".[dev]"
```

## Examples

### Example 1: A Typed Dataclass

```python
from dataclasses import dataclass, field

@dataclass(slots=True)
class User:
    """A user entity with validation helpers."""
    id: int
    name: str
    email: str
    roles: list[str] = field(default_factory=list)

    @property
    def is_admin(self) -> bool:
        return "admin" in self.roles
```

### Example 2: Guarded Library Entry Point

```python
# myproject/cli.py
import argparse

def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="myproject")
    parser.add_argument("name", help="name to greet")
    args = parser.parse_args(argv)
    print(f"Hello, {args.name}!")

if __name__ == "__main__":
    main()
```

## References

- [Python PEP 8 Style Guide](https://peps.python.org/pep-0008/)
- [PEP 484 Type Hints](https://peps.python.org/pep-0484/)
- [Python Packaging User Guide](https://packaging.python.org/en/latest/)
- [pyproject.toml specification (PEP 621)](https://peps.python.org/pep-0621/)
- [ruff documentation](https://docs.astral.sh/ruff/)
- [mypy documentation](https://mypy.readthedocs.io/)
- [The Hitchhiker's Guide to Python](https://docs.python-guide.org/)

## Notes

- Commit `requirements.txt` for applications but not for published libraries.
- Add `.venv`, `__pycache__`, and `*.egg-info/` to `.gitignore`.
- Run `ruff check . && mypy src/` in CI and as a pre-commit hook.
- Use `enum` for fixed value sets instead of string constants.
- Favor `dataclasses` and `pydantic` over hand-written `__init__` methods.
- On Windows use `py -m venv .venv` when `python3` is unavailable.
- Keep modules small; a file over 300 lines usually deserves splitting.
