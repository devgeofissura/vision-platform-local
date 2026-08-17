---
name: style-guide-context
description: Style guide for OpenCode Engineering Kit
type: conventions
version: 0.1.0
author: devtiagoabreu
---

# Style Guide

## Markdown

### General

- Maximum 80 characters per line
- Paragraphs separated by blank line
- Use `-` for bullets, not '*'
- Always specify language in code blocks
- Use reference links when possible
- Descriptive alt text for images

### Headers

```markdown
# H1 - Main Title
## H2 - Sections
### H3 - Subsections
#### H4 - Sub-subsections
```

### Lists

```markdown
- Item 1
- Item 2
  - Sub-item
- Item 3
```

### Code

````markdown
```python
def hello():
    print("Hello, World!")
```
````

### Tables

```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Value 1  | Value 2  | Value 3  |
```

### Links

```markdown
[link text](url)
[link text](url "link title")
```

### Images

```markdown
![alt text](url)
![alt text](url "title")
```

## YAML

### General

- 2-space indentation
- Use quotes only when necessary
- Use flow format for short lists
- Comments to explain decisions

### Example

```yaml
---
name: skill-name
description: Skill description
tags: [tag1, tag2]
compatible:
  - opencode
  - claude-code
---
```

## Bash

### General

- Shebang `#!/bin/bash`
- `set -euo pipefail` at the beginning
- 2-space indentation
- Variables with `${VAR}`
- Double-quoted strings

### Example

```bash
#!/bin/bash
set -euo pipefail

function main() {
    local input="${1:?Usage: $0 <input>}"
    echo "Processing: ${input}"
}

main "$@"
```

### Functions

```bash
#!/bin/bash
set -euo pipefail

# Function with return
is_valid() {
    local input="$1"
    [[ "$input" =~ ^[a-zA-Z0-9]+$ ]]
}

# Function with echo
get_value() {
    local key="$1"
    echo "${key}_value"
}

# Usage
if is_valid "test"; then
    echo "Valid"
fi
```

## References

- [Naming](./naming.md) - Naming conventions
- [Conventions](./conventions.md) - Code conventions

## Anti-Patterns

| Anti-Pattern | Correct Pattern | Reason |
|--------------|-----------------|--------|
| Hardcoded secrets | Environment variables | Security |
| Duplicated code | Reusable functions | Maintenance |
| Generic names | Descriptive names | Readability |
| Long functions | Small functions | Comprehension |
| Excessive comments | Self-documenting code | Maintenance |
| Silent errors | Explicit handling | Debugging |
| Magic numbers | Named constants | Readability |

## Quality Metrics

| Metric | Minimum | Ideal |
|--------|---------|-------|
| Test coverage | 80% | 90%+ |
| Cyclomatic complexity | < 10 | < 5 |
| Duplication | < 5% | 0% |
| Documentation | 100% | 100% |

## Quality Checklist

- [ ] Code is readable
- [ ] Names are descriptive
- [ ] Functions are small
- [ ] No duplicated code
- [ ] Error handling adequate
- [ ] Tests present
- [ ] Documentation updated
