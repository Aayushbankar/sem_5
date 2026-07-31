# UNIT 5 — Security, Emerging Trends & Green Energy 🔐🌱

**Syllabus weightage:** 8 hrs / 15% | **Related practicals:** [P08](../practicals/writeups/P08_erc20_token.md), [P10](../practicals/writeups/P10_case_study_security_green_energy_dao.md)
**Star guide:** ⭐ = likely · ⭐⭐ = very likely · ⭐⭐⭐ = practically guaranteed in some form

---

## 🧭 Chapter Roadmap

```
UNIT 5: Security, Emerging Trends & Green Energy
├── 5.1 Blockchain Security & Risks
│     ├── 5.1.1 Smart-contract vulnerabilities (Re-entrancy)  ⭐⭐
│     └── 5.1.2 51% & Sybil attacks                           ⭐⭐⭐ (51% = 7-marker staple)
├── 5.2 Emerging Trends
│     ├── 5.2.1 DeFi: Yield Farming & Liquidity Pools         ⭐⭐
│     ├── 5.2.2 NFTs & the Metaverse                          ⭐
│     └── 5.2.3 DAOs                                          ⭐⭐⭐ (DAO vs Traditional org asked 3×)
└── 5.3 Blockchain in Green Energy
      ├── 5.3.1 Greenwashing & Tokenization of Energy         ⭐
      ├── 5.3.2 The Oracle Problem                            ⭐⭐
      └── 5.3.3 IoT Oracles                                   ⭐
```

### Learning outcomes — after this unit you can:
- Explain **re-entrancy**, **51%** and **Sybil** attacks with examples (and the fix for each)
- Describe DeFi's yield farming & liquidity pools, NFTs, and the Metaverse
- Define a **DAO**, contrast it with traditional organizations, and list its pros/cons
- Explain greenwashing, energy tokenization, and the **oracle problem** (how to trust off-chain data)

---

## 5.1 Blockchain Security & Risks

### 5.1.1 Common Smart Contract Vulnerabilities — Re-entrancy Attacks ⭐⭐

A **re-entrancy attack** exploits a contract that updates its state *after* calling an external contract — the external contract **re-enters** the function before the state is saved, draining funds repeatedly.

```
1. Attacker's contract calls victim.withdraw()
2. Victim transfers ETH to attacker  ← state NOT yet updated
3. Attacker's receive()  calls victim.withdraw() AGAIN
4. Victim checks "balance >= amount" — still true (old state!)
5. Repeat until victim's balance is drained
```

**The DAO hack (2016)** — attackers drained ~3.6M ETH (then ~$60M) via exactly this bug, forcing Ethereum's historic hard fork.

**Fixes:**
1. **Checks-Effects-Interactions** — update state (balance = 0) *before* the external call.
2. **Re-entrancy guard** — a `bool locked` modifier that rejects re-entry.
3. Use `transfer` (2300 gas stipend) instead of `call` — historically used to starve re-entry.

### 5.1.2 51% Attacks and Sybil Attacks ⭐⭐⭐

**51% attack** — if one entity controls >50% of the network's hashrate (PoW) or staked value (PoS):
- **Double-spend:** spend coins → get goods/services → re-mine the chain to orphan your spend → coins back.
- **Censorship:** exclude chosen transactions/blocks from the chain.
- **Cannot** forge signatures, steal others' coins, or mint new coins (supply is consensus-capped).
- *Cost:* enormous electricity/hardware (Bitcoin: hundreds of millions $); attacks happen mainly on small chains (e.g. Ethereum Classic hit in 2020). Note: >50% isn't even required — ~30–40% can still cause probabilistic double-spend damage.

**Sybil attack** — one attacker creates **many fake nodes** to out-vote honest ones or isolate victims (censorship, blocking blocks). *Why PoW defeats it:* fake nodes are free, fake *hash power* isn't. Influence is bought with electricity (PoW) or stake (PoS), not identities.

**51% vs Sybil — exam one-liner:** *Sybil attacks multiply your identities cheaply; 51% attacks buy majority influence expensively. Proof-of-work/stake stops the first by pricing influence; economic game theory stops the second by making attacks unprofitable.*

---

## 5.2 Emerging Trends

### 5.2.1 Decentralized Finance (DeFi): Yield Farming & Liquidity Pools ⭐⭐

**DeFi** = financial services (lending, borrowing, trading, interest) built on smart contracts, **without banks or brokers** — open 24/7, permissionless, auditable.

