# UNIT 3 — Ethereum & Smart Contracts 🟣

**Syllabus weightage:** 12 hrs / **30%** — the biggest unit. | **Related practicals:** [P07](../practicals/writeups/P07_hello_world_smart_contract_remix.md), [P08](../practicals/writeups/P08_erc20_green_energy_token.md)
**Star guide:** ⭐ = likely · ⭐⭐ = very likely · ⭐⭐⭐ = practically guaranteed in some form

---

## 🧭 Chapter Roadmap

```
UNIT 3: Ethereum & Smart Contracts  (30% — biggest marks chunk)
├── 3.1 Ethereum Essentials
│     ├── 3.1.1 Ethereum Virtual Machine (EVM) & Gas Fees  ⭐⭐
│     └── 3.1.2 Ether (ETH) vs Tokens (ERC-20 basics)      ⭐⭐⭐ (adv/disadv asked 4×)
├── 3.2 Introduction to Solidity
│     ├── 3.2.1 Syntax: variables, functions, mappings     ⭐⭐
│     ├── 3.2.2 Writing "Hello World" smart contract       ⭐ (→ P07)
│     ├── 3.2.3 Compiling & deploying on a testnet (Remix) ⭐
│     └── 3.2.4 Introduction to MetaMask                   ⭐
└── Related concepts examiners love from this unit:
      ├── Smart contracts: definition, features, working   ⭐⭐⭐
      ├── Bitcoin vs Ethereum / Blockchain vs Bitcoin      ⭐⭐⭐
      ├── dApps                                           ⭐⭐
      └── ERC-20 advantages & disadvantages                ⭐⭐⭐
```

### Learning outcomes — after this unit you can:
- Explain the **EVM** (the "world computer") and why **gas** exists
- Define ETH, tokens, and ERC-20; list the standard's advantages & disadvantages (repeated 4 times in PYQ!)
- Read and write basic Solidity — variables, functions, mappings (see P07/P08)
- Compare **Bitcoin vs Ethereum** and **Blockchain vs Bitcoin** cleanly (both asked)
- Explain smart-contract features, working mechanism, and applications

---

## 3.1 Ethereum Essentials

### 3.1.1 Ethereum Virtual Machine (EVM) & Gas Fees ⭐⭐

**Ethereum** (Vitalik Buterin, 2015) is a *programmable blockchain*: anyone can deploy **code that runs exactly as written**. Bitcoin answers "who spent what?"; Ethereum answers "what did this program compute?"

- The **EVM (Ethereum Virtual Machine)** is the runtime that executes every smart contract, on every full node, identically. It makes Ethereum a **"world computer"** — deterministic, tamper-proof, decentralized.
- Every contract call costs **gas** — a fee paid in ETH measured per operation. **Why gas exists:**
  1. **Prevents infinite loops** — a contract that loops forever would otherwise stall nodes; gas runs out and execution stops.
  2. **Compensates miners/validators** for computing your contract.
  3. **Prices scarce compute** — more complex operations cost more gas (`SSTORE` ≫ `ADD`).
- Gas math: `tx cost = gasUsed × gasPrice`. `gasLimit` is your budget ceiling; unused gas is refunded. A gas-starved tx reverts but **still burns the used gas**.
- Gas helps **Turing-complete-but-bounded** execution: the EVM can compute anything, but only within a paid budget.

### 3.1.2 Ether (ETH) vs Tokens (ERC-20 basics) ⭐⭐⭐

| | ETH (native) | ERC-20 token (programmable) |
|---|---|---|
| What is it | Native currency of Ethereum | A smart contract defining its own ledger |
| Lives in | Protocol-level balance | Contract storage (a mapping of balances) |
| Who creates | The network itself (mining/staking) | Anyone — deploy a contract |
| Used for | Paying gas, staking, store of value | Anything: stablecoins (USDC), project coins, utility |
| Transfer | Native transfer opcode | Function call `transfer(to, amount)` |

**ERC-20** = the standard interface every token contract must implement so wallets/exchanges handle it uniformly:
`totalSupply()`, `balanceOf()`, `transfer()`, `transferFrom()`, `approve()`, `allowance()` + events `Transfer`, `Approval`. (See [P08](../practicals/writeups/P08_erc20_green_energy_token.md).)

