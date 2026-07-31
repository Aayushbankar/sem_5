---
title: "P03 — Basic Blockchain Python"
sidebar:
  order: 3
---

# P03 — Basic Blockchain Structure in Python

**Subject:** Foundation of Blockchain | **Unit:** 1 | **Approx. Hrs:** 2
**PrO (verbatim):** *To create a basic blockchain structure in Python demonstrating how blocks are cryptographically linked.*

---

## 1. Objective
- Build a minimal blockchain as a Python list of `Block` objects.
- Each block stores: **index, timestamp, data, previous_hash, nonce**.
- Each block's own hash = `SHA-256(index + timestamp + data + previous_hash + nonce)`.
- Prove **tamper-evidence**: modifying one block invalidates every subsequent block.

## 2. Theory (exam-ready)

### The anatomy of a block
| Field | Meaning |
|---|---|
| **Index** | Position of the block in the chain (0 = genesis). |
| **Timestamp** | When the block was created. |
| **Data** | Transactions or payload. |
| **Previous Hash** | Hash of the block that came before → this is the cryptographic link. |
| **Hash** | `SHA-256` of everything in the block including `previous_hash`. |

### How blocks are "linked"
```
Genesis ──prev: 0x000...000──► Block 1 ──prev: hash0──► Block 2 ──prev: hash1──► Block 3
hash = SHA256(genesis)          hash = SHA256(b1)      hash = SHA256(b2)
```
- `hash_n = SHA256(n + data + hash_{n-1})`. Because the previous hash is *inside* the next block's hash input, the chain is **cryptographically chained**.
- **Tamper-evidence:** change any byte in block *i* → its hash changes → block *i+1*'s `previous_hash` no longer matches → whole chain is flagged invalid.

### Genesis block
- The first block (index 0), created manually with `previous_hash = "0"*64`. Its content is trusted by everyone as the start of the chain.

## 3. Steps Performed
1. Define `Block` class with `compute_hash()` using `hashlib.sha256`.
2. Define `SimpleBlockchain` with a `create_genesis_block()`.
3. Add 3 transaction blocks (each chained to the previous).
4. Run `is_valid()` → verifies each block's stored hash matches a recomputation and `previous_hash` matches the prior block.
5. Tamper with block 1 (`"1 coin"` → `"100 coins"`), re-run validity → chain invalid.

## 4. Code
```python
import hashlib, json, time
from typing import List

class Block:
    def __init__(self, index, timestamp, data, previous_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = json.dumps({
            "index": self.index, "timestamp": self.timestamp,
            "data": self.data, "previous_hash": self.previous_hash,
            "nonce": self.nonce}, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

class SimpleBlockchain:
    def __init__(self):
        self.chain: List[Block] = [self.create_genesis_block()]
    def create_genesis_block(self):
        return Block(0, time.time(), "Genesis Block", "0"*64)
    def add_block(self, data):
        prev = self.chain[-1]
        block = Block(prev.index+1, time.time(), data, prev.hash)
        self.chain.append(block); return block
    def is_valid(self):
        for i in range(1, len(self.chain)):
            cur, prev = self.chain[i], self.chain[i-1]
            if cur.hash != cur.compute_hash(): return False
            if cur.previous_hash != prev.hash: return False
        return True
    def tamper(self, index, new_data):
        self.chain[index].data = new_data
```

> Full runnable script: [`p03_blockchain.py`](./p03_blockchain.py.md)

## 5. Expected Output (actual run)
```
[1] Blockchain after adding 4 blocks (genesis + 3):
Idx Data                        Previous hash     Hash
0   Genesis Block               0000000000000000  bdb16bbff0518dcc
1   Student A sends 1 coin to   bdb16bbff0518dcc  00a017f696a0fdba
2   Student C sends 2 coins to  00a017f696a0fdba  67b74a82858027bd
3   Student A sends 0.5 coin t  67b74a82858027bd  43522bf7d32b2b81

[2] Chain validity check:  VALID ✓

[3] Tampering: change data of block index 1
[4] Chain validity check after tampering:  INVALID ✗
```

## 6. Conclusion
Every block's hash embeds the previous block's hash, producing a chain where any tampering is immediately detectable. This is the core integrity mechanism behind real blockchains like Bitcoin.

## 7. Viva Q&A
1. **What links two adjacent blocks?** — The `previous_hash` stored in the later block.
2. **Why is a chain valid only if every link matches?** — Because a changed block alters its own hash and therefore the next block's stored `previous_hash`, cascading to the end.
3. **What is a genesis block?** — Block 0, hard-coded, the trust root of the chain.
4. **Why store `previous_hash` instead of just index?** — The hash cryptographically commits to the entire previous block's content; an index alone proves nothing.

## 8. Resources
- *Mastering Bitcoin*, Ch. 9 "The Blockchain": https://github.com/bitcoinbook/bitcoinbook
- Anders Brownworth's Blockchain demo (visual): https://andersbrownworth.com/blockchain/
- Blockchain structure explained: https://en.wikipedia.org/wiki/Blockchain#Structure_and_design

---



---

## 🐛 Failure Modes & Debugging (Real-World Experience)

> [!bug] What goes wrong in production?
> When running **Basic Blockchain Python** in a real environment, it almost never works perfectly the first time. 
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

- **tamper-evidence** — modifying one block invalidates every subsequent block.
- **What links two adjacent blocks?** — The `previous_hash` stored in the later block.
- **Why is a chain valid only if every link matches?** — Because a changed block alters its own hash and therefore the next block's stored `previous_hash`, cascading to the end.
- **What is a genesis block?** — Block 0, hard-coded, the trust root of the chain.
- **Why store `previous_hash` instead of just index?** — The hash cryptographically commits to the entire previous block's content; an index alone proves nothing.

> [!tip] Viva Prep
> Be ready to explain the *why* behind each step, not just the output.
