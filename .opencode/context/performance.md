---
name: performance-context
description: Performance context for OpenCode Engineering Kit
type: project
version: 0.1.0
author: devtiagoabreu
---

# Performance Context

## Performance Goals

| Metric | Target | Measurement |
|--------|--------|-------------|
| Load time | < 1s | Manual measurement |
| File size | < 1MB | wc -c |
| Complexity | O(n) | Code analysis |
| Memory | < 100MB | top/htop |

## Limits

| Resource | Limit | Action |
|----------|-------|--------|
| Skill size | 600 lines | Split into multiple |
| Agent size | 200 lines | Simplify |
| Prompt size | 100 lines | Simplify |
| Total skills | 100+ | Better organization |
| Total agents | 50+ | Consolidate |

## Optimizations

### Files

- Use compression for large files
- Split very long files
- Use lazy loading when possible

### Scripts

- Avoid unnecessary loops
- Use efficient shell commands
- Minimize system calls

### Documentation

- Use reference links
- Avoid large images
- Compress assets when needed

## Benchmarks

```bash
# Measure execution time
time ./scripts/bootstrap.sh

# Measure size
du -sh skills/
du -sh agents/
du -sh templates/

# Measure complexity
find . -name "*.md" | wc -l
find . -name "*.sh" | wc -l
```

## Monitoring

### Performance

- Monitor load time
- Track file sizes
- Measure memory usage

### Quality

- Check test coverage
- Measure error rate
- Track user satisfaction
