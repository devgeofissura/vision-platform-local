---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-15
name: delphi-best-practices
description: Delphi best practices covering object-oriented Pascal structure, VCL/FMX patterns, and database access
category: languages
version: 0.1.0
author: devtiagoabreu
tags: [delphi, pascal, vcl, firemonkey, firebird, sql, windows]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Delphi (RAD Studio) 10.4 or newer, or the free Community Edition
provides:
  - Object-oriented Pascal structure and naming conventions
  - VCL and FireMonkey UI patterns
  - Database access patterns (FireDAC, TDataSet)
  - Error handling and unit testing guidance
---

# Delphi Best Practices

## Overview

This skill is a guide to writing clean, maintainable Delphi applications using
Object Pascal. It covers project organization, naming conventions, the
DataModule pattern for database access, and structured exception handling. The
patterns apply to both VCL (Windows) and FireMonkey (cross-platform)
applications and keep codebases easy to navigate as they grow.

## Prerequisites

- Delphi / RAD Studio installed, or the free Community Edition
- Basic familiarity with Object Pascal syntax
- A target platform in mind (Windows, Android, iOS, macOS)

## Usage Instructions

Use this skill when creating new units, adding database access, or reviewing
existing Delphi code. Follow the conventions below to keep units cohesive and
testable.

## Unit Structure

```
unit CustomerService;

interface

uses
  System.SysUtils, Data.DB;

type
  TCustomerService = class
  private
    FConnection: TFDConnection;
  public
    constructor Create(AConnection: TFDConnection);
    function LoadCustomers: TDataSet;
  end;

implementation

constructor TCustomerService.Create(AConnection: TFDConnection);
begin
  FConnection := AConnection;
end;

function TCustomerService.LoadCustomers: TDataSet;
begin
  Result := FConnection
    .ExecSQL('SELECT * FROM customers ORDER BY name', [], False);
end;

end.
```

## Naming Conventions

- Types start with `T` (e.g., `TCustomerService`)
- Interfaces start with `I` (e.g., `IPaymentGateway`)
- Fields start with `F` (e.g., `FConnection`)
- Properties, methods, and units use PascalCase
- Constants and local variables use camelCase

## Database Access

### Use FireDAC with DataModules

Create a DataModule holding the connection so it can be reused:

```pascal
type
  TdmDatabase = class(TDataModule)
    FDConnection: TFDConnection;
  private
    class var FInstance: TdmDatabase;
  public
    class function GetInstance: TdmDatabase;
  end;

class function TdmDatabase.GetInstance: TdmDatabase;
begin
  if FInstance = nil then
    FInstance := TdmDatabase.Create(nil);
  Result := FInstance;
end;
```

### Parameterized queries

```pascal
function TCustomerRepository.FindByName(const AName: string): TDataSet;
begin
  Result := FConnection.ExecSQL(
    'SELECT * FROM customers WHERE name LIKE :name',
    [AName + '%'], False);
end;
```

## Error Handling

### Use try/except/raise

```pascal
try
  FConnection.ExecSQL('DELETE FROM orders WHERE id = :id', [AOrderId], True);
except
  on E: EDatabaseError do
  begin
    Logger.Error('Delete order failed: %s', [E.Message]);
    raise;
  end;
end;
```

### Use finally to release resources

```pascal
FQuery := TFDQuery.Create(nil);
try
  FQuery.Connection := FConnection;
  FQuery.Open('SELECT * FROM products');
finally
  FQuery.Free;
end;
```

## UI Patterns

### Keep the UI thin

Business logic belongs in service/repository classes, not in form event
handlers. A form should only bind data to visual controls:

```pascal
procedure TFormMain.FormCreate(Sender: TObject);
begin
  FDQuery.DataSource := FService.DataSource;
end;
```

## Testing

### Write unit tests with DUnitX

```pascal
uses
  DUnitX.TestFramework;

[TestFixture]
TCustomerServiceTests = class
  procedure TestLoadCustomers;
end;

procedure TCustomerServiceTests.TestLoadCustomers;
begin
  Assert.IsNotNull(FService.LoadCustomers);
end;
```

## Common Pitfalls

- Long event handlers in forms that mix UI and business logic
- Creating and freeing connections per query instead of reusing one
- Hard-coding connection strings in source code
- Using global variables instead of dependency injection

## Examples

### Export customers to a CSV file

```pascal
procedure TCustomerService.ExportToCsv(const AFileName: string);
var
  LWriter: TStreamWriter;
  LDS: TDataSet;
begin
  LDS := LoadCustomers;
  LWriter := TStreamWriter.Create(AFileName, False, TEncoding.UTF8);
  try
    while not LDS.Eof do
    begin
      LWriter.WriteLine(Format('%s;%s', [LDS.FieldByName('name').AsString,
        LDS.FieldByName('email').AsString]));
      LDS.Next;
    end;
  finally
    LWriter.Free;
  end;
end;
```
