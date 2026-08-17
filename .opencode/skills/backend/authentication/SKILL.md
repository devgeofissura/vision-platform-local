---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: authentication
description: Best practices for authentication and authorization implementation
category: backend
version: 0.1.0
author: devtiagoabreu
tags: [authentication, authorization, security, jwt]
compatible:
  - opencode
  - claude-code
  - cursor
---

# Authentication Best Practices

## Overview

This skill provides best practices for authentication and authorization implementation, including JWT, OAuth, and session management.

## Prerequisites

- Basic understanding of authentication concepts
- Security knowledge

## Usage Instructions

### Step 1: JWT Implementation

Implement JWT properly:

```python
import jwt
from datetime import datetime, timedelta

def create_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=1),
        'iat': datetime.utcnow()
    }
    
    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm='HS256'
    )

def verify_token(token):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=['HS256']
        )
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
```

### Step 2: Password Hashing

Hash passwords properly:

```python
import bcrypt

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(
        password.encode('utf-8'),
        salt
    )

def verify_password(password, hashed):
    return bcrypt.checkpw(
        password.encode('utf-8'),
        hashed
    )
```

### Step 3: OAuth Implementation

Implement OAuth 2.0:

```python
from authlib.integrations.requests_client import OAuth2Session

# Authorization URL
authorization_url, state = oauth2.authorization_url(
    'https://provider.com/oauth/authorize',
    access_type="offline",
    prompt="consent"
)

# Token exchange
token = oauth2.fetch_token(
    'https://provider.com/oauth/token',
    authorization_response=redirect_url,
    client_secret=CLIENT_SECRET
)
```

### Step 4: Session Management

Implement secure sessions:

```python
from flask import session
import secrets

# Generate secure session ID
session_id = secrets.token_hex(32)

# Store session
session['user_id'] = user_id
session['expires'] = datetime.utcnow() + timedelta(hours=1)

# Validate session
def validate_session():
    if 'expires' not in session:
        return False
    
    if session['expires'] < datetime.utcnow():
        return False
    
    return True
```

## Examples

### JWT Middleware

```python
from functools import wraps

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return {'error': 'Token missing'}, 401
        
        user_id = verify_token(token)
        
        if not user_id:
            return {'error': 'Invalid token'}, 401
        
        return f(*args, **kwargs)
    
    return decorated
```

## Best Practices

1. Use HTTPS only
2. Hash passwords with bcrypt
3. Implement proper JWT validation
4. Use short-lived tokens
5. Implement refresh tokens
6. Log authentication events
7. Implement rate limiting

## References

- [JWT Best Practices](https://auth0.com/blog/node-js-and-express-tutorial-building-and-securing-restful-apis/)
- [OAuth 2.0 Specification](https://oauth.net/2/)
- [OWASP Authentication Cheatsheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)