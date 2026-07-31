# UNIT 2 — Bitcoin & The Proof-of-Work Era ⛏️

**Syllabus weightage:** 8 hrs / 15% | **Related practicals:** [P05](../practicals/writeups/P05_nonce_mining_difficulty.md), [P06](../practicals/writeups/P06_wallets_mnemonic_bip39.md)
**Star guide:** ⭐ = likely asked · ⭐⭐ = very likely · ⭐⭐⭐ = practically guaranteed in some form

---

## 🧭 Chapter Roadmap

```
UNIT 2: Bitcoin & Proof-of-Work
├── 2.1 The Bitcoin Protocol
│     ├── 2.1.1 UTXO model vs Account model      ⭐⭐ (every year: define UTXO)
│     └── 2.1.2 Bitcoin wallets: hot vs cold, seed phrases  ⭐
├── 2.2 Mining & Game Theory
│     ├── 2.2.1 Proof of Work & "Difficulty"      ⭐⭐⭐ (7-mark favourite)
│     ├── 2.2.2 Life cycle of a transaction       ⭐⭐⭐ (mempool → block)
│     └── 2.2.3 Mining incentives: rewards & halving  ⭐⭐
└── 2.3 Advanced Consensus
      ├── 2.3.1 Proof of Stake & Slashing         ⭐⭐ (PoW vs PoS = 4-marker staple)
      ├── 2.3.2 PoW vs PoS comparison             ⭐⭐⭐
      └── 2.3.3 The role of forks in consensus    ⭐⭐ (hard vs soft fork)
```

### Learning outcomes — after this unit you can:
- Explain exactly how a Bitcoin transaction travels from wallet → mempool → block → confirmations
- Define UTXO, difficulty, halving, slashing, finality, minting and use each correctly in an answer
- Compare **PoW vs PoS** on energy, security, entry cost and finality (the classic 4-marker)
- Distinguish hard fork vs soft fork and explain why forks exist
- Draw the block-lifecycle / mining flow diagrams that examiners award marks for

---

## 2.1 The Bitcoin Protocol

### 2.1.1 UTXO Model vs Account Model ⭐⭐

> **Short definition (memorize this sentence):** A **UTXO (Unspent Transaction Output)** is a "coin" — an output of a previous transaction that has not yet been spent. Bitcoin has **no account balances**; the network only knows which outputs are unspent.

Bitcoin launched **January 2009** by pseudonymous **Satoshi Nakamoto** (whitepaper published Oct 2008). Supply is hard-capped at **21 million BTC**. One BTC divides down to 10⁻⁸ — the smallest unit is the **satoshi** (`1 BTC = 100,000,000 satoshi`).

Think of UTXOs like **cash bills**:
- You can't spend "half a note" — you pay with whole notes and get **change** back.
- A transaction **consumes** whole UTXOs as *inputs*, and creates fresh UTXOs as *outputs* (recipient + your change).

```
Inputs (old UTXOs you own)          Outputs (new UTXOs)
┌────────────────────────┐         ┌────────────────────────┐
│ UTXO A (2 BTC)     ────┼────────►│ recipient   (1.7 BTC)   │  ← new UTXO
│ UTXO B (1 BTC)     ────┼────────►│ change (you) (1.2 BTC)  │  ← new UTXO
└────────────────────────┘         └────────────────────────┘
                                  fee = (2+1) − (1.7+1.2) = 0.1 BTC
```

| Aspect | UTXO (Bitcoin) | Account (Ethereum) |
|---|---|---|
| What is stored | Set of unspent outputs | Account balances + nonce |
| A transaction | Spends old UTXOs, mints new ones | Debits sender, credits receiver |
| Double-spend check | Each UTXO spent exactly once | Nonce prevents replay |
| Privacy | Better — new address per payment | Balances linkable to an address |
| Parallelism | High (independent UTXOs) | Lower (shared state conflicts) |
| Smart-contract friendliness | Harder (scripting is limited) | Native (EVM accounts) |
| Analogy | Cash + change | Bank ledger |

**Exam trick:** If a question asks *"Why is UTXO called unspent?"* — an output is only a UTXO until a transaction spends it; once spent it becomes an input record and is removed from the unspent set.

### 2.1.2 Bitcoin Wallets: Hot vs Cold Storage & Seed Phrases ⭐

A wallet is **a collection of keys** — it never "contains" coins; it contains the *right to spend* them.

