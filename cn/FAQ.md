# NEO 开发常见问题解答 (FAQ)

本文档收集了NEO开发过程中的常见问题和解答。

## 目录

- [钱包相关](#钱包相关)
- [交易相关](#交易相关)
- [智能合约相关](#智能合约相关)
- [网络与节点](#网络与节点)

---

## 钱包相关

### Q1: NEO地址为什么都以字母"A"开头？

**A:** NEO地址使用Base58Check编码，版本前缀为`0x17`。经过Base58编码后，这个前缀会产生以"A"开头的地址。这是NEO的设计选择，便于用户识别NEO地址。

### Q2: 私钥和WIF有什么区别？

**A:** 
- **私钥**: 原始的256位随机数，通常以64字符的十六进制表示
- **WIF (Wallet Import Format)**: 私钥的编码格式，添加了版本前缀和校验和

WIF的优势：
1. 更易读
2. 内置错误检测
3. 便于导入导出

### Q3: 如何安全地生成私钥？

**A:** 
```python
import os
# 使用操作系统的加密安全随机数生成器
private_key = os.urandom(32)
```

⚠️ **注意**: 不要使用普通的随机函数（如`random.random()`），必须使用加密安全的随机源。

### Q4: 脚本哈希和地址的关系是什么？

**A:** 
```
公钥 → 验证脚本 → SHA256 → RIPEMD160 → 脚本哈希 → Base58Check → 地址
```

脚本哈希是20字节的二进制数据，地址是其可读形式。在智能合约中通常使用脚本哈希。

### Q5: 如何将私钥转换为WIF格式？

**A:**
```python
import hashlib
import base58

def private_key_to_wif(private_key: bytes) -> str:
    # 添加版本前缀 0x80
    extended = b'\x80' + private_key + b'\x01'
    # 双重SHA256计算校验和
    checksum = hashlib.sha256(hashlib.sha256(extended).digest()).digest()[:4]
    # Base58编码
    return base58.b58encode(extended + checksum).decode()

# 示例
private_key = bytes.fromhex('your_64_char_hex_private_key')
wif = private_key_to_wif(private_key)
```

### Q6: 如何验证NEO地址是否有效？

**A:**
```python
import base58
import hashlib

def is_valid_neo_address(address: str) -> bool:
    try:
        decoded = base58.b58decode(address)
        if len(decoded) != 25:
            return False
        # 验证版本前缀
        if decoded[0] != 0x17:
            return False
        # 验证校验和
        checksum = hashlib.sha256(hashlib.sha256(decoded[:-4]).digest()).digest()[:4]
        return checksum == decoded[-4:]
    except:
        return False

# 示例
print(is_valid_neo_address("AQVh2pG732YvtNaxEGkQUei3YA4cvo7d2i"))  # True
```

---

## 交易相关

### Q7: UTXO模型和账户模型有什么区别？

**A:**

| 特性 | UTXO模型 | 账户模型 |
|------|----------|----------|
| 使用资产 | NEO, GAS | NEP-5代币 |
| 余额计算 | 累加未花费输出 | 直接读取余额 |
| 并行处理 | 更容易 | 需要锁定 |
| 隐私性 | 较好 | 较差 |

### Q8: 交易费用如何计算？

**A:** NEO交易费用分为两部分：
- **系统费 (sys_fee)**: 执行智能合约消耗的GAS
- **网络费 (net_fee)**: 交易大小相关的费用

```
总费用 = 系统费 + 网络费
```

### Q9: 为什么我的交易一直未确认？

**A:** 可能原因：
1. 网络费不足
2. 交易格式错误
3. 输入的UTXO已被花费
4. 签名验证失败

解决方法：检查交易结构，确保签名正确，适当增加网络费。

### Q10: 如何通过RPC查询账户余额？

**A:**
```python
import requests
import json

def get_balance(address: str, rpc_url: str = "http://localhost:10332") -> dict:
    payload = {
        "jsonrpc": "2.0",
        "method": "getnep17balances",
        "params": [address],
        "id": 1
    }
    response = requests.post(rpc_url, json=payload)
    return response.json()

# 示例
balance = get_balance("NXV7ZhHiyM1aHXwpVsRZC6BwNFP2jghXAq")
print(json.dumps(balance, indent=2))
```

---

## 智能合约相关

### Q11: NEP-5和NEP-17有什么区别？

**A:** NEP-17是NEO 3.0的代币标准，相比NEP-5：
- 使用`onNEP17Payment`回调
- 支持更多功能
- 更好的安全性

### Q12: 智能合约部署失败怎么办？

**A:** 检查以下几点：
1. 合约代码是否正确编译
2. 是否有足够的GAS支付部署费用
3. 合约大小是否超过限制
4. 参数类型是否正确

### Q13: 如何调试智能合约？

**A:** 推荐方法：
1. 使用NEO私有链进行测试
2. 使用`Runtime.Log()`输出调试信息
3. 使用NEO调试器逐步执行
4. 编写单元测试

### Q14: 智能合约中如何存储和读取数据？

**A:**
```csharp
// C# 智能合约示例
using Neo.SmartContract.Framework;
using Neo.SmartContract.Framework.Services;

public class StorageExample : SmartContract
{
    // 存储数据
    public static void Put(string key, string value)
    {
        Storage.Put(Storage.CurrentContext, key, value);
    }
    
    // 读取数据
    public static string Get(string key)
    {
        return Storage.Get(Storage.CurrentContext, key);
    }
    
    // 删除数据
    public static void Delete(string key)
    {
        Storage.Delete(Storage.CurrentContext, key);
    }
}
```

### Q15: 如何在智能合约中触发事件通知？

**A:**
```csharp
using Neo.SmartContract.Framework;

public class EventExample : SmartContract
{
    // 定义事件
    public static event Action<byte[], byte[], BigInteger> Transfer;
    
    public static bool DoTransfer(byte[] from, byte[] to, BigInteger amount)
    {
        // 业务逻辑...
        
        // 触发事件
        Transfer(from, to, amount);
        return true;
    }
}
```

---

## 网络与节点

### Q16: 主网、测试网、私有链如何选择？

**A:**
- **私有链**: 开发和测试阶段
- **测试网**: 集成测试，模拟真实环境
- **主网**: 正式部署

### Q17: 如何搭建私有链？

**A:** 参考 [私有链搭建指南](9-smartContract/Development_privateChain.md)

基本步骤：
1. 下载neo-cli
2. 配置共识节点
3. 创建钱包
4. 启动节点

### Q18: RPC接口调用失败怎么办？

**A:** 检查：
1. 节点是否正常运行
2. RPC端口是否开放
3. 请求格式是否正确
4. 网络连接是否正常

### Q19: 如何通过RPC获取区块信息？

**A:**
```python
import requests

def get_block(index_or_hash, rpc_url="http://localhost:10332"):
    payload = {
        "jsonrpc": "2.0",
        "method": "getblock",
        "params": [index_or_hash, 1],  # 1表示返回详细信息
        "id": 1
    }
    response = requests.post(rpc_url, json=payload)
    return response.json()

# 按高度查询
block = get_block(1000)
# 按哈希查询
block = get_block("0x...")
```

---

## 更多资源

- [NEO官方文档](https://docs.neo.org/)
- [NEO GitHub](https://github.com/neo-project)
- [NEO开发者社区](https://discord.gg/neo)

---

*如有更多问题，欢迎提交Issue或参与社区讨论。*
