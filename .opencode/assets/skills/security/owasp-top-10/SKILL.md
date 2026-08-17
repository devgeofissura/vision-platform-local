---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: owasp-top-10
description: Best practices for addressing OWASP Top 10 security risks
category: security
version: 0.1.0
author: devtiagoabreu
tags: [owasp, security, vulnerabilities, best-practices]
compatible:
  - opencode
  - claude-code
  - cursor
---

# OWASP Top 10 Best Practices

## Overview

This skill provides best practices for addressing the OWASP Top 10 security risks, including injection, broken authentication, and cross-site scripting.

## Prerequisites

- Basic understanding of web security
- Knowledge of common vulnerabilities

## Usage Instructions

### Step 1: Injection Prevention

Prevent SQL injection:

```python
# Bad - vulnerable to SQL injection
query = f"SELECT * FROM users WHERE id = {user_id}"

# Good - use parameterized queries
query = "SELECT * FROM users WHERE id = %s"
cursor.execute(query, (user_id,))
```

### Step 2: Authentication Security

Implement secure authentication:

```python
# Use strong password hashing
import bcrypt

def hash_password(password):
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode(), salt)

# Implement account lockout
def check_login_attempts(user_id):
    attempts = get_login_attempts(user_id)
    if attempts >= 5:
        lock_account(user_id)
        return False
    return True
```

### Step 3: XSS Prevention

Prevent cross-site scripting:

```python
# Escape user input
from markupsafe import escape

user_input = request.form.get('name')
safe_output = escape(user_input)

# Use Content Security Policy
@app.after_request
def set_csp(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response
```

### Step 4: CSRF Protection

Implement CSRF protection:

```python
from flask_wtf.csrf import CSRF

csrf = CSRF(app)

# In templates
<form method="post">
    {{ csrf_token() }}
    <input type="text" name="name">
    <button type="submit">Submit</button>
</form>
```

## Examples

### Security Headers

```python
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response
```

## Best Practices

1. Use parameterized queries
2. Implement secure authentication
3. Escape user input
4. Implement CSRF protection
5. Use security headers
6. Validate and sanitize input

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)