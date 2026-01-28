## Neo N3 Fundamentals

Neo is a public blockchain that offers smart contract functionality, allowing developers to build decentralized applications that can manage digital assets and identities. It is often compared to [Ethereum](https://www.ethereum.org/), the largest and most well known smart contract platform, however the two have many fundamental differences that set them apart.

### Dual Token Model

Although Neo can support an unlimited number of digital assets created by contracts, it has two assets that are native to the network itself; NEO and GAS.

NEO, referred to as the governance token, is used to elect consensus nodes via the use of a voting mechanism. NEO owners can be considered as the managers of the Neo network, responsible for selecting which candidates are best suited to participate in the creation and validation of blocks.

In return, NEO holders receive GAS, the second native asset on the Neo blockchain. GAS is the utility token, used to pay for operations on the network. This includes system fees, such as the cost of deploying a smart contract, and also network fees that are used to give priority to a transaction.

In Neo N3, both NEO and GAS are implemented as **Native Contracts** (NeoToken and GasToken), providing standardized NEP-17 compatible interfaces.

### Consensus and Transaction Finality

Unlike the majority of current blockchains that use variants of PoW (Proof-of-Work) or PoS (Proof-of-Stake) for their respective consensus mechanisms, Neo uses **dBFT 2.0** (delegated Byzantine Fault Tolerance), an enhanced version of the original dBFT consensus mechanism.

PoW- and PoS-based consensus mechanisms encourage a large number of participants to propose blocks to the network. Conflicts are resolved through the use of forks, with the longest chain considered to be the truthful chain. 

In these blockchains, transactions within blocks are finalized over time in a probabilistic manner through the use of confirmations. The more blocks have been added to the blockchain since the block containing a given transaction, the less likely that transaction will be nullified by a fork.

In dBFT 2.0, NEO owners vote to elect a set of consensus nodes; a delegated group responsible for producing blocks. Each block in Neo must be agreed on by a 2/3 majority of consensus nodes before it is committed to the blockchain.

**dBFT 2.0 improvements** include:
- Recovery mechanism for failed consensus rounds
- Improved view change protocol
- Better handling of network partitions
- One-block finality guarantee

As each potential block must receive full network consensus in this manner before being accepted, transactions in Neo have absolute finality as soon as they are confirmed in a single block. This prevents transactions from being reversed by preventing forks, allowing for immediate settlement of all transactions on the network.

### Contract Languages

Neo N3 primarily supports **C#** as the main smart contract development language through the [neo-devpack-dotnet](https://github.com/neo-project/neo-devpack-dotnet) SDK. This provides the most complete tooling and best integration with the Neo ecosystem.

Additional language support includes:
- **Python** via [neo3-boa](https://github.com/CityOfZion/neo3-boa)
- **Go** via [NeoGo](https://github.com/nspcc-dev/neo-go)
- **Java** via [neow3j](https://github.com/neow3j/neow3j)

Contracts in Neo are compiled to NeoVM bytecode before being deployed to the Neo blockchain. When called, these deployed contracts are interpreted and executed by the enhanced **NeoVM** (Neo Virtual Machine), which in N3 features improved opcodes and better performance.

[Next chapter](4-NEO_Tutorial.md) or [return to contents](README.md#contents).
