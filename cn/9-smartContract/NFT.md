---
layout: post
lang: cn
lang-ref: NFT
---

## 什么是非同质通证 (NFT)?

非同质通证（NFT）可以被看作是一个财产契约——每个财产都是唯一的，并且携带一些不可更改的信息（例如，财产的物理地址），不过其他信息，例如财产的所有者，是可以更改的。NFT智能合约有助于追踪真实世界中物品的所有权，在网络游戏中也是如此，它允许用户拥有特有的角色或限量供应的道具，这些道具可以在用户之间转移，而无需获得游戏所有者的许可。

Neo N3的NFT标准是**NEP-11**。本文档提供了C#示例，展示了如何编写这样的智能合约。

> 注意：NEP-11仍然是一个草案提案。生产使用请参考最新的[NEP-11规范](https://github.com/neo-project/proposals/blob/master/nep-11.md)。

### NEP-11方法（草案）

#### name

```csharp
public static string Name() => "MyNFT";
```

返回通证的名称。每次调用此方法时，它都必须返回相同的值。

#### symbol

```csharp
public static string Symbol() => "MNFT";
```

返回此合约中管理的通证的短字符串符号。这个符号应该是简短的（推荐是3-8个字符）。

#### totalSupply

```csharp
public static BigInteger TotalSupply() => ...
```

返回系统中部署的通证的供应总量。

#### decimals

```csharp
public static byte Decimals() => 0;
```

返回通证使用的小数位数。对于NFT（不可分割），这应该返回`0`。

#### balanceOf

```csharp
public static BigInteger BalanceOf(UInt160 owner)
```

返回指定所有者账户的指定通证的余额。

参数`owner`必须是有效的`UInt160`地址。

#### ownerOf

```csharp
public static UInt160 OwnerOf(byte[] tokenId)
```

返回指定通证的所有者。

参数`tokenId`应该是有效的NFT token ID。

#### transfer

```csharp
public static bool Transfer(UInt160 from, UInt160 to, byte[] tokenId, object data)
```

将ID为`tokenId`的通证从地址`from`转到地址`to`。

该方法必须：
1. 检查`from`是否是通证的所有者
2. 使用`Runtime.CheckWitness(from)`验证调用者
3. 更新通证所有权
4. 触发`Transfer`事件

#### tokensOfOwner

```csharp
public static Iterator TokensOfOwner(UInt160 owner)
```

返回一个迭代器，包含指定地址拥有的所有通证。

### 事件

#### Transfer

```csharp
[DisplayName("Transfer")]
public static event Action<UInt160, UInt160, byte[]> OnTransfer;
```

必须在通证转账（包括零值转账）时触发。

- 铸造通证时：`from`为`null`
- 销毁通证时：`to`为`null`

### 示例合约结构

```csharp
using Neo.SmartContract.Framework;
using Neo.SmartContract.Framework.Services;
using System;
using System.Runtime.InteropServices;

public class MyNFT : SmartContract
{
    [DisplayName("Transfer")]
    public static event Action<UInt160, UInt160, byte[]> OnTransfer;

    private static StorageMap TokenOwner => 
        Storage.CurrentContext.CreateMap(nameof(TokenOwner));

    public static bool Transfer(UInt160 from, UInt160 to, byte[] tokenId, object data)
    {
        if (!from.IsValid || !to.IsValid)
            throw new Exception("Invalid address");
        if (tokenId == null || tokenId.Length == 0)
            throw new Exception("Invalid token ID");
        
        UInt160 owner = TokenOwner.Get(tokenId);
        if (!owner.IsValid)
            throw new Exception("Token does not exist");
        if (owner != from && !Runtime.CheckWitness(from))
            return false;

        TokenOwner.Put(tokenId, to);
        OnTransfer(from, to, tokenId);
        return true;
    }

    public static UInt160 OwnerOf(byte[] tokenId)
    {
        return TokenOwner.Get(tokenId);
    }

    public static BigInteger BalanceOf(UInt160 owner)
    {
        // 实现取决于存储结构
    }
}
```

## 下一步骤

- 探索[NEP-11规范](https://github.com/neo-project/proposals/blob/master/nep-11.md)获取最新详情
- 查看[Neo N3文档](https://docs.neo.org/docs/zh-cn/)了解原生合约支持

## 上一步

了解更多关于[NEP-17代币](What_is_nep5.md)。
