## Overview of Transaction Fees in Neo N3

All transactions on the Neo N3 network require fees. The network uses a fee structure with two types of fees: **System Fee** and **Network Fee**. All fees are paid in GAS.

| Type        | Description                                                    |
|-------------|----------------------------------------------------------------|
| System Fee  | Cost of executing the transaction script in NeoVM (burned)     |
| Network Fee | Fee for transaction processing and priority (paid to validators)|

**Key difference from Neo Legacy:** In Neo N3, there are no free transactions. Every transaction requires both system and network fees.

### System Fee

The system fee covers the cost of executing the transaction script in the NeoVM. It is calculated based on:
- Opcodes executed
- Syscalls invoked
- CPU and storage resources used

**System fees are burned** - they are removed from circulation, reducing the total GAS supply.

The system fee is calculated before transaction execution. If the actual execution cost exceeds the declared system fee, the transaction fails.

#### Common Operation Costs

| Operation | Approximate Cost |
|-----------|------------------|
| Simple NEP-17 transfer | ~0.0001 GAS |
| Contract deployment | ~10 GAS |
| Storage write (per byte) | ~0.001 GAS |
| Signature verification | ~0.001 GAS |

### Network Fee

The network fee covers:
1. **Transaction size** - cost per byte of the serialized transaction
2. **Signature verification** - cost of verifying witness scripts
3. **Priority** - higher fees result in faster inclusion in blocks

Network fees are **paid to consensus nodes** as a reward for processing transactions.

#### Network Fee Calculation

```
NetworkFee = SizeFee + VerificationFee

SizeFee = TransactionSize × FeePerByte
VerificationFee = Sum of verification costs for all witnesses
```

The `FeePerByte` is a network policy parameter (default: 0.00001 GAS).

#### Transaction Priority

Transactions in the memory pool are prioritized by `NetworkFee / Size` ratio. Higher ratios mean faster confirmation. During network congestion, increasing the network fee ensures your transaction is processed quickly.

## Fee Estimation

Most Neo N3 SDKs provide automatic fee calculation:

### Using neon-js
```javascript
// Automatic fee calculation
const result = await Neon.create.transaction({
  script: script,
  signers: [signer]
})
.withSystemFee()  // Auto-calculate system fee
.withNetworkFee() // Auto-calculate network fee
.sign(account)
.execute(rpcClient);
```

### Using RPC
```json
// invokefunction with "test" mode to estimate fees
{
  "jsonrpc": "2.0",
  "method": "invokefunction",
  "params": ["contractHash", "method", [], [signer]],
  "id": 1
}
```

## GAS Distribution

In Neo N3, GAS is automatically distributed to NEO holders. The distribution happens when:
- NEO is transferred
- A vote is cast or changed
- GAS is explicitly claimed via transfer

There is no need for manual GAS claiming like in Neo Legacy.

[Return to contents](README.md#contents).
