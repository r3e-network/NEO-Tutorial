---
layout: post
lang: en
lang-ref: Implementation_of_NEP17
---

# Implementation of NEP-17 Token (Neo N3)

>
> **Objective**: Learn how to implement a NEP-17 token on Neo N3
>
> **Main points**:
>
> 1. Implementation according to the NEP-17 standard
>
> 2. Using neo-devpack-dotnet for Neo N3 smart contracts
>

## Neo N3 Contract Structure

In Neo N3, smart contracts no longer use a `Main` method with triggers. Instead, contracts are classes that inherit from `SmartContract` and expose public methods directly.

First, let's set up the basic contract structure:

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
        // Contract code here
    }
}
```

## Define Contract Owner

```csharp
[InitialValue("NiHURyS83nX2mpxtA7xq84cGxVbHojj5Wc", ContractParameterType.Hash160)]
static readonly UInt160 Owner = default;
```

Note: In Neo N3, we use `UInt160` type instead of `byte[]` for addresses.

## Token Properties

```csharp
public static string Symbol() => "MYT";

public static byte Decimals() => 8;
```

## Storage Keys

```csharp
private static readonly byte[] TotalSupplyKey = new byte[] { 0x00 };
private static readonly byte[] BalancePrefix = new byte[] { 0x01 };
```

## Transfer Event

```csharp
[DisplayName("Transfer")]
public static event Action<UInt160, UInt160, BigInteger> OnTransfer;
```

## TotalSupply Method

```csharp
public static BigInteger TotalSupply() => (BigInteger)Storage.Get(Storage.CurrentContext, TotalSupplyKey);
```

## BalanceOf Method

```csharp
public static BigInteger BalanceOf(UInt160 account)
{
    if (!account.IsValid)
        throw new Exception("Invalid account");
    return (BigInteger)Storage.Get(Storage.CurrentContext, BalancePrefix.Concat(account));
}
```

## Transfer Method (NEP-17)

The key difference from NEP-5 is the `data` parameter:

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

    // Update balances
    if (amount > 0)
    {
        UpdateBalance(from, -amount);
        UpdateBalance(to, amount);
    }

    // Fire Transfer event
    OnTransfer(from, to, amount);

    // Call onNEP17Payment if 'to' is a contract
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

## Deploy Method (Mint Initial Supply)

```csharp
public static void _deploy(object data, bool update)
{
    if (update) return;
    
    BigInteger totalSupply = 10_000_000_00000000; // 10 million with 8 decimals
    Storage.Put(Storage.CurrentContext, TotalSupplyKey, totalSupply);
    Storage.Put(Storage.CurrentContext, BalancePrefix.Concat(Owner), totalSupply);
    OnTransfer(null, Owner, totalSupply);
}
```

The `_deploy` method is automatically called when the contract is deployed.

## OnNEP17Payment (Receiver Callback)

If your contract needs to receive NEP-17 tokens:

```csharp
public static void OnNEP17Payment(UInt160 from, BigInteger amount, object data)
{
    // Handle incoming token payment
    // This is called automatically when tokens are sent to this contract
}
```

## Compiling and Deploying

1. Install neo-devpack-dotnet:
```bash
dotnet new install Neo.SmartContract.Template
dotnet new neo-contract -n MyToken
```

2. Compile:
```bash
dotnet build
```

3. Deploy using neo-cli or neon-js

## Next Step

Now you can extend this to create a [token sale](Give_an_ITO.md).

## Previous Step

Learn about [NEP-17 standard](What_is_nep5.md).
