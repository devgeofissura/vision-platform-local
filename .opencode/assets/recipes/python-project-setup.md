---
name: python-project-setup
description: Complete recipe for setting up a modern Python project
version: 0.1.0
author: devtiagoabreu
tags: [python, backend, project-setup]
category: project-setup
ingredients:
  - type: skill
    name: python-testing
    version: 0.1.0
  - type: skill
    name: database-design
    version: 0.1.0
steps:
  - description: Create project directory and virtual environment
    commands:
      - mkdir my-python-project
      - cd my-python-project
      - python -m venv venv
      - source venv/bin/activate
  - description: Initialize project structure
    commands:
      - mkdir -p src tests docs
      - touch README.md .gitignore requirements.txt
  - description: Set up package configuration
    commands:
      - touch setup.py pyproject.toml
  - description: Install development dependencies
    commands:
      - pip install pytest black flake8 mypy
      - pip freeze > requirements.txt
  - description: Configure linting and formatting
    commands: []
  - description: Write initial tests
    commands: []
outcome: A fully configured Python project with testing, linting, and type checking
difficulty: intermediate
---

# Python Project Setup Recipe

## Overview

This recipe guides you through setting up a modern Python project with testing, linting, and best practices.

## Prerequisites

- Python 3.8+ installed
- pip installed
- Code editor (VS Code recommended)

## Ingredients

- **python-testing**: Python testing best practices
- **database-design**: Database design patterns

## Steps

### Step 1: Create Project Directory and Virtual Environment

```bash
mkdir my-python-project
cd my-python-project
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 2: Initialize Project Structure

```bash
mkdir -p src tests docs
touch README.md .gitignore requirements.txt
```

### Step 3: Set Up Package Configuration

```bash
touch setup.py pyproject.toml
```

Configure `pyproject.toml`:

```toml
[tool.poetry]
name = "my-python-project"
version = "0.1.0"
description = ""
authors = ["Your Name <your.email@example.com>"]

[tool.poetry.dependencies]
python = "^3.8"

[tool.poetry.dev-dependencies]
pytest = "^7.0"
black = "^22.0"
flake8 = "^4.0"
mypy = "^0.900"
```

### Step 4: Install Development Dependencies

```bash
pip install pytest black flake8 mypy
pip freeze > requirements.txt
```

### Step 5: Configure Linting and Formatting

Create `setup.cfg`:

```ini
[flake8]
max-line-length = 88
extend-ignore = E203

[mypy]
python_version = 3.8
```

### Step 6: Write Initial Tests

```python
# tests/test_example.py
def test_example():
    assert 1 + 1 == 2
```

## Expected Outcome

- Modern Python project with virtual environment
- Configured linting and formatting
- Basic testing setup
- Clean project structure

## References

- [Python Documentation](https://docs.python.org/3/)
- [pytest Documentation](https://docs.pytest.org/)
- [Black Documentation](https://black.readthedocs.io/)