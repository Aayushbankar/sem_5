# P04 — Simplified Merkle Tree

**Subject:** Foundation of Blockchain | **Unit:** 1 | **Approx. Hrs:** 4
**PrO (verbatim):** *To manually construct a simplified Merkle Tree to understand efficient data verification.*

---

## 1. Objective
- Build a Merkle tree bottom-up from transaction leaves.
- Compute the **Merkle root** for an even number of leaves and for an odd number (last node duplicated).
- Demonstrate how changing **one leaf** changes the root → tamper detection with O(log n) verification.

## 2. Theory (exam-ready)

### What is a Merkle Tree?
- A **binary hash tree** introduced by Ralph Merkle (1979).
- **Leaves** = hashes of data items (e.g., `SHA-256(tx)`).
- **Internal nodes** = hash of the concatenation of their two children.
- **Root** (Merkle root / root hash) = single hash committing to **all** leaves at once.

### How it is built (4 transactions)
```
                        Root = H(h01 + h23)
                       /                    \
              h01 = H(h0+h1)          h23 = H(h2+h3)
             /          \             /          \
        h0=H(tx0)  h1=H(tx1)   h2=H(tx2)  h3=H(tx3)
```
- **Odd number of leaves:** duplicate the last leaf (Bitcoin convention).

### Why it gives *efficient* verification
- To prove a single transaction belongs in a block you need only **log₂(n)** sibling hashes (**Merkle proof** / branch), not all n transactions.
- Bitcoin: **Simplified Payment Verification (SPV)** — light wallets store only the block header (root) and verify a transaction with a short proof.

### Where it's used
- Bitcoin block header (single Merkle root for ~2000+ txs).
- Ethereum (state trie uses a Merkle-Patricia variant).
- Git object integrity, IPFS.

## 3. Steps Performed
1. Hash each transaction → leaves.
2. Pair leaves, sort pairs (`left < right`) and hash concatenations → next layer.
3. Repeat until one node remains = Merkle root.
4. Repeat with 5 transactions (odd count → duplicate last leaf).
5. Change the text of one transaction and recompute the root → compare with the original root.

## 4. Code
```python
import hashlib

def sha256(data): return hashlib.sha256(data.encode()).hexdigest()

def hash_pair(left, right):
    if left > right:            # canonical ordering avoids H(L||R) vs H(R||L) ambiguity
        left, right = right, left
    return sha256(left + right)

def build_merkle_tree(leaves):
    layer = [sha256(leaf) for leaf in leaves]
    while len(layer) > 1:
        next_layer = []
        for i in range(0, len(layer), 2):
            left = layer[i]
            right = layer[i+1] if i+1 < len(layer) else left   # duplicate odd node
            next_layer.append(hash_pair(left, right))
        layer = next_layer
    return layer[0]
```

> Full runnable script: [`p04_merkle_tree.py`](../code/p04_merkle_tree.py)

## 5. Expected Output (actual run)
```
[1] Four transactions:
Leaves  -> ['968b0210', '4a6c84c9', 'd1df1733', '6b660d57']
Node    -> ['4d12a419', '06a40d50']
Node    -> ['ce17f4c5']
    Merkle root (4 txs): ce17f4c5ae78b9871375ff9b12c85266f1e4096a32d0589cd4a3f4ab30f24a6b

[2] Five transactions (last node duplicated):
    Merkle root (5 txs): 8b6ab6bcfd866563edac1a989a3021adb36c120813d2fb6f4c9927f2bc66e03a

[3] Tamper detection: change Tx3 text
    Original root : ce17f4c5ae78b9871375ff9b12c85266f1e4096a32d0589cd4a3f4ab30f24a6b
    Tampered root : 1eb2a430c77c83e5d2ecea8b47fc887fab36d6b7a5c1deb464cc3b44e93dff31
    Roots match   : NO -> tampering detected ✓
```

## 6. Conclusion
A Merkle tree compresses any number of data items into a single root hash, allows O(log n) membership proofs, and makes tampering detectable with a single root comparison.

## 7. Viva Q&A
1. **Why duplicate the last leaf when the count is odd?** — So every parent has two children (Balanced binary tree).
2. **How many hashes are needed to prove one tx in an 8-tx tree?** — log₂(8) = 3 sibling hashes.
3. **What is a Merkle proof?** — The path of sibling hashes from a leaf to the root used to verify membership.
4. **Why not just hash all transactions together?** — Then verifying one tx requires all txs; a Merkle tree only needs the branch.

## 8. Resources
- Bitcoin Merkle tree in *Mastering Bitcoin*, Ch. 9: https://github.com/bitcoinbook/bitcoinbook
- Wikipedia: https://en.wikipedia.org/wiki/Merkle_tree
- Interactive demo: https://andersbrownworth.com/blockchain/blockchain
