---
layout: post
lang: cn
lang-ref: Implementation_of_NEP17
---

# 实现NEP-17代币 (Neo N3)

>
> **目的**:  学习如何在Neo N3上实现NEP-17代币
>
> **要点**:
>
> 1. 根据NEP-17标准实现每个要点
>
> 2. 使用neo-cli或SDK部署NEP-17通证

## Neo N3合约结构

在Neo N3中，智能合约不再使用带有触发器的`Main`方法。相反，合约是继承自`SmartContract`的类，直接暴露公共方法。

首先，让我们设置基本的合约结构：

```csharp
using Neo;
using Neo.SmartContract;
using Neo.SmartContract.Framework;
using Neo.SmartContract.Framework.Attributes;
using Neo.SmartContract.Framework.Native;
using Neo.SmartContract.Framework.Services;
using System;
using System.Numerics;

namespace MyToken
{
    [DisplayName("MyToken")]
    [ManifestExtra("Author", "Your Name")]
    [ManifestExtra("Description", "My NEP-17 Token")]
    [SupportedStandards("NEP-17")]
    [ContractPermission("*", "onNEP17Payment")]
    public class MyTokenContract : SmartContract
    {
        // 合约代码在这里
    }
}
```

## 定义合约所有者

```csharp
[InitialValue("NiHURyS83nX2mpxtA7xq84cGxVbHojj5Wc", ContractParameterType.Hash160)]
static readonly UInt160 Owner = default;
```

**注意：** 在Neo N3中，我们使用`UInt160`类型代替`byte[]`来表示地址。

## 代币属性

```csharp
public static string Symbol() => "MYT";

public static byte Decimals() => 8;
```

## 存储键

```csharp
private static readonly byte[] TotalSupplyKey = new byte[] { 0x00 };
private static readonly byte[] BalancePrefix = new byte[] { 0x01 };
```

## 转账事件

```csharp
[DisplayName("Transfer")]
public static event Action<UInt160, UInt160, BigInteger> OnTransfer;
```

## TotalSupply方法

```csharp
public static BigInteger TotalSupply() => (BigInteger)Storage.Get(Storage.CurrentContext, TotalSupplyKey);
```

## BalanceOf方法

```csharp
public static BigInteger BalanceOf(UInt160 account)
{
    if (!account.IsValid)
        throw new Exception("Invalid account");
    return (BigInteger)Storage.Get(Storage.CurrentContext, BalancePrefix.Concat(account));
}
```

## Transfer方法 (NEP-17)

与NEP-5的主要区别是`data`参数：

```csharp
public static bool Transfer(UInt160 from, UInt160 to, BigInteger amount, object data)
{
    if (!from.IsValid || !to.IsValid)
        throw new Exception("Invalid address");
    if (amount < 0)
        throw new Exception("Invalid amount");
    if (!Runtime.CheckWitness(from) && !from.Equals(Runtime.CallingScriptHash))
        return false;
    if (BalanceOf(from) < amount)
        return false;
    if (from == to)
        return true;

    // 更新余额
    if (amount > 0)
    {
        UpdateBalance(from, -amount);
        UpdateBalance(to, amount);
    }

    // 触发Transfer事件
    OnTransfer(from, to, amount);

    // 如果 'to' 是合约，调用 onNEP17Payment
    if (ContractManagement.GetContract(to) != null)
        Contract.Call(to, "onNEP17Payment", CallFlags.All, from, amount, data);

    return true;
}

private static void UpdateBalance(UInt160 account, BigInteger amount)
{
    var key = BalancePrefix.Concat(account);
    var balance = (BigInteger)Storage.Get(Storage.CurrentContext, key) + amount;
    if (balance <= 0)
        Storage.Delete(Storage.CurrentContext, key);
    else
        Storage.Put(Storage.CurrentContext, key, balance);
}
```

## 部署方法 (铸造初始供应量)

```csharp
public static void _deploy(object data, bool update)
{
    if (update) return;
    
    BigInteger totalSupply = 10_000_000_00000000; // 1000万代币，8位小数
    Storage.Put(Storage.CurrentContext, TotalSupplyKey, totalSupply);
    Storage.Put(Storage.CurrentContext, BalancePrefix.Concat(Owner), totalSupply);
    OnTransfer(null, Owner, totalSupply);
}
```

`_deploy`方法在合约部署时自动调用。

## OnNEP17Payment (接收者回调)

如果你的合约需要接收NEP-17代币：

```csharp
public static void OnNEP17Payment(UInt160 from, BigInteger amount, object data)
{
    // 处理接收到的代币
    // 当代币转入此合约时自动调用
}
```

## 编译和部署

1. 安装neo-devpack-dotnet：
```bash
dotnet new install Neo.SmartContract.Template
dotnet new neo-contract -n MyToken
```

2. 编译：
```bash
dotnet build
```

3. 使用neo-cli或neon-js部署

## 下一步骤

现在你可以扩展此功能来[发起代币销售](Give_an_ITO.md)。

## 上一步

了解更多关于[NEP-17标准](What_is_nep5.md)。
