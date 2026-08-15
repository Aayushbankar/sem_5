---
subject: FOB
status: not-started
tags: [subject/fob, practical, unit/2]
practical: 5
unit: 2
hours: 2
---
# P05 — The "Nonce" & Mining Difficulty (Proof-of-Work)

**Subject:** Foundation of Blockchain | **Unit:** 2 | **Approx. Hrs:** 2
**PrO (verbatim):** *To understand the concept of a "Nonce" and how mining difficulty secures a network.*

---

## 1. Objective
- Understand the **nonce** and its role in Proof-of-Work.
- Simulate mining: brute-force a nonce so the block hash meets a difficulty target.
- Observe how raising **difficulty** exponentially increases the work required.

## 2. Theory (exam-ready)

### The Nonce
- **Nonce** = "**n**umber used **once**" — a counter in the block header that miners change to alter the resulting hash.
- Mining = repeatedly changing the nonce until `SHA256(SHA256(block_header + nonce)) < Target`.

### Difficulty & the Target
- The block hash must start with **D zero hex characters** (equivalently hash < 2^(256 − 4·D)).
- Probability of a single hash succeeding = **1/16ᴰ**. Work grows **16× for every +1 difficulty**.

| Difficulty (leading zeros) | P(success per hash) | Expected attempts |
|---|---|---|
| 1 (`0…`) | 1/16 | ~16 |
| 2 (`00…`) | 1/256 | ~256 |
| 3 (`000…`) | 1/4096 | ~4096 |
| 4 (`0000…`) | 1/65536 | ~65536 |

### How mining difficulty secures the network
1. **Cost of attack:** rewriting history requires re-mining every subsequent block at current difficulty → expensive (51% attack needs majority hashrate).
2. **Block pacing:** Bitcoin adjusts difficulty every 2016 blocks to target a 10-minute block interval → predictable emission.
3. **Proof-of-work** = the nonce (work) proves energy/effort was spent; nodes trust the longest valid chain.

### Terms
- **Block reward + transaction fees** = miner incentive (halving every ~210,000 blocks).
- **Mempool → block lifecycle:** valid txs wait in the mempool, miners select them, mine the block, broadcast, peers validate.

## 3. Steps Performed
1. Define `mine_block(block_data, difficulty)`: loop nonce `0,1,2,…` until `hash` starts with `difficulty` zeros.
2. Record the **nonce found, block hash, and time**.
3. Repeat for difficulties 1 → 4 and compare work/time.

## 4. Code
```python
import hashlib, json, time

def sha256(data): return hashlib.sha256(data.encode()).hexdigest()

def mine_block(block_data, difficulty):
    prefix, nonce, start = "0"*difficulty, 0, time.time()
    while True:
        h = sha256(json.dumps({**block_data, "nonce": nonce}, sort_keys=True))
        if h.startswith(prefix):
            return nonce, h, time.time()-start
        nonce += 1

block = {"index": 1, "timestamp": "2026-07-31T10:00:00Z",
         "data": "Student A pays 1 coin to Student B",
         "previous_hash": "0"*64}

for difficulty in range(1, 5):
    nonce, h, elapsed = mine_block(block, difficulty)
    print(f"Difficulty {difficulty}: nonce={nonce}, time={elapsed:.3f}s, hash={h}")
```

> Full runnable script: [[p05_mining_difficulty.py|`p05_mining_difficulty.py`]]

## 5. Expected Output (actual run)
```
[ Difficulty 1 -> target: hash starts with '0' ]   Nonce found: 0       Time: 0.000 s
[ Difficulty 2 -> target: hash starts with '00' ]  Nonce found: 13      Time: 0.000 s
[ Difficulty 3 -> target: hash starts with '000' ] Nonce found: 2386    Time: 0.036 s
[ Difficulty 4 -> target: hash starts with '0000'] Nonce found: 128231  Time: 1.900 s
```
> Nonce values vary run-to-run, but the growth pattern (~16× per +1 difficulty) is consistent.

## 6. Conclusion
The nonce is brute-forced until the block hash satisfies a difficulty target. Increasing difficulty by one hex-zero multiplies expected work by ~16×, which makes rewriting history economically infeasible and keeps block production regular — this is the security core of PoW blockchains.

## 7. Viva Q&A
1. **What does a miner change to find a valid block?** — The nonce (and timestamp) in the header.
2. **What happens if two miners solve a block together?** — A fork; the network follows the longest chain, other block is orphaned.
3. **How often does Bitcoin adjust difficulty?** — Every 2016 blocks (~2 weeks).
4. **What is a 51% attack?** — An entity controlling >50% hashrate can reorg/reverse transactions (theoretically).
5. **What is the target?** — A 256-bit number; a valid block hash must be numerically less than it.

## 8. Resources
- *Mastering Bitcoin*, Ch. 8 "Mining and Consensus": https://github.com/bitcoinbook/bitcoinbook
- Bitcoin difficulty: https://en.bitcoin.it/wiki/Difficulty
- Mininet of concepts (hash brute force): https://www.blockchain.com/explorer

---



---

## 🐛 Failure Modes & Debugging (Real-World Experience)

> [!bug] What goes wrong in production?
> When running **Nonce Mining Difficulty** in a real environment, it almost never works perfectly the first time. 
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

- **What does a miner change to find a valid block?** — The nonce (and timestamp) in the header.
- **What happens if two miners solve a block together?** — A fork; the network follows the longest chain, other block is orphaned.
- **How often does Bitcoin adjust difficulty?** — Every 2016 blocks (~2 weeks).
- **What is a 51% attack?** — An entity controlling >50% hashrate can reorg/reverse transactions (theoretically).
- **What is the target?** — A 256-bit number; a valid block hash must be numerically less than it.

> [!tip] Viva Prep
> Be ready to explain the *why* behind each step, not just the output.
