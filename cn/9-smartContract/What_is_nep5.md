---
layout: post
lang: cn
lang-ref: What_is_nEP17
---

# NEP-17代币标准 (Neo N3)

>
> **目的**:  学习NEP-17的基本概念
>
> **要点:**
>
> 1. 什么是NEP (NEO增强提案)
>
> 2. NEP-17的细节 (取代Neo Legacy中的NEP-5)

## 什么是NEP?
NEP代表NEO增强提案。NEP是一种设计文档，用于向NEO社区提供信息，或者描述NEO/流程/环境的新特性。NEP应该提供该特性的简明的技术规范和基本原理。你可以在这个 [GitHub存储库](https://github.com/neo-project/proposals) 中找到所有的NEP。

## NEP-17介绍

**NEP-17是Neo N3的代币标准**，取代了Neo Legacy中的NEP-5。它代表了Neo N3区块链上发行的可替代代币的代币化智能合约标准。

与NEP-5的主要区别：
- 添加了 `data` 参数到 `transfer` 方法，用于合约交互
- 使用 `onNEP17Payment` 回调来接收代币
- 使用 `UInt160` 类型代替 `byte[]` 表示地址
- 不再需要检查 `payable` 标志

### 方法

#### symbol

```csharp
public static string Symbol() => "MYT";
```

返回代币的短字符串符号。例如，`"MYT"`。这个符号应该是简短的 (推荐是3-8个字符)。

#### decimals

```csharp
public static byte Decimals() => 8;
```

返回代币使用的小数位数——例如，`8`，表示将代币数量除以`100,000,000`，从而得到它的用户表示。

#### totalSupply

```csharp
public static BigInteger TotalSupply() => TotalSupplyStorage.Get();
```

返回系统中部署的代币的供应总量。

#### balanceOf

```csharp
public static BigInteger BalanceOf(UInt160 account)
```

返回`account`的代币余额。

参数 `account` 必须是20字节长的地址（UInt160类型）。如果不是，这个方法应该`抛出`异常。

#### transfer

```csharp
public static bool Transfer(UInt160 from, UInt160 to, BigInteger amount, object data)
```

从`from`账户转数量为`amount`的代币至`to`账户。

**与NEP-5的主要区别：**
- 添加了 `data` 参数 - 传递给 `onNEP17Payment` 如果 `to` 是合约
- 使用 `UInt160` 类型代替 `byte[]`

该方法必须：
1. 如果 `from` 账户余额不足，返回 `false`
2. 成功时触发 `Transfer` 事件
3. 如果 `to` 是已部署的合约，调用其 `onNEP17Payment` 方法

### 事件

#### Transfer

```csharp
[DisplayName("Transfer")]
public static event Action<UInt160, UInt160, BigInteger> Transfer;
```

必须在代币转账(包括零值转账)时触发。

- 铸造代币时：`from` 为 `null`
- 销毁代币时：`to` 为 `null`

### 接收者接口

希望接收NEP-17代币的合约必须实现：

```csharp
public static void OnNEP17Payment(UInt160 from, BigInteger amount, object data)
```

当代币转入该合约时，此方法会自动被调用。

## NEP-17 vs NEP-5 对比

| 特性 | NEP-5 (Legacy) | NEP-17 (N3) |
|------|----------------|--------------|
| 地址类型 | `byte[]` | `UInt160` |
| Transfer参数 | `from, to, amount` | `from, to, amount, data` |
| 接收回调 | 检查 `payable` 标志 | `onNEP17Payment` |
| 方法命名 | `camelCase` | `PascalCase` |

## 下一步骤
现在让我们[实现一个NEP-17代币!](Implementation_of_NEP5.md)

## 上一步
如果你想了解智能合约的知识要点，请点击[这里](Smart_Contract_basics.md)。