**Advantages of ERC-20 (S24 Q.5(a), S26 Q.4(b)-alt, S25 Q.5(b)):**
1. **Interoperability** — standard interface works in every wallet/exchange instantly.
2. **Easy creation** — anyone can launch a token with a few lines of code; no ICO required for basic use.
3. **Liquidity & market depth** — listed on all major exchanges, huge adoption.
4. **Reusability** — developers inherit battle-tested standards instead of writing token logic.
5. **Smart-contract composability** — ERC-20s plug into DeFi (lending, DEXes) directly.

**Disadvantages of ERC-20 (S24 Q.5(a)-alt, S26 Q.4(b)):**
1. **ERC-20 transfer vs transferFrom bug** — naive contracts accept tokens but can't move them ("stuck tokens" forever).
2. **No refund on failed transfer** — sending tokens to a contract that can't receive them locks them permanently.
3. **No built-in minting limit / governance** — the deployer controls supply; rug pulls possible.
4. **Approval phishing** — unlimited `approve()` grants let scammers drain wallets.
5. **Blockchain congestion** — gas spikes during network stress make small transfers unviable.

---

## 3.2 Introduction to Solidity

**Solidity** = the main smart-contract language, C-like syntax, compiled to EVM bytecode.

### 3.2.1 Solidity Syntax: Variables, Functions, and Mappings ⭐⭐

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract Counter {
    uint public count;                    // state variable (persisted on-chain)
    mapping(address => uint) public scores; // key → value storage

    function increment() public {         // mutates state → costs gas
        count += 1;
    }

    function setScore(address who, uint s) external {  // external = cheaper caller-side
        scores[who] = s;
    }

    function readScore(address who) public view returns (uint) {  // view = free
        return scores[who];
    }
}
```

- **Types:** `uint`/`int` (sizes 8–256), `bool`, `address`, `bytes`, `string`, arrays, structs, **mappings**.
- **Visibility:** `public` (auto-getter), `private` (contract only), `internal` (contract + derived), `external` (only outside).
- **Storage & gas:** `storage` (persistent, expensive) vs `memory` (temporary, cheap) vs `calldata`.
- **`view`/`pure`** functions read nothing / modify nothing → **free**, no gas.
- **`msg.sender`** = the caller's address (the "who" of every call) — the backbone of access control.
- **Events** (`emit`) are cheap logs dApps read off-chain to track what happened.

### 3.2.2 Writing "Hello World" — the classic first contract

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract HelloWorld {
    string public message = "Hello, Blockchain!";

    function setMessage(string calldata newMsg) public {
        message = newMsg;
    }
}
```
Deployed in Remix → a `setMessage` call costs gas; `message()` reads are free. Full walkthrough with screenshots in [P07](../practicals/writeups/P07_hello_world_smart_contract_remix.md).

### 3.2.3 Compiling & Deploying on a Testnet (Remix IDE) ⭐

1. **Remix IDE** (`remix.ethereum.org`) — browser IDE; compile tab turns Solidity → ABI + bytecode.
2. Compile → check the green check; ABI is what external tools need to call your contract.
3. **Deploy** → pick environment:
   - *JavaScript VM* — instant, fake, for learning.
   - *Injected Provider (MetaMask)* → deploy to a **testnet** (Sepolia) with **faucet ETH** (free test coins).
4. Testnet = mainnet replica, costs nothing real. Every contract call there behaves identically to mainnet.

### 3.2.4 Introduction to MetaMask ⭐

- MetaMask = browser extension **wallet** → holds your private keys, signs transactions, shows balances.
- Connects dApps to Ethereum via **Injected Provider** (the dApp never sees your private key; MetaMask signs for you).
- Parts: account address (`0x…`), secret recovery phrase (12 words = your seed), network switcher (Mainnet/Sepolia/…), gas controls.
- Security rule: the seed phrase **never leaves MetaMask**; "support agents" and "validation sites" asking for it are scams.

---

## 🧠 Deep-Dive Topics

