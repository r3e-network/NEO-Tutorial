---
layout: post
lang: en
lang-ref: Development_privateChain
---

# Neo N3 Private Network

>
> **Objective**: Set up a private network on the local computer for Neo N3 development
>
> **Main points**:
>
> 1. Using Neo N3 CLI (neo-cli) for private chain setup
> 2. How to use neo-gui or other wallets
> 3. Obtaining testnet assets
>


NEO blockchain has been running for several years, and every day a number of users are making transactions and using dApps on the MainNet. When you develop a smart contract, you need to deploy it to the blockchain and test it with invocation. Deploying smart contracts on the MainNet costs real GAS, which is not an economical option for developers. When developers want to test their smart contracts or dApps, the best choices are:

- **TestNet**: An environment where users can develop, commission, and test programs. Testing on the TestNet incurs TestNet GAS fees (not real GAS!!). TestNet NEO and GAS can be obtained free of charge from the official faucet.
- **Private Chain**: A local blockchain for development and testing, giving you full control over the network.

All transactions and blocks can be viewed on [Neo N3 TestNet Explorer](https://testnet.explorer.onegate.space/) or [Dora](https://dora.coz.io/).

Building a private chain using multiple nodes is a convenient and fast way for developers who want to learn how to develop smart contracts step by step. By using a private chain, developers don't have to worry about GAS costs, and deployment and testing on a local network is much faster.


## Setting Up a Private Chain

For Neo N3, you can set up a private chain using neo-cli. Here's how:

### Option 1: Using Pre-built Private Network

Download the pre-configured Neo N3 private network from the [Neo Documentation](https://docs.neo.org/docs/en-us/network/private-chain.html).

### Option 2: Setting Up from Scratch

#### 1. Download neo-cli

Download the latest neo-cli from the [Neo GitHub releases](https://github.com/neo-project/neo-node/releases).

#### 2. Create Configuration

Create a `config.json` file:

```json
{
  "ApplicationConfiguration": {
    "Paths": {
      "Chain": "Chain"
    },
    "P2P": {
      "Port": 20333,
      "WsPort": 20334
    },
    "RPC": {
      "Port": 20332,
      "SslCert": "",
      "SslCertPassword": ""
    },
    "UnlockWallet": {
      "Path": "wallet.json",
      "Password": "password",
      "IsActive": true
    }
  }
}
```

#### 3. Create Wallet

```bash
./neo-cli wallet create password
```

This creates a wallet with genesis NEO and GAS.

#### 4. Start the Node

```bash
./neo-cli
```

In the neo-cli console:
```
neo> start consensus
```

This will start consensus and generate blocks. The genesis NEO and GAS will be in the wallet.


## Using Wallets with Neo N3

### NeoLine Wallet (Recommended for Development)

[NeoLine](https://neoline.io/) is a popular browser extension wallet for Neo N3. It supports:
- Private key and seed phrase login
- dApp connections
- NEO, GAS, and NEP-17 token management

### Other Wallets

- **O3 Wallet**: Multi-chain wallet with Neo N3 support
- **OneGate**: Mobile wallet for Neo N3
- **Neo-cli**: Command-line wallet

### Connecting to TestNet

Most wallets support switching between MainNet and TestNet. For development, use TestNet to:
1. Get free test tokens from faucets
2. Test smart contracts without real GAS costs
3. Verify your contracts work correctly before MainNet deployment

 ## Next Step
**Great!** After setting up the private chain or TestNet, the next step is to [Set up the development tools](Development_set_up.md).

## Previous Step
If you are not familiar with the concept of smart contracts, click [here](What_is_smart_contract.md)
