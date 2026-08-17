---
name: security-context
description: Security context for OpenCode Engineering Kit
type: project
version: 0.1.0
author: devtiagoabreu
---

# Security Context

## Security Principles

1. **Never expose secrets** — API keys, tokens, and passwords must never be committed
2. **Principle of least privilege** — Minimum necessary access
3. **Defense in depth** — Multiple layers of protection
4. **Security by design** — Consider security from the start

## Security Rules

| Rule | Priority | Consequence |
|------|----------|-------------|
| No hardcoded secrets | Critical | Immediate rejection |
| Input validation | High | Mandatory review |
| Output sanitization | High | Mandatory review |
| Use environment variables | High | Mandatory review |
| Vulnerability documentation | Medium | Review required |

## What NEVER to Commit

```bash
# ❌ NEVER DO THIS

# API keys
API_KEY=sk-1234567890

# Passwords
DATABASE_PASSWORD=mysecretpassword

# Tokens
GITHUB_TOKEN=ghp_1234567890

# Certificates
*.pem
*.key

# Sensitive files
.env
.env.local
.env.production
```

## .gitignore

```gitignore
# Secrets
.env
.env.*
*.pem
*.key

# Dependencies
node_modules/
venv/
__pycache__/

# Build
dist/
build/
*.log

# IDE
.vscode/
.idea/
*.swp
```

## Environment Variables

```bash
# ✅ DO THIS

# Use environment variables
export API_KEY=${API_KEY:?API_KEY not defined}
export DATABASE_URL=${DATABASE_URL:?DATABASE_URL not defined}

# Or use .env (not committed)
# .env
API_KEY=sk-1234567890
DATABASE_URL=postgres://...
```

## Input Validation

```bash
#!/bin/bash
# ✅ Proper validation

validate_input() {
    local input="${1:?Input required}"
    
    # Check if not empty
    if [[ -z "$input" ]]; then
        echo "ERROR: Input cannot be empty"
        return 1
    fi
    
    # Check maximum length
    if (( ${#input} > 1000 )); then
        echo "ERROR: Input exceeds 1000 characters"
        return 1
    fi
    
    # Check for dangerous characters
    if [[ "$input" =~ [\<\>\&\|\;\`] ]]; then
        echo "ERROR: Input contains invalid characters"
        return 1
    fi
    
    return 0
}
```

## Security Audit

| Area | Frequency | Responsible |
|------|-----------|-------------|
| Dependencies | Weekly | Automated |
| Code | Per PR | Reviewers |
| Configurations | Monthly | Team |
| Logs | Continuous | Monitoring |

## Vulnerability Response

```
1. Identify vulnerability
2. Assess severity
3. Create fix
4. Test fix
5. Publish hotfix
6. Notify users
7. Document lesson
```

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)
- [Secret Scanning](https://docs.github.com/en/code-security/secret-scanning)
