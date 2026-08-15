---
subject: FOB
status: not-started
tags: [subject/fob, practical, unit/4]
practical: 9
unit: 4
hours: 2
---
# P09 — Case Study: Public vs Private Blockchains (Hyperledger Fabric)

**Subject:** Foundation of Blockchain | **Unit:** 4 | **Approx. Hrs:** 2
**PrO (verbatim):** *Case Study 1: To differentiate between Public and Private Blockchains by exploring Hyperledger Fabric concepts.*

---

## 1. Objective
- Compare **public (permissionless)** vs **private (permissioned)** blockchains.
- Understand **Hyperledger Fabric** architecture: Peers, Orderers, Channels, Chaincode.

## 2. Case Study — Public vs Private Blockchain

### 2.1 Side-by-side comparison (exam table)

| Feature | Public (e.g., Bitcoin, Ethereum) | Private / Permissioned (e.g., Hyperledger Fabric) |
|---|---|---|
| **Access** | Anyone can join, read, write, mine | Invited members only |
| **Identity** | Pseudonymous addresses | Known, certified identities (X.509) |
| **Consensus** | PoW / PoS (energy & token based) | Practical Byzantine Fault Tolerance (Raft, PBFT-like) |
| **Transaction speed** | Slow (Bitcoin ~7 tps; ETH ~15-30 tps) | Fast (thousands of tps) |
| **Scalability** | Low (replicated on all nodes) | High (channels isolate data) |
| **Finality** | Probabilistic (confirmation delays) | Immediate (deterministic) |
| **Data privacy** | All data visible to everyone | Channel-level privacy; only members see channel data |
| **Token needed?** | Yes (native currency/gas) | No token required |
| **Cost to use** | Gas fees | Membership + infrastructure |
| **Governance** | Open community / miners / stakers | Consortium / enterprise members |
| **Use cases** | Cryptocurrency, DeFi, public registries | Supply chain, banking, healthcare, govt records |

### 2.2 When to use which
- **Public:** open value transfer, censorship-resistant money, global DeFi, provable scarcity, NFTs.
- **Private:** regulated industries (banks, insurance, healthcare), companies that must know their counterparties and keep data confidential, high throughput + fast finality needs.

## 3. Hyperledger Fabric — Deep Dive

### 3.1 What is it?
- Open-source **permissioned** blockchain framework (Linux Foundation), founded 2015; now used by IBM and many enterprise consortia.
- Modules: **Hyperledger Fabric** (framework) + **Hyperledger Caliper** (benchmarking) + **Hyperledger Ursa** (crypto).

### 3.2 Core components
| Component | Role |
|---|---|
| **Peer** | Stores the ledger + state DB; executes **chaincode** in isolated containers; `endorsing peer` vs `committing peer`. |
| **Orderer** | Orders endorsed transactions into blocks and broadcasts them (consensus on **order**, not on state). |
| **Channel** | Private sub-network; only channel members receive/see that channel's ledger. |
| **Chaincode** | "Smart contracts" for Fabric, written in Go / Node.js / Java. |
| **MSP (Membership Service Provider)** | X.509 certificates issue & validate identities; defines who can act. |
| **World State DB** | Current state (LevelDB / CouchDB); chain provides history. |

### 3.3 Transaction flow (Fabric v2.x)
1. Client builds a transaction proposal → sends to **endorsing peers**.
2. Each endorsing peer runs the chaincode against its state, returns **endorsed read/write set** + signature.
3. Client collects enough endorsements → sends to **Orderer**.
4. Orderer batches, orders, and cuts **blocks** → broadcasts to peers on the channel.
5. Each peer **validates** (endorsement policy, read-set versioning) and commits to ledger.
> Note the difference from public chains: Fabric separates **endorse → order → validate**, and only the write-set result is committed (not the code re-run).

### 3.4 Endorsement policies
- E.g., `AND('Org1.member', 'Org2.member')` — a transaction is valid only if both orgs endorsed it. This enables business trust rules.

