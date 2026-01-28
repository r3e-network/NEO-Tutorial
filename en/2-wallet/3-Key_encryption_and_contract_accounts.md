## Private key encryption (NEP-2) and Wallet files (NEP-6)
Storing raw private keys on disk is a security liability. Anyone that that has access to a raw private key can drain these funds. It would be more secure if these keys were encrypted via a password. For this reason we have the NEP-2 standard format (https://github.com/neo-project/proposals/blob/master/nep-2.mediawiki)

This encrypted key provides an additional layer of security to the raw private key, requiring an attacker to acquire both the encrypted key and the password in order to access the funds. This is good, but it is often the case that one might need to have multiple accounts, which means that they have multiple keys. Storing each NEP-2 encrypted key would be very cumbersome, so instead we can create a file structure that would allow for all of these encrypted keys to be stored in the same place.

The NEP-6 wallet standard allows for a standardized way of importing addresses into various blockchain clients and contains the additional security guarantees of the NEP-2 format.

A full specification of the file format can be found here. (https://github.com/neo-project/proposals/blob/master/nep-6.mediawiki). It follows a JSON structure that contains information about the private/public key pairs, as well as metadata about each account. The metadata details contains information such as which wallet should be used as the default, the encryption parameters, and any other relevant metadata. 

The NEP-6 file also supports watch-only addresses. Watch-only addresses do not contain any information related to the private key, which maybe useful if the account is stored separately in a more secure location.

## Contract Accounts & Multi-signatures
NEO also supports more sophisticated account types. In these cases, the funds are not associated with a single user but stored in a smart contract. The contract would include special rules which define what is required in order for funds to to be withdrawn from the account. 

The most common case for this type of account is a multi-signature account. A multi-signature account requires that *N* of *X* people provides signatures for the transaction in order to transfer funds. For example, 2 out of 3 of the account owners must sign in order for the funds to be withdrawn.

We can generate a simple contract for this account using Neo opcodes. Suppose we want to create a multi-signature contract account for THREE different persons (public keys):

**Important: Public keys must be sorted by their ECPoint(X,Y) in ascending order before creating the script, otherwise you will get a different script hash which leads to a different Neo address.**

```
//pubkey1
036245f426b4522e8a2901be6ccc1f71e37dc376726cc6665d80c5997e240568fb

//pubkey2
0303897394935bb5418b1c1c4cf35513e276c6bd313ddd1330f113ec3dc34fbd0d

//pubkey3
02e2baf21e36df2007189d05b9e682f4192a101dcdf07eed7d6313625a930874b4
```

We want to require at least TWO of them to sign the transactions. In Neo N3, the multi-signature verification script format uses the SYSCALL opcode:

```
// Push minimum signatures required (2)
PUSH 2

// Push all public keys (using PUSHDATA1)
PUSHDATA1 <pubkey1>
PUSHDATA1 <pubkey2>
PUSHDATA1 <pubkey3>

// Push total number of public keys (3)
PUSH 3

// SYSCALL System.Crypto.CheckMultisig
SYSCALL 0x9ED0DC3A
```

We then calculate the script hash and address of this account. In Neo N3, the resulting address will start with 'N' (using version byte 0x35).

This contract information can also be stored in the NEP-6 file, which allows a user to keep track of accounts that are not necessarily associated with a single private key. More complex account types can be created using NEO's scripting capabilities. 

Multi-signatures are supported in Neo N3 through various tools including [Neo-GUI](https://github.com/neo-project/neo-gui), [neon-js](https://github.com/CityOfZion/neon-js), and [neo-go](https://github.com/nspcc-dev/neo-go).

### Wallet File Formats

Neo N3 continues to use the **NEP-6** wallet format as the standard. The legacy DB3 format from Neo 2.x is no longer supported in Neo N3 tools.

For more information on Neo N3 wallet management, see the official documentation:
https://docs.neo.org/docs/n3/node/cli/cli.html

[Next chapter](4-UTXO_and_account_models.md) or [return to contents](README.md#contents).