- **Liquidity pool (LP):** users deposit token pairs (e.g. ETH/USDC) into a smart contract; traders swap against the pool (AMM — automated market maker, e.g. Uniswap). Providers earn a share of trading fees.
- **Yield farming:** users **lock/stake** their LP tokens (or single tokens) into farms to earn extra rewards (governance tokens, extra yield) — "put your money to work."
- **The catch (study it):** **impermanent loss** — if the token price ratio changes, liquidity providers can lose value vs simply holding; **smart-contract risk** — a bug means funds lost, no insurance; **gas** — every farm action costs transaction fees.
- Exam-friendly flow: *deposit LP → receive LP-token → stake LP-token in farm → earn rewards → compound.*

### 5.2.2 NFTs & the Metaverse ⭐

- **NFT (Non-Fungible Token):** a unique, non-interchangeable token (ERC-721) representing ownership of a specific digital/real asset — art, collectibles, in-game items, real estate deeds.
- **Fungible** = interchangeable (1 BTC = 1 BTC); **non-fungible** = each is unique (your Bored Ape ≠ mine).
- **Metaverse:** persistent virtual worlds (Decentraland, The Sandbox) where land/items are NFTs and economies run on crypto. Blockchain gives verifiable ownership & portability across virtual worlds.

### 5.2.3 DAOs (Decentralized Autonomous Organizations) ⭐⭐⭐

**DAO** = an organization governed by **code + token-holder voting** instead of a management hierarchy. Rules are encoded in smart contracts; members propose/vote with governance tokens; treasury funds are released automatically when a vote passes.

**DAO vs Traditional organization (W25 Q.5(b)-alt, S26 Q.5(b)):**

| Aspect | Traditional organization | DAO |
|---|---|---|
| Governance | Board of directors / hierarchy | Token-weighted voting |
| Decision speed | Slow (meetings, approvals) | Fast (proposals + smart-contract execution) |
| Trust | Trust in management | Trust in audited code |
| Transparency | Selective | Fully open on-chain |
| Location/legal | Jurisdiction-bound | Global, borderless |
| Human error/risk | Corruption, bias | Smart-contract bugs (DAO hack 2016!) |
| Coordination | Salaries, hierarchy | Incentives, treasury, proposals |

**Steps to launch a DAO (S24/S26 Q.5(b)-alt):** (1) define the mission & governance model (voting rules, quorum); (2) write the smart contracts (token, treasury, voting — Snapshot/Aragon/Zodiac); (3) audit the contracts; (4) deploy on-chain and create the governance token; (5) distribute/airdrop tokens to members; (6) fund the treasury; (7) go live — members propose & vote.

**Advantages (S24 Q.5(c)-alt):** transparency, trustless automation, global participation, community ownership, censorship resistance.
**Disadvantages:** legal/regulatory grey zone, slow under high participation, smart-contract vulnerability (the original DAO hack), token-vote manipulation (whales), no HR/support if things break.

---

## 5.3 Blockchain in Green Energy

### 5.3.1 The Problem of Greenwashing & Tokenization of Energy ⭐

- **Greenwashing** = claiming environmental friendliness without proof. Blockchain fixes this with **verifiable provenance**: every energy unit's origin (solar/wind/coal) is recorded immutably → claims can be audited instead of trusted.
- **Tokenization of energy:** renewable energy production is split into **energy tokens** — 1 token = 1 kWh (or a share of a solar farm). You can trade them like commodities: buy, sell, retire (burn) to prove you used green energy. P2P energy trading (Prosumer→neighbor) becomes automatic via smart contracts.
- This ties to UNIT 3 practical [P08](../practicals/writeups/P08_erc20_token.md) — a green-energy token contract.

### 5.3.2 The Oracle Problem: How Do We Trust the Data? ⭐⭐

- **The problem:** blockchains are **deterministic and isolated** — they cannot fetch real-world data (weather, price, temperature) by themselves. If a smart contract reads "temperature > 40°C" for crop insurance, *who feeds it that number?*
- **The oracle** = a trusted data source that bridges off-chain data into the chain. **The problem** = how to trust that bridge: a single oracle is a **single point of failure** (hackable, bribable, wrong).
- **Solutions:** (1) **Decentralized oracles** — multiple independent oracles + majority aggregation (Chainlink); (2) **Reputation/staking** — oracles stake tokens and are slashed for bad data; (3) **TLS/TEE + cryptography** — verifiable off-chain computation (Town Crier); (4) **Direct sensors** with signed hardware.