### Deep Dive A: The EVM execution model, step by step
1. A user calls `transfer(...)` on a token contract via MetaMask.
2. MetaMask builds the calldata + signs it; the tx is broadcast.
3. Every node runs the SAME bytecode on the SAME state → deterministic result. This determinism is what lets nodes agree without trusting each other.
4. Gas is deducted as each opcode runs; if the budget runs out, execution **reverts** (state rolled back), but the spent gas is gone.
5. Result: the contract's storage updated, an event emitted, and all nodes store the identical new state. The "world computer" is really *millions of parallel copies agreeing on one answer*.

### Deep Dive B: Why ERC-20 "transfer vs transferFrom" matters (the stuck-token bug)
- `transfer()` moves YOUR tokens to a recipient.
- `approve(spender, amount)` + `transferFrom(spender→sender→to)` lets a *third party* (a DEX contract) pull tokens you approved.
- Classic bug: contract asks users to `transfer()` directly but the contract never gets custody → tokens arrive at the contract address and are **unrecoverable** (no function to move them). This is why P08 follows the standard strictly.

### Deep Dive C: Bitcoin vs Ethereum — the 4-marker answer, memorized
| | Bitcoin | Ethereum |
|---|---|---|
| Purpose | Decentralized digital cash | Programmable "world computer" |
| Programming | Limited Bitcoin Script (not Turing-complete) | Solidity → EVM (Turing-complete, gas-bounded) |
| Model | UTXO | Account balance |
| Consensus | PoW (mining) | PoS (since The Merge 2022) |
| Block time | ~10 min | ~12 sec |
| Assets | BTC only | ETH + unlimited ERC-20 tokens/NFTs |
| Fees | Fee market, byte-size based | Gas per operation |

**Blockchain vs Bitcoin** — *Blockchain* is the distributed-ledger *technology*; *Bitcoin* is one specific *application* built on it (its first and largest). Blockchain exists without Bitcoin; Bitcoin doesn't exist without blockchain.

### Deep Dive D: Smart contracts — definition, features, working, applications (the 7-marker)
- **Definition:** a self-executing program stored on the blockchain that runs exactly as written, automatically enforcing an agreement without intermediaries.
- **Features:** (1) self-executing/automatic, (2) immutable once deployed, (3) trustless (no middleman), (4) transparent (public code + state), (5) deterministic, (6) decentralized.
- **Working:** developer writes contract in Solidity → compiles to bytecode → deploys (pays gas) → the EVM stores code on-chain → users trigger it via transactions/function calls → nodes execute deterministically → state changes + events → anyone can verify the outcome. Nobody — not even the deployer — can stop it once live.
- **Applications:** payments & escrow, DeFi (lending, DEX, stablecoins), NFTs & gaming, supply-chain provenance, identity, DAO governance, insurance (parametric payouts).

---

## 🚀 Beyond the Textbook (what most classes won't tell you)

- **"World computer" is a metaphor with a huge asterisk:** it's *incredibly slow and expensive* vs a normal computer — every opcode executes in parallel on every node, so you pay for redundancy.
- **You can't "change" a deployed contract.** You deploy a *new* version and migrate users — hence the "proxy contract" pattern in production.
- **A failed tx still costs money.** Users don't see the *state* roll back and assume refunds; only unused gas is returned.
- **ERC-20 is why DeFi exploded** — a single standard made composable finance (DEX→lending→stablecoin) possible.
- **Testnet ETH is free** (faucets). "I can't afford to learn" is never true for this unit.

---

## 📝 PYQ Map — UNIT 3 (all available papers)

