# NeoVM Instruction Set

## Overview

NeoVM uses a rich instruction set with over 200 opcodes. Instructions are categorized by their function.

## Instruction Categories

1. Constants
2. Flow Control
3. Stack Operations
4. Slot Operations
5. String Operations
6. Logical Operations
7. Arithmetic Operations
8. Compound Type Operations
9. Type Operations

## 1. Constants

Push constant values onto the stack:

| Opcode | Name | Description |
|--------|------|-------------|
| 0x00 | PUSHINT8 | Push 1-byte signed integer |
| 0x01 | PUSHINT16 | Push 2-byte signed integer |
| 0x02 | PUSHINT32 | Push 4-byte signed integer |
| 0x03 | PUSHINT64 | Push 8-byte signed integer |
| 0x04 | PUSHINT128 | Push 16-byte signed integer |
| 0x05 | PUSHINT256 | Push 32-byte signed integer |
| 0x08 | PUSHT | Push true |
| 0x09 | PUSHF | Push false |
| 0x0B | PUSHNULL | Push null |

## 2. Flow Control

Control program execution flow:

| Opcode | Name | Description |
|--------|------|-------------|
| 0x20 | JMP | Unconditional jump |
| 0x21 | JMP_L | Long unconditional jump |
| 0x22 | JMPIF | Jump if true |
| 0x23 | JMPIF_L | Long jump if true |
| 0x24 | JMPIFNOT | Jump if false |
| 0x25 | JMPIFNOT_L | Long jump if false |
| 0x26 | JMPEQ | Jump if equal |
| 0x27 | JMPEQ_L | Long jump if equal |
| 0x34 | CALL | Call a function |
| 0x35 | CALL_L | Long call |
| 0x40 | RET | Return from function |

## 3. Stack Operations

Manipulate the evaluation stack:

| Opcode | Name | Description |
|--------|------|-------------|
| 0x45 | DEPTH | Get stack depth |
| 0x46 | DROP | Remove top item |
| 0x47 | NIP | Remove second item |
| 0x48 | XDROP | Remove item at index |
| 0x49 | CLEAR | Clear the stack |
| 0x4A | DUP | Duplicate top item |
| 0x4B | OVER | Copy second item to top |
| 0x4D | SWAP | Swap top two items |
| 0x4E | ROT | Rotate top three items |
| 0x50 | REVERSE3 | Reverse top 3 items |
| 0x51 | REVERSE4 | Reverse top 4 items |

## 4. Arithmetic Operations

Mathematical operations:

| Opcode | Name | Description |
|--------|------|-------------|
| 0x8B | SIGN | Get sign of number |
| 0x8C | ABS | Absolute value |
| 0x8D | NEGATE | Negate value |
| 0x8E | INC | Increment by 1 |
| 0x8F | DEC | Decrement by 1 |
| 0x90 | ADD | Addition |
| 0x91 | SUB | Subtraction |
| 0x92 | MUL | Multiplication |
| 0x93 | DIV | Division |
| 0x94 | MOD | Modulo |
| 0x95 | POW | Power |
| 0x96 | SQRT | Square root |

## 5. Logical Operations

| Opcode | Name | Description |
|--------|------|-------------|
| 0xA8 | NOT | Logical NOT |
| 0xA9 | AND | Bitwise AND |
| 0xAA | OR | Bitwise OR |
| 0xAB | XOR | Bitwise XOR |
| 0xB1 | EQUAL | Check equality |
| 0xB2 | NOTEQUAL | Check inequality |

## 6. Comparison Operations

| Opcode | Name | Description |
|--------|------|-------------|
| 0xB3 | LT | Less than |
| 0xB4 | LE | Less or equal |
| 0xB5 | GT | Greater than |
| 0xB6 | GE | Greater or equal |

## Example: Simple Addition

```
PUSHINT8 5    // Push 5
PUSHINT8 3    // Push 3
ADD           // Result: 8
```