| | Hot wallet | Cold wallet |
|---|---|---|
| Keys on | Internet-connected device | Offline device / paper |
| Examples | Exchange apps, MetaMask, mobile wallets | Hardware wallets (Ledger, Trezor), paper |
| Convenience | High — instant transactions | Low — must sign then broadcast |
| Security risk | Exposure to hacks/malware | Much safer (keys never online) |
| Best for | Daily spending, small amounts | Long-term storage of large amounts |

**Seed phrase (BIP39):** A wallet derives all its keys deterministically from a **12 or 24-word seed phrase** (e.g. `abandon … about`). 
- One phrase → one deterministic tree of addresses.
- **Anyone who knows the phrase controls every derived address** — write it on paper, never type it into a website. See [P06](../practicals/writeups/P06_wallets_mnemonic_bip39.md) to build one yourself.
- Mnemonic → entropy → `HMAC-SHA512` (passphrase "mnemonic") → 512-bit seed → master key → child keys (BIP32/44 derivation paths).

---

## 2.2 Mining & Game Theory

### 2.2.1 Proof of Work & the Concept of "Difficulty" ⭐⭐⭐

**Mining** is the act of finding a valid block header by brute force. A block header contains the Merkle root, timestamp, previous-hash, version, and a **nonce** the miner can change freely.

```
Goal: find nonce such that
      SHA256( SHA256( block_header ) )  <  Target

Smaller target  ⇒  more leading zeros required  ⇒  exponentially harder
```

- **Difficulty** = how much harder mining is now vs the easiest-ever target.
- The network **re-targets difficulty every 2016 blocks** (~2 weeks) so that blocks arrive roughly every **10 minutes** regardless of total hashrate.
- If miners add machines → blocks arrive faster → difficulty rises; if miners leave → difficulty falls.
- Because hashing is one-way, miners can't "cheat" by predicting a winning nonce — expected work = `Target/2²⁵⁶` hashes. (Try it in [P05](../practicals/writeups/P05_nonce_mining_difficulty.md).)

### 2.2.2 The Life Cycle of a Transaction (Mempool → Block) ⭐⭐⭐

This is the single most-asked diagram in UNIT 2. Draw it and label every arrow:

```
     1. SIGN         2. BROADCAST       3. VALIDATE         4. QUEUE
 ┌───────────┐   ┌──────────────┐   ┌───────────────┐   ┌───────────────┐
 │ Wallet    │──►│ P2P network  │──►│ Every full    │──►│ MEMPOOL       │
 │ signs tx  │   │ (gossip)     │   │ node checks   │   │ (unconfirmed) │
 └───────────┘   └──────────────┘   │ signatures &  │   └───────┬───────┘
                                     │ double-spends │           │ miners pick
                                     └───────────────┘           │ by fee/vByte
                                                                 ▼
     6. COMMIT         5. MINE                          ┌───────────────────┐
 ┌───────────────┐   ┌──────────────┐                   │ candidate block   │
 │ Nodes re-     │◄──│ Miner solves │◄──────────────────│ (PoW loop: nonce) │
 │ validate &    │   │ PoW, shares  │                   └───────────────────┘
 │ add to chain  │   └──────────────┘
 └──────┬────────┘
        ▼
 ~6 confirmations later → the tx is effectively FINAL
```

Key exam vocabulary for the mempool stage:
- **Mempool** = the pool of valid-but-unconfirmed transactions every node holds.
- **Fee rate (fee/vByte)** = a tx's priority; miners pack the most profitable txs first.
- **Confirmation** = a block containing your tx has been mined and built upon. 1 confirmation = your tx is in 1 block.
- **Finality** = the point past which a transaction cannot realistically be reversed. Bitcoin's is **probabilistic** (~6 blocks ≈ 1 hour); PoS chains have explicit finality gadgets.
- **Double-spend** = same UTXO spent twice. Nodes drop the second spend; only the first to reach a mined block is valid.

### 2.2.3 Mining Incentives: Block Rewards & Halving ⭐⭐

Why do miners behave honestly instead of attacking? **Because honesty pays more.**

