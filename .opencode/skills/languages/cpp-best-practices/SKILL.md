---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-15
name: cpp-best-practices
description: C++ best practices covering modern C++ (11-23), RAII, smart pointers, and testing
category: languages
version: 0.1.0
author: devtiagoabreu
tags: [cpp, c++, smart-pointers, raii, cmake, testing]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - A C++17 or newer compiler (GCC, Clang, or MSVC)
  - CMake 3.16 or newer (recommended)
provides:
  - Modern C++ feature guidance
  - RAII and smart pointer patterns
  - Build system conventions with CMake
  - Testing with GoogleTest or Catch2
---

# C++ Best Practices

## Overview

This skill is a guide to writing modern, safe C++. It covers smart pointers
and RAII, modern language features, build conventions with CMake, and unit
testing. The goal is to write code that is memory-safe by default, easy to
read, and free of the classic pitfalls of manual resource management.

## Prerequisites

- A C++17 or newer compiler (GCC 9+, Clang 10+, or MSVC 2019+)
- CMake 3.16 or newer for building
- Basic familiarity with the C++ language

## Usage Instructions

Use this skill when writing or reviewing C++ code. Prefer smart pointers over
raw ownership, compile with warnings enabled, and run the test suite before
committing.

## RAII and Smart Pointers

### Prefer unique_ptr for exclusive ownership

```cpp
#include <memory>

std::unique_ptr<Connection> conn = std::make_unique<Connection>(config);
```

### Use shared_ptr only for shared ownership

```cpp
std::shared_ptr<Cache> cache = std::make_shared<Cache>();
```

### Avoid raw new/delete

```cpp
// Correct:
auto buffer = std::make_unique<std::vector<char>>(size);

// Avoid:
// char* buffer = new char[size];
// delete[] buffer;
```

## Modern Language Features

### Use auto where the type is obvious

```cpp
auto result = computeValue();
auto items = std::vector<int>{1, 2, 3};
```

### Use structured bindings

```cpp
auto [name, age] = getPerson();
```

### Use std::optional for optional values

```cpp
#include <optional>

std::optional<int> findIndex(const std::vector<int>& v, int target)
{
    auto it = std::find(v.begin(), v.end(), target);
    if (it == v.end())
        return std::nullopt;
    return static_cast<int>(it - v.begin());
}
```

## Error Handling

### Prefer exceptions over error codes

```cpp
#include <stdexcept>

int divide(int a, int b)
{
    if (b == 0)
        throw std::invalid_argument("division by zero");
    return a / b;
}
```

### Use noexcept for non-throwing functions

```cpp
void close(Connection& conn) noexcept
{
    conn.close();
}
```

## Build System with CMake

```cmake
cmake_minimum_required(VERSION 3.16)
project(MyApp CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(myapp src/main.cpp src/logger.cpp)
target_compile_options(myapp PRIVATE -Wall -Wextra -Wpedantic)

include(CTest)
if(BUILD_TESTING)
  add_subdirectory(tests)
endif()
```

## Testing with GoogleTest

```cpp
#include <gtest/gtest.h>
#include "logger.h"

TEST(LoggerTest, LogsFormattedMessage)
{
    Logger logger;
    EXPECT_EQ(logger.format("Hello {}", "World"), "Hello World");
}
```

## Common Pitfalls

- Using raw pointers where ownership is exclusive
- Forgetting to mark overridden methods with `override`
- Using `#define` macros instead of constexpr or templates
- Ignoring compiler warnings that catch real bugs

## Examples

### RAII resource wrapper

```cpp
class FileGuard
{
public:
    explicit FileGuard(const std::string& path)
        : handle_(std::fopen(path.c_str(), "r"))
    {
        if (!handle_)
            throw std::runtime_error("cannot open file");
    }

    ~FileGuard()
    {
        if (handle_)
            std::fclose(handle_);
    }

    FileGuard(const FileGuard&) = delete;
    FileGuard& operator=(const FileGuard&) = delete;

private:
    std::FILE* handle_;
};
```