### 3.5 Fabric vs Ethereum (exam one-liner)
- **Ethereum:** open, tokenized, everyone runs all code, probabilistic consensus, data public.
- **Fabric:** permissioned, identity-based, endorsement policies + channels, deterministic finality, private data.

## 4. Hands-on (suggested, optional)
- Official test network (runs via Docker): `./network.sh up createChannel -c mychannel -s couchdb` then deploy the asset-transfer chaincode — https://hyperledger-fabric.readthedocs.io/en/latest/test_network.html
- Needs: Docker Desktop + ~4 GB RAM (student machine).

## 5. Expected Deliverable (report skeleton)
1. Title, aim, date.
2. Comparison table (2.1) with 4-6 rows explained in prose.
3. Fabric architecture diagram (label peers, orderers, channels).
4. One use case: *"Supply-chain provenance with Fabric"* — orgs, channel, chaincode functions, endorsement policy.
5. Conclusion: why an enterprise (e.g., a bank consortium) would pick Fabric over Ethereum.

## 6. Conclusion
Public chains trade privacy/throughput for openness; permissioned chains like Hyperledger Fabric trade openness for identity, privacy (channels), and enterprise speed. Fabric's endorse-order-validate pipeline and endorsement policies map directly onto real business trust requirements.

## 7. Viva Q&A
1. **What is a channel in Fabric?** — A private broadcast sub-network; its ledger is visible only to its members.
2. **What does the orderer do?** — Orders endorsed transactions into blocks (determines sequence).
3. **Why doesn't Fabric need a token?** — It uses identity (MSP) + endorsement policies instead of economic incentives.
4. **What is chaincode?** — Fabric's smart contracts (Go/Node/Java).
5. **PoW vs Fabric consensus?** — PoW = competitive mining; Fabric = Raft/PBFT ordering among known orderers.

## 8. Resources
- Hyperledger Fabric docs: https://hyperledger-fabric.readthedocs.io
- Test network tutorial: https://hyperledger-fabric.readthedocs.io/en/latest/test_network.html
- Fabric Architecture explained (IBM blog): https://www.ibm.com/blockchain/what-is-hyperledger-fabric
- *Hands-On Blockchain with Hyperledger* (Nitin Gaur, Packt 2018)

---



---

## 🐛 Failure Modes & Debugging (Real-World Experience)

> [!bug] What goes wrong in production?
> When running **Case Study Public Vs Private Hyperledger** in a real environment, it almost never works perfectly the first time. 
> 
> **Common Edge Cases to Test:**
> 1. **Network partitions:** What happens to this code if the Wi-Fi drops halfway through execution?
> 2. **Malformed Inputs:** How does the system behave if fed null values, extremely large datasets, or unexpected data types?
> 3. **Resource Exhaustion:** Does this script handle memory leaks or rate-limiting from APIs?

## 🔬 Extension Challenge

> [!example] Prove your expertise
> To truly master this practical, try modifying the code to achieve the following:
> - **Add robust error handling** (try/catch blocks) and structured logging instead of print statements.
> - **Parameterize the inputs** so the script can be run dynamically from the CLI without hardcoding values.
> - **Optimize it:** Can you reduce the execution time or memory footprint?

## 🎯 Key Takeaways

- **What is a channel in Fabric?** — A private broadcast sub-network; its ledger is visible only to its members.
- **What does the orderer do?** — Orders endorsed transactions into blocks (determines sequence).
- **Why doesn't Fabric need a token?** — It uses identity (MSP) + endorsement policies instead of economic incentives.
- **What is chaincode?** — Fabric's smart contracts (Go/Node/Java).
- **PoW vs Fabric consensus?** — PoW = competitive mining; Fabric = Raft/PBFT ordering among known orderers.

> [!tip] Viva Prep
> Be ready to explain the *why* behind each step, not just the output.
