---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-15
name: c-best-practices
description: C best practices covering memory management, pointer safety, and defensive programming
category: languages
version: 0.1.0
author: devtiagoabreu
tags: [c, pointers, memory, security, embedded]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - A C11 compiler (GCC or Clang)
  - make or CMake for building
provides:
  - Memory management and pointer safety rules
  - Buffer and bounds-checking practices
  - Makefile and compiler flags conventions
  - Static analysis guidance
---

# C Best Practices

## Overview

This skill is a guide to writing safe, reliable C code. It focuses on memory
management, pointer safety, and defensive programming, which are the leading
sources of bugs and security vulnerabilities in C. The patterns apply to
system tools, libraries, and embedded firmware.

## Prerequisites

- A C11 compiler such as GCC or Clang
- make or CMake for building
- Basic familiarity with the C language and pointers

## Usage Instructions

Use this skill when writing or reviewing C code. Always check bounds, check
return values, and compile with warnings and sanitizers enabled.

## Memory Management

### Always check malloc results

```c
#include <stdlib.h>

char *buffer = malloc(1024);
if (buffer == NULL) {
    return -1;  /* allocation failed */
}
free(buffer);
buffer = NULL;
```

### Never use after free

```c
free(ptr);
ptr = NULL;  /* prevents dangling pointer access */
```

## Pointer and Bounds Safety

### Bound all buffer operations

```c
#include <string.h>

char dst[64];
strncpy(dst, src, sizeof(dst) - 1);
dst[sizeof(dst) - 1] = '\0';  /* guarantee termination */
```

### Use size parameters for arrays

```c
size_t sum_array(const int *values, size_t count)
{
    size_t total = 0;
    for (size_t i = 0; i < count; i++) {
        total += values[i];
    }
    return total;
}
```

## Defensive Programming

### Check all function return values

```c
FILE *file = fopen("config.ini", "r");
if (file == NULL) {
    perror("fopen");
    return -1;
}
fclose(file);
```

### Validate inputs at the boundary

```c
int parse_index(const char *s, int max)
{
    char *end = NULL;
    long value = strtol(s, &end, 10);
    if (end == s || *end != '\0' || value < 0 || value >= max) {
        return -1;
    }
    return (int)value;
}
```

## Compiler and Analysis Flags

```makefile
CC     = gcc
CFLAGS = -std=c11 -Wall -Wextra -Wpedantic -Wshadow -Wconversion
SAN    = -fsanitize=address,undefined -g
```

Run with sanitizers during development:

```bash
gcc -std=c11 -Wall -Wextra -fsanitize=address,undefined -g main.c -o app
./app
```

## Common Pitfalls

- Using `gets()` or unbounded `sprintf()` — always use the bounded variants
- Assuming `sizeof(ptr)` gives the array size
- Casting away `const` without good reason
- Integer overflow in sizes and offsets

## Examples

### Growable buffer helper

```c
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *data;
    size_t len;
    size_t cap;
} Buffer;

int buffer_append(Buffer *buf, const char *text, size_t len)
{
    if (buf->len + len + 1 > buf->cap) {
        size_t new_cap = buf->cap ? buf->cap * 2 : 64;
        while (new_cap < buf->len + len + 1) {
            new_cap *= 2;
        }
        char *tmp = realloc(buf->data, new_cap);
        if (tmp == NULL) {
            return -1;
        }
        buf->data = tmp;
        buf->cap = new_cap;
    }
    memcpy(buf->data + buf->len, text, len);
    buf->len += len;
    buf->data[buf->len] = '\0';
    return 0;
}
```
