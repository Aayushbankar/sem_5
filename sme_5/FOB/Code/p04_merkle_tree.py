import hashlib
from typing import List, Optional


def sha256(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()


def hash_pair(left: str, right: str) -> str:
    # Standard Merkle convention: left < right (lexicographic sort) prevents ambiguity
    if left > right:
        left, right = right, left
    return sha256(left + right)


def build_merkle_tree(leaves: List[str]) -> Optional[str]:
    """
    Builds the tree bottom-up and returns the Merkle root.
    Odd node count: the last node is duplicated (Bitcoin style).
    """
    if not leaves:
        return None

    layer: List[str] = [sha256(leaf) for leaf in leaves]
    print(f"{'Leaves':<10} -> {[h[:8] for h in layer]}")

    while len(layer) > 1:
        next_layer: List[str] = []
        for i in range(0, len(layer), 2):
            left = layer[i]
            right = layer[i + 1] if i + 1 < len(layer) else left  # duplicate odd node
            next_layer.append(hash_pair(left, right))
        print(f"{'Node':<10} -> {[h[:8] for h in next_layer]}")
        layer = next_layer

    return layer[0]


def main() -> None:
    print("=" * 70)
    print("PRACTICAL: Simplified Merkle Tree")
    print("=" * 70)

    transactions = [
        "Tx1: A pays 1 coin to B",
        "Tx2: B pays 0.5 coin to C",
        "Tx3: C pays 2 coins to D",
        "Tx4: D pays 1 coin to A",
    ]
    print("\n[1] Four transactions (leaves = SHA-256 of each tx):\n")
    root_4 = build_merkle_tree(transactions)
    print(f"\n    Merkle root (4 txs): {root_4}")

    print("\n[2] Five transactions (odd count -> last node duplicated):\n")
    transactions5 = transactions + ["Tx5: E pays 3 coins to F"]
    root_5 = build_merkle_tree(transactions5)
    print(f"\n    Merkle root (5 txs): {root_5}")

    # Tamper proof
    print("\n[3] Tamper detection: change Tx3 text and recompute root")
    tampered = transactions[:]
    tampered[2] = "Tx3: C pays 200 coins to D"
    root_t = build_merkle_tree(tampered)
    print(f"\n    Original root : {root_4}")
    print(f"    Tampered root : {root_t}")
    print("    Roots match   :", "YES (BAD)" if root_4 == root_t else "NO -> tampering detected \u2713")


if __name__ == "__main__":
    main()
