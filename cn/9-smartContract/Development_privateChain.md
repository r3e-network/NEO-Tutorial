---
layout: post
lang: cn
lang-ref: Development_privateChain
---

# Neo N3私有网络

>
> **目的**: 在本地计算机上设置私有网络
>
> **要点**:
>
> 1. 使用Neo N3 CLI (neo-cli) 设置私有链
>
> 2. 如何使用neo-gui或其他钱包
>
> 3. 获取测试网资产

NEO区块链已经运行多年，每天都有大量用户在主网上进行交易和使用dApps。当开发智能合约时，你需要将合约部署到区块链上并通过调用进行测试。在主网上部署智能合约需要花费真正的GAS，这对于开发人员来说并不是经济的选择。当开发人员想要测试智能合约或dApps时，最好的选择是：

- **测试网 (TestNet)**：用户可以开发、测试程序的环境。在测试网上测试会产生测试网GAS费用（不是真正的GAS！！）。测试网NEO和GAS可以从官方水龙头免费获取。
- **私有链**：用于开发和测试的本地区块链，让你完全控制网络。

所有交易和区块都可以在 [Neo N3测试网浏览器](https://testnet.explorer.onegate.space/) 或 [Dora](https://dora.coz.io/) 上查看。

使用多个节点构建私有链是一种更方便、更快速的方式，适合想要逐步学习智能合约开发的开发人员。通过使用私有链，开发人员不必担心GAS开销，而且在本地网络上部署和测试要快得多。

## 设置私有链

对于Neo N3，你可以使用neo-cli设置私有链。具体步骤如下：

### 方式一：使用预构建的私有网络

从 [Neo文档](https://docs.neo.org/docs/zh-cn/network/private-chain.html) 下载预配置的Neo N3私有网络。

### 方式二：从头开始设置

#### 1. 下载neo-cli

从 [Neo GitHub releases](https://github.com/neo-project/neo-node/releases) 下载最新的neo-cli。

#### 2. 创建配置文件

创建`config.json`文件：

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

#### 3. 创建钱包

```bash
./neo-cli wallet create password
```

这将创建一个包含创世NEO和GAS的钱包。

#### 4. 启动节点

```bash
./neo-cli
```

在neo-cli控制台中：
```
neo> start consensus
```

这将启动共识并生成区块。创世NEO和GAS将在钱包中。

## 使用Neo N3钱包

### NeoLine钱包（推荐用于开发）

[NeoLine](https://neoline.io/)是Neo N3的热门浏览器扩展钱包，支持：
- 私钥和助记词登录
- dApp连接
- NEO、GAS和NEP-17代币管理

### 其他钱包

- **O3 Wallet**：支持Neo N3的多链钱包
- **OneGate**：Neo N3移动端钱包
- **neo-cli**：命令行钱包

### 连接到测试网

大多数钱包支持在主网和测试网之间切换。用于开发时，使用测试网可以：
1. 从水龙头获取免费测试代币
2. 测试智能合约无需真正的GAS成本
3. 在主网部署前验证合约是否正常工作

## 下一步
**太好了！** 设置好私有链或测试网后，下一步是[设置开发工具](Development_set_up.md)。

## 上一步
如果你对智能合约的概念还不清楚，请点击[这里](What_is_smart_contract.md)