1. **Block reward** — newly minted BTC to the winning miner. Started at 50 BTC; **halved every 210,000 blocks (~4 years):** 50 → 25 (2012) → 12.5 (2016) → 6.25 (2020) → **3.125 (2024)**.
2. **Transaction fees** — the difference between inputs and outputs of every tx they include.
3. **Game theory** — attacking (double-spend / reorg) requires spending electricity on an industrial scale, and succeeds only if the attacker already controls ~50%+ of hashrate. When honest, a miner earns steadily; when attacking, they risk massive sunk cost for a one-time gain.
4. By ~**2140** the block reward hits 0; miners will be paid **only by fees** — the fee market keeps the chain secure.

```
WHY THE HALVING MATTERS (exam-worthy):
supply inflow halved every 4 years → if demand is constant,
the inflation pressure halves → historically coincides with price
appreciation. Also: 21M cap ≈ 2140, enforced purely by code.
```

---

## 2.3 Advanced Consensus Mechanisms

### 2.3.1 Proof of Stake (PoS) — Energy Efficiency & "Slashing" ⭐⭐

PoS replaces *electricity* with *capital at risk*:

- **Validators** lock (stake) tokens — Ethereum requires **32 ETH** per validator.
- A validator is selected **pseudorandomly, weighted by stake** to propose the next block; a committee **attests** (votes) on it.
- **Slashing** = economic punishment. If a validator signs conflicting blocks (equivocation) or mis-attests, a proof of the misbehaviour is submitted and part of their stake is **burned**.
- Because an attacker must control ≥50% of staked ETH, the attack cost equals buying half the network — and a successful attack destroys the value of the very tokens they stole. **The attack becomes economically self-defeating.**

Ethereum switched from PoW to PoS in **The Merge (Sept 2022)**, cutting its energy use by ~99.95%.

### 2.3.2 Comparison: PoW vs PoS ⭐⭐⭐

This table **is** the 4-mark answer. Learn it as two-column facts, not prose.

| Criterion | Proof of Work (Bitcoin) | Proof of Stake (Ethereum) |
|---|---|---|
| Resource spent | Electricity + ASICs | Staked tokens (ETH) |
| Security bound | Majority of hashrate | Majority of staked value |
| Energy consumption | Very high | Very low (≈99% less) |
| Entry cost | Buy ASIC hardware | 32 ETH minimum validator |
| Penalty for cheating | Sunk energy (already wasted) | Slashing — stake burned |
| Block proposer | First miner to solve | Randomly chosen validator |
| Finality | Probabilistic (~6 blocks) | Explicit finality (fast, near-instant) |
| "Nothing at stake" problem | Not applicable | Historically debated; solved by slashing |
| Decentralization pressure | Mining-pool centralization | Large-staker centralization |

### 2.3.3 The Role of Forks in Consensus ⭐⭐

A **fork** = a divergence in the chain. Two flavours:

| | Soft fork | Hard fork |
|---|---|---|
| Compatibility | Backward-compatible — old nodes still accept new blocks | Not backward-compatible — chain splits |
| Who must upgrade | Only miners/producers | Everyone (miners + users) |
| Example | SegWit (2017) tightened block rules | Bitcoin Cash (2017), Ethereum Classic (2016, after the DAO hack) |
| Result | One chain, old nodes work | Two separate chains + two coins |

- **Accidental fork:** two miners solve at the same height → network converges on the longest chain; the loser's block is **orphaned**.
- **Planned hard fork:** a community rule change (bigger blocks, fix a hack) that old software can't follow → the chain splits; holders of the original coin usually receive the new coin 1:1.
- Exam line: *"A hard fork is a permanent divergence; a soft fork is a tightening of rules old nodes can still obey."*

---

## 🧠 Deep-Dive Topics

### Deep Dive A: Mempool → block, minute by minute
1. Wallet builds the tx: inputs = your UTXOs; outputs = recipient + change; fee = `inputs − outputs`.
2. Nodes verify: signatures valid? inputs unspent? → passes → enters **mempool**.
3. Miners rank mempool by **fee/vByte** and fill a candidate block (~1 MB, ~2–3k tx).
4. PoW loop: `nonce++` until `SHA256(SHA256(header)) < target`.
5. Winner broadcasts the block; every peer **re-validates each tx** before relaying.
6. Confirmation depth grows as new blocks stack on top. At 6 blocks (~1 hr) a reorg is practically impossible — this is Bitcoin's "finality".

### Deep Dive B: 51% attack — what an attacker actually can and cannot do
- To rewrite history, an attacker re-mines the target block **plus every following block** while the honest network mines too — a race they must win over and over.
- With ~51% hashrate they eventually win the race → **double-spend** their own coins (spend, get goods, then orphan the spend).
- **They cannot** forge signatures, spend others' coins, or create coins out of thin air — because signatures are unforgeable and supply is capped by consensus.
- Cost: huge electricity + lost block rewards during the attack + destroyed market confidence.

