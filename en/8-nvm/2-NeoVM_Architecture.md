# NeoVM Architecture

## Overview

NeoVM is designed as a stack-based virtual machine with a clear separation between execution logic and blockchain interaction. This chapter explores the internal architecture of NeoVM in Neo N3.

## Core Components

### 1. Execution Engine

The execution engine is the heart of NeoVM, responsible for:
- Loading and parsing bytecode
- Executing instructions sequentially
- Managing the execution context
- Handling exceptions

### 2. Stack System

NeoVM operates with multiple stacks:

#### Evaluation Stack
The primary stack for all computations:
```
┌─────────────┐
│   Top       │  ← Most recent push
├─────────────┤
│   Item 2    │
├─────────────┤
│   Item 1    │
├─────────────┤
│   Bottom    │  ← First push
└─────────────┘
```

#### Alternative Stack
Used for temporary storage during complex operations.

### 3. Invocation Stack

Manages execution contexts when contracts call other contracts:
```
┌─────────────────────┐
│  Current Context    │  ← Active execution
├─────────────────────┤
│  Caller Context     │
├─────────────────────┤
│  Original Context   │
└─────────────────────┘
```

## Data Types

NeoVM supports the following primitive types:

| Type | Description | Example |
|------|-------------|---------|
| Boolean | True/False | `true`, `false` |
| Integer | Arbitrary precision | `12345`, `-999` |
| ByteString | Immutable byte array | `0x48656c6c6f` |
| Buffer | Mutable byte array | Used for building data |
| Array | Dynamic list | `[1, 2, 3]` |
| Struct | Value-type array | Copied on assignment |
| Map | Key-value pairs | `{"key": "value"}` |
| InteropInterface | External objects | Contract references |

## Execution Context

Each execution context contains:

- **Script** - The bytecode being executed
- **Instruction Pointer** - Current position in the script
- **Local Variables** - Function-local storage
- **Static Fields** - Contract-level storage
- **Arguments** - Parameters passed to the method

## Exception Handling

Neo N3 introduced full exception handling:

```csharp
try
{
    // Code that might throw
    SomeRiskyOperation();
}
catch (Exception e)
{
    // Handle the exception
    Runtime.Log("Error occurred");
}
finally
{
    // Always executed
    Cleanup();
}
```

## Limits and Constraints

| Parameter | Value |
|-----------|-------|
| Max Stack Size | 2048 items |
| Max Item Size | 1024 * 1024 bytes |
| Max Invocation Depth | 1024 |
| Max Script Length | Unlimited (GAS limited) |
