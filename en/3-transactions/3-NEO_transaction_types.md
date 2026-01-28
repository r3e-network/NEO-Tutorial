## Transaction Operations in Neo N3

**Neo N3 uses a unified transaction format** - there are no longer different transaction types like `ContractTransaction`, `ClaimTransaction`, `InvocationTransaction`, etc. All operations are performed through smart contract invocations using a single transaction structure.

This is a fundamental architectural change from Neo Legacy (Neo 2.x). In Neo N3:
- All asset transfers are smart contract calls
- NEO and GAS are Native Contracts (NeoToken, GasToken)
- Voting is done through the NeoToken contract
- GAS is automatically distributed (no manual claiming)

## Common Operations

### Transferring NEO or GAS

In Neo N3, transferring NEO or GAS is done by invoking the `transfer` method on the respective Native Contract:

```csharp
// NEO Token Contract Hash: 0xef4073a0f2b305a38ec4050e4d3d28bc40ea63f5
// GAS Token Contract Hash: 0xd2a4cff31913016155e38e474a2c06d08be276cf

// Transfer parameters:
// - from: sender's script hash (UInt160)
// - to: recipient's script hash (UInt160)  
// - amount: amount to transfer (BigInteger)
// - data: additional data (can be null)
```

Example transaction script for NEO transfer:
```json
{
  "script": "CwBkDBSTtgJScsqTnE8pBlXTU6u0pnLfhgwUk7YCUnLKk5xPKQZV01OrtKZy34YUwB8MCHRyYW5zZmVyDBT1Y+pAvCg9TQ4FxI6jBbPyoHNA70FifVtS"
}
```

### Voting for Consensus Nodes

Voting is done by invoking the `vote` method on the NeoToken contract:

```csharp
// Vote for a consensus node candidate
// Parameters:
// - account: voter's script hash (UInt160)
// - voteTo: candidate's public key (ECPoint) or null to cancel vote
```

### GAS Distribution

In Neo N3, **GAS is automatically distributed** to NEO holders. There is no need to manually claim GAS like in Neo Legacy. When you hold NEO, your claimable GAS accumulates and can be retrieved by calling `transfer` on the GasToken contract (even transferring 0 GAS to yourself will claim accumulated GAS).

### Deploying Smart Contracts

Contract deployment is done by invoking the `deploy` method on the ContractManagement native contract:

```csharp
// ContractManagement Contract Hash: 0xfffdc93764dbaddd97c48f252a53ea4643faa3fd

// Deploy parameters:
// - nefFile: compiled contract (byte[])
// - manifest: contract manifest (string)
// - data: deployment data (object)
```

## Native Contracts

Neo N3 introduces Native Contracts - built-in contracts that are part of the protocol:

| Contract | Hash | Description |
|----------|------|-------------|
| NeoToken | `0xef4073a0f2b305a38ec4050e4d3d28bc40ea63f5` | NEO governance token |
| GasToken | `0xd2a4cff31913016155e38e474a2c06d08be276cf` | GAS utility token |
| ContractManagement | `0xfffdc93764dbaddd97c48f252a53ea4643faa3fd` | Contract lifecycle |
| PolicyContract | `0xcc5e4edd9f5f8dba8bb65734541df7a1c081c67b` | Network policies |
| RoleManagement | `0x49cf4e5378ffcd4dec034fd98a174c5491e395e2` | Role designation |
| OracleContract | `0xfe924b7cfe89ddd271abaf7210a80a7e11178758` | Oracle services |
| LedgerContract | `0xda65b600f7124ce6c79950c1772a36403104f2be` | Blockchain data |
| CryptoLib | `0x726cb6e0cd8628a1350a611384688911ab75f51b` | Crypto functions |
| StdLib | `0xacce6fd80d44e1796aa0c2c625e9e4e0ce39efc0` | Standard library |

## NEP-17 Token Transfers

All fungible tokens in Neo N3 follow the NEP-17 standard. To transfer any NEP-17 token (including NEO and GAS), invoke the `transfer` method:

```csharp
public static bool Transfer(UInt160 from, UInt160 to, BigInteger amount, object data)
```

The `Transfer` event is emitted on successful transfers:
```csharp
public static event Transfer(UInt160 from, UInt160 to, BigInteger amount);
```

## Migration from Neo Legacy

If you're migrating from Neo Legacy (Neo 2.x), here's a summary of the changes:

| Neo Legacy | Neo N3 |
|------------|--------|
| `ContractTransaction` | Invoke NeoToken/GasToken `transfer` |
| `ClaimTransaction` | Automatic GAS distribution |
| `StateTransaction` | Invoke NeoToken `vote` method |
| `InvocationTransaction` | Standard transaction with script |
| `MinerTransaction` | Handled by consensus automatically |
| `RegisterTransaction` | Deploy NEP-17 contract |

## Building Transactions with SDKs

### Using neon-js (JavaScript)

```javascript
import Neon, { sc, wallet, tx, u } from "@cityofzion/neon-js";

// Create a NEO transfer transaction
const script = sc.createScript({
  scriptHash: "0xef4073a0f2b305a38ec4050e4d3d28bc40ea63f5", // NeoToken
  operation: "transfer",
  args: [
    sc.ContractParam.hash160(fromAddress),
    sc.ContractParam.hash160(toAddress),
    sc.ContractParam.integer(amount),
    sc.ContractParam.any(null)
  ]
});

const transaction = new tx.Transaction({
  signers: [{ account: fromScriptHash, scopes: "CalledByEntry" }],
  script: script,
  validUntilBlock: currentHeight + 100
});
```

[Next chapter](4-NEO_transaction_fees.md) or [return to contents](README.md#contents).
