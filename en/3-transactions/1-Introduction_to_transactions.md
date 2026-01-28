## Introduction to transactions
A Neo transaction is a signed data package with an instruction for the network, for example a user indicating that they want to transfer assets to another address or invoke a smart contract. Each Neo block in the blockchain ledger contains one or more transactions, making each block a transaction batch. To use the Neo blockchain we need to understand how transactions work.

**Neo N3 uses a unified transaction format** - all operations are performed through smart contract invocations.

- **[Structure of transactions](2-Structure_of_NEO_transactions.md)**
  - [version](2-Structure_of_NEO_transactions.md#version)
  - [nonce](2-Structure_of_NEO_transactions.md#nonce)
  - [fees](2-Structure_of_NEO_transactions.md#fees)
  - [validUntilBlock](2-Structure_of_NEO_transactions.md#validuntilblock)
  - [signers](2-Structure_of_NEO_transactions.md#signers)
  - [attributes](2-Structure_of_NEO_transactions.md#attributes)
  - [script](2-Structure_of_NEO_transactions.md#script)
  - [witnesses](2-Structure_of_NEO_transactions.md#witnesses)

### Transaction Operations
In Neo N3, all operations are performed through smart contract invocations using a unified transaction format.

- **[Transaction operations](3-NEO_transaction_types.md)**
  - [Transferring NEO or GAS](3-NEO_transaction_types.md#transferring-neo-or-gas)
  - [Voting for Consensus Nodes](3-NEO_transaction_types.md#voting-for-consensus-nodes)
  - [Deploying Smart Contracts](3-NEO_transaction_types.md#deploying-smart-contracts)
  - [Native Contracts](3-NEO_transaction_types.md#native-contracts)

### Transaction fees
All transactions on the Neo N3 network require fees. The network uses a fee structure with two types of fees: system fees and network fees. All fees are paid in GAS.

- **[Transaction fees](4-NEO_transaction_fees.md)**
  - [System fees](4-NEO_transaction_fees.md#system-fee)
  - [Network fees](4-NEO_transaction_fees.md#network-fee)
  - [Fee estimation](4-NEO_transaction_fees.md#fee-estimation)

## Broadcasting
Once a transaction has been created it can be sent to a network peer node. If the peer node determines the transaction as being valid, it will be placed in the memory pool and distributed through the rest of the network. Eventually a consensus node (validators on the NEO blockchain) will receive the transaction and process it by including it in a block.

[Next chapter](2-Structure_of_NEO_transactions.md) or [return to contents](README.md#contents).
