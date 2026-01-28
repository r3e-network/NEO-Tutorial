# Gas Consumption

## Overview

Every NeoVM operation consumes GAS. This mechanism prevents infinite loops and ensures fair resource allocation.

## Base Costs

| Category | Cost (GAS) |
|----------|------------|
| Simple operations | 1/64000 |
| Arithmetic | 1/64000 |
| Stack operations | 1/64000 |
| Crypto operations | Variable |
| Storage operations | Variable |

## Storage Costs

| Operation | Cost |
|-----------|------|
| Storage.Get | 0.01 GAS |
| Storage.Put (new) | 0.1 GAS per byte |
| Storage.Put (update) | 0.01 GAS per byte |
| Storage.Delete | 0.01 GAS |

## Optimization Tips

1. **Minimize storage writes**
2. **Batch operations when possible**
3. **Use appropriate data types**
4. **Avoid unnecessary computations**
