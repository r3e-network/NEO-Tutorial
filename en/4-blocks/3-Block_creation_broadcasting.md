## Block creation by Consensus Nodes
As discussed in [Part 1](1-Introduction_to_blocks_and_blockchain.md), NEO uses the dBFT mechanism to generate new blocks. In short, this means there are a selected amount of consensus nodes, elected by the network, which are required to reach a 2/3 majority agreement on any new potential block.

For each new block that needs to be generated, one of these nodes is elected as the speaker (primary). In the best case scenario, where we have no Byzantine nodes, the speaker node will propose a new block and distribute it to all other consensus nodes for agreement. When the speaker node receives enough signatures from other consensus nodes, the block is propagated to the network and final. For more details on the dBFT consensus mechanism, have a look at the [whitepaper](https://docs.neo.org/docs/n3/foundation/consensus/dbft.html).

## The new block
When a user wants to send a transaction, typically their wallet will create and sign the transaction and send it to either an RPC or P2P node. Both RPC and P2P nodes will relay valid transactions across the network, where they eventually reach one of the consensus nodes. More can be read in the section [5. Network](../5-network/).

Once the valid transaction has arrived at the consensus nodes, it is stored in the mempool. When creating a new block, transactions will be selected from this mempool to be included. In Neo N3, blocks are generated approximately every 15 seconds.

## Transaction fees in Neo N3

Neo N3 uses an **account-based model** with two types of fees:

### Network Fee (netfee)
The network fee compensates nodes for processing and relaying the transaction. It is calculated based on:
- **Transaction size**: Larger transactions require more bandwidth
- **Signature verification cost**: More complex verification scripts cost more

The speaker node receives all network fees from transactions included in the block it proposes. This incentivizes including transactions with higher fees.

### System Fee (sysfee)
The system fee covers the cost of executing the transaction's script on the NeoVM. It is calculated based on:
- **OpCode execution costs**: Each NeoVM instruction has a GAS cost
- **Syscall costs**: Interacting with the blockchain (storage, contracts) has specific costs
- **Native contract method costs**: Calling native contracts has defined fees

System fees are burned (destroyed) rather than paid to consensus nodes, which helps control GAS inflation.

### Fee calculation example
When sending a simple NEO or GAS transfer:
- Network fee: ~0.001 GAS (depends on signature type)
- System fee: ~0.001 GAS (for the transfer operation)

For smart contract deployments and complex operations, fees can be significantly higher. The complete fee structure is documented in the [official documentation](https://docs.neo.org/docs/n3/fees.html).

## Smart Contract Fees

- ***Smart Contract Deployment***: Deploying a contract costs a base fee plus additional fees based on the contract size. The current formula is approximately 10 GAS + (contract size in bytes × 0.001 GAS).

- ***Smart Contract Execution***: Each operation in a smart contract has an associated GAS cost. Simple operations cost fractions of GAS, while storage operations and cross-contract calls cost more. Developers should optimize their contracts to minimize execution costs.

## Block broadcasting
Once the consensus nodes agree on a new block according to the dBFT mechanism, they will broadcast the new block to the entire network. Because of the characteristics of the dBFT consensus mechanism, block finality is achieved immediately in 1 single block. This means that all clients can query the blockchain (any RPC or P2P node) immediately after a new block has been created, and be certain these transactions are final.

Unlike Proof of Work blockchains where you might wait for multiple confirmations, Neo N3 transactions are final as soon as they are included in a block.

[Next chapter](4-Block_validation_processing.md) or [return to contents](README.md#contents).
