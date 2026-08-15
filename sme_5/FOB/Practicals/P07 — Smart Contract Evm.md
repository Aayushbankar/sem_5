---
subject: FOB
status: not-started
tags: [subject/fob, practical, unit/3]
practical: 7
unit: 3
hours: 4
---
# P07 — Write, Compile & Deploy a Smart Contract on the EVM

**Subject:** Foundation of Blockchain | **Unit:** 3 | **Approx. Hrs:** 4
**PrO (verbatim):** *To write, compile, and deploy a basic smart contract on the Ethereum Virtual Machine (EVM).*

---

## 1. Objective
- Write a simple **Solidity** contract (`SimpleStorage`).
- Compile it in **Remix IDE** (free, no install).
- Deploy it to a **test network** (Sepolia) and interact with its functions.

## 2. Theory (exam-ready)

### Smart Contract
- Code + data deployed at an address on the blockchain; executes deterministically on the **EVM**.
- Once deployed it **cannot be changed** (immutability) — bugs are permanent unless a proxy pattern is used.
- Execution is paid in **gas**.

### Ethereum Virtual Machine (EVM)
- A deterministic, sandboxed runtime that executes EVM bytecode on every full node.
- Anyone can deploy code; every node produces the **same result** for the same input → consensus on state.

### Gas
- **Gas** = unit of computation. Each opcode has a fixed gas cost.
- `gas_used × gas_price` = transaction fee, paid in ETH. **State-changing ops cost gas; `view`/`pure` reads are free.**

### Solidity essentials (used here)
| Item | Purpose |
|---|---|
| `pragma solidity ^0.8.20` | Version pragma (breaks code if compiler < 0.8.20). |
| `contract X { }` | Contract definition. |
| `uint256 public n` | State variable → auto-generated getter; stored on-chain. |
| `function store(uint _x) public` | Changes state → costs gas. |
| `view` | Read-only, no gas. |
| `msg.sender` | Address that called the function. |
| `event` | Off-chain log the network records (cheap logs). |

### Accounts & deployment
- **EOA (Externally Owned Account)** — controlled by a private key (MetaMask).
- **Contract Account** — has code + storage, controlled by the contract.
- Deployment = a transaction (with code as data) sent from an EOA; you pay gas and get a **contract address**.

## 3. Steps Performed (Remix — free, no install)
1. Open https://remix.ethereum.org → **File Explorer** → `contracts/` → new file `SimpleStorage.sol`, paste the code below.
2. **Solidity Compiler** tab: select `0.8.20+` and **Compile**. Fix errors if any; bytecode + ABI are produced.
3. **Deploy & Run Transactions** tab:
   - Environment: choose **Remix VM** (local test, free) first; later **Injected Provider - MetaMask** for Sepolia.
   - Account: Remix VM gives you 10 test accounts.
   - Click **Deploy**; watch the transaction in the terminal (gas used shown).
4. Under **Deployed Contracts**: expand the contract →
   - Call `read()` → returns `0`.
   - Call `store(42)` → confirm, gas charged, event `NumberChanged` logged.
   - Call `read()` again → returns `42`. ✓

### Deploying to a real testnet (optional, for marks)
1. Install **MetaMask** browser wallet → create wallet (save seed phrase!).
2. Add **Sepolia testnet** network (faucet at https://sepoliafaucet.com for free test ETH).
3. In Remix select **Injected Provider - MetaMask**, pick your account, Deploy, approve the gas fee in MetaMask.
4. Get your contract address from Remix or etherscan (sepolia.etherscan.io).

## 4. Code
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract SimpleStorage {
    uint256 public storedNumber;

    event NumberChanged(address indexed by, uint256 oldValue, uint256 newValue);

    function read() public view returns (uint256) {
        return storedNumber;
    }

    function store(uint256 _newNumber) public {
        uint256 oldValue = storedNumber;
        storedNumber = _newNumber;
        emit NumberChanged(msg.sender, oldValue, _newNumber);
    }

    function whoAmI() public view returns (address) {
        return msg.sender;
    }
}
```

> Contract file: [[P07_SimpleStorage.sol|`P07_SimpleStorage.sol`]]

## 5. Expected Output
- **Compile:** green check, ABI + bytecode generated, no warnings.
- **Deploy (Remix VM):** terminal shows `[vm] contract created` + contract address `0x…`.
- **Interactions:**
  - `read()` → `0: uint256: 0`
  - `store(42)` → transaction confirmed (≈ 26,000+ gas), event logged
  - `read()` → `0: uint256: 42`
  - `whoAmI()` → your account address `0x…`

## 6. Conclusion
A smart contract is ordinary code compiled to EVM bytecode, deployed via a transaction, and executed on-chain for gas. The deployed address is the contract's permanent identity; any EOA can interact with its public functions.

## 7. Viva Q&A
1. **What does the EVM guarantee?** — Deterministic execution: same input → same state on every node.
2. **What is gas and why does it exist?** — It prices computation, preventing infinite loops/DoS and paying nodes.
3. **Can you edit a deployed contract?** — No; bytecode is immutable (use upgrade/proxy patterns if needed).
4. **Difference between EOA and contract account?** — EOA is key-controlled; contract account is code-controlled and has no private key.
5. **What is `msg.sender`?** — The address of whoever triggered the current call.

## 8. Resources
- Remix IDE: https://remix.ethereum.org
- Solidity docs: https://docs.soliditylang.org
- CryptoZombies (interactive Solidity course): https://cryptozombies.io
- Cyfrin Updraft (free Solidity bootcamp): https://updraft.cyfrin.io
- Sepolia faucet: https://sepoliafaucet.com

---



---

## 🐛 Failure Modes & Debugging (Real-World Experience)

> [!bug] What goes wrong in production?
> When running **Smart Contract Evm** in a real environment, it almost never works perfectly the first time. 
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

- **EOA (Externally Owned Account)** — controlled by a private key (MetaMask).
- **Contract Account** — has code + storage, controlled by the contract.
- **Deployed Contracts** — expand the contract →
- **Interactions:** — `read()` → `0: uint256: 0`
- **What does the EVM guarantee?** — Deterministic execution: same input → same state on every node.
- **What is gas and why does it exist?** — It prices computation, preventing infinite loops/DoS and paying nodes.
- **Can you edit a deployed contract?** — No; bytecode is immutable (use upgrade/proxy patterns if needed).
- **Difference between EOA and contract account?** — EOA is key-controlled; contract account is code-controlled and has no private key.

> [!tip] Viva Prep
> Be ready to explain the *why* behind each step, not just the output.
