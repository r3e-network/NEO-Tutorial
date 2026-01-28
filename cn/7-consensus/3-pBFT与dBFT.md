## pBFT

> **注意**: 本章节已更新至 Neo N3 版本，重点介绍 dBFT 2.0。

有人认为，完全基于异步系统实现共识是不可能的，*M. Fischer, N. Lynch, and M. Paterson*于1985年在ACM期刊上发表的"具有单一故障过程的分布式共识的不可能性"一文提到。

从这个意义上说，我们必须依靠同步的基本概念来提供网络的活性。

有关pBFT状态图的概述可以查看下图。![Neo 规范](https://github.com/NeoResearch/yellowpaper/blob/master/sections/graphviz-images/graphviz-pbft.jpg?raw=true)

pBFT专为许可网络设计，是dBFT的理论基础。


## dBFT 2.0

**免责声明:** *本教程的部分内容摘自[dBFT正式规范](https://github.com/NeoResearch/yellowpaper/blob/master/sections/08_dBFT.md)。*

Neo N3 采用 **dBFT 2.0**，相比 dBFT 1.0 有重大改进：

### dBFT 2.0 vs dBFT 1.0 对比

| 特性 | dBFT 1.0 | dBFT 2.0 |
|------|----------|----------|
| **恢复机制** | 基础 | 增强的 Recovery 消息 |
| **视图更改** | 可能导致分叉 | 安全的视图更改 |
| **Commit 锁定** | 存在问题 | 已解决 |
| **网络稳定性** | 一般 | 显著提升 |

### dBFT 2.0 消息类型

```
ChangeView     = 0x00,  // 请求更改视图
PrepareRequest = 0x20,  // 议长发起的准备请求
PrepareResponse= 0x21,  // 备份节点的准备响应
Commit         = 0x30,  // 提交消息
RecoveryRequest= 0x40,  // 恢复请求
RecoveryMessage= 0x41   // 恢复消息
```

下图为当前dBFT 2.0的状态图

![这里](https://github.com/NeoResearch/yellowpaper/blob/master/sections/graphviz-images/graphviz-dbft-v2-recover.jpg?raw=true)

### 一区块终局性

一区块终局性为现实世界的应用程序带来了显著的优势。例如，终端用户，商家和交易所可以确保他们的交易已被最终处理，并且不可能被撤销。

**Neo N3 的终局性保证：**
- 区块一旦被确认，永不回滚
- 无需等待多个确认（对比比特币需要 6 个确认）
- 适合金融应用和 DeFi 场景

```csharp
// Neo N3 区块确认逻辑
public bool VerifyBlock(Block block, DataCache snapshot)
{
    // 验证见证人签名数量 >= M (2f+1)
    var validators = NativeContract.NEO.GetNextBlockValidators(snapshot, 
        ProtocolSettings.Default.ValidatorsCount);
    
    int m = validators.Length - (validators.Length - 1) / 3;
    
    // 验证多签
    return block.Witness.VerifyMultiSig(block.Hash, validators, m);
}
```

这个问题被称为**不知疲倦的矿工问题**（在此定义）：

1. 该议长是一名地质工程师，正在寻找一个可以挖掘氪石的地方;
1. 他提议了一个地理位置（待挖掘的地理坐标）;
1. 团队中的大多数成员(`M` 个人)对该坐标达成了共识（带有他们的签名）并签署了合约同意开始挖掘;
1. 挖掘的时间：他们会不停地挖掘，直到他们找到氪石（在发现氪石前不会去任何其他地方进行挖掘）。氪石是一种无限可分的晶体，因此，一旦有人挖掘到氪石，他就可共享以便所有人都能拥有一块氪石从而履行完他们的合约（3.）;
1. 如果有人死亡了，当有其他人加入时，他将看到先前签署的协议（3.），并自动开始挖掘。其他小部分人也会遇到相同的问题，可以通过隐藏的信息来告知他们也应该进行挖掘。

### dBFT 2.0 视图更改与恢复机制

为了保持活性，dBFT 2.0 引入了改进的视图更改和恢复机制：

**视图更改触发条件：**
- 议长超时未发送 PrepareRequest
- 收到无效的提案
- 网络分区恢复后状态不一致

**Recovery 消息机制（dBFT 2.0 新增）：**
```csharp
// 恢复消息包含当前共识状态
public class RecoveryMessage : ConsensusMessage
{
    public PrepareRequest PrepareRequestMessage;
    public Dictionary<int, byte[]> PreparationMessages;
    public Dictionary<int, byte[]> CommitMessages;
    public byte[] ViewChangeMessages;
}
```

 - 如果节点不相信当前的网络拓扑结构，则应阻止节点提交它们的签名（请求`更改视图`）。

然而，在 dBFT 2.0 中，Commit 阶段锁定问题已得到解决。当节点进入 Commit 阶段后，即使发生视图更改，也能通过 Recovery 消息恢复状态。

[点击此链接开始学习](4-dBFT共识示例与场景.md)或者[返回目录](README.md#目录)