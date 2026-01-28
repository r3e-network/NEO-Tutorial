## Validation of blocks
As with transactions, blocks are validated by every node on the network. The goal for this validation is that every block can independently be validated on any node, and is not depending on any external characteristics. For more information on transaction validations, have a look at [Chapter 3](../3-transaction).

## Witnesses (Invocation and Verification Scripts)
Every full node on the network receives the full NEO blockchain from its peers, and will independently validate every block it receives to ensure that the block received was not sent by a malicious or faulty node. This way, the nodes are not required to trust any other node, creating a secure and trustless system.

In Neo N3, both blocks and transactions use **witnesses** for validation. A witness consists of two parts:
- **Invocation Script**: Contains the signatures proving authorization
- **Verification Script**: Contains the logic to verify those signatures

For transactions, the witness proves that the sender has the right to spend from their account. For blocks, the witness proves that the consensus nodes agreed on this block.

## Block Witness Example

When we look at block #1,000,000 from the Neo N3 MainNet (introduced in [Part 2, Structure of a block](2-Structure_of_a_block.md)), we can identify the witness:

```json
"witnesses": [
  {
    "invocation": "DECwVxETF8qrPmMlIv9DiEY00nPaxeM4wfRrSpT22LYzurc9CA3pe+ezCAtkhJAxGA/R65ILWTddWsJn5VLCtl+MDEAq5VAJksSDKb+VK91ZByxZjP+hxG83Xp4xe1jVvuksimFpjzM/fV/O1fxqzcIWn5cBG4wyGTb8ZyB/DCuQJE5JDED7zm3/wd36cpFFAmP+sAQLuafRrENxRn3f0IMhQIa5vy0TLDR4X6LquSoBvfYFU5W0WZG0Vjr1+Ur9j4r/c3EyDEBrx1gt2Vfcyz2Jx78grfCklQKWVfV7i67935teMNlTGUxhdZF8tKjQA50zKaBhS5JGRDyAJq/vSqhuPfc0cM4nDEBrCrjPUHVMggzeWDJubudh/Dq6yfJnJI+a6jEkSwvpxwch7QwIAuTQPTy8PjSIRcI9iLKRuEhrvqHGtY1UTPPX",
    "verification": "FQwhAjmjdDZlL0GzuALKRMvLfWXTqguIyaA4AkO9vhqqXLNbDCECSG/RVwLESQomcDESpcwdCSP9aXozQGvVocAOABOwmnAMIQKq7DhHD2qtAELG6HfP2Ah9Jnaw9Rb93TYoAbm9OTY5ngwhA7IJ/U9TpxcOpERODLCmu2pTwr0BaSaYnPhfmw+6F6cMDCEDuNnVdx2PUTqghpucyNUJhkA7eMbaNokGOMPUalrc4EoMIQLKDidpe5wkj28W4IX9AGHib0TahbWO6DXBEMql7DulVAwhA9nosWvZsi0zRdbUzeMb4cPh0WFTLj0MzsuV7OLrWDNuF0Ge0Nw6"
  }
]
```

Note: In Neo N3, the witness data is Base64 encoded rather than hex encoded as in Neo Legacy.

## Opcodes
The OpCodes for NeoVM can be found [here](https://github.com/neo-project/neo-vm/blob/master/src/Neo.VM/OpCode.cs). When validating a block, these OpCodes tell the NeoVM how to proceed.

### Decoding the Verification Script

First, let's decode the Base64 verification script to hex:
```
1521023...
```

The verification script follows a pattern for multi-signature validation:

1. **PUSH opcodes** (0x0C-0x20): Push the required number of signatures
2. **PUSHDATA opcodes**: Push each public key (33 bytes each for compressed EC points)
3. **PUSH opcodes**: Push the total number of public keys
4. **CHECKMULTISIG** (0xAE): Verify that M of N signatures are valid

For the Neo N3 MainNet consensus, this is typically a 5-of-7 multisig, meaning 5 out of 7 consensus nodes must sign each block.

### Decoding the Invocation Script

The invocation script contains the actual signatures from the consensus nodes. Each signature is pushed onto the stack using PUSHDATA opcodes. For a 5-of-7 consensus, there will be 5 signatures (each 64 bytes for secp256r1 signatures).

## Interpretation

The goal of these scripts is to allow any node to validate that the block was actually created and agreed upon by the consensus nodes. The process works as follows:

1. **Consensus nodes sign the block**: Each participating consensus node signs the block header with their private key
2. **Signatures are collected**: The primary (speaker) node collects signatures from other consensus nodes
3. **Block is finalized**: Once 2/3+ signatures are collected (5 of 7), the block is complete
4. **Any node can verify**: Using the verification script, any node can confirm the signatures are valid

The verification script contains the public keys of all consensus nodes. The `CHECKMULTISIG` opcode verifies that the signatures in the invocation script match at least M of the N public keys.

A block is considered valid if:
- The required number of signatures (M) in the Invocation Script can be verified
- Using M out of N public keys provided in the Verification Script
- For Neo N3 MainNet: 5 out of 7 consensus node signatures

This mechanism ensures that no single node can create fraudulent blocks - consensus from the majority of validators is always required.

[Return to contents](README.md#contents).