### Deep Dive C: Halving math (a 3-marker hidden in a 7-marker)
- `210,000 blocks × 10 min ≈ 4 years` per cycle.
- Cumulative supply after n halvings: `21M × (1 − 0.5ⁿ)` (only ~94% mined so far; remaining tail drags to ~2140).
- Mining is a **business**: revenue = `block reward + fees`, cost = electricity + hardware amortization. Miners break even at `breakeven_price = cost / BTC_mined`.

### Deep Dive D: Why slashing fixes "nothing at stake"
In pure PoS, a validator could theoretically vote on **every** competing chain for free ("nothing at stake") → no convergence. Slashing makes it **economically fatal** to vote on the wrong chain, so rational validators only vote on the one true chain. This is the same game-theoretic trick PoW does with energy — PoS does it with collateral.

---

## 🚀 Beyond the Textbook (what most classes won't tell you)

- **Difficulty ≠ complexity.** The network *wants* ~10-min blocks; difficulty is just the feedback knob. If the hashrate doubled today, difficulty roughly doubles within 2 weeks.
- **The 21M cap is not "hard-coded" everywhere** — it emerges from the halving rule (`50 → 25 → …`), which is the real consensus rule.
- **A seed phrase is a password to a whole tree of addresses.** Losing it = losing every address derived from it; no support ticket can help.
- **"Confirmations" is a trust threshold, not a rule.** 6 is convention (probability of double-spend success drops below ~0.1%). Exchanges pick their own (some use 3 for small txs).
- **Mining pools ≠ miners.** Most individual miners join pools; the pool operator constructs the block — a *de facto* centralization point Satoshi didn't foresee.

---

## 📝 PYQ Map — UNIT 2 (all available papers)

| Paper | Q. | Topic | Marks |
|---|---|---|---|
| **Winter 2024** | Q.3(a) | Short note: Consensus Mechanism | 3 |
| | Q.3(b) | Compare Hard Fork vs Soft Fork | 4 |
| | Q.3(c) | What is PoW? How does it work? | 7 |
| | Q.3(a)-alt | Short note: Block Rewards | 3 |
| | Q.3(b)-alt | 51% attack — what & how it works | 4 |
| | Q.3(c)-alt | What is PoS? How does it work? | 7 |
| | Q.5(a) | Short note: Bitcoin Scripting | 3 |
| | Q.5(a)-alt | Short note: Bitcoin Mining | 3 |
| **Summer 2025** | Q.3(a) | Define Consensus Mechanism, explain any one | 3 |
| | Q.3(b) | Why is forking needed? Types of forks | 4 |
| | Q.3(c) | Explain bitcoin mining (working, difficulty, benefits) | 7 |
| | Q.3(a)-alt | Differentiate soft fork vs hard fork | 3 |
| | Q.3(b)-alt | Importance of Finality in blockchain | 4 |
| | Q.3(c)-alt | Short note: 51% attack | 7 |
| | Q.5(a) | List & explain cryptocurrency wallets | 3 |
| **Summer 2026** | Q.3(a) | Explain "mining" wrt blockchain | 3 |
| | Q.3(b) | Differentiate PoW and PoS | 4 |
| | Q.3(c) | Consensus mechanisms — list & explain | 7 |
| | Q.3(a)-alt | Explain "minting" wrt blockchain | 3 |
| | Q.3(b)-alt | Differentiate soft vs hard fork | 4 |
| | Q.3(c)-alt | 51% attack wrt blockchain | 7 |
| **Winter 2025** | Q.3(a) | Define consensus; list consensus algorithms | 3 |
| | Q.3(b) | Explain Sybil attack with example | 4 |
| | Q.3(c) | Explain PoS in detail | 7 |
| | Q.3(a)-alt | Role of bitcoin miners | 3 |
| | Q.3(b)-alt | 51% attack with example | 4 |
| | Q.3(c)-alt | Explain PoW in detail | 7 |
| **Summer 2024** | Q.3(a) | Define "Confirmation" and "Finality" | 3 |
| | Q.3(b) | Differentiate PoW and PoS | 4 |
| | Q.3(c) | Explain 51% attack | 7 |
| | Q.3(a)-alt | Define "Hard fork" and "Soft fork" | 3 |
| | Q.3(b)-alt | List consensus types; explain any one | 4 |
| | Q.3(c)-alt | Explain Sybil attack | 7 |
| | Q.2(b)-alt | Types of wallets + factors for selecting a wallet | 4 |

