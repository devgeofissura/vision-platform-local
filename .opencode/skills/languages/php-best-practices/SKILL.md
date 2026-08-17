---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-15
name: php-best-practices
description: PHP best practices covering modern PHP 8 features, PSR standards, PDO database access, and testing
category: languages
version: 0.1.0
author: devtiagoabreu
tags: [php, pdo, psr, composer, testing, web]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - PHP 8.1 or newer
  - Composer installed
provides:
  - Modern PHP 8 features and type declarations
  - PSR standards and autoloading
  - Secure PDO database access
  - Unit testing with PHPUnit
---

# PHP Best Practices

## Overview

This skill is a guide to writing clean, secure, and maintainable PHP. It
covers modern PHP 8 features, PSR standards, secure database access with PDO,
and automated testing. These conventions help PHP applications stay readable,
testable, and free of common injection and XSS vulnerabilities.

## Prerequisites

- PHP 8.1 or newer installed
- Composer for dependency management
- Basic familiarity with the PHP language

## Usage Instructions

Use this skill when writing or reviewing PHP code. Follow the PSR conventions,
use PDO for database access, and run `composer test` before committing changes.

## Modern PHP 8 Features

### Declare strict types

```php
<?php

declare(strict_types=1);
```

### Use typed properties and return types

```php
class Customer
{
    public function __construct(
        public readonly int $id,
        public readonly string $name,
        public readonly string $email,
    ) {
    }
}
```

### Use match expressions

```php
$label = match ($status) {
    'active' => 'Active',
    'inactive' => 'Inactive',
    default => 'Unknown',
};
```

## PSR Standards

### Autoload with PSR-4 in composer.json

```json
{
  "autoload": {
    "psr-4": {
      "App\\": "src/"
    }
  },
  "require-dev": {
    "phpunit/phpunit": "^11.0"
  }
}
```

### Namespace every class

```php
<?php

namespace App\Services;

use App\Repositories\CustomerRepository;

class CustomerService
{
    public function __construct(private CustomerRepository $repository)
    {
    }
}
```

## Database Access with PDO

### Use prepared statements

```php
<?php

$pdo = new PDO($dsn, $user, $password, [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
]);

$stmt = $pdo->prepare('SELECT * FROM customers WHERE email = :email');
$stmt->execute(['email' => $email]);
$customer = $stmt->fetch();
```

### Never interpolate user input into SQL

```php
// Correct: bound parameters
$stmt = $pdo->prepare('SELECT * FROM products WHERE name LIKE :name');
$stmt->execute(['name' => "%{$search}%"]);

// Avoid: string concatenation with user input
// $pdo->query("SELECT * FROM products WHERE name LIKE '%{$search}%'");
```

## Security

### Escape output to prevent XSS

```php
<?php echo htmlspecialchars($userInput, ENT_QUOTES, 'UTF-8'); ?>
```

### Use password_hash and password_verify

```php
$hash = password_hash($password, PASSWORD_DEFAULT);

if (password_verify($password, $hash)) {
    // login ok
}
```

## Testing with PHPUnit

```php
<?php

namespace Tests\Unit;

use App\Services\CustomerService;
use PHPUnit\Framework\TestCase;

final class CustomerServiceTest extends TestCase
{
    public function testGreeting(): void
    {
        $service = new CustomerService();
        $this->assertSame('Hello, Ana', $service->greet('Ana'));
    }
}
```

## Common Pitfalls

- Using `mysql_*` functions instead of PDO or mysqli with prepared statements
- Outputting raw user input without escaping
- Ignoring type declarations and relying on dynamic types
- Skipping Composer autoloading and hand-requiring files

## Examples

### A simple repository class

```php
<?php

namespace App\Repositories;

use PDO;

class CustomerRepository
{
    public function __construct(private PDO $pdo)
    {
    }

    public function findById(int $id): ?array
    {
        $stmt = $this->pdo->prepare(
            'SELECT * FROM customers WHERE id = :id'
        );
        $stmt->execute(['id' => $id]);
        $customer = $stmt->fetch();
        return $customer ?: null;
    }
}
```

### Routing entry point with front controller

```php
<?php

// public/index.php
declare(strict_types=1);

require __DIR__ . '/../vendor/autoload.php';

$path = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
$routes = [
    '/' => fn () => 'Home',
    '/health' => fn () => 'OK',
];

echo $routes[$path] ?? 'Not found';
```
