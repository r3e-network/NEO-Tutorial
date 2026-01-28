## Account Model in Neo N3

One of the main functions of a wallet is to facilitate the transfer of assets. **Neo N3 uses a pure account model** for all assets, including the native NEO and GAS tokens. This is a significant change from Neo Legacy (Neo 2.x), which used the UTXO model for NEO and GAS.

### What Changed from Neo Legacy

In Neo Legacy, NEO and GAS followed the UTXO (Unspent Transaction Output) model, similar to Bitcoin. Users had to manage UTXOs and handle "change" when sending assets. This added complexity to wallet implementations.

**Neo N3 simplified this** by adopting a pure account model for everything:
- NEO and GAS are now **Native Contracts** (NeoToken and GasToken)
- All tokens follow the **NEP-17** standard (replacing NEP-5)
- Balance tracking is straightforward - just a number associated with each address

### How the Account Model Works

The account model creates a global state for each account. Instead of having a set of UTXOs which must be combined for transactions, you simply have a balance associated with your account.

For example, if you have 10 NEO and want to send 4 NEO to someone:
- Your balance: 10 NEO → 6 NEO
- Recipient balance: 0 NEO → 4 NEO

No need to worry about combining UTXOs or handling change - the virtual machine handles the state changes automatically.

### NEP-17 Token Standard

NEP-17 is the token standard for Neo N3, replacing the NEP-5 standard from Neo Legacy. All fungible tokens on Neo N3, including the native NEO and GAS tokens, implement the NEP-17 interface.

The NEP-17 standard defines the following methods:
- `symbol()` - Returns the token symbol
- `decimals()` - Returns the number of decimals
- `totalSupply()` - Returns the total token supply
- `balanceOf(account)` - Returns the balance of an account
- `transfer(from, to, amount, data)` - Transfers tokens between accounts

Token transfers trigger the `Transfer` event, which wallets and explorers use to track token movements.

### Native Contracts

Neo N3 introduces **Native Contracts** - built-in contracts that are part of the Neo protocol itself. These include:

| Contract | Description |
|----------|-------------|
| NeoToken | The NEO governance token |
| GasToken | The GAS utility token |
| PolicyContract | Network policy settings |
| ContractManagement | Contract deployment/updates |
| RoleManagement | Designation of special roles |
| OracleContract | Oracle services |
| LedgerContract | Blockchain data access |

Native contracts provide standardized interfaces and are more efficient than regular smart contracts.

[Return to contents](README.md#contents).
