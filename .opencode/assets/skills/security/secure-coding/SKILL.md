---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: secure-coding
description: Best practices for secure coding and development
category: security
version: 0.1.0
author: devtiagoabreu
tags: [secure-coding, security, best-practices, development]
compatible:
  - opencode
  - claude-code
  - cursor
---

# Secure Coding Best Practices

## Overview

This skill provides best practices for secure coding and development, including input validation, error handling, and cryptography.

## Prerequisites

- Basic understanding of secure coding
- Programming knowledge

## Usage Instructions

### Step 1: Input Validation

Validate all input:

```python
import re

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    return True
```

### Step 2: Secure Error Handling

Handle errors securely:

```python
import logging

def handle_error(error):
    # Log the error
    logging.error(f"Error: {str(error)}")
    
    # Return generic error message
    return {
        "error": "An error occurred",
        "message": "Please try again later"
    }

# Never expose internal details
try:
    result = risky_operation()
except Exception as e:
    logging.error(f"Operation failed: {str(e)}")
    return {"error": "Operation failed"}
```

### Step 3: Cryptography

Use proper cryptography:

```python
from cryptography.fernet import Fernet

# Generate key
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Encrypt
encrypted = cipher_suite.encrypt(b"secret message")

# Decrypt
decrypted = cipher_suite.decrypt(encrypted)
```

### Step 4: Secrets Management

Manage secrets properly:

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Use environment variables
db_password = os.getenv('DB_PASSWORD')
api_key = os.getenv('API_KEY')

# Never commit secrets to version control
# Use .env files for local development
# Use secret managers for production
```

## Examples

### Secure Configuration

```python
# config.py
import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    DATABASE_URI = os.getenv('DATABASE_URI')
    API_KEY = os.getenv('API_KEY')
    
    # Security settings
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Rate limiting
    RATELIMIT_DEFAULT = "100/hour"
```

## Best Practices

1. Validate all input
2. Handle errors securely
3. Use proper cryptography
4. Manage secrets properly
5. Keep dependencies updated
6. Use security linting tools

## References

- [OWASP Secure Coding Practices](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/)
- [Python Security](https://python-security.readthedocs.io/)