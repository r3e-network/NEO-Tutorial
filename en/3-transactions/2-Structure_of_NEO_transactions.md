## Structure of transactions on Neo N3

A Neo transaction is a signed data package with an instruction for the network, for example a user indicating that they want to transfer assets to another address or invoke a smart contract. Each Neo block in the blockchain ledger contains one or more transactions, making each block a transaction batch.

**Neo N3 uses a unified transaction format** - there are no longer different transaction types like in Neo Legacy. All operations are performed through smart contract invocations, including native token transfers.

## Structure

In Neo N3, each transaction has the following structure:

| Field             | Type    | Description                                      |
|-------------------|---------|--------------------------------------------------|
| `version`         | uint8   | Transaction format version (currently 0)         |
| `nonce`           | uint32  | Random number to avoid hash collision            |
| `sysfee`          | int64   | System fee paid for execution (in GAS fractions) |
| `netfee`          | int64   | Network fee paid for transaction size/validation |
| `validUntilBlock` | uint32  | Transaction validity deadline (block height)     |
| `signers`         | array   | Array of signers with scopes                     |
| `attributes`      | array   | Additional transaction attributes                |
| `script`          | bytes   | NeoVM script to execute                          |
| `witnesses`       | array   | Scripts used to validate the transaction         |

For all transactions, the unique transaction hash `hash` (UInt256) and `size` parameters will be calculated.

Read more about the transaction fields:
- [version](#version)
- [nonce](#nonce)
- [fees](#fees)
- [validUntilBlock](#validuntilblock)
- [signers](#signers)
- [attributes](#attributes)
- [script](#script)
- [witnesses](#witnesses)

Example Neo N3 transaction:

```json
{
   "hash": "0x2b03f7a8db3649c9e2cb6d429dd358819b3fd536825f2053a4ab3028ec5c8b15",
   "size": 252,
   "version": 0,
   "nonce": 1234567890,
   "sender": "NikhQp1aAD1YFCiwknhM5LQQebj4464bCJ",
   "sysfee": "0.0100001",
   "netfee": "0.0124352",
   "validuntilblock": 5000,
   "signers": [
      {
         "account": "0x86df72a6b4ab5335d506294f9ce993722253b6e2",
         "scopes": "CalledByEntry"
      }
   ],
   "attributes": [],
   "script": "CwBkDBSTtgJScsqTnE8pBlXTU6u0pnLfhgwUk7YCUnLKk5xPKQZV01OrtKZy34YUwB8MCHRyYW5zZmVyDBT1Y+pAvCg9TQ4FxI6jBbPyoHNA70FifVtS",
   "witnesses": [
      {
         "invocation": "DEBhsuS9LxQ2PKpx2XJJ/aGEr8KToVvsqEHRYAHa3gTqKvP3xh+cHiu1XQXS9gYNYbBb+/9PcqTcwLQU4Iq5f5LB",
         "verification": "DCEDhb5FxABpGyfLhLAzDlPpKRjLqPi/qY1FzuEyNB4wfcBBVuezJw=="
      }
   ]
}
```

### Version
The version field indicates the transaction format version. Currently, only version `0` is supported in Neo N3.

### Nonce
The nonce is a random 32-bit number used to avoid transaction hash collisions. Two transactions with identical content but different nonces will have different hashes.

### Fees
Neo N3 has two types of fees:

**System Fee (`sysfee`)**: The cost of executing the transaction script in the NeoVM. This is calculated based on the opcodes and syscalls used. The fee is burned (removed from circulation).

**Network Fee (`netfee`)**: The fee paid for transaction processing, including:
- Transaction size (bytes)
- Signature verification cost
- Priority in the memory pool

Higher network fees result in faster transaction confirmation.

### ValidUntilBlock
The `validUntilBlock` field specifies the block height until which the transaction is valid. If the transaction is not included in a block before this height, it will be rejected. This prevents old transactions from being replayed.

### Signers
Signers define which accounts authorize the transaction and what permissions they grant. Each signer has:

| Field     | Type    | Description                              |
|-----------|---------|------------------------------------------|
| `account` | UInt160 | Script hash of the signing account       |
| `scopes`  | enum    | Permission scope for contract invocation |

**Witness Scopes** control what contracts can use the signer's signature:

| Scope              | Value | Description                                           |
|--------------------|-------|-------------------------------------------------------|
| `None`             | 0     | Only for fee payment, signature not usable by scripts |
| `CalledByEntry`    | 1     | Only the entry script can use the signature           |
| `CustomContracts`  | 16    | Only specified contracts can use the signature        |
| `CustomGroups`     | 32    | Only contracts in specified groups can use signature  |
| `Global`           | 128   | All contracts can use the signature (use with caution)|

Example:
```json
{
   "signers": [
      {
         "account": "0x86df72a6b4ab5335d506294f9ce993722253b6e2",
         "scopes": "CalledByEntry"
      }
   ]
}
```

### Attributes
Neo N3 supports a simplified set of transaction attributes:

| Type              | Description                                    |
|-------------------|------------------------------------------------|
| `HighPriority`    | Marks transaction as high priority (committee) |
| `OracleResponse`  | Contains oracle response data                  |
| `NotValidBefore`  | Transaction not valid before specified block   |
| `Conflicts`       | Marks conflicting transaction hashes           |

Most regular transactions do not require attributes.

### Script
The `script` field contains the NeoVM bytecode to execute. This is where the actual operation is defined - whether it's a token transfer, contract deployment, or any other blockchain operation.

For example, a NEP-17 token transfer script would invoke the `transfer` method on the token contract:

```
// Pseudocode for transfer script
PUSH data      // Additional data parameter
PUSH amount    // Amount to transfer  
PUSH to        // Recipient address
PUSH from      // Sender address
PUSH 4         // Number of parameters
PACK           // Pack into array
PUSH "transfer"
PUSH contractHash
SYSCALL System.Contract.Call
```

### Witnesses
Witnesses provide the cryptographic proof that the signers authorized the transaction. Each witness consists of:

| Field          | Description                                      |
|----------------|--------------------------------------------------|
| `invocation`   | Script containing signatures                     |
| `verification` | Script to verify the signatures (account script) |

Example:
```json
{
   "witnesses": [
      {
         "invocation": "DEBhsuS9LxQ2PKpx2XJJ/aGEr8KToVvsqEHRYAHa3gTqKvP3xh+cHiu1XQXS9gYNYbBb+/9PcqTcwLQU4Iq5f5LB",
         "verification": "DCEDhb5FxABpGyfLhLAzDlPpKRjLqPi/qY1FzuEyNB4wfcBBVuezJw=="
      }
   ]
}
```

#### Invocation Script
The invocation script pushes signatures onto the stack. For a single signature:
1. `PUSHDATA1` followed by the 64-byte signature

#### Verification Script  
The verification script validates signatures. For a standard account:
1. `PUSHDATA1` followed by the 33-byte compressed public key
2. `SYSCALL` with `System.Crypto.CheckSig` hash

For multi-signature accounts, the verification script includes multiple public keys and uses `System.Crypto.CheckMultisig`.

[Next chapter](3-NEO_transaction_types.md) or [return to contents](README.md#contents).