| Paper | Q. | Topic | Marks |
|---|---|---|---|
| **Summer 2024** | Q.5(a) | Advantages of ERC-20 | 3 |
| | Q.5(b) | Working mechanism of a smart contract | 4 |
| | Q.5(c) | Smart contract — definition, features, applications | 7 |
| | Q.5(a)-alt | Disadvantages of ERC-20 | 3 |
| | Q.5(b)-alt | Steps to launch a DAO | 4 |
| | Q.5(c)-alt | DAO — advantages & disadvantages | 7 |
| **Winter 2024** | Q.4(b) | How does a smart contract work? | 4 |
| | Q.4(b)-alt | Types of smart contracts | 4 |
| | Q.5(b) | dApps — what & how they work | 4 |
| **Summer 2025** | Q.4(b) | Differentiate Blockchain and Bitcoin | 4 |
| | Q.5(b) | Advantages & disadvantages of ERC-20 | 4 |
| | Q.5(a)-alt | Tokenized vs token-less blockchain | 3 |
| **Summer 2026** | Q.4(b) | Disadvantages of ERC-20 | 4 |
| | Q.4(b)-alt | Advantages of ERC-20 | 4 |
| | Q.5(b)-alt | Steps to launch a DAO | 4 |
| | Q.5(a)-alt | Key features & applications of CORDA | 3 |
| **Winter 2025** | Q.4(b) | Compare Bitcoin and Ethereum | 4 |
| | Q.5(a) | Types of decentralization | 3 |
| | Q.5(b) | Working of a smart contract | 4 |
| | Q.5(a)-alt | Define smart contract + list features | 3 |
| | Q.5(b)-alt | Compare DAO vs Traditional organization | 4 |

### ✅ Solved PYQ answers (UNIT 3)

**W25 Q.5(b) — Working of a smart contract (4 marks).**
> A smart contract works through the following steps: **1. Authoring** — the contract is written in Solidity (variables, functions, mappings) defining the rules of the agreement. **2. Compilation** — it is compiled into EVM bytecode plus an ABI that describes its interface. **3. Deployment** — the bytecode is deployed to the blockchain in a transaction, paying gas; the code becomes permanently stored at a contract address, and **nobody can alter it**. **4. Invocation** — users trigger functions by sending transactions (e.g. `transfer`, `approve`, game moves); every call specifies the sender (`msg.sender`). **5. Execution** — each full node runs the same bytecode against the same state in the EVM, producing the **same deterministic result**, so nodes reach consensus without trusting each other. **6. Settlement & events** — state (storage/mappings) is updated, events are emitted for off-chain apps, and the outcome is permanently recorded. The contract acts as a **trustless escrow**: it enforces the coded rules automatically, with no human intermediary.

**S24 Q.5(c) — What is a smart contract? Features & applications (7 marks).**
> **Definition:** A smart contract is a self-executing computer program stored on the blockchain that automatically enforces and executes the terms of an agreement when predefined conditions are met, without needing a trusted third party. **Features:** (1) *Automatic & self-executing* — no human approval step; (2) *Immutable* — once deployed it cannot be changed, guaranteeing reliability; (3) *Trustless* — parties need not trust each other, only the code; (4) *Transparent* — code and state are public and verifiable by anyone; (5) *Deterministic* — same inputs always give the same output, enabling consensus; (6) *Decentralized* — runs on every node, so there is no single point of failure. **Working (brief):** written in Solidity → compiled to EVM bytecode → deployed in a transaction paying gas → triggered by function calls → executed identically on all nodes. **Applications:** digital payments & escrow (funds released on condition), DeFi (lending, decentralized exchanges, stablecoins like USDC), NFTs & gaming assets, supply-chain provenance tracking, insurance with automatic payouts, DAO governance voting, and identity management.

**S26 Q.4(b) — Disadvantages of ERC-20 (4 marks).**
> 1. **Token-transfer bug:** ERC-20 has separate `transfer()` and `transferFrom()`; contracts that receive tokens but only implement `transfer()` cannot move them, permanently **locking funds**.
> 2. **No refund on failed transfer:** tokens sent to a contract address that cannot receive them are **lost forever**.
> 3. **No supply or governance limits:** the deploying contract controls minting, enabling dilution or **rug-pull** schemes.
> 4. **Approval-phishing risk:** users granting unlimited `approve()` let malicious contracts drain their entire balance later.
> 5. **Congestion sensitivity:** during network congestion, high gas fees make micro-transactions uneconomical.

**W25 Q.4(b) — Compare Bitcoin and Ethereum (4 marks).** — see Deep Dive C table (memorize the 6 rows).

**S24 Q.5(a)-alt — Disadvantages of ERC-20 (3 marks).** — take any 3 of the 5 points above.

