---
title: "P10 — Case Study Security Green Energy Dao"
sidebar:
  order: 10
---

# P10 — Case Study: Smart Contract Vulnerability + Green Energy DAO/Token

**Subject:** Foundation of Blockchain | **Unit:** 5 | **Approx. Hrs:** 2
**PrO (verbatim):** *Case Study 2: To identify a common security vulnerability and conceptualize a Green Energy DAO/Token system.*

---

## 1. Objective
- Identify a **common smart-contract vulnerability** (re-entrancy), understand the attack, and apply mitigations.
- Conceptualize a **Green Energy DAO + Token** system, including the **oracle problem**.

---

## Part A — Security Vulnerability: Re-entrancy

### A.1 What it is
A malicious contract **re-enters** a victim contract *before* the victim updates its balance/state, draining funds repeatedly — the famous **DAO hack (June 2016, ~$60M stolen from "The DAO")**.

### A.2 The vulnerable pattern (Checks-Effects-Interactions VIOLATED)
```solidity
// VULNERABLE: updates balance AFTER the external call
function withdraw() public {
    require(balances[msg.sender] >= amount);      // CHECK
    (bool ok, ) = msg.sender.call{value: amount}("");  // INTERACTION (external call)
    require(ok);
    balances[msg.sender] -= amount;               // EFFECT comes last -> BUG
}
```
Attack: attacker's `receive()` calls `withdraw()` again. Because `balances` is not yet updated, the `require` passes again → **recursive draining**.

### A.3 Fixes
| Fix | How |
|---|---|
| **Checks-Effects-Interactions** | Update state (`balances` minus) BEFORE making the external call. |
| **Re-entrancy guard** | `modifier nonReentrant` (OpenZeppelin `ReentrancyGuard`) — a lock flag. |
| **Pull payments** | Never push ETH directly; let users withdraw via a function (patterns like OpenZeppelin `PullPayment`). |
| **`transfer()` (deprecated)** | Old 2300-gas cap limited re-entry; do not rely on it in 2026, use guards. |

### A.4 Other common vulnerabilities (exam one-liners)
- **51% Attack** — entity with >50% hashrate (PoW) can reorg/reverse transactions.
- **Sybil Attack** — one adversary creates many fake identities to sway consensus/voting.
- **Integer overflow/underflow** — prevented automatically in Solidity ≥0.8 (reverts).
- **Oracle manipulation** — attacker moves an on-chain price feed to exploit lending/derivatives.
- **Front-running** — observing a pending tx and inserting your own first (MEV).

---

## Part B — Conceptual Design: Green Energy DAO/Token

### B.1 Vision
A DAO where members jointly own and govern **solar/wind energy assets**; energy production is **tokenized** (1 GET = 1 kWh) and tradeable; governance & treasury decisions are made by token voting.

### B.2 System components
| Component | Design |
|---|---|
| **Token** | ERC-20 `GET` (Green Energy Token) — 1 token = 1 kWh produced (see P08). |
| **DAO** | Governance contract; proposals + voting weight = GET balance; quorum rules. |
| **Treasury** | Multi-sig / DAO-controlled wallet holding revenue from energy sales. |
| **Oracles** | IoT sensors on inverters/meters feed real kWh production **off-chain → on-chain** (see B.4). |
| **Carbon/Green credits** | Credits minted against verified production; tradeable → liquidity for the DAO. |

### B.3 Token flows
```
Solar farm sensors ──► Oracle ──► GET minted (verified kWh)
                                  │
          ┌───────────────────────┼────────────────────────┐
          ▼                       ▼                        ▼
   Consumers pay GET        DAO members vote          Credits/DEX liquidity
   for green energy         on proposals             (buy/sell GET)
```

### B.4 The Oracle Problem (key exam concept)
- Blockchains are **deterministic & closed** — they cannot "see" the real world.
- **Oracle** = trusted bridge that brings external data (kWh readings) on-chain.
- **Problem:** *"How do we trust the data?"* A malicious oracle can mint tokens for electricity that was never produced.
- **Mitigations:**
  - **Decentralized oracles** (Chainlink): multiple independent sources + aggregation.
  - **IoT oracles:** signed readings from hardware attestation (TEE), tamper-resistant sensors.
  - **Reputation/slashing:** staked oracles lose collateral on false reports.
  - **Multi-source + majority:** only trust data confirmed by >N independent oracles.

### B.5 Tokenization of energy (why)
- Fractional ownership of expensive assets (community solar).
- Transparent production credits (fights **greenwashing**).
- Programmable settlement: revenue automatically split to investors every period.

---

## 3. Expected Deliverable (report skeleton)
1. Part A: pick the vulnerability (re-entrancy), diagram the attack flow, write the fix (`nonReentrant` guard), and explain 2 other vulnerabilities.
2. Part B: architecture diagram of the DAO (token, treasury, governance, oracle); write the oracle-data flow; list 3 oracle trust mitigations.
3. Conclusion: security + trust design is what separates a toy system from a production one.

## 4. Viva Q&A
1. **Which real-world event is the re-entrancy cautionary tale?** — The DAO hack, 2016 (~$60M).
2. **What is Checks-Effects-Interactions?** — Ordering rule: validate, update state, then call external contracts.
3. **What is the oracle problem?** — Trusting external/off-chain data sent into a deterministic blockchain.
4. **How do IoT oracles help green-energy tokenization?** — Signed, attested sensor data proves actual kWh → prevents fake token minting.
5. **What is greenwashing, and how does tokenization counter it?** — Falsely claiming eco-friendliness; verifiable on-chain credits make claims auditable.

## 5. Resources
- Solidity security docs (re-entrancy): https://docs.soliditylang.org/en/latest/security-considerations.html
- OpenZeppelin `ReentrancyGuard`: https://docs.openzeppelin.com/contracts/4.x/api/security
- The DAO hack explainer: https://en.wikipedia.org/wiki/The_DAO_(organization)
- Chainlink (decentralized oracles): https://chain.link/education/blockchain-oracles
- *Mastering Ethereum* (smart-contract security chapter)

---



---

## 🐛 Failure Modes & Debugging (Real-World Experience)

> [!bug] What goes wrong in production?
> When running **Case Study Security Green Energy Dao** in a real environment, it almost never works perfectly the first time. 
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

- **51% Attack** — entity with >50% hashrate (PoW) can reorg/reverse transactions.
- **Sybil Attack** — one adversary creates many fake identities to sway consensus/voting.
- **Integer overflow/underflow** — prevented automatically in Solidity ≥0.8 (reverts).
- **Oracle manipulation** — attacker moves an on-chain price feed to exploit lending/derivatives.
- **Front-running** — observing a pending tx and inserting your own first (MEV).
- **deterministic & closed** — they cannot "see" the real world.
- **Mitigations:** — **Decentralized oracles** (Chainlink): multiple independent sources + aggregation.
- **What is Checks-Effects-Interactions?** — Ordering rule: validate, update state, then call external contracts.

> [!tip] Viva Prep
> Be ready to explain the *why* behind each step, not just the output.