### 5.3.3 Introduction of IoT Oracles ⭐

- **IoT oracle** = a device (sensor, smart meter, GPS) that pushes *physical-world* measurements onto the blockchain via an oracle node.
- **Flow:** IoT sensor reads data → signs it → oracle transmits → smart contract uses it → payout/action (e.g. insurance payout when rainfall crosses a threshold).
- **Challenges:** sensor spoofing, connectivity, data volume vs gas cost, device key management.
- **Applications:** parametric insurance (drought/flood auto-payout), cold-chain monitoring for pharma/food, renewable-energy certificate generation from smart meters, supply-chain GPS tracking.

---

## 🧠 Deep-Dive Topics

### Deep Dive A: Re-entrancy — the attack explained in one Solidity story
The victim:
```solidity
function withdraw() public {
    uint bal = balances[msg.sender];
    (bool ok,) = msg.sender.call{value: bal}("");  // external call BEFORE state update
    if (ok) balances[msg.sender] = 0;              // ← too late: attacker re-entered
}
```
The attacker's `receive()` fires on the ETH receipt and calls `withdraw()` again. Since `balances[msg.sender]` is still the old value, the check passes again → drain. **The fix:** set `balances[msg.sender] = 0` *before* the call (checks-effects-interactions), or add a `nonReentrant` modifier.

