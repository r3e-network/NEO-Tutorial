---
layout: post
lang: en
lang-ref: UTXO
---

# UTXO vs Account Model

>
> **Objective**:  Understand UTXO and Account models in Neo
>
> **Main points**:
>
> 1. UTXO model (Neo Legacy)
> 2. Account-based model (Neo N3)
>
> **Note:** Neo N3 uses the **account-based model** instead of UTXO for all assets including NEO and GAS.

## UTXO Model (Neo Legacy)

If you are familiar with blockchain or have used digital coins before, you may have heard of `UTXO`. UTXO stands for **Unspent Transaction Output**, which means an output of a blockchain transaction that has not been spent and can be used as an input in a new transaction.

When you use digital coin wallets, you see an account balance number. Actually, in a UTXO-based blockchain, the stored number is aggregated by the wallet application itself from the UTXOs. The concept of UTXO is very similar to a wallet in real life. Imagine you open your wallet, you see 100 dollars. You don't know where the 100 dollars came from - it might be payment from a customer for your website design last week, that's a UTXO from your customer to you. When you spend 10 dollars to buy a magazine, you get 90 dollars as change. The 10 dollars you spent becomes a UTXO to the magazine shop.

## Account Model (Neo N3)

**Neo N3 uses an account-based model** (similar to Ethereum), not UTXO.

In the account model:
- Each account has a balance stored directly
- No need to track unspent outputs
- Simpler for smart contract integration
- Better for parallel processing

| Feature | UTXO Model | Account Model |
|---------|------------|---------------|
| Assets | NEO, GAS (Legacy) | NEO, GAS, NEP-17 Tokens |
| Balance Calculation | Sum of unspent outputs | Direct balance read |
| Smart Contracts | Limited support | Full support |

## Neo N3 Native Contracts

In Neo N3, NEO and GAS are implemented as **Native Contracts** - they are built-in smart contracts that provide standardized NEP-17 compatible interfaces:

```csharp
// Native Contract addresses
NeoToken: 0xef4073a0f2b305a38ec4050e4d3ff28c31c1609e
GasToken: 0xd2a4cff31913016155e38e474a2c06e08e6c3a8b
```

You can transfer NEO and GAS like any other NEP-17 token:

```csharp
// Using Native Contract
Neo.Transfer(from, to, amount, data);
Gas.Transfer(from, to, amount, data);
```
