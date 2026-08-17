---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: unit-testing
description: Best practices for unit testing and test-driven development
category: testing
version: 0.1.0
author: devtiagoabreu
tags: [unit-testing, tdd, testing, quality]
compatible:
  - opencode
  - claude-code
  - cursor
---

# Unit Testing Best Practices

## Overview

This skill provides best practices for unit testing and test-driven development, including test structure, mocking, and coverage.

## Prerequisites

- Basic understanding of testing concepts
- Testing framework knowledge (Jest, pytest, etc.)

## Usage Instructions

### Step 1: Test Structure

Use AAA pattern (Arrange, Act, Assert):

```python
def test_calculate_total():
    # Arrange
    items = [
        {"name": "Item 1", "price": 10},
        {"name": "Item 2", "price": 20}
    ]
    
    # Act
    total = calculate_total(items)
    
    # Assert
    assert total == 30
```

### Step 2: Test Naming

Use descriptive test names:

```python
# Good
def test_calculate_total_with_multiple_items():
    pass

def test_calculate_total_with_empty_list():
    pass

def test_calculate_total_with_discount():
    pass

# Bad
def test_calculate():
    pass
```

### Step 3: Mocking

Mock external dependencies:

```python
from unittest.mock import Mock, patch

def test_get_user():
    # Arrange
    mock_db = Mock()
    mock_db.query.return_value = {"id": 1, "name": "John"}
    
    # Act
    user = get_user(1, db=mock_db)
    
    # Assert
    assert user["name"] == "John"
    mock_db.query.assert_called_once()
```

### Step 4: Test Coverage

Aim for high coverage:

```bash
# Run with coverage
pytest --cov=src tests/

# Generate coverage report
pytest --cov=src --cov-report=html tests/
```

## Examples

### Unit Test Suite

```python
import pytest
from calculator import Calculator

class TestCalculator:
    def setup_method(self):
        self.calc = Calculator()
    
    def test_add(self):
        result = self.calc.add(2, 3)
        assert result == 5
    
    def test_subtract(self):
        result = self.calc.subtract(5, 3)
        assert result == 2
    
    def test_multiply(self):
        result = self.calc.multiply(2, 3)
        assert result == 6
    
    def test_divide(self):
        result = self.calc.divide(6, 3)
        assert result == 2
    
    def test_divide_by_zero(self):
        with pytest.raises(ZeroDivisionError):
            self.calc.divide(1, 0)
```

## Best Practices

1. Follow AAA pattern
2. Use descriptive test names
3. Mock external dependencies
4. Aim for high coverage
5. Test edge cases
6. Keep tests independent

## References

- [pytest Documentation](https://docs.pytest.org/)
- [Jest Documentation](https://jestjs.io/)