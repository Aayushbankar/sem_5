---
subject: FOB
status: not-started
tags: [subject/fob, practical, unit/2]
practical: 6
unit: 2
hours: 4
---
# P06 — Wallets: Keys from Mnemonic Seed Phrases (BIP39)

**Subject:** Foundation of Blockchain | **Unit:** 2 | **Approx. Hrs:** 4
**PrO (verbatim):** *To understand how wallets generate keys from mnemonic seed phrases.*

---

## 1. Objective
- Understand **BIP39** mnemonic generation from random entropy.
- Convert a **12-word / 24-word phrase** into a 512-bit **seed** (PBKDF2) and then a **BIP32 master private key**.
- Verify correctness against the **official BIP39 test vector** (all-zero entropy + passphrase `TREZOR`).

## 2. Theory (exam-ready)

### Why mnemonics?
A raw private key is 64 hex chars — unreadable and unbackupable. BIP39 encodes 128–256 bits of entropy as **12–24 human-readable words**, making backups (paper wallets) possible.

### Generation pipeline (BIP39)
```
random entropy (128 bits)  +  checksum (first 4 bits of SHA256(entropy))
      → 132 bits  →  split into 12 groups of 11 bits  →  12 wordlist indices
      →  map indices 0..2047 to the BIP39 English wordlist (2048 words)
```
- Checksum length = `entropy_bits / 32` (128→4 bits, 256→8 bits).
- Total bits = `entropy + checksum` must be divisible by 11 (12, 15, 18, 21, or 24 words).

### From mnemonic → seed
```
seed = PBKDF2-HMAC-SHA512(password = mnemonic phrase,
                         salt = "mnemonic" + passphrase,   # passphrase = optional extra word
                         iterations = 2048, dklen = 64 bytes)
```
- The optional **passphrase** (BIP39 "25th word") adds a layer: same words → different seed. Different passphrase = different wallet.

### From seed → master key (BIP32 HD wallets)
```
I  = HMAC-SHA512(key = "Bitcoin seed", data = seed)
IL = master private key (first 32 bytes),  IR = master chain code (last 32 bytes)
```
- From the master key + chain code, BIP32 derives a tree of child keys → all wallet addresses come from **one seed phrase**.

### Wallet types (exam terms)
- **Hot wallet** — keys online (mobile/desktop wallets, exchanges) → convenient, riskier.
- **Cold wallet** — keys offline (hardware wallets, paper) → safer for long-term storage.
- **Seed phrases must be stored offline**; anyone with the phrase controls the funds.

## 3. Steps Performed
1. Load the official 2048-word BIP39 English wordlist (`p06_bip39_wordlist.txt`).
2. Generate random entropy (128 and 256 bits) → append SHA-256 checksum → split into 11-bit groups → map to words.
3. Derive the 512-bit seed with PBKDF2-HMAC-SHA512.
4. Derive BIP32 master private key + chain code with HMAC-SHA512.
5. Verify: all-zero entropy → `abandon … about`; with passphrase `TREZOR` the seed equals the **official BIP39 test vector**.

## 4. Code
```python
import hashlib, hmac, os
WORDS = Path("p06_bip39_wordlist.txt").read_text().splitlines()

def entropy_to_mnemonic(entropy: bytes) -> list[str]:
    bits = "".join(f"{b:08b}" for b in entropy)
    n = (len(entropy) * 8) // 32                       # checksum length
    bits += "".join(f"{b:08b}" for b in hashlib.sha256(entropy).digest())[:n]
    return [WORDS[int(bits[i:i+11], 2)] for i in range(0, len(bits), 11)]

def mnemonic_to_seed(mnemonic: str, passphrase: str = "") -> bytes:
    return hashlib.pbkdf2_hmac("sha512", mnemonic.encode(),
                               b"mnemonic" + passphrase.encode(), 2048)

def seed_to_master_key(seed: bytes):
    I = hmac.new(b"Bitcoin seed", seed, hashlib.sha512).digest()
    return I[:32], I[32:]                              # (master privkey, chain code)
```

> Full runnable script: [[p06_bip39_wallet.py|`p06_bip39_wallet.py`]] + [[p06_bip39_wordlist.txt|`p06_bip39_wordlist.txt`]] (stdlib only)

## 5. Expected Output (actual run)
```
[ Entropy 128 bits -> 12-word mnemonic ]
    Entropy (hex)   : af24563f1197db05fe189a28228b7343
    Mnemonic phrase : quality cargo more case laundry load wear battle choice begin system mango
    Seed (hex)      : e4ba14386e04215dd1760a47e58073fea128f9d0fb082ca051bc721b4fd67dd59... (512 bits)
    Master priv key : 6e57d36e965995925a1a7e2d11774d53d45082201cc6a38a52277e2567620e97

[ Entropy 256 bits -> 24-word mnemonic ]
    Mnemonic phrase : exotic bag replace bike drill daring better road glue someone label alert ...
    Master priv key : e3e18d75ac3b6811319755c21749eb08bfe93373756c20518b728071b91d960d

[ Deterministic demo - fixed entropy ]
    Mnemonic: abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about
```
**Verification against official BIP39 test vector** (all-zero entropy, passphrase `TREZOR`):
`c55257c360c07c72029aebc1b53c05ed0362ada38ead3e3e9efa3708e53495531f09a6987599d18264c1e1c92f2cf141630c7a3c4ab7c81b2f001698e7463b04` → **MATCHES ✓**

## 6. Conclusion
A wallet's entire key tree collapses into 12–24 words. Entropy → checksum → wordlist indices produces the phrase; PBKDF2 turns it into a 512-bit seed; BIP32 derives the master key and all child keys. Backing up the phrase (offline, cold) is backing up the wallet.

## 7. Viva Q&A
1. **How many words for 128-bit entropy?** — 12 (132 bits with 4-bit checksum).
2. **What is the "25th word"?** — The optional BIP39 passphrase; same mnemonic + different passphrase = different wallet.
3. **What KDF converts mnemonic → seed?** — PBKDF2-HMAC-SHA512, 2048 iterations.
4. **Hot vs cold wallet?** — Hot = keys online; cold = offline (hardware/paper).
5. **What is a chain code in BIP32?** — The second half of the HMAC output, used with IL to deterministically derive child keys.

## 8. Resources
- BIP39 spec: https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki (incl. test vectors)
- BIP32 spec: https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki
- iancoleman BIP39 tool (interactive): https://iancoleman.io/bip39/
- *Mastering Bitcoin*, Ch. 5 "Wallets": https://github.com/bitcoinbook/bitcoinbook

---



---

## 🐛 Failure Modes & Debugging (Real-World Experience)

> [!bug] What goes wrong in production?
> When running **Wallets Mnemonic Bip39** in a real environment, it almost never works perfectly the first time. 
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

- **Hot wallet** — keys online (mobile/desktop wallets, exchanges) → convenient, riskier.
- **Cold wallet** — keys offline (hardware wallets, paper) → safer for long-term storage.
- **How many words for 128-bit entropy?** — 12 (132 bits with 4-bit checksum).
- **What is the "25th word"?** — The optional BIP39 passphrase; same mnemonic + different passphrase = different wallet.
- **What KDF converts mnemonic → seed?** — PBKDF2-HMAC-SHA512, 2048 iterations.
- **Hot vs cold wallet?** — Hot = keys online; cold = offline (hardware/paper).
- **What is a chain code in BIP32?** — The second half of the HMAC output, used with IL to deterministically derive child keys.

> [!tip] Viva Prep
> Be ready to explain the *why* behind each step, not just the output.
