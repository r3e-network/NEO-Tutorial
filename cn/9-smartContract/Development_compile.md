---
layout: post
lang: cn
lang-ref: Development_compile
---

# 编译和部署智能合约 (Neo N3)

>
> **目的**: 了解智能合约的编译、部署和调用流程
>
> **要点**:
>
> 1. 将智能合约编译为AVM
>
> 2. 使用neo-cli或SDK部署智能合约
>
> 3. 调用智能合约并获取结果

## 编译智能合约

让我们使用.NET CLI编译项目：

```bash
dotnet build
```

编译完成后，Neo N3智能合约文件`MyContract.avm`会生成在项目的`bin/Debug/netstandard2.1/`（或`bin/Release/netstandard2.1/`）目录中。

`.abi.json`文件是智能合约的描述文件，包含合约的ScriptHash、入口点、参数和返回值的信息。更多关于智能合约ABI的信息请参考[NeoContract ABI](https://github.com/neo-project/proposals/blob/master/nep-3.md)。

## 部署合约

### 方式一：使用neo-cli

1. 打开neo-cli并解锁钱包：
```
neo> open wallet wallet.json
neo> wallet password password
```

2. 部署合约：
```
neo> deploy MyContract.avm
```

### 方式二：使用neon-js（JavaScript SDK）

```javascript
const { Neon, api, wallet, tx } = require('@cityofzion/neon-js');
const fs = require('fs');

const privateKey = 'your-private-key-here';
const script = fs.readFileSync('./MyContract.avm');

const account = new wallet.Account(privateKey);
const client = new api.neo3.NeonRPC('https://testnet1.neo.coz.io:443');

async function deploy() {
  const txHash = await client.doInvoke({
    sign: account.scriptHash, scopes: 'ers: [{ accountCalledByEntry' }],
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
  
  console.log('部署交易:', txHash);
}

deploy();
```

### 方式三：使用Neo Express

对于本地开发，[Neo Express](https://github.com/neo-project/neo-express)提供了快速部署和测试合约的方式：

```bash
neo-express deploy MyContract.avm
neo-express invoke <script-hash> <method> [params]
```

## 调用合约

现在你可以调用刚部署的智能合约了。

### 使用neo-cli

1. 获取合约脚本散列（部署后显示）
2. 调用合约：
```
neo> invokefunction <script-hash> <method> [params]
```

示例 - 调用NEP-17代币的`balanceOf`方法：
```
neo> invokefunction 0x1234567890abcdef1234567890abcdef12345678 balanceOf NWuHQdxabXPdC6vVwJhxjYELDQPqc1d4TG
```

### 使用neon-js

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
  
  console.log('结果:', result);
}
```

## 下一步骤
**恭喜！** 你已经成功设置私有网络并调用了你的第一个智能合约。现在让我们开始学习[NEO智能合约的基础知识并创建你的第一个合约](Smart_Contract_basics.md)。

## 上一步
如果你还没有设置IDE，请先点击[这里](Development_set_up.md)。
