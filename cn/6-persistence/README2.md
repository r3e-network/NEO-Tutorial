### LevelDB 区块链数据结构

> **注意**: 本章节已更新至 Neo N3 版本。Neo N3 相比 Neo Legacy 有重大架构变化，移除了 UTXO 模型，采用账户余额模型。

Neo N3 使用高效的键值数据库来持久化区块链数据。默认支持 LevelDB 和 RocksDB。数据库用于存储系统数据（区块、交易）以及智能合约的状态数据。

当节点接收到一条会触发状态改变的消息时（比如一个新的区块），它会检索并更新快照信息，并在操作结束后提交结果。

![snapshot](persistence_snapshot.png)

#### Neo N3 存储前缀

数据使用 [Ledger](https://github.com/neo-project/neo/tree/master/src/Neo/Ledger) 包中的类定义的结构进行存储。使用`前缀`来区分各个`表`。

Neo N3 中使用的存储前缀：

| 前缀 | 说明 | 键 | 值 |
|:-----|:-----|:---|:---|
| 0x05 | **当前区块** | 仅前缀 | HashIndexState |
| 0x09 | **区块** | 区块哈希 | TrimmedBlock |
| 0x0b | **交易** | 交易哈希 | TransactionState |
| 0x0c | **合约** | 合约哈希 | ContractState |
| 0x0e | **存储区** | 合约ID + 键 | StorageItem |
| 0x0f | **区块头哈希列表** | 索引 | HeaderHashList |

#### 原生合约存储

Neo N3 引入了原生合约（Native Contracts）的概念，系统功能通过原生合约实现：

| 原生合约 | 说明 | 合约哈希 |
|:---------|:-----|:---------|
| **ContractManagement** | 合约管理 | 0xfffdc93764dbaddd97c48f252a53ea4643faa3fd |
| **NeoToken** | NEO 代币 | 0xef4073a0f2b305a38ec4050e4d3d28bc40ea63f5 |
| **GasToken** | GAS 代币 | 0xd2a4cff31913016155e38e474a2c06d08be276cf |
| **PolicyContract** | 策略管理 | 0xcc5e4edd9f5f8dba8bb65734541df7a1c081c67b |
| **RoleManagement** | 角色管理 | 0x49cf4e5378ffcd4dec034fd98a174c5491e395e2 |
| **OracleContract** | 预言机 | 0xfe924b7cfe89ddd271abaf7210a80a7e11178758 |
| **LedgerContract** | 账本查询 | 0xda65b600f7124ce6c79950c1772a36403104f2be |


#### 内存池

内存池是内存中用于跟踪那些还没有提交/持久化交易的集合。在 Neo N3 中，内存池的管理更加高效。

![memory_pool_1](persistence_memory_pool_1.png)

```csharp
// Neo N3 内存池实现
public class MemoryPool : IReadOnlyCollection<Transaction>
{
    private readonly ConcurrentDictionary<UInt256, PoolItem> _unsortedTransactions = new();
    private readonly SortedSet<PoolItem> _sortedTransactions = new(PoolItemComparer);
    
    public bool TryAdd(Transaction tx, DataCache snapshot)
    {
        // 验证交易
        var context = new TransactionVerificationContext();
        var result = tx.VerifyStateDependent(snapshot, context);
        if (result != VerifyResult.Succeed) return false;
        
        // 添加到内存池
        var item = new PoolItem(tx);
        if (!_unsortedTransactions.TryAdd(tx.Hash, item)) return false;
        _sortedTransactions.Add(item);
        return true;
    }
}
```

#### 区块结构 (Neo N3)

Neo N3 的区块结构相比 Legacy 版本有所简化：

| 长度 | 字段 | 数据类型 | 说明 |
|------|------|----------|------|
| 4 | **Version** | uint32 | 区块版本号，当前为 0 |
| 32 | **PrevHash** | UInt256 | 前一个区块的哈希值 |
| 32 | **MerkleRoot** | UInt256 | 交易列表的默克尔根 |
| 8 | **Timestamp** | uint64 | 时间戳（毫秒） |
| 8 | **Nonce** | uint64 | 随机数 |
| 4 | **Index** | uint32 | 区块高度 |
| 1 | **PrimaryIndex** | byte | 议长索引 |
| 20 | **NextConsensus** | UInt160 | 下一轮共识节点的多签地址 |
| ? | **Witness** | Witness | 见证人（签名） |
| ?*? | **Transactions** | Transaction[] | 交易列表 |


#### 交易结构 (Neo N3)

Neo N3 移除了 UTXO 模型，采用更简洁的交易结构：

| 长度 | 字段 | 数据类型 | 说明 |
|------|------|----------|------|
| 1 | **Version** | byte | 交易版本，当前为 0 |
| 4 | **Nonce** | uint32 | 随机数，防止哈希冲突 |
| 8 | **SystemFee** | int64 | 系统费（执行费用） |
| 8 | **NetworkFee** | int64 | 网络费（打包优先级） |
| 4 | **ValidUntilBlock** | uint32 | 交易有效期 |
| ?*? | **Signers** | Signer[] | 签名者列表 |
| ?*? | **Attributes** | TransactionAttribute[] | 交易属性 |
| ? | **Script** | byte[] | 执行脚本 |
| ?*? | **Witnesses** | Witness[] | 见证人列表 |

```csharp
// Neo N3 交易验证
public VerifyResult VerifyStateDependent(DataCache snapshot, TransactionVerificationContext context)
{
    uint height = NativeContract.Ledger.CurrentIndex(snapshot);
    if (ValidUntilBlock <= height || ValidUntilBlock > height + MaxValidUntilBlockIncrement)
        return VerifyResult.Expired;
    
    UInt160[] hashes = GetScriptHashesForVerifying(snapshot);
    if (NativeContract.Policy.IsBlocked(snapshot, hashes))
        return VerifyResult.PolicyFail;
    
    BigInteger balance = NativeContract.GAS.BalanceOf(snapshot, Sender);
    BigInteger fee = SystemFee + NetworkFee;
    if (balance < fee) return VerifyResult.InsufficientFunds;
    
    return VerifyResult.Succeed;
}
```

