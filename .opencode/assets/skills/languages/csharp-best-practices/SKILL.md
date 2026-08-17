---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-15
name: csharp-best-practices
description: C# best practices covering modern language features, async patterns, dependency injection, and testing
category: languages
version: 0.1.0
author: devtiagoabreu
tags: [csharp, dotnet, async, dependency-injection, testing, aspnet]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - .NET 8 SDK or newer
provides:
  - Modern C# language features and conventions
  - Async/await and task-based patterns
  - Dependency injection and SOLID guidance
  - Unit testing with xUnit and mocking
---

# C# Best Practices

## Overview

This skill is a practical guide to writing clean, maintainable C# code with
the .NET platform. It covers modern language features, asynchronous
programming, dependency injection, and unit testing. The patterns apply to
ASP.NET Core web applications, console tools, and class libraries, keeping
code consistent and easy to test.

## Prerequisites

- .NET 8 SDK or newer installed
- A code editor such as Visual Studio, VS Code, or Rider
- Basic familiarity with the C# language

## Usage Instructions

Use this skill when writing or reviewing C# code. Follow the conventions below
for namespaces, async operations, and dependency injection, and run `dotnet
build` plus `dotnet test` before committing.

## Modern Language Features

### Prefer records for data models

```csharp
public record Customer(int Id, string Name, string Email);
```

### Use nullable reference types

```csharp
string? MaybeName = LookupName(id);
if (MaybeName is not null)
{
    Console.WriteLine(MaybeName);
}
```

### Prefer pattern matching over cascading ifs

```csharp
return result switch
{
    > 0 => "Positive",
    0 => "Zero",
    _ => "Negative",
};
```

## Async Patterns

### Follow the async/await naming convention

```csharp
public async Task<Customer?> GetCustomerAsync(int id)
{
    return await _repository.FindByIdAsync(id);
}
```

### Avoid async void

Only use `async void` for event handlers:

```csharp
private async void OnLoadClicked(object sender, EventArgs e)
{
    await LoadDataAsync();
}
```

### Use Task.WhenAll for independent work

```csharp
var customerTask = GetCustomerAsync(id);
var ordersTask = GetOrdersAsync(id);
await Task.WhenAll(customerTask, ordersTask);

var customer = await customerTask;
var orders = await ordersTask;
```

## Dependency Injection

### Register services in the composition root

```csharp
builder.Services.AddScoped<ICustomerRepository, CustomerRepository>();
builder.Services.AddScoped<ICustomerService, CustomerService>();
```

### Inject interfaces, not implementations

```csharp
public class CustomerController(ICustomerService service) : ControllerBase
{
    [HttpGet("{id}")]
    public async Task<ActionResult<Customer>> Get(int id)
    {
        var customer = await service.FindByIdAsync(id);
        return customer is null ? NotFound() : Ok(customer);
    }
}
```

## Testing

### Write focused unit tests

```csharp
public class CustomerServiceTests
{
    [Fact]
    public async Task FindById_ReturnsCustomer_WhenExists()
    {
        var repository = new Mock<ICustomerRepository>();
        repository.Setup(r => r.FindByIdAsync(1))
            .ReturnsAsync(new Customer(1, "Ana", "ana@example.com"));
        var service = new CustomerService(repository.Object);

        var result = await service.FindByIdAsync(1);

        Assert.NotNull(result);
        Assert.Equal("Ana", result.Name);
    }
}
```

### Use the Arrange-Act-Assert structure

Structure every test into setup (arrange), the call (act), and the
assertion (assert) with blank lines between them.

## Common Pitfalls

- Blocking calls like `.Result` or `.Wait()` on async code, causing deadlocks
- Huge controllers with business logic instead of service classes
- Newing up services with `new` instead of using the DI container
- Ignoring cancellation tokens in long-running operations

## Examples

### Async repository with cancellation

```csharp
public class CustomerRepository : ICustomerRepository
{
    private readonly AppDbContext _db;

    public CustomerRepository(AppDbContext db)
    {
        _db = db;
    }

    public async Task<Customer?> FindByIdAsync(int id, CancellationToken ct = default)
    {
        return await _db.Customers
            .AsNoTracking()
            .FirstOrDefaultAsync(c => c.Id == id, ct);
    }
}
```

### Exception middleware

```csharp
app.Use(async (context, next) =>
{
    try
    {
        await next();
    }
    catch (Exception ex)
    {
        context.Response.StatusCode = StatusCodes.Status500InternalServerError;
        await context.Response.WriteAsJsonAsync(new { error = ex.Message });
    }
});
```
