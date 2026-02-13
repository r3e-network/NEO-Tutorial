# NEO Development FAQ

This document collects frequently asked questions and answers for NEO development.

## Table of Contents

- [Wallet](#wallet)
- [Transactions](#transactions)
- [Smart Contracts](#smart-contracts)
- [Network & Nodes](#network--nodes)

---

## Wallet

### Q1: Why do all NEO addresses start with the letter "A"?

**A:** NEO addresses use Base58Check encoding with a version prefix of `0x17`. After Base58 encoding, this prefix produces addresses starting with "A". This is a design choice by NEO to help users easily identify NEO addresses.

### Q2: What's the difference between a private key and WIF?

**A:** 
- **Private Key**: The raw 256-bit random number, typically represented as a 64-character hexadecimal string
- **WIF (Wallet Import Format)**: An encoded format of the private key with version prefix and checksum

WIF advantages:
1. More readable
2. Built-in error detection
3. Easy to import/export

### Q3: How to securely generate a private key?

**A:** 
```python
import os
# Use the operating system's cryptographically secure random number generator
private_key = os.urandom(32)
```

⚠️ **Warning**: Do not use regular random functions (like `random.random()`). You must use a cryptographically secure random source.

### Q4: What's the relationship between script hash and address?

**A:** 
```
Public Key → Verification Script → SHA256 → RIPEMD160 → Script Hash → Base58Check → Address
```

Script hash is 20 bytes of binary data, while address is its human-readable form. Smart contracts typically use script hashes.

### Q5: How to convert a private key to WIF format?

**A:**
```python
import hashlib
import base58

def private_key_to_wif(private_key: bytes) -> str:
    # Add version prefix 0x80
    extended = b'\x80' + private_key + b'\x01'
    # Double SHA256 for checksum
    checksum = hashlib.sha256(hashlib.sha256(extended).digest()).digest()[:4]
    # Base58 encode
    return base58.b58encode(extended + checksum).decode()

# Example
private_key = bytes.fromhex('your_64_char_hex_private_key')
wif = private_key_to_wif(private_key)
```

### Q6: How to validate if a NEO address is valid?

**A:**
```python
import base58
import hashlib

def is_valid_neo_address(address: str) -> bool:
    try:
        decoded = base58.b58decode(address)
        if len(decoded) != 25:
            return False
        # Verify version prefix
        if decoded[0] != 0x17:
            return False
        # Verify checksum
        checksum = hashlib.sha256(hashlib.sha256(decoded[:-4]).digest()).digest()[:4]
        return checksum == decoded[-4:]
    except:
        return False

# Example
print(is_valid_neo_address("AQVh2pG732YvtNaxEGkQUei3YA4cvo7d2i"))  # True
```

---

## Transactions

### Q7: What's the difference between UTXO model and Account model?

**A:**

| Feature | UTXO Model | Account Model |
|---------|------------|---------------|
| Assets Used | NEO, GAS (Neo Legacy) | NEP-17 Tokens, NEO, GAS (Neo N3) |
| Balance Calculation | Sum of unspent outputs | Direct balance read |
| Parallel Processing | Easier | Requires locking |
| Privacy | Better | Worse |

**Note:** Neo N3 uses an account-based model (similar to Ethereum), not UTXO.

### Q8: How are transaction fees calculated?

**A:** NEO transaction fees consist of two parts:
- **System Fee (sys_fee)**: GAS consumed by smart contract execution
- **Network Fee (net_fee)**: Fee related to transaction size

```
Total Fee = System Fee + Network Fee
```

### Q9: Why is my transaction not being confirmed?

**A:** Possible reasons:
1. Insufficient network fee
2. Invalid transaction format
3. Input UTXO already spent
4. Signature verification failed

Solution: Check transaction structure, ensure correct signature, and increase network fee if needed.

### Q10: How to query account balance via RPC?

**A:**
```python
import requests
import json

def get_balance(address: str, rpc_url: str = "https://testnet1.neo.coz.io:443") -> dict:
    payload = {
        "jsonrpc": "2.0",
        "method": "getnep17balances",
        "params": [address],
        "id": 1
    }
    response = requests.post(rpc_url, json=payload)
    return response.json()

# Example
balance = get_balance("NXV7ZhHiyM1aHXwpVsRZC6BwNFP2jghXAq")
print(json.dumps(balance, indent=2))
```

**Neo N3 RPC Ports:**
- TestNet: 20332 (REST: 80), e.g., `https://testnet1.neo.coz.io:443`
- MainNet: 10332 (REST: 80), e.g., `https://mainnet1.neo.coz.io:443`

---

## Smart Contracts

### Q11: What's the difference between NEP-5 and NEP-17?

**A:** NEP-17 is the token standard for Neo N3, replacing NEP-5 from Neo Legacy. Key differences:
- Uses `UInt160` type instead of `byte[]` for addresses
- Uses `onNEP17Payment` callback instead of checking `payable` flag
- Added `data` parameter to `transfer` method for contract interaction
- Uses `PascalCase` method naming instead of `camelCase`
- Uses `Action<T1, T2, T3>` for events with `DisplayName` attribute

### Q12: What to do if smart contract deployment fails?

**A:** Check the following:
1. Is the contract code compiled correctly?
2. Do you have enough GAS to pay deployment fees?
3. Does the contract size exceed the limit?
4. Are parameter types correct?

### Q13: How to debug smart contracts?

**A:** Recommended methods:
1. Use NEO private chain for testing
2. Use `Runtime.Log()` to output debug information
3. Use NEO debugger for step-by-step execution
4. Write unit tests

### Q14: How to store and read data in smart contracts?

**A:**
```csharp
// C# Smart Contract Example (Neo N3)
using Neo.SmartContract.Framework;
using Neo.SmartContract.Framework.Services;

public class StorageExample : SmartContract
{
    // Store data
    public static void PutData(string key, string value)
    {
        Storage.Put(Storage.CurrentContext, key, value);
    }
    
    // Read data
    public static string GetData(string key)
    {
        return Storage.Get(Storage.CurrentContext, key).TryParse();
    }
    
    // Delete data
    public static void DeleteData(string key)
    {
        Storage.Delete(Storage.CurrentContext, key);
    }
}
```

### Q15: How to trigger event notifications in smart contracts?

**A:**
```csharp
// Neo N3 Smart Contract Example
using Neo.SmartContract.Framework;

public class EventExample : SmartContract
{
    // Define event with Action<T1, T2, T3>
    [DisplayName("Transfer")]
    public static event Action<UInt160, UInt160, BigInteger> OnTransfer;
    
    public static bool DoTransfer(UInt160 from, UInt160 to, BigInteger amount)
    {
        // Business logic...
        
        // Trigger event
        OnTransfer(from, to, amount);
        return true;
    }
}
```

---

## Network & Nodes

### Q16: How to choose between MainNet, TestNet, and Private Chain?

**A:**
- **Private Chain**: Development and testing phase
- **TestNet**: Integration testing, simulating real environment
- **MainNet**: Production deployment

### Q17: How to set up a private chain?

**A:** Refer to [Private Chain Setup Guide](9-smartContract/Development_privateChain.md)

Basic steps:
1. Download neo-cli
2. Configure consensus nodes
3. Create wallets
4. Start nodes

### Q18: What to do if RPC calls fail?

**A:** Check:
1. Is the node running properly?
2. Is the RPC port open?
3. Is the request format correct?
4. Is the network connection working?

### Q19: How to get block information via RPC?

**A:**
```python
import requests

def get_block(index_or_hash, rpc_url="https://testnet1.neo.coz.io:443"):
    payload = {
        "jsonrpc": "2.0",
        "method": "getblock",
        "params": [index_or_hash, 1],  # 1 means return detailed info
        "id": 1
    }
    response = requests.post(rpc_url, json=payload)
    return response.json()

# Query by height
block = get_block(1000)
# Query by hash
block = get_block("0x...")
```

---

## More Resources

- [NEO Official Documentation](https://docs.neo.org/)
- [NEO GitHub](https://github.com/neo-project)
- [NEO Developer Community](https://discord.gg/neo)

---

*For more questions, feel free to submit an Issue or join community discussions.*
