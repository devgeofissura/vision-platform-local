---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: python-testing
description: Complete guide to Python testing with pytest
category: testing
version: 0.1.0
author: devtiagoabreu
tags: [python, testing, pytest, unit-tests]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Python 3.7+ installed
  - pytest installed
provides:
  - Test configuration
  - Test examples
  - Best practices
---

# Python Testing

## Overview

This skill provides a complete guide for writing tests in Python using pytest,
including unit tests, integration tests, and mocks.

## Prerequisites

- Python 3.7 or higher
- pytest installed (`pip install pytest`)
- pytest-cov for coverage (`pip install pytest-cov`)

## Usage Instructions

### 1. Configuration

```bash
# Install dependencies
pip install pytest pytest-cov

# Create pytest.ini
cat > pytest.ini << 'EOF'
[pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*
addopts = -v --tb=short
EOF
```

### 2. Test Structure

```
my_project/
├── src/
│   └── my_module.py
├── tests/
│   ├── __init__.py
│   ├── test_my_module.py
│   └── conftest.py
└── pytest.ini
```

### 3. Unit Tests

```python
# tests/test_my_module.py
import pytest
from src.my_module import add, subtract

class TestAdd:
    def test_add_positive(self):
        assert add(2, 3) == 5
    
    def test_add_negative(self):
        assert add(-1, -1) == -2
    
    def test_add_zero(self):
        assert add(0, 5) == 5

class TestSubtract:
    def test_subtract_basic(self):
        assert subtract(5, 3) == 2
    
    def test_subtract_negative_result(self):
        assert subtract(3, 5) == -2
```

### 4. Tests with Fixtures

```python
# tests/conftest.py
import pytest

@pytest.fixture
def valid_data():
    return {
        "name": "John",
        "email": "john@example.com",
        "age": 30
    }

@pytest.fixture
def mock_client(mocker):
    return mocker.patch('src.client.Client')
```

### 5. Tests with Parametrize

```python
@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
    (10, -5, 5),
])
def test_add_parametrized(a, b, expected):
    assert add(a, b) == expected
```

### 6. Exception Tests

```python
def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)
```

### 7. Mocking

```python
from unittest.mock import Mock, patch

def test_call_api():
    with patch('src.api.requests.get') as mock_get:
        mock_get.return_value.json.return_value = {"status": "ok"}
        result = call_api()
        assert result["status"] == "ok"
        mock_get.assert_called_once()
```

## Examples

### Example 1: Class Test

```python
# src/calculator.py
class Calculator:
    def __init__(self):
        self.history = []
    
    def add(self, a, b):
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result
    
    def get_history(self):
        return self.history.copy()

# tests/test_calculator.py
import pytest
from src.calculator import Calculator

@pytest.fixture
def calc():
    return Calculator()

def test_add(calc):
    assert calc.add(2, 3) == 5

def test_history(calc):
    calc.add(1, 2)
    calc.add(3, 4)
    assert len(calc.get_history()) == 2
```

### Example 2: Integration Test

```python
# tests/test_integration.py
import pytest
from src.database import Database

@pytest.fixture
def db():
    database = Database(":memory:")
    yield database
    database.close()

def test_create_table(db):
    db.create_table("users")
    assert "users" in db.list_tables()

def test_insert_user(db):
    db.create_table("users")
    db.insert("users", {"name": "John"})
    users = db.select("users")
    assert len(users) == 1
```

## Useful Commands

```bash
# Run all tests
pytest

# Run with verbose
pytest -v

# Run with coverage
pytest --cov=src

# Run specific test
pytest tests/test_my_module.py

# Run specific test
pytest tests/test_my_module.py::TestAdd::test_add_positive

# Run tests matching pattern
pytest -k "add"
```

## References

- [pytest Documentation](https://docs.pytest.org/)
- [Python Testing with pytest](https://www.amazon.com/Python-Testing-pytest-Brian-Okken/dp/1680502409)
- [Real Python - Testing](https://realpython.com/testing-in-python/)

## Notes

- Write tests before code (TDD)
- Keep tests independent
- Use descriptive names for tests
- Test edge cases and exceptions
- Use fixtures for shared setup
- Keep tests fast
