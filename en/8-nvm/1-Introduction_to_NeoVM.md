# Introduction to NeoVM

## What is NeoVM?

The Neo Virtual Machine (NeoVM) is a lightweight, stack-based virtual machine designed to execute smart contracts on the Neo blockchain. It provides a secure, deterministic execution environment that ensures all nodes in the network reach the same result when processing transactions.

## History and Evolution

NeoVM was first introduced with Neo 2.x and has undergone significant improvements in Neo N3:

| Feature | Neo Legacy | Neo N3 |
|---------|-----------|--------|
| Instruction Set | ~100 opcodes | 200+ opcodes |
| Exception Handling | Limited | Full try-catch-finally |
| Debugging | Basic | Enhanced with source mapping |
| Performance | Good | Optimized execution engine |

## Key Characteristics

### 1. Deterministic Execution

NeoVM guarantees that the same contract code with the same input will always produce the same output, regardless of which node executes it. This is essential for blockchain consensus.

### 2. Sandboxed Environment

Smart contracts run in complete isolation from the host system. They cannot:
- Access the file system
- Make network calls directly
- Access system resources

All external interactions go through controlled interoperability services.

### 3. Stack-Based Architecture

NeoVM uses two primary stacks:
- **Evaluation Stack** - For computation and data manipulation
- **Alternative Stack** - For temporary storage during execution

### 4. Gas Metering

Every operation in NeoVM consumes GAS, preventing infinite loops and ensuring fair resource allocation.

## NeoVM in the Neo N3 Ecosystem

```
┌─────────────────────────────────────────────┐
│              Neo N3 Blockchain              │
├─────────────────────────────────────────────┤
│  ┌─────────────────────────────────────┐    │
│  │         Application Layer           │    │
│  │    (Smart Contracts, dApps)         │    │
│  └─────────────────────────────────────┘    │
│                    ↓                        │
│  ┌─────────────────────────────────────┐    │
│  │            NeoVM Layer              │    │
│  │   • Execution Engine                │    │
│  │   • Instruction Processing          │    │
│  │   • Stack Management                │    │
│  └─────────────────────────────────────┘    │
│                    ↓                        │
│  ┌─────────────────────────────────────┐    │
│  │      Interoperability Layer         │    │
│  │   • Native Contracts                │    │
│  │   • System Calls                    │    │
│  │   • Storage Access                  │    │
│  └─────────────────────────────────────┘    │
│                    ↓                        │
│  ┌─────────────────────────────────────┐    │
│  │          Ledger Layer               │    │
│  │   • Block Storage                   │    │
│  │   • State Management                │    │
│  └─────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
```

## Supported Languages

Neo N3 smart contracts can be written in multiple languages, all compiled to NeoVM bytecode:

- **C#** - Primary language with full SDK support
- **Python** - Via neo3-boa compiler
- **Go** - Via NeoGo compiler
- **Java** - Via neow3j compiler
- **TypeScript** - Via Neo-ONE framework

## Next Steps

In the following sections, we'll explore:
- The detailed architecture of NeoVM
- The complete instruction set
- How GAS consumption is calculated