### ✅ Solved PYQ answers (UNIT 2)

**W25 Q.3(b) — Explain Sybil attack with example (4 marks).**
> A **Sybil attack** is when a single attacker creates **many fake identities (nodes)** to gain disproportionate influence over a peer-to-peer network, pretending to be many independent participants. Since blockchain relies on distributed nodes for consensus, a Sybil attacker who floods the network with thousands of malicious nodes can:
> - Isolate honest nodes and control which data they receive (censorship),
> - Surround a victim so their transactions only pass through attacker-controlled nodes,
> - Block the propagation of blocks/transactions.
> **Example:** In a decentralized network where each node gets one vote, an attacker creates 10,000 fake nodes to win most votes. Bitcoin resists Sybil attacks not by identity checks but by **proof-of-work** — creating fake nodes costs nothing, but creating fake *hash power* costs real electricity. So Sybil resistance in Bitcoin = economic cost per unit of influence.

**S25 Q.3(c) — Explain bitcoin mining in detail (7 marks).**
> Bitcoin mining is the process of adding new blocks to the blockchain by solving a computational puzzle, called **Proof of Work**. **Working:** miners group valid transactions from the mempool into a candidate block. Each miner then repeatedly changes the block header's **nonce** and hashes it (`SHA256(SHA256(header))`) until the resulting hash is **less than the current target**. The target is chosen so that on average **one block is found every 10 minutes**. When a miner finds a valid nonce, they broadcast the block; every node verifies the hash and the transactions before adding it to the chain, and miners begin mining on top of it. **Difficulty:** the target is adjusted every **2016 blocks (~2 weeks)** to keep block time near 10 minutes as the total hashrate rises or falls. More hashrate → smaller target (harder). **Benefits/security:** mining enforces consensus (everyone agrees on one canonical chain), secures against double-spending (rewriting history requires redoing the PoW work), resists Sybil attacks (influence costs electricity, not fake identities), and **incentivizes honest behaviour** through the block reward and transaction fees — attacking would be economically irrational because it costs more than it can earn.

**S26 Q.3(a)-alt — Explain "minting" wrt blockchain (3 marks).**
> **Minting** is the process of creating new coins/tokens directly on-chain. In **Proof of Stake** systems, minting (also called *forging*) replaces PoW mining: validators lock (stake) their tokens and are pseudorandomly chosen — weighted by the size of their stake — to validate a block and, in return, **receive newly created coins and transaction fees**. Unlike mining, minting consumes almost no electricity because no computational puzzle is solved; security comes instead from the economic stake the validator risks being **slashed** if they misbehave. Minting is also used to create NFTs: *minting an NFT* means writing its unique metadata onto the blockchain so it becomes an owned, tradeable token.

**S26 Q.3(b) — Differentiate PoW and PoS (4 marks).**
> 1. **Resource used:** PoW spends electricity/computational power; PoS locks up staked tokens (capital).
> 2. **Block proposer selection:** In PoW the first miner to find a valid hash wins; in PoS a validator is selected pseudorandomly, weighted by stake.
> 3. **Security basis:** PoW is secure while no entity controls 51% of hashrate; PoS is secure while no entity controls 51% of staked value.
> 4. **Energy:** PoW consumes very high energy; PoS uses ≈99% less, making it far more eco-friendly.
> 5. **Penalty for misbehaviour:** PoW loses wasted electricity; PoS loses part of the stake through **slashing**.
> 6. **Finality:** PoW finality is probabilistic (~6 blocks); PoS can achieve faster, explicit finality. Examples: Bitcoin uses PoW; Ethereum (post-Merge, 2022) uses PoS.

