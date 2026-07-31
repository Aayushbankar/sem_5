---
title: "P02 — Public Private Keys Digital Signatures"
sidebar:
  order: 2
---

# P02 — Public/Private Key Pair & Digital Signatures

**Subject:** Foundation of Blockchain | **Unit:** 1 | **Approx. Hrs:** 2
**PrO (verbatim):** *To generate a public/private key pair and understand how digital signatures ensure data authenticity.*

---

## 1. Objective
- Generate an ECDSA **public/private key pair** (curve `secp256k1`, used by Bitcoin & Ethereum).
- Sign a message with the **private key**.
- Verify authenticity using only the **public key**.
- Show that a **tampered message** and a **wrong public key** both fail verification.

## 2. Theory (exam-ready)

### Public Key Cryptography (asymmetric)
- Two mathematically related keys are generated together:
  - **Private key** — secret, known only to owner. Used to *sign* / decrypt.
  - **Public key** — derived from the private key, freely shared. Used to *verify* / encrypt.
- One-way: it is computationally infeasible to derive the private key from the public key (elliptic-curve discrete log problem).

### ECDSA (Elliptic Curve Digital Signature Algorithm)
- Bitcoin/Ethereum use ECDSA on curve **secp256k1**.
- A signature is a pair `(r, s)` of numbers.
- ECDSA signatures are **non-deterministic** (random nonce k) → two signatures of the same message differ.

### How a digital signature ensures authenticity (Sign → Verify)
```
Alice (signer)                       Bob (verifier)
  1. hash(message) = H                1. receives (message, signature)
  2. signature = sign(H, privKey)     2. hash(message) = H'
  3. sends (message, signature)       3. verify(signature, H', pubKey)
                                      4. OK if and only if signed by privKey partner
```

### What a signature guarantees
| Property | Achieved by |
|---|---|
| **Authenticity** | Only the private-key holder can produce a valid signature. |
| **Integrity** | Any change to the message breaks verification. |
| **Non-repudiation** | Signer cannot deny having signed (private key only with them). |

## 3. Steps Performed
1. `ec.generate_private_key(ec.SECP256K1())` → private key; derive `.public_key()`.
2. Serialize both keys to **PEM** to view them.
3. Sign the message with `private_key.sign(msg, ec.ECDSA(hashes.SHA256()))`.
4. Verify with the **public key** → VALID.
5. Modify one word in the message ("5 ETH" → "50 ETH") → verification **fails**.
6. Use a **different public key** → verification **fails**.

## 4. Code
```python
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature

private_key = ec.generate_private_key(ec.SECP256K1())
public_key = private_key.public_key()

priv_pem = private_key.private_bytes(
    serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8,
    serialization.NoEncryption())
pub_pem = public_key.public_bytes(
    serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo)

message = b"Transfer 5 ETH to StudentB - transaction #1001"
signature = private_key.sign(message, ec.ECDSA(hashes.SHA256()))
r, s = decode_dss_signature(signature)

print(priv_pem.decode()); print(pub_pem.decode())
print("Signature r:", r.to_bytes(32, 'big').hex())
print("Signature s:", s.to_bytes(32, 'big').hex())

# verify
public_key.verify(signature, message, ec.ECDSA(hashes.SHA256()))       # OK
public_key.verify(signature, b"Transfer 50 ETH...", ec.ECDSA(hashes.SHA256()))  # raises
```

> Full runnable script: [`p02_keys_signatures.py`](./p02_keys_signatures.py.md) — requires `pip install cryptography`

## 5. Expected Output (actual run)
```
[1] Private key (PEM, keep SECRET):
-----BEGIN PRIVATE KEY-----
MIGEAgEAMBAGByqGSM49AgEGBSuBBAAKBG0wawIBAQQg2mwoIJaFXAumzUMEJTEX
FpuWwVHAbOeb5MHzX0REpBWhRANCAAR5HZ12BDkGUXezqwZuKbvT245RsriUmY/m
oGrMO0cropRbarx08u1CFN2JgrqCmGL8LRlyiSTJfRd0g/W5m7pI
-----END PRIVATE KEY-----

[3] Message to sign: Transfer 5 ETH to StudentB - transaction #1001
    Signature r (hex): 27baad3ac77a943d6c4911f9916ea0df7abf58402495450fba84e1aad35f78bb
    Signature s (hex): 22572ab7f8b70e6d462ef80fe4fde981b8db4dfd747fbebcebed35571009dc20

[4] Verification with PUBLIC key : VALID ✓ (message unchanged)
[5] Verification of TAMPERED msg  : INVALID ✓ (signature rejected)
[6] Verification with WRONG pubkey: INVALID ✓ (signature rejected)
```
> Note: r/s and PEM keys are random on every run (ECDSA non-determinism). Your output will differ — that is expected.

## 6. Conclusion
A digital signature binds a message to a private key. Anyone holding the corresponding public key can prove the message is authentic and untampered, while an attacker without the private key cannot forge a valid signature.

## 7. Viva Q&A
1. **Which curve do Bitcoin and Ethereum use?** — `secp256k1`.
2. **Can you recover the private key from the public key?** — No, computationally infeasible (ECDLP).
3. **Why are two signatures of the same message different?** — ECDSA uses a random nonce *k*.
4. **What is non-repudiation?** — The signer cannot deny signing, because only their private key could produce the valid signature.

## 8. Resources
- `cryptography` docs (Elliptic Curve): https://cryptography.io/en/latest/hazmat/primitives/asymmetric/ec/
- *Mastering Bitcoin*, Ch. 4 "Keys, Addresses, Wallets": https://github.com/bitcoinbook/bitcoinbook
- ECDSA explained: https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm
- OpenSSL quick check: `openssl ecparam -name secp256k1 -genkey`

---



---

## 🐛 Failure Modes & Debugging (Real-World Experience)

> [!bug] What goes wrong in production?
> When running **Public Private Keys Digital Signatures** in a real environment, it almost never works perfectly the first time. 
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

- **Private key** — secret, known only to owner. Used to *sign* / decrypt.
- **Public key** — derived from the private key, freely shared. Used to *verify* / encrypt.
- **Can you recover the private key from the public key?** — No, computationally infeasible (ECDLP).
- **Why are two signatures of the same message different?** — ECDSA uses a random nonce *k*.
- **What is non-repudiation?** — The signer cannot deny signing, because only their private key could produce the valid signature.

> [!tip] Viva Prep
> Be ready to explain the *why* behind each step, not just the output.
