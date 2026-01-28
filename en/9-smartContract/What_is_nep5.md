---
layout: post
lang: en
lang-ref: What_is_nep17
---

#  NEP-17 Token Standard (Neo N3)

>
> **Objective**:  Learn the general idea of NEP-17
>
> **Main points**:
>
> 1. What is NEP (NEO Enhancement Proposals)
>
> 2. The detail of NEP-17 (replacing NEP-5 from Neo Legacy)
>

## What is NEP?
NEP stands for NEO Enhancement Proposal. An NEP is a design document providing information to the Neo community, or describing a new feature for Neo or its processes or environment. The NEP should provide a concise technical specification of the feature and a rationale for the feature. You can find all NEPs in the [GitHub repository](https://github.com/neo-project/proposals).

## Introduction to NEP-17

**NEP-17 is the token standard for Neo N3**, replacing NEP-5 from Neo Legacy. It represents a tokenized smart contract standard that regulates fungible tokens issued on the Neo N3 blockchain.

Key differences from NEP-5:
- Added `data` parameter to `transfer` method for contract interaction
- `onNEP17Payment` callback for receiving contracts
- Uses `UInt160` type instead of `byte[]` for addresses
- No more `payable` flag checking

### Methods

#### symbol

```csharp
public static string Symbol() => "MYT";
```

Returns a short string symbol of the token. e.g. `"MYT"`. This symbol SHOULD be short (3-8 characters is recommended).

#### decimals

```csharp
public static byte Decimals() => 8;
```

Returns the number of decimals used by the token - e.g. `8`, means to divide the token amount by `100,000,000` to get its user representation.

#### totalSupply

```csharp
public static BigInteger TotalSupply() => TotalSupplyStorage.Get();
```

Returns the total token supply deployed in the system.

#### balanceOf

```csharp
public static BigInteger BalanceOf(UInt160 account)
```

Returns the token balance of the `account`.

The parameter `account` MUST be a 20-byte address. If not, this method SHOULD `throw` an exception.

#### transfer

```csharp
public static bool Transfer(UInt160 from, UInt160 to, BigInteger amount, object data)
```

Transfers an `amount` of tokens from the `from` account to the `to` account.

**Key differences from NEP-5:**
- Added `data` parameter - passed to `onNEP17Payment` if `to` is a contract
- Uses `UInt160` type instead of `byte[]`

The function MUST:
1. Return `false` if the `from` account balance does not have enough tokens
2. Fire the `Transfer` event on success
3. Call `onNEP17Payment` on the `to` contract if it's a deployed contract

### Events

#### Transfer

```csharp
public static event Action<UInt160, UInt160, BigInteger> Transfer;
```

MUST trigger when tokens are transferred, including zero value transfers.

- When minting tokens: `from` is `null`
- When burning tokens: `to` is `null`

### Receiver Interface

Contracts that want to receive NEP-17 tokens MUST implement:

```csharp
public static void OnNEP17Payment(UInt160 from, BigInteger amount, object data)
```

This method is called automatically when tokens are transferred to the contract.

## NEP-17 vs NEP-5 Comparison

| Feature | NEP-5 (Legacy) | NEP-17 (N3) |
|---------|----------------|-------------|
| Address type | `byte[]` | `UInt160` |
| Transfer params | `from, to, amount` | `from, to, amount, data` |
| Receiver callback | Check `payable` flag | `onNEP17Payment` |
| Method naming | `camelCase` | `PascalCase` |

## Next Step
Now let us [implement a NEP-17 Token!](Implementation_of_NEP5.md)

## Previous Step
If you want to learn the knowledge points of smart contract, click [here](Smart_Contract_basics.md).
