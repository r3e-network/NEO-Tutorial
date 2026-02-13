
---
layout: post
lang: en
lang-ref: NFT
---

## What is a Non-Fungible Token (NFT)?

A non-fungible token (NFT) can be thought of like a property deed - each one is unique and carries some non-mutable information (e.g., the physical address of the property) although other information, such as the owner of the property can be changed. An NFT smart contract is useful to track ownership of real-world items, as well as in online gaming, allowing users to possess unique characters or items of a limited supply, that can be transferred between users without requiring the permission of the game owner.

The NFT standard for Neo N3 is **NEP-11**. This document provides an example in C# showing how such a smart contract might be written.

> Note: NEP-11 is still a draft proposal. For production use, refer to the latest [NEP-11 specification](https://github.com/neo-project/proposals/blob/master/nep-11.md).

### NEP-11 Methods (Draft)

#### name

```csharp
public static string Name() => "MyNFT";
```

Returns the name of the token. This method MUST always return the same value every time it is invoked.

#### symbol

```csharp
public static string Symbol() => "MNFT";
```

Returns a short string symbol of the token managed in this contract. This symbol SHOULD be short (3-8 characters is recommended).

#### totalSupply

```csharp
public static BigInteger TotalSupply() => ...
```

Returns the total token supply deployed in the system.

#### decimals

```csharp
public static byte Decimals() => 0;
```

Returns the number of decimals used by the token. For NFTs (indivisible), this should return `0`.

#### balanceOf

```csharp
public static BigInteger BalanceOf(UInt160 owner)
```

Returns the balance of the specified tokens for the specified owner's account.

The parameter `owner` MUST be a valid `UInt160` address.

#### ownerOf

```csharp
public static UInt160 OwnerOf(byte[] tokenId)
```

Returns the owner of the specified token.

The parameter `tokenId` SHOULD be a valid NFT token ID.

#### transfer

```csharp
public static bool Transfer(UInt160 from, UInt160 to, byte[] tokenId, object data)
```

Transfers token with id `tokenId` from address `from` to address `to`.

The method MUST:
1. Check if `from` is the owner of the token
2. Verify the caller using `Runtime.CheckWitness(from)`
3. Update the token ownership
4. Fire the `Transfer` event

#### tokensOfOwner

```csharp
public static Iterator TokensOfOwner(UInt160 owner)
```

Returns an iterator containing all the tokens owned by the specified address.

### Events

#### Transfer

```csharp
[DisplayName("Transfer")]
public static event Action<UInt160, UInt160, byte[]> OnTransfer;
```

MUST trigger when tokens are transferred, including zero value transfers.

- When minting tokens: `from` is `null`
- When burning tokens: `to` is `null`

### Example Contract Structure

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
        // Implementation depends on storage structure
    }
}
```

## Next Steps

- Explore [NEP-11 specification](https://github.com/neo-project/proposals/blob/master/nep-11.md) for the latest details
- Check [Neo N3 Documentation](https://docs.neo.org/docs/en-us/) for native contract support

## Previous Step

Learn about [NEP-17 Tokens](What_is_nep5.md).
