---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: integration-testing
description: Best practices for integration testing and API testing
category: testing
version: 0.1.0
author: devtiagoabreu
tags: [integration-testing, api-testing, testing, quality]
compatible:
  - opencode
  - claude-code
  - cursor
---

# Integration Testing Best Practices

## Overview

This skill provides best practices for integration testing and API testing, including test data management and environment setup.

## Prerequisites

- Basic understanding of integration testing
- Testing framework knowledge

## Usage Instructions

### Step 1: Test Data Management

Use factories for test data:

```python
import factory
from models import User

class UserFactory(factory.Factory):
    class Meta:
        model = User
    
    id = factory.Sequence(lambda n: n)
    name = factory.Faker('name')
    email = factory.Faker('email')
    created_at = factory.LazyFunction(datetime.now)
```

### Step 2: Database Testing

Use transactions for isolation:

```python
@pytest.fixture
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()
```

### Step 3: API Testing

Test API endpoints:

```python
def test_create_user(client):
    # Arrange
    data = {
        "name": "John Doe",
        "email": "john@example.com"
    }
    
    # Act
    response = client.post("/api/users", json=data)
    
    # Assert
    assert response.status_code == 201
    assert response.json()["name"] == "John Doe"
```

### Step 4: External Service Mocking

Mock external services:

```python
@patch('requests.get')
def test_get_weather(mock_get):
    # Arrange
    mock_get.return_value.json.return_value = {
        "temperature": 72,
        "condition": "sunny"
    }
    
    # Act
    weather = get_weather("New York")
    
    # Assert
    assert weather["temperature"] == 72
    mock_get.assert_called_once()
```

## Examples

### Integration Test Suite

```python
import pytest
from app import create_app
from models import db

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_user_workflow(client):
    # Create user
    response = client.post("/api/users", json={
        "name": "John",
        "email": "john@example.com"
    })
    assert response.status_code == 201
    user_id = response.json()["id"]
    
    # Get user
    response = client.get(f"/api/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "John"
    
    # Update user
    response = client.put(f"/api/users/{user_id}", json={
        "name": "John Updated"
    })
    assert response.status_code == 200
    
    # Delete user
    response = client.delete(f"/api/users/{user_id}")
    assert response.status_code == 204
```

## Best Practices

1. Use factories for test data
2. Use transactions for isolation
3. Test API endpoints
4. Mock external services
5. Test error scenarios
6. Use realistic test data

## References

- [pytest Documentation](https://docs.pytest.org/)
- [Testing Flask Applications](https://flask.palletsprojects.com/en/2.3.x/testing/)