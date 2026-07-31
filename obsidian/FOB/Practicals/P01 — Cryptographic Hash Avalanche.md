---
subject: FOB
status: not-started
tags: [subject/fob, practical, unit/1]
practical: 1
unit: 1
hours: 4
---
# P01 — Cryptographic Hash Functions & the Avalanche Effect

**Subject:** Foundation of Blockchain | **Unit:** 1 | **Approx. Hrs:** 4
**PrO (verbatim):** *To understand how cryptographic hash functions convert input data into fixed-length outputs and to demonstrate the "Avalanche Effect."*

---

## 1. Objective
- Understand what a cryptographic hash function is and its 6 core properties.
- Verify that any input (any length) produces a **fixed-length output** (SHA-256 → 64 hex chars / 256 bits).
- Demonstrate the **Avalanche Effect**: changing a single bit of input changes ≥50% of the output bits.
- Verify **determinism** (same input → same hash, every time).

## 2. Theory (exam-ready)

### What is a hash function?
A hash function takes an input (message/data of any size) and produces a fixed-size string of bytes, called a **digest** or **hash**.

### SHA-256
- SHA-256 = **Secure Hash Algorithm 256-bit**, part of the SHA-2 family (NSA designed, NIST standardized).
- Output: **256 bits** = 32 bytes = **64 hexadecimal characters**.
- Used in Bitcoin to link blocks and in mining (double SHA-256).

### 6 required properties of a cryptographic hash
| Property | Meaning |
|---|---|
| **Deterministic** | Same input always gives the same output. |
| **Fixed output length** | Input of any size → output of fixed size (256 bits for SHA-256). |
| **Pre-image resistance** | Given hash *h*, it is infeasible to find *m* such that hash(m) = h (one-way). |
| **Second pre-image resistance** | Given *m*, infeasible to find *m' ≠ m* with hash(m') = hash(m). |
| **Collision resistance** | Infeasible to find any two different inputs with the same hash. |
| **Avalanche effect** | A tiny change in input (even 1 bit) → a completely different output; ideally ~50% of bits flip. |

### Why it matters in blockchain
- **Block linking:** each block stores the hash of the previous block (tamper-evidence).
- **Merkle trees:** efficient verification of data (Practical P04).
- **Mining (PoW):** miners search for a nonce so that `hash(block)` is below the difficulty target (Practical P05).

## 3. Steps Performed
1. Import the `hashlib` module (Python built-in).
2. Define `sha256_hex()` to hash any text and return hex.
3. Compute SHA-256 of inputs of different lengths to show **fixed output length**.
4. Hash two messages that differ by one character (`!` → `?`) and by one capital letter → compute the **Hamming distance** of the two digests to quantify the avalanche effect.
5. Hash the same input twice to prove **determinism**.

## 4. Code
```python
import hashlib


def sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def hamming_distance(hex1: str, hex2: str) -> int:
    return sum(bin(int(a, 16) ^ int(b, 16)).count("1") for a, b in zip(hex1, hex2))


def demo(label_a, label_b, text_a, text_b):
    h_a, h_b = sha256_hex(text_a), sha256_hex(text_b)
    print(f"Input A ({label_a!r:>8}): {text_a!r}")
    print(f"Input B ({label_b!r:>8}): {text_b!r}")
    print(f"SHA-256(A): {h_a}")
    print(f"SHA-256(B): {h_b}")
    print(f"Length of both hashes        : {len(h_a)} hex chars = {len(h_a) * 4} bits")
    print(f"Hamming distance (bit diffs) : {hamming_distance(h_a, h_b)} bits out of 256")
    print("-" * 70)


for text in ["a", "hello", "The quick brown fox jumps over the lazy dog"]:
    print(f"  input {len(text):>3d} chars -> SHA-256 {len(sha256_hex(text))} hex chars")

demo("original", "changed", "Hello, World!", "Hello, World?")
demo("lower", "UPPER", "blockchain", "Blockchain")
print(f"  SHA-256('GTU') = {sha256_hex('GTU')}")
print(f"  SHA-256('GTU') = {sha256_hex('GTU')}")
```

> Full runnable script: [[p01_hash_avalanche.py|`p01_hash_avalanche.py`]]

## 5. Expected Output (actual run)
```
[1] Fixed-length output
  input   1 chars -> SHA-256 64 hex chars
  input   5 chars -> SHA-256 64 hex chars
  input  43 chars -> SHA-256 64 hex chars

[2] Avalanche Effect (one-bit change in input)
Input A ('original'): 'Hello, World!'
Input B ( 'changed'): 'Hello, World?'
SHA-256(A): dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f
SHA-256(B): f16c3bb0532537acd5b2e418f2b1235b29181e35cffee7cc29d84de4a1d62e4d
Hamming distance (bit diffs): 113 bits out of 256

[3] Avalanche Effect (capitalisation change)
Input A ( 'lower'): 'blockchain'
Input B ( 'UPPER'): 'Blockchain'
SHA-256(A): ef7797e13d3a75526946a3bcf00daec9fc9c9c4d51ddc7cc5df888f74dd434d1
SHA-256(B): 625da44e4eaf58d61cf048d168aa6f5e492dea166d8bb54ec06c30de07db57e1
Hamming distance (bit diffs): 130 bits out of 256

[4] Deterministic
  SHA-256('GTU') = ca8f6d1fc20cf7e737aa6e2d9fbd1603822ce8dbd607d87b41499f79fad8d63b
  SHA-256('GTU') = ca8f6d1fc20cf7e737aa6e2d9fbd1603822ce8dbd607d87b41499f79fad8d63b
```

**Interpretation:** `Hello, World!` vs `Hello, World?` differ by **1 bit**, yet 113/256 output bits flipped (~44%). Capitalisation change flipped 130/256 (~51%) — close to the ideal 50%. This proves one-way, avalanche behaviour.

## 6. Conclusion
- SHA-256 converts inputs of any size into a fixed 256-bit (64-hex) digest.
- A 1-bit input change produces a completely different hash (avalanche effect).
- The hash is deterministic, so hashes are tamper-evident — the foundation of blockchain block-linking and mining.

## 7. Viva Q&A
1. **What is the output size of SHA-256?** — 256 bits = 64 hexadecimal characters.
2. **What is the avalanche effect?** — A small change in input (~1 bit) should flip ~50% of output bits.
3. **What is pre-image resistance?** — You cannot reverse a hash to find the original input.
4. **Why does Bitcoin use double SHA-256?** — `SHA256(SHA256(x))` for additional security margin.

## 8. Resources
- hashlib docs: https://docs.python.org/3/library/hashlib.html
- SHA-2 on Wikipedia: https://en.wikipedia.org/wiki/SHA-2
- CyberChef (visual hash tool): https://gchq.github.io/CyberChef/
- Andreas Antonopoulos, *Mastering Bitcoin*, Ch. 4 "Keys, Addresses" (hash background)

---



---

## 🐛 Failure Modes & Debugging (Real-World Experience)

> [!bug] What goes wrong in production?
> When running **Cryptographic Hash Avalanche** in a real environment, it almost never works perfectly the first time. 
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

- **Avalanche Effect** — changing a single bit of input changes ≥50% of the output bits.
- **What is the output size of SHA-256?** — 256 bits = 64 hexadecimal characters.
- **What is the avalanche effect?** — A small change in input (~1 bit) should flip ~50% of output bits.
- **What is pre-image resistance?** — You cannot reverse a hash to find the original input.
- **Why does Bitcoin use double SHA-256?** — `SHA256(SHA256(x))` for additional security margin.

> [!tip] Viva Prep
> Be ready to explain the *why* behind each step, not just the output.
