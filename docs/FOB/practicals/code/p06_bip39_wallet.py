"""
BIP39 Mnemonic Seed Phrase -> HD Wallet Seed -> Master Private Key
Companion file needed: p06_bip39_wordlist.txt (official 2048-word English list)
Requires: pip install mnemonic? No - implemented from scratch with stdlib only.
"""
import hashlib
import hmac
import os
from pathlib import Path

WORDS = Path(__file__).parent.joinpath("p06_bip39_wordlist.txt").read_text().splitlines()


def bytes_to_bits(data: bytes) -> str:
    return "".join(f"{b:08b}" for b in data)


def checksum_bits(entropy: bytes) -> str:
    """First (len(entropy)*8 // 32) bits of SHA-256(entropy)."""
    n = (len(entropy) * 8) // 32
    return bytes_to_bits(hashlib.sha256(entropy).digest())[:n]


def entropy_to_mnemonic(entropy: bytes) -> list[str]:
    assert len(entropy) in (16, 20, 24, 28, 32), "BIP39 entropy must be 16-32 bytes"
    bits = bytes_to_bits(entropy) + checksum_bits(entropy)
    return [WORDS[int(bits[i : i + 11], 2)] for i in range(0, len(bits), 11)]


def mnemonic_to_seed(mnemonic: str, passphrase: str = "") -> bytes:
    """PBKDF2-HMAC-SHA512, 2048 iterations, salt = 'mnemonic' + passphrase."""
    return hashlib.pbkdf2_hmac("sha512", mnemonic.encode(), b"mnemonic" + passphrase.encode(), 2048)


def seed_to_master_key(seed: bytes) -> tuple:
    """BIP32 root: HMAC-SHA512(key=b'Bitcoin seed', data=seed) -> (IL, IR)."""
    I = hmac.new(b"Bitcoin seed", seed, hashlib.sha512).digest()
    return I[:32], I[32:]  # master private key, master chain code


def main() -> None:
    print("=" * 70)
    print("PRACTICAL: Wallets generating keys from mnemonic seed phrases (BIP39)")
    print("=" * 70)

    for bits in (128, 256):
        entropy = os.urandom(bits // 8)
        mnemonic = entropy_to_mnemonic(entropy)
        phrase = " ".join(mnemonic)

        print(f"\n[ Entropy {bits} bits -> {len(mnemonic)}-word mnemonic ]")
        print(f"    Entropy (hex)   : {entropy.hex()}")
        print(f"    Mnemonic phrase : {phrase}")

        seed = mnemonic_to_seed(phrase)
        print(f"    Seed (hex)      : {seed.hex()}  ({len(seed)*8} bits)")

        master_key, chain_code = seed_to_master_key(seed)
        print(f"    Master priv key : {master_key.hex()}")
        print(f"    Master chaincode: {chain_code.hex()}")

    # Determinism / passphrase demonstration
    entropy = bytes.fromhex("00000000000000000000000000000000")
    m1 = entropy_to_mnemonic(entropy)
    print("\n[ Deterministic demo - fixed entropy ]")
    print(f"    Mnemonic (no pass): {' '.join(m1)}")
    print(f"    Mnemonic (same)   : {' '.join(entropy_to_mnemonic(entropy))}")
    print(f"    Seed same?        : {mnemonic_to_seed(' '.join(m1)) == mnemonic_to_seed(' '.join(m1))}")


if __name__ == "__main__":
    main()