**S25 Q.5(a)-alt — Tokenized vs token-less blockchain (3 marks).**
> A **tokenized blockchain** issues its own digital tokens to incentivize the network and transfer value (e.g. Bitcoin's BTC, Ethereum's ETH and ERC-20 tokens); tokens fuel transaction fees, staking, and DAO voting. A **token-less (or token-free) blockchain** has **no native cryptocurrency**; it is designed purely for enterprise data sharing, with access controlled by permissioned identity rather than token economics (e.g. **Hyperledger Fabric**, CORDA — permissioned networks where participants are known). In short: tokenized = public, incentive-driven, crypto-priced; token-less = permissioned, identity-driven, no coins.

---

## ✍️ Practice Problems (self-test — answers upside-down)

1. (3) What is the EVM? Why is gas required to run a contract?
2. (4) Differentiate ETH and ERC-20 tokens.
3. (7) With a diagram/flow, explain how a smart contract is created and executed.
4. (4) List and explain any four ERC-20 functions.
5. (3) Why can `view` functions be called without paying gas?
6. (4) Differentiate Blockchain and Bitcoin.
7. (3) What is MetaMask? Why must the seed phrase never be shared?
8. (4) Write a minimal Solidity contract with a `mapping` and a function that updates it.

<details>
<summary><b>Click for answers</b></summary>

1. EVM = Ethereum Virtual Machine, the runtime executing every smart contract on every node deterministically. Gas exists to (a) stop infinite loops, (b) pay validators, (c) price scarce compute — and to keep the "world computer" Turing-complete *but* budget-bounded.
2. ETH is Ethereum's native currency (pays gas, stake, store of value); ERC-20 tokens are programmable contracts implementing a standard interface (balanceOf/transfer/approve) — used for stablecoins, project coins, utility.
3. Author → compile (bytecode+ABI) → deploy (gas) → store at address → users call functions (`msg.sender`) → EVM runs deterministically on all nodes → state updated + events → immutable, verifiable.
4. `totalSupply()`, `balanceOf(addr)`, `transfer(to, amount)`, `transferFrom(from,to,amount)` (needs `approve()`), `allowance(owner,spender)` — the last two enable third-party contracts (DEXes) to pull funds.
5. `view` functions only read state and return data to the caller's local node — nothing is broadcast or stored, so no computation is executed on-chain and no gas is charged.
6. Blockchain = the underlying distributed-ledger technology (blocks, hashes, consensus); Bitcoin = one application built on it — a decentralized digital cash system. Blockchain is the platform; Bitcoin is a specific instance.
7. MetaMask = browser-extension wallet holding your private keys and signing transactions. The seed phrase derives all keys — anyone who has it owns everything, and there is no recovery or customer support.
8. See the `Counter` contract in §3.2.1 — a `mapping(address => uint) public scores` + `setScore()`/`readScore()` demonstrates it.

</details>

---

## 📖 Glossary of Key Terms

| Term | One-line meaning |
|---|---|
| EVM | Ethereum Virtual Machine — the deterministic runtime for smart contracts |
| Gas | Unit of computation cost paid in ETH to run contract code |
| Gas limit / gas price | Max gas you budget / amount you pay per unit |
| ETH | Ethereum's native cryptocurrency |
| ERC-20 | Standard interface for fungible tokens |
| Solidity | Main smart-contract programming language |
| State variable | Data permanently stored on-chain by a contract |
| Mapping | Key→value storage structure in Solidity |
| msg.sender | Address that called the current function |
| ABI | Application Binary Interface — how apps call a contract |
| Testnet / faucet | Free practice network / service giving free test ETH |
| MetaMask | Browser wallet that signs transactions for dApps |
| dApp | Decentralized application (frontend + smart contracts) |
| Immutable | Cannot be changed after deployment |

---

## 🔗 Curated Resources (per concept)

- **Ethereum & EVM:** https://ethereum.org/en/developers/docs/evm/
- **Gas:** https://ethereum.org/en/developers/docs/gas/ | *Mastering Ethereum* Ch. 1, 13
- **ERC-20 spec:** https://eips.ethereum.org/EIPS/eip-20
- **Solidity docs (official):** https://docs.soliditylang.org/
- **Remix IDE:** https://remix.ethereum.org | **Sepolia faucet:** https://faucet.sepolia.dev
- **MetaMask:** https://metamask.io (only ever install from the official store)
- **Smart contracts:** https://ethereum.org/en/smart-contracts/