### Deep Dive B: The DAO hack — history that split a chain
2016: *The DAO* raised ~$150M. Attackers exploited re-entrancy to drain ~$60M. The community split: **fork Ethereum** to refund victims (→ today's Ethereum) or **keep the original chain** (→ Ethereum Classic). Lesson: **smart contracts are code, and code is law only if correct** — audits matter. This single event is why "audit" appears in every DAO launch checklist.

### Deep Dive C: Yield farming — where returns actually come from
- **Real returns:** trading fees from the pool + incentives paid by protocols in their own token.
- **Fake returns:** high APY in a token whose price is crashing = negative real return. Rule of thumb examiners love: *yield farmers supply liquidity; protocols buy growth by printing tokens; late entrants hold the bag.*
- **Impermanent loss formula intuition:** the pool rebalances toward the cheaper asset; when the price ratio returns to entry, loss "disappears" (it's only realized if you withdraw during divergence).

### Deep Dive D: The oracle problem — a 7-marker in three acts
1. **The requirement:** smart contracts are deterministic — they can't call the internet. For real-world contracts (insurance, energy, supply chain) they need external data.
2. **The risk:** a single data source is trustable but vulnerable — corrupt, wrong, or hacked data poisons the contract and its money. "Blockchain is trustless" fails at the data boundary.
3. **The resolution:** decentralize the source (many oracles + consensus, e.g. Chainlink), align incentives (staked oracles, slashing), and verify the transport (TLS-notarization, TEEs). Then "trust the network, not the source."

---

## 🚀 Beyond the Textbook (what most classes won't tell you)

- **The 2016 DAO hack wasn't a "bug in Ethereum"** — Ethereum worked exactly as written; the *contract* was wrong. That's the key nuance examiners respect.
- **PoW isn't the only thing that stops Sybil attacks** — cost-per-influence is. PoS does it with stake; reputation systems with identity.
- **Most "51% attacks" happen on tiny chains** — with ~1% of Bitcoin's hashrate you could reorg a small altcoin for a day. Bitcoin is attacked by economics, not hash power.
- **Yield farming is a marketing term, not a law of finance** — "liquidity mining" pays you in the protocol's own token; APY is denominated in a token that can crash 90%.
- **Green energy + blockchain is genuinely one of the most *sensible* real-world use cases** — because verification (not hype) is the actual bottleneck, and provenance is exactly what a blockchain records.

---

## 📝 PYQ Map — UNIT 5 (all available papers)

| Paper | Q. | Topic | Marks |
|---|---|---|---|
| **Winter 2024** | Q.3(b)-alt | 51% attack — what & how it works | 4 |
| | Q.5(b) | dApps in blockchain — explain & working | 4 |
| | Q.5(b)-alt | Short note: DAO | 4 |
| **Summer 2025** | Q.3(c)-alt | Short note: 51% attack | 7 |
| | Q.5(c) | dApps — uses, advantages & disadvantages | 7 |
| **Summer 2026** | Q.3(c)-alt | 51% attack wrt blockchain | 7 |
| | Q.5(b) | Differentiate Traditional org vs DAO | 4 |
| | Q.5(b)-alt | Steps to launch a DAO | 4 |
| **Winter 2025** | Q.3(b) | Sybil attack with example | 4 |
| | Q.5(b)-alt | Compare DAO and Traditional organization | 4 |
| **Summer 2024** | Q.3(c) | Explain 51% attack | 7 |
| | Q.3(c)-alt | Explain Sybil attack | 7 |
| | Q.5(b)-alt | Steps to launch a DAO | 4 |
| | Q.5(c)-alt | DAO — definition, advantages & disadvantages | 7 |

### ✅ Solved PYQ answers (UNIT 5)

**S25 Q.5(c) — What are dApps used for? Advantages & disadvantages (7 marks).**
> **dApps (Decentralized Applications)** are applications whose **backend runs on smart contracts** instead of a centralized server — the frontend is normal, but logic, data, and money are on-chain. **Uses:** DeFi (Uniswap, Aave — trading/lending), gaming & NFTs (Axie, CryptoKitties), DAO governance, social/communication apps, supply-chain and identity tools. **Advantages:** (1) *Open & permissionless* — anyone can use them without an account or KYC; (2) *Censorship-resistant* — no company can shut them down or freeze your funds; (3) *Transparent & auditable* — code and transactions are public; (4) *User-controlled assets* — users hold keys, not the platform; (5) *Interoperable* — contracts can compose (a lending dApp can borrow from a DEX). **Disadvantages:** (1) *Scalability & speed* — on-chain execution is slow and costly (gas); (2) *Bug risk* — a smart-contract bug can permanently lose funds with no recovery; (3) *UX friction* — wallets, gas, seed phrases scare mainstream users; (4) *No customer support* — if you lose your key or funds, nobody can help; (5) *Regulatory uncertainty* — legal status of many dApps is unclear.

**S26 Q.5(b) — Differentiate Traditional Organizations and DAOs (4 marks).** — see §5.2.3 table (governance, speed, trust, transparency, borders, error risk, coordination). Pick any 4 rows.

**S24 Q.5(c)-alt — What is a DAO? Advantages & disadvantages (7 marks).**
> **Definition:** A DAO (Decentralized Autonomous Organization) is an organization governed by **smart contracts and token-weighted voting** instead of a management hierarchy; rules are encoded in code and the treasury is released automatically when votes pass. **Advantages:** (1) *Transparency* — every proposal and vote is public on-chain; (2) *Trustless automation* — execution is code, not management discretion; (3) *Global & permissionless participation* — anyone holding tokens can join/vote; (4) *Community ownership* — no central CEO to capture value; (5) *Censorship resistance* — no single point of failure or shutdown. **Disadvantages:** (1) *Smart-contract risk* — a bug can drain the treasury (the 2016 DAO hack lost ~$60M); (2) *Slow governance* — high participation can stall decisions; (3) *Whale dominance* — large token holders can control votes; (4) *Legal grey area* — DAOs have no recognized legal personality in most jurisdictions; (5) *No safety net* — errors and losses are irreversible.

**S24 Q.3(c)-alt — Explain Sybil attack (7 marks).**
> A **Sybil attack** is an attack on a peer-to-peer network in which a single entity creates **numerous fake identities (nodes)** to gain a disproportionately large influence, appearing to be many independent participants. **How it works:** the attacker registers thousands of nodes, then uses them to (1) **out-vote** honest nodes in consensus or voting, (2) **isolate** a victim so all their connections route through attacker nodes (censoring blocks/transactions), (3) **starve** honest nodes of information, and (4) prevent double-spend detection by controlling what the victim sees. **Example:** in a network that counts one-vote-per-node, an attacker with 10,000 fake nodes beats 100 honest users. **Why blockchains resist it:** influence in Bitcoin is not per-node but **per-hashpower** (PoW) — creating fake nodes is free, but creating fake computational work costs real electricity. Similarly, PoS ties influence to staked value, and permissioned chains tie it to vetted identity. Thus **Sybil resistance = economic cost per unit of influence.**

**W25 Q.3(b) — Explain Sybil attack with example (4 marks).** — condensed version of the 7-marker above (definition + mechanism + the hash-power example).

**S26 Q.3(c)-alt — 51% attack (7 marks).**
> A **51% attack** occurs when a single miner/pool/entity controls **more than 50% of the network's mining (hashing) power** — or staked value in PoS — giving them the ability to influence consensus. **Capabilities:** (1) **Double-spend** — spend coins, receive goods, then re-mine the chain to discard the original spend, regaining the coins; (2) **Transaction censorship** — exclude specific addresses' transactions from being included; (3) **Reordering** — delay or reorder transactions. **Limitations:** the attacker **cannot** forge signatures or steal other users' coins, and **cannot** create coins beyond the protocol's supply cap — they can only manipulate *their own* spends. **Feasibility & defence:** on Bitcoin, >50% hashrate costs hundreds of millions of dollars and even then the attack destroys the coin's value (the attacker's own reward), so it is **economically irrational**; smaller chains (e.g. Ethereum Classic 2020) have suffered real attacks. Defences: high total hashrate, checkpoints, and proof-of-stake's economic finality.

**S24 Q.5(b)-alt / S26 Q.5(b)-alt — Steps to launch a DAO (4 marks).** — the 7 steps in §5.2.3 (mission → contracts → audit → deploy → tokens → treasury → go live).

---

## ✍️ Practice Problems (self-test — answers upside-down)

1. (7) Explain the re-entrancy attack with a step-by-step example and how to fix it.
2. (4) Differentiate a 51% attack and a Sybil attack.
3. (7) What is yield farming? Explain liquidity pools and impermanent loss.
4. (4) Compare DAO and traditional organization on any four points.
5. (3) What is an NFT? How is it different from a cryptocurrency?
6. (7) Explain the oracle problem and the role of IoT oracles in green-energy blockchain.
7. (4) How does blockchain help prevent greenwashing?
8. (3) Why can't a 51% attacker steal other users' coins?

<details>
<summary><b>Click for answers</b></summary>

1. See Deep Dive A — external call before state update lets `receive()` re-enter; fixes = checks-effects-interactions, re-entrancy guard, transfer-stipend. Cite the 2016 DAO hack.
2. Sybil = fake identities multiply cheaply (influence via nodes); 51% = majority hashpower/stake bought expensively (influence via economic majority). PoW/PoS defeat Sybil by pricing influence; economics defeats 51%.
3. LP = pairs deposited for traders to swap against (AMM), earning fees; yield farming = staking LP/rewards to earn more; impermanent loss = divergence loss vs holding when price ratio moves.
4. Any 4 rows from §5.2.3 table.
5. NFT = unique, non-fungible (ERC-721, one-of-a-kind ownership); crypto = fungible (interchangeable units).
6. Blockchains can't fetch external data → oracles bridge it → single source = single point of failure → decentralized oracles/staking/aggregation. IoT oracles = sensors signing physical data (rainfall, kWh) into contracts for automatic payouts.
7. Immutable provenance: every energy unit's origin is recorded and auditable, so green claims can be verified, not just asserted (fights greenwashing).
8. Signatures are unforgeable; the attacker can only reorder their *own* spends. Others' coins require forging keys, which crypto prevents.

</details>

---

## 📖 Glossary of Key Terms

| Term | One-line meaning |
|---|---|
| Re-entrancy | Attack where an external contract re-enters before state updates |
| 51% attack | Majority-hashpower control → double-spend & censorship |
| Sybil attack | One attacker impersonating many nodes |
| DeFi | Decentralized finance — bankless financial apps on smart contracts |
| Liquidity pool | Contract holding token pairs for AMM trading |
| Yield farming | Staking LP tokens to earn extra rewards |
| Impermanent loss | Value loss vs holding when pool price ratios diverge |
| NFT | Non-fungible token — unique ownership (ERC-721) |
| Metaverse | Persistent virtual worlds with crypto/NFT economies |
| DAO | Code-governed, token-voting organization |
| Greenwashing | Unverifiable environmental claims |
| Oracle | Bridge bringing off-chain data on-chain |
| Oracle problem | How to trust the data bridge |
| IoT oracle | Sensor feeding signed physical data to contracts |

---

## 🔗 Curated Resources (per concept)

- **Re-entrancy (consensys):** https://consensys.github.io/smart-contract-best-practices/attacks/reentrancy/
- **DAOs:** https://ethereum.org/en/dao/ | Snapshot (voting): https://snapshot.org
- **DeFi & yield farming:** https://ethereum.org/en/defi/ | Uniswap AMM docs
- **NFTs:** https://ethereum.org/en/nft/ | ERC-721: https://eips.ethereum.org/EIPS/eip-721
- **Oracle problem & Chainlink:** https://chain.link/education-hub/what-is-a-blockchain-oracle
- **IoT + blockchain (IoTex / Helium):** https://www.iotex.io/
- **Green energy case study (energy web):** https://www.energyweb.org/

---

## 🎥 Video Study Guide (YouTube)

> Your video path for the whole unit — exact keywords to search + channels you can trust.

### 🧑‍🎓 Step 0 — Pick your learning style

| Style | You learn best by | Your path through this unit |
|---|---|---|
| 🎧 **Listener** | short, clear explainers | 1 explainer per topic in the table below |
| 🛠️ **Builder** | hands-on | Re-run [P08](../practicals/writeups/P08_erc20_token.md); try a re-entrancy CTF |
| 🔧 **Tinkerer** | experimenting & demos | Damage Labs / Capture-the-Ether re-entrancy challenges |
| 🧠 **Deep Diver** | full theory, "why" | Playlists at the bottom |
| 🧭 **Explorer** | breadth & curiosity | Start with DeFi/NFT explainers |
| 🎓 **Academic** | exam marks | Revision videos → grind the PYQ map above |

### 🎬 Step 1 — Watch by topic (search these on YouTube)

| Topic | YouTube search keywords (copy-paste ready) | Best channels | Style served |
|---|---|---|---|
| Smart-contract security | `smart contract vulnerabilities` · `reentrancy attack explained` · `solidity security best practices` | White Hat / Secureum, RareSkills, Smart Contract Programmer | 🧠 Deep Diver |
| 51% & Sybil attacks | `51 percent attack explained` · `sybil attack explained with example` · `how ethereum classic was attacked` | Computerphile, Simply Explained, Coin Bureau | 🎓 Academic |
| DeFi overview | `what is defi` · `decentralized finance explained` · `defi for beginners` | Finematics, Coin Bureau, Whiteboard Crypto | 🧭 Explorer |
| Yield farming & liquidity | `yield farming explained` · `liquidity pools explained` · `impermanent loss explained` | Finematics, Whiteboard Crypto, Coin Bureau | 🎓 Academic |
| NFTs & Metaverse | `what are nfts` · `nft explained 5 minutes` · `metaverse explained` | Whiteboard Crypto, Fireship, Coin Bureau | 🧭 Explorer |
| DAOs | `what is a dao` · `dao explained` · `dao vs traditional company` · `how to launch a dao` | Finematics, Whiteboard Crypto, Coin Bureau | 🎓 Academic |
| Oracle problem | `blockchain oracle explained` · `what is chainlink` · `oracle problem smart contracts` | Finematics, Chainlink official, Simply Explained | 🧠 Deep Diver |
| IoT + blockchain | `iot blockchain explained` · `iot oracles` · `iotex blockchain` · `sensor data on blockchain` | Helium/IoTeX channels, Simply Explained | 🧭 + 🎧 |
| Green energy & blockchain | `blockchain green energy` · `energy tokenization explained` · `p2p solar energy trading blockchain` | Energy Web, Coin Bureau | 🧭 + 🎓 |
| Whole-unit revision | `blockchain security full course` · `defi nft dao full course` · `blockchain trends exam revision` | freeCodeCamp, MIT OCW, Gate Smashers, Neso Academy | 🎓 Academic |

### 🎬 Step 2 — Full playlists (for Deep Divers & Academics)

1. **"Finematics — DeFi, DAO & oracle explainer library"** — the visual backbone of this unit.
2. **"Secureum / Smart Contract Programmer — smart-contract security bootcamp"** — if you want to truly understand re-entrancy and more.
3. **"MIT 15.S12 — security & applications lectures"** — exam-grade framing of DAOs, DeFi, and trust.

### 🎬 Step 3 — Proof you got it (5 min)

- Re-tell the re-entrancy attack as a story (withdraw → receive → withdraw…).
- Say the DAO-vs-traditional table from memory.
- Explain to a friend why a sensor feeding a contract needs an oracle and why one oracle isn't enough.

---

*End of FOB notes. 🎉 Next: revisit [UNIT 1](../notes/UNIT_1_Foundations_of_Decentralization.md) to start your revision loop.*