**S25 Q.3(b)-alt — Importance of Finality (4 marks).**
> **Finality** is the guarantee that a transaction, once confirmed, will never be reversed or altered. Its importance in blockchain:
> 1. **Prevents double-spending** — after finality, the same coins cannot be re-spent, so merchants can safely release goods/services.
> 2. **Economic settlement** — payments (especially large ones) need certainty; without finality no business would accept crypto as payment.
> 3. **Protects against chain reorgs/51% attacks** — finality marks the point beyond which rewriting history becomes impractical.
> 4. **Defines the trust model** — Bitcoin gives *probabilistic finality* (deeper confirmations → higher certainty, conventionally 6 blocks ≈ 1 hour), while PoS chains (e.g. Ethereum's Casper) provide *explicit/economic finality* almost immediately. A system without finality cannot serve as a reliable ledger or store of value.

**S24 Q.3(b) — Differentiate PoW and PoS (4 marks)** — see solved S26 Q.3(b) above (same skill, reuse the six-point table).

---

## ✍️ Practice Problems (self-test — answers upside-down)

1. (3) Define UTXO. Why does the "U" in UTXO matter to double-spend prevention?
2. (4) Compare hot and cold wallets. Which one would you use for your life savings and why?
3. (7) With a diagram, explain the life cycle of a bitcoin transaction from signing to finality.
4. (4) A network's hashrate triples. What happens to difficulty and average block time over the next few weeks?
5. (3) What is the block reward in 2026? When does the next halving occur (≈)?
6. (7) "PoS secures the chain with slashing instead of electricity." Justify.
7. (3) Differentiate Confirmation vs Finality.
8. (4) Why would a 51% attacker still be unable to steal other users' bitcoins?

<details>
<summary><b>Click for answers</b></summary>

1. UTXO = Unspent Transaction Output, an output of a prior tx not yet spent. It can be spent exactly once; the "unspent" flag is what the network tracks, so a second spend of the same output is immediately invalid.
2. Cold (hardware/paper) — keys never touch the internet, so they survive malware/hacks; hot wallets are only for small day-to-day amounts.
3. See Deep Dive A + the mempool→block diagram: sign → broadcast → validate → mempool → fee-ranked mining → PoW → broadcast/verify → confirmations → probabilistic finality.
4. Blocks arrive ~3× faster → difficulty rises at the next 2016-block retarget (~1/3 of 2 weeks) → block time returns to ~10 min.
5. 3.125 BTC (halved April 2024). Next halving ≈ 2028 (block 1,050,000).
6. Validators stake real tokens; equivocation/mis-attesting triggers slashing (burned stake). Attack cost = 51% of staked value, and success destroys the stolen tokens' value — economically self-defeating.
7. Confirmation = tx is included in a block (and blocks stacked on it); Finality = point beyond which reversal is practically/technically impossible.
8. Signatures are unforgeable — attackers can only reorder their *own* spends (double-spend), never forge a spend of someone else's coins.

</details>

---

## 📖 Glossary of Key Terms

| Term | One-line meaning |
|---|---|
| UTXO | Unspent Transaction Output — a spendable "coin" |
| Mempool | Pool of valid, unconfirmed transactions |
| Nonce | Number a miner varies to change the header hash |
| Target / Difficulty | Threshold the block hash must beat / how hard that is now |
| Block reward | Newly minted BTC given to the winning miner |
| Halving | Reward cut by 50% every 210,000 blocks (~4 years) |
| Confirmation | One block built on top of your tx |
| Finality | Point past which a tx can't realistically be reversed |
| Double-spend | Spending the same UTXO twice |
| Orphan block | Valid block that lost the longest-chain race |
| Staking | Locking tokens as validator collateral |
| Slashing | Burning a validator's stake for misbehaviour |
| Hard fork | Non-backward-compatible split creating two chains |
| Soft fork | Backward-compatible tightening of rules |
| Sybil attack | One attacker impersonating many nodes |
| Minting | Creating coins/validating blocks in PoS |

---

## 🔗 Curated Resources (per concept)

- **UTXO & transactions:** *Mastering Bitcoin* (Andreas Antonopoulos) Ch. 5–6; https://mempool.space (watch a live tx enter the mempool)
- **Mining & difficulty:** *Mastering Bitcoin* Ch. 8; https://bitcoin.org/bitcoin.pdf §4–5
- **Halving history:** https://bitcoin.halving.help (all four halvings)
- **PoS & The Merge:** https://ethereum.org/en/developers/docs/consensus-mechanisms/pos/
- **Forks:** *Mastering Bitcoin* Ch. 10; https://www.investopedia.com/terms/h/hard-fork.asp
- **51% attack (real case):** Ethereum Classic 51% attacks 2020 — Bitcoin Magazine coverage

---

## 🎥 Video Study Guide (YouTube)

> Your video path for the whole unit — exact keywords to search (links rot, keywords don't) + channels you can trust.

### 🧑‍🎓 Step 0 — Pick your learning style

| Style | You learn best by | Your path through this unit |
|---|---|---|
| 🎧 **Listener** | short, clear explainers | 1 explainer per topic in the table below |
| 🛠️ **Builder** | writing code yourself | Watch the build-along → run [P05](../practicals/writeups/P05_nonce_mining_difficulty.md) & [P06](../practicals/writeups/P06_wallets_mnemonic_bip39.md), then break them |
| 🔧 **Tinkerer** | experimenting & demos | Watch demo videos → change the difficulty/halving constants in P05 and watch blocks slow/speed |
| 🧠 **Deep Diver** | full theory, "why" | Playlists at the bottom (university-level depth) |
| 🧭 **Explorer** | breadth & curiosity | Classic "how bitcoin works" explainers first |
| 🎓 **Academic** | exam marks | Watch revision videos → grind the PYQ map above |

### 🎬 Step 1 — Watch by topic (search these on YouTube)

| Topic | YouTube search keywords (copy-paste ready) | Best channels | Style served |
|---|---|---|---|
| What is bitcoin (overview) | `what is bitcoin explained simply` · `how bitcoin works 5 minutes` | Simply Explained, 3Blue1Brown | 🧭 Explorer |
| UTXO model | `utxo vs account model` · `what is utxo bitcoin` · `bitcoin unspent transaction outputs` | Bitcoin Dev, Blockgeeks | 🎧 + 🎓 |
| Wallets & seed phrases | `how bitcoin wallets work` · `bip39 seed phrase explained` · `hot vs cold wallet` | Andreas Antonopoulos, Simply Explained | 🎓 Academic |
| Mining & difficulty | `bitcoin mining explained` · `proof of work explained` · `bitcoin difficulty explained` | Computerphile, 3Blue1Brown, Fireship | 🧠 Deep Diver |
| Mempool → block | `bitcoin mempool explained` · `how a bitcoin transaction is confirmed` · `fee rate priority mempool` | Coin Bureau, Bitcoin Dev | 🧭 + 🎧 |
| Halving economics | `bitcoin halving explained` · `why bitcoin halving matters` · `bitcoin halving history` | Coin Bureau, Real Vision | 🎓 Academic |
| Build your own (hands-on) | `build a blockchain in python` · `bitcoin from scratch python code` · `proof of work python implementation` | freeCodeCamp, build-along devs | 🛠️ Builder |
| PoS & slashing | `proof of stake explained` · `what is slashing ethereum` · `ethereum merge how it works` | Finematics, Simply Explained, Coin Bureau | 🧠 + 🎧 |
| PoW vs PoS | `proof of work vs proof of stake` · `pow vs pos which is better` | Finematics, Coin Bureau | 🎓 Academic |
| 51% attack & Sybil | `51 percent attack explained` · `sybil attack explained with example` · `how to double spend bitcoin` | Computerphile, Simply Explained | 🧠 Deep Diver |
| Forks | `hard fork vs soft fork bitcoin` · `bitcoin cash fork explained` · `what is a fork in blockchain` | Simply Explained, Blockgeeks | 🎓 Academic |
| Whole-unit revision | `bitcoin and proof of work full lecture` · `cryptocurrency basics full course` · `bitcoin mining exam revision` | MIT OCW, freeCodeCamp, Gate Smashers, Neso Academy | 🎓 Academic |

### 🎬 Step 2 — Full playlists (for Deep Divers & Academics)

1. **"MIT 15.S12 Blockchain and Money"** — the Bitcoin & money lectures are the definitive treatment of this unit.
2. **"Andreas Antonopoulos — Bitcoin overview & technical deep dives"** — best developer-grade intuition for UTXOs, mining, and keys.
3. **"3Blue1Brown — But how does Bitcoin actually work?"** (single video) — the one video that makes PoW click.

### 🎬 Step 3 — Proof you got it (5 min)

- Run [P05](../practicals/writeups/P05_nonce_mining_difficulty.md), crank the difficulty up, and watch the mining time explode — that's the 10-minute-block idea in miniature.
- Re-draw the mempool → block → confirmations diagram from memory.
- Explain to a friend why a 51% attacker can double-spend *their own* coins but can't steal yours.

---

*Next: [UNIT 3 — Ethereum & Smart Contracts](./UNIT_3_Ethereum_and_Smart_Contracts.md)*