---

## 🎥 Video Study Guide (YouTube)

> Your video path for the whole unit — exact keywords to search + channels you can trust.

### 🧑‍🎓 Step 0 — Pick your learning style

| Style | You learn best by | Your path through this unit |
|---|---|---|
| 🎧 **Listener** | short, clear explainers | 1 explainer per topic in the table below |
| 🛠️ **Builder** | writing code yourself | Watch the build-along → deploy [P07](../practicals/writeups/P07_hello_world_smart_contract_remix.md) & [P08](../practicals/writeups/P08_erc20_green_energy_token.md) in Remix |
| 🔧 **Tinkerer** | experimenting & demos | Deploy on Sepolia with a faucet; break the token contract and watch reverts |
| 🧠 **Deep Diver** | full theory, "why" | Playlists at the bottom |
| 🧭 **Explorer** | breadth & curiosity | Start with "how ethereum works" explainers |
| 🎓 **Academic** | exam marks | Revision videos → grind the PYQ map above |

### 🎬 Step 1 — Watch by topic (search these on YouTube)

| Topic | YouTube search keywords (copy-paste ready) | Best channels | Style served |
|---|---|---|---|
| Ethereum overview | `what is ethereum explained` · `ethereum in 5 minutes` · `how ethereum works` | Simply Explained, Fireship | 🧭 Explorer |
| EVM | `ethereum virtual machine explained` · `what is the evm` · `evm vs bitcoin script` | Fireship, Finematics, Coin Bureau | 🧠 Deep Diver |
| Gas fees | `ethereum gas fees explained` · `why are gas fees so high` · `how gas works ethereum` | Coin Bureau, Finematics | 🎧 + 🎓 |
| ETH vs tokens / ERC-20 | `erc20 tokens explained` · `ethereum token standard` · `what is an erc 20 token` | Simply Explained, Finematics | 🎓 Academic |
| Solidity basics | `solidity for beginners` · `learn solidity in 1 hour` · `solidity functions variables mappings` | freeCodeCamp, Dapp University, EatTheBlocks | 🛠️ Builder |
| Build hello world contract | `deploy your first smart contract remix` · `hello world solidity remix tutorial` | Dapp University, freeCodeCamp | 🛠️ Builder |
| Testnets & MetaMask | `how to use metamask 2026` · `sepolia testnet faucet how to get free eth` · `deploy contract on testnet` | EatTheBlocks, Coin Bureau | 🔧 + 🛠️ |
| Smart contracts deep | `what are smart contracts` · `how smart contracts work` · `smart contract use cases` | Simply Explained, Finematics, Coin Bureau | 🧠 Deep Diver |
| Bitcoin vs Ethereum | `bitcoin vs ethereum` · `btc vs eth comparison` | Coin Bureau, Finematics | 🎓 Academic |
| dApps | `what are dapps` · `how dapps work explained` · `decentralized applications examples` | Finematics, Simply Explained | 🎧 + 🧭 |
| Whole-unit revision | `ethereum and smart contracts full course` · `solidity full course for beginners` · `blockchain ethereum exam revision` | MIT OCW, freeCodeCamp, Gate Smashers, Neso Academy | 🎓 Academic |

### 🎬 Step 2 — Full playlists (for Deep Divers & Academics)

1. **"freeCodeCamp — Learn Solidity and smart contracts"** (long-form course) — the fastest way to become a Builder.
2. **"MIT 15.S12 Blockchain and Money — Ethereum & smart contracts lectures"** — exam-grade theory of this unit.
3. **"EatTheBlocks — Solidity & smart contract testing"** — if you want to Tinker beyond the syllabus.

### 🎬 Step 3 — Proof you got it (5 min)

- Deploy the [P08 token](../practicals/writeups/P08_erc20_green_energy_token.md) on Sepolia and mint/transfer to yourself.
- Explain to a friend why a failed transaction still costs gas.
- Say the 6 rows of the Bitcoin vs Ethereum table from memory.

---

*Next: [UNIT 4 — Enterprise & Private Blockchains](./UNIT_4_Enterprise_and_Private_Blockchains.md)*
