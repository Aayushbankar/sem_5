import hashlib


def sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def hamming_distance(hex1: str, hex2: str) -> int:
    return sum(bin(int(a, 16) ^ int(b, 16)).count("1") for a, b in zip(hex1, hex2))


def demo(label_a: str, label_b: str, text_a: str, text_b: str) -> None:
    h_a = sha256_hex(text_a)
    h_b = sha256_hex(text_b)
    print(f"Input A ({label_a!r:>8}): {text_a!r}")
    print(f"Input B ({label_b!r:>8}): {text_b!r}")
    print(f"SHA-256(A): {h_a}")
    print(f"SHA-256(B): {h_b}")
    print(f"Length of both hashes      : {len(h_a)} hex chars = {len(h_a) * 4} bits")
    print(f"Hamming distance (bit diffs): {hamming_distance(h_a, h_b)} bits out of 256")
    print("-" * 70)


def main() -> None:
    print("=" * 70)
    print("PRACTICAL: Cryptographic Hash Function & the Avalanche Effect")
    print("=" * 70)

    # Fixed-length output: different input sizes, same output length
    print("\n[1] Fixed-length output")
    for text in ["a", "hello", "The quick brown fox jumps over the lazy dog"]:
        print(f"  input {len(text):>3d} chars -> SHA-256 {len(sha256_hex(text))} hex chars")

    # Avalanche effect: one tiny change produces a completely different hash
    print("\n[2] Avalanche Effect (one-bit change in input)")
    demo("original", "changed", "Hello, World!", "Hello, World?")

    print("\n[3] Avalanche Effect (capitalisation change)")
    demo("lower", "UPPER", "blockchain", "Blockchain")

    print("\n[4] Deterministic (same input -> same hash)")
    print(f"  SHA-256('GTU') = {sha256_hex('GTU')}")
    print(f"  SHA-256('GTU') = {sha256_hex('GTU')}")


if __name__ == "__main__":
    main()
