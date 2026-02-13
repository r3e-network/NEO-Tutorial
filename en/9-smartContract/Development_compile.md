---
layout: post
lang: en
lang-ref: Development_compile
---

# Compile and Deploy the Smart Contract (Neo N3)

>
> **Objective**: Know the process of compiling, deploying, and invoking the smart contract
>
> **Main points**:
>
> 1. Compile the smart contract to AVM
>
> 2. Deploy the smart contract using neo-cli or SDK
>
> 3. Invoke the smart contract and get the result
>


## Compiling the Smart Contract

Let's compile the project using the .NET CLI:

```bash
dotnet build
```

When the compilation is done, the Neo N3 smart contract file `MyContract.avm` is generated in the `bin/Debug/netstandard2.1/` (or `bin/Release/netstandard2.1/`) directory of the project.

The `.abi.json` file is a descriptive file of the smart contract, which contains descriptions of the ScriptHash, entry, parameters, and return values of the contract. More information about the smart contract ABI can be found in [NeoContract ABI](https://github.com/neo-project/proposals/blob/master/nep-3.md).

## Deploying the Contract

### Option 1: Using neo-cli

1. Open neo-cli and unlock your wallet:
```
neo> open wallet wallet.json
neo> wallet password password
```

2. Deploy the contract:
```
neo> deploy MyContract.avm
```

### Option 2: Using neon-js (JavaScript SDK)

```javascript
const { Neon, api, wallet, tx } = require('@cityofzion/neon-js');
const fs = require('fs');

const privateKey = 'your-private-key-here';
const script = fs.readFileSync('./MyContract.avm');

const account = new wallet.Account(privateKey);
const client = new api.neo3. NeonRPC('https://testnet1.neo.coz.io:443');

async function deploy() {
  const txHash = await client.doInvoke({
    signers: [{ account: account.scriptHash, scopes: 'CalledByEntry' }],
    operations: [
      new tx.TransactionContractParameter({
        type: 'Hash',
        value: '0x0000000000000000000000000000000000000000'
      }),
      new tx.TransactionAttribute({
        type: 'Usage',
        data: 'Deploy'
      })
    ],
    script: script
  }, [account]);
  
  console.log('Deployment transaction:', txHash);
}

deploy();
```

### Option 3: Using neo-python

```python
from neo import Neo
from neo.Wallets import Wallet

# Deploy contract
wallet = Wallet('wallet.json')
wallet.open()

# Deploy using neo-cli API
# POST to /v1/contracts/deploy
```

## Invoking the Contract

Now you may invoke the smart contract you just deployed.

### Using neo-cli

1. Get the contract script hash (displayed after deployment)
2. Invoke the contract:
```
neo> invokefunction <script-hash> <method> [params]
```

Example - invoking a NEP-17 token's `balanceOf` method:
```
neo> invokefunction 0x1234567890abcdef1234567890abcdef12345678 balanceOf NWuHQdxabXPdC6vVwJhxjYELDQPqc1d4TG
```

### Using neon-js

```javascript
const { Neon, api, wallet } = require('@cityofzion/neon-js');

async function invoke() {
  const account = new wallet.Account('your-private-key');
  const client = new api.neo3.NeonRPC('https://testnet1.neo.coz.io:443');
  
  const result = await client.invokeFunction(
    '0xcontract-script-hash',
    'methodName',
    [
      { type: 'Hash160', value: account.scriptHash }
    ]
  );
  
  console.log('Result:', result);
}
```

### Using Neo Express

For local development, [Neo Express](https://github.com/neo-project/neo-express) provides a fast and easy way to deploy and test contracts:

```bash
neo-express deploy MyContract.avm
neo-express invoke <script-hash> <method> [params]
```

## Next Step
**Congratulations!**, you have set up your private network and invoked your first smart contract successfully. Now let's begin to learn [the basics of NEO smart contracts and create your first one.](Smart_Contract_basics.md)

## Previous Step
If you have not set up the IDE yet, you may first click [here](Development_set_up.md).
