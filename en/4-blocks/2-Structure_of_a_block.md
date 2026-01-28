## Structure of a block

Below is the JSON dump of block #1000000 on the NEO N3 MainNet. It can be obtained using the following command:
```
curl -X POST https://mainnet1.neo.coz.io:443 -H 'Content-Type: application/json' -d '{"jsonrpc":"2.0","id":1,"method":"getblock","params":[1000000,1]}'
```

## Example block (Neo N3)
```json
{
  "hash": "0x7339b8a32e6ff7e8affbbb7a7be62d95f09c7a9426f2bea582d910f2228fded0",
  "size": 1014,
  "version": 0,
  "previousblockhash": "0xa1b416c14198261ab596996eb76ca5906b701b1a7ac48d53ba717e6f19a02a7f",
  "merkleroot": "0x60f556e19f9576bf633f849f26e549414bdbdfd6e125cb327b4a80dd5f1f5909",
  "time": 1643652240769,
  "nonce": "F6EB0BE2759EC31B",
  "index": 1000000,
  "primary": 1,
  "nextconsensus": "NSiVJYZej4XsxG5CUpdwn7VRQk8iiiDMPM",
  "witnesses": [
    {
      "invocation": "DECwVxETF8qrPmMlIv9DiEY00nPaxeM4wfRrSpT22LYzurc9CA3pe+ezCAtkhJAxGA/R65ILWTddWsJn5VLCtl+M...",
      "verification": "FQwhAjmjdDZlL0GzuALKRMvLfWXTqguIyaA4AkO9vhqqXLNbDCECSG/RVwLESQomcDESpcwdCSP9aXozQGvVocAO..."
    }
  ],
  "tx": [
    {
      "hash": "0x60f556e19f9576bf633f849f26e549414bdbdfd6e125cb327b4a80dd5f1f5909",
      "size": 317,
      "version": 0,
      "nonce": 1380947213,
      "sender": "NWuHQdxabXPdC6vVwJhxjYELDQPqc1d4TG",
      "sysfee": "16792785",
      "netfee": "130052",
      "validuntilblock": 1005758,
      "signers": [
        {
          "account": "0xb8a020fce295c9e36ab7ec3502c9ebbabf2d8878",
          "scopes": "Global"
        }
      ],
      "attributes": [],
      "script": "A+U1U7F+AQAADBQqTJpNQCJniwPvG74INPlmRg3ESAwU...",
      "witnesses": [
        {
          "invocation": "DECHJ7eC3Ay1ykPzz1a6CMqrsbQdAOBB7qyGocON+yJ1pt1p9EpCSBrBsMAJLnXEXnTOtUVgZoNHftefRlYNa7wX",
          "verification": "DCECQrIu3IhB/8EOac44LJu7HFUZm/uo8P6NCYnFAoFXywNBVuezJw=="
        }
      ]
    }
  ],
  "confirmations": 7764091,
  "nextblockhash": "0x499ed7cdef6a276035c6ee58ee40b595f7b99c5a7cd33b76c6d3b40352fbfcb1"
}
```

## Visual representation
The block can be inspected in a more user-friendly way by using a block explorer. [Dora](https://dora.coz.io/) is one such explorer for Neo N3, and the block above can be found at [this URL](https://dora.coz.io/block/neo3/mainnet/1000000). Another option is [OneGate Explorer](https://explorer.onegate.space/). The information and transactions included in this block are shown in the explorer interface. The witnesses (invocation and verification scripts) are discussed in detail in [Block Validation & Processing](4-Block_validation_processing.md).

# Block contents
## Block header
- ***hash***: The hash of the header of the block. The following fields are used when calculating the hash:
	* version
	* previousblockhash
	* merkleroot
	* time
	* nonce
	* index
	* primary
	* nextconsensus

- ***size***: The size of the block in bytes.

- ***version***: The block version number indicates which set of block validation rules to follow.

- ***previousblockhash***: The hash of the previous block, also known as the parent of the current block. The child block always refers to a single parent block. Referencing the previous block hash is an important part of the security of the network.

	Since the block will always reference the previous block by the hash of its header, any changes to any of the transactions inside the previous block would result in a new hash of the [Merkle root](2a-Merkle-Tree.md) of that previous block. Since the Merkle root hash is used in calculating the block header hash, changing any transaction would totally change the block header hash. This hash would then be totally different from what it was, thus changing what the next block is referring to as its parent block. This way any change can easily be detected, as it would effectively break the chain.

	NEO uses [dBFT](https://docs.neo.org/docs/n3/foundation/consensus/dbft.html), which results in a block being final as soon as it is committed to the blockchain. For a hacker to submit a malicious block, he would need to convince 2/3 of the consensus nodes to build the next block on top of his malicious blockchain.

- ***merkleroot***: The hash of the root of the Merkle Tree of the block's transactions.

- ***time***: The block time as a Unix timestamp in milliseconds. This represents the moment the block was created.

- ***index***: The height of the current block. The Genesis block has index 0.

- ***nonce***: A random number generated during consensus. In Neo N3, this can be used by smart contracts as a source of randomness for that block.

- ***primary***: The index of the primary consensus node (speaker) that proposed this block.

- ***nextconsensus***: The script hash of the consensus nodes for the next block, represented as an address.

- ***witnesses***: Array of witness objects used to validate the block. Each witness contains:
	* **invocation**: The invocation script containing signatures from consensus nodes
	* **verification**: The verification script (multi-signature script of consensus nodes)

## Block body

The body of a block contains all the transactions that are included in that block.

### Transaction Structure (Neo N3)

Neo N3 uses an **account-based model** (similar to Ethereum) rather than the UTXO model used in Neo Legacy. All transactions in Neo N3 follow a unified structure:

* **hash**: The transaction hash, uniquely identifying this transaction.
* **size**: Size of the transaction in bytes.
* **version**: Transaction format version.
* **nonce**: A random number to prevent hash collisions for identical transactions.
* **sender**: The address of the account paying the fees.
* **sysfee**: System fee paid for executing the transaction (in GAS fractions, 1 GAS = 10^8 fractions).
* **netfee**: Network fee paid for transaction size and signature verification.
* **validuntilblock**: The block height until which this transaction is valid. If not included in a block by this height, the transaction expires.
* **signers**: Array of accounts that sign this transaction, each with:
	* **account**: The script hash of the signing account
	* **scopes**: Permission scope for the signature (None, CalledByEntry, Global, CustomContracts, CustomGroups, WitnessRules)
* **attributes**: Optional transaction attributes for special purposes (like HighPriority, OracleResponse, NotValidBefore).
* **script**: The NeoVM script to be executed (e.g., smart contract invocation).
* **witnesses**: Array of witnesses proving authorization, each containing invocation and verification scripts.

## Additional fields

- ***confirmations***: The number of blocks built on top of this block. This field is calculated by the node serving the RPC request.

- ***nextblockhash***: The hash of the next block. This field is calculated by the node serving the RPC request.

[Next chapter](3-Block_creation_broadcasting.md) or [return to contents](README.md#contents).
