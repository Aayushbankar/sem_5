# P08 — Tokenization: Deploying a Basic ERC-20 Token

**Subject:** Foundation of Blockchain | **Unit:** 3 | **Approx. Hrs:** 4
**PrO (verbatim):** *To understand tokenization by deploying a basic ERC-20 token contract. Tools Required: Remix IDE.*

---

## 1. Objective
- Understand **tokenization** and the **ERC-20 standard**.
- Deploy a minimal, standards-compliant **ERC-20** token in Remix.
- Interact: `transfer`, `approve`, `transferFrom`, check balances.

## 2. Theory (exam-ready)

### Ether (ETH) vs Tokens
- **ETH** is the *native* asset of Ethereum — part of the protocol (gas).
- **Tokens** are *smart contracts* implementing a standard. ERC-20 = the fungible-token standard.

### What the ERC-20 standard mandates
| Function | Purpose |
|---|---|
| `totalSupply()` | Total tokens in existence. |
| `balanceOf(addr)` | Balance of an account. |
| `transfer(to, value)` | Move tokens directly (msg.sender → to). |
| `approve(spender, value)` | Allow another address to spend up to `value`. |
| `transferFrom(from, to, value)` | Move tokens using an allowance (for DEXs, contracts). |
| `allowance(owner, spender)` | Check remaining allowance. |
| `event Transfer(from, to, value)` | Log every movement. |
| `event Approval(owner, spender, value)` | Log approvals. |

### Tokenization concept
- Converting a real-world or digital asset into a **blockchain token** (a divisible, transferable, provably scarce unit).
- Example used here: **Green Energy Token (GET)** — 1 token = 1 kWh of green energy, tradeable on-chain.

### decimals
- Tokens use 18 decimals by convention (`1 GET = 10^18` base units) — same as ETH (wei). `transfer` amounts are in base units.

### OpenZeppelin
- Industry-standard audited contracts library. `import "@openzeppelin/contracts/token/ERC20/ERC20.sol";` gives you a battle-tested token. Our manual version implements the same interface with `require` guards so the concepts are visible.

## 3. Steps Performed (Remix)
1. New file `GreenEnergyToken.sol` in Remix; paste code below; compile `0.8.20+`.
2. Deploy with constructor arg `1000000` (1M tokens) → check `totalSupply`, `balanceOf(deployer)` = `1000000000000000000000000` (1M × 10¹⁸).
3. **transfer:** send `1000` tokens to a second account → check both balances; `Transfer` event emitted.
4. **approve + transferFrom:** approve a second account for `500`; from that account call `transferFrom` → allowance decreases, balances move.
5. **Error cases:** try transferring more than balance → Remix shows the revert reason (`ERC20: insufficient balance`).
6. **Optional:** same steps with the OpenZeppelin `ERC20` import for comparison.

## 4. Code
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract GreenEnergyToken {
    string public name = "Green Energy Token";
    string public symbol = "GET";
    uint8 public decimals = 18;
    uint256 public totalSupply;

    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);

    constructor(uint256 _initialSupply) {
        totalSupply = _initialSupply * 10 ** decimals;
        balanceOf[msg.sender] = totalSupply;
        emit Transfer(address(0), msg.sender, totalSupply);
    }

    function transfer(address to, uint256 value) external returns (bool) {
        require(to != address(0), "ERC20: transfer to zero address");
        require(balanceOf[msg.sender] >= value, "ERC20: insufficient balance");
        balanceOf[msg.sender] -= value;
        balanceOf[to] += value;
        emit Transfer(msg.sender, to, value);
        return true;
    }

    function approve(address spender, uint256 value) external returns (bool) {
        allowance[msg.sender][spender] = value;
        emit Approval(msg.sender, spender, value);
        return true;
    }

    function transferFrom(address from, address to, uint256 value) external returns (bool) {
        require(to != address(0), "ERC20: transfer to zero address");
        require(balanceOf[from] >= value, "ERC20: insufficient balance");
        require(allowance[from][msg.sender] >= value, "ERC20: insufficient allowance");
        allowance[from][msg.sender] -= value;
        balanceOf[from] -= value;
        balanceOf[to] += value;
        emit Transfer(from, to, value);
        return true;
    }
}
```

> Contract file: [`P08_GreenEnergyToken.sol`](../code/P08_GreenEnergyToken.sol)

## 5. Expected Output
- **Deploy (1,000,000):** `totalSupply = 1000000000000000000000000`
- **transfer (1000 to B):** `balanceOf[A]` ↓, `balanceOf[B] = 1000000000000000000` (1000 × 10¹⁸); `Transfer(A, B, 1000)` event.
- **approve(B, 500) + transferFrom(A, C, 500) by B:** `allowance(A,B)` = 0; `balanceOf[C]` +500.
- **Over-transfer:** revert `"ERC20: insufficient balance"`.

## 6. Conclusion
A token is a smart contract following ERC-20. `transfer`/`approve`/`transferFrom` give the full transfer + allowance model used by exchanges, DEXs, and DAO treasuries. Tokenization turns any asset into divisible, programmable, provably scarce on-chain units.

## 7. Viva Q&A
1. **Difference between ETH and an ERC-20 token?** — ETH is native protocol asset (pays gas); ERC-20 is a smart contract implementing a standard.
2. **Why use `transferFrom`?** — Lets a third party (e.g., a DEX contract) spend on your behalf after approval.
3. **What is an allowance?** — The amount a spender is authorized to pull from an owner's balance.
4. **Why 18 decimals?** — Convention to avoid precision loss (mirrors wei).
5. **What is a "standard" like ERC-20?** — An interface definition (EIP) that wallets/exchanges can rely on.

## 8. Resources
- EIP-20 spec: https://eips.ethereum.org/EIPS/eip-20
- OpenZeppelin ERC-20: https://docs.openzeppelin.com/contracts/4.x/erc20
- Remix IDE: https://remix.ethereum.org
- CryptoZombies (token lessons): https://cryptozombies.io
