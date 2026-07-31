import hashlib
import json
import time
from typing import Any, Dict, List


class Block:
    def __init__(self, index: int, timestamp: float, data: str, previous_hash: str, nonce: int = 0) -> None:
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.compute_hash()

    def compute_hash(self) -> str:
        block_string = json.dumps(
            {
                "index": self.index,
                "timestamp": self.timestamp,
                "data": self.data,
                "previous_hash": self.previous_hash,
                "nonce": self.nonce,
            },
            sort_keys=True,
        ).encode()
        return hashlib.sha256(block_string).hexdigest()

    def __repr__(self) -> str:
        return (
            f"Block(index={self.index}, data={self.data!r}, hash={self.hash[:16]}..., "
            f"prev={self.previous_hash[:16]}...)"
        )


class SimpleBlockchain:
    def __init__(self) -> None:
        self.chain: List[Block] = [self.create_genesis_block()]

    def create_genesis_block(self) -> Block:
        return Block(0, time.time(), "Genesis Block", "0" * 64)

    @property
    def last_block(self) -> Block:
        return self.chain[-1]

    def add_block(self, data: str) -> Block:
        prev = self.last_block
        block = Block(prev.index + 1, time.time(), data, prev.hash)
        self.chain.append(block)
        return block

    def is_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current, previous = self.chain[i], self.chain[i - 1]
            if current.hash != current.compute_hash():
                print(f"  INVALID: block {current.index} hash was tampered with!")
                return False
            if current.previous_hash != previous.hash:
                print(f"  INVALID: block {current.index} link to block {previous.index} broken!")
                return False
        return True

    def tamper(self, index: int, new_data: str) -> None:
        self.chain[index].data = new_data


def show_chain(chain: SimpleBlockchain) -> None:
    print(f"{'Idx':<4}{'Data':<28}{'Previous hash':<18}{'Hash':<18}")
    print("-" * 68)
    for b in chain.chain:
        print(f"{b.index:<4}{b.data[:26]:<28}{b.previous_hash[:16]:<18}{b.hash[:16]}")


def main() -> None:
    print("=" * 70)
    print("PRACTICAL: Basic Blockchain Structure in Python")
    print("=" * 70)

    bc = SimpleBlockchain()
    bc.add_block("Student A sends 1 coin to Student B")
    bc.add_block("Student C sends 2 coins to Student D")
    bc.add_block("Student A sends 0.5 coin to Student C")

    print("\n[1] Blockchain after adding 4 blocks (genesis + 3):\n")
    show_chain(bc)

    print("\n[2] Chain validity check: ", "VALID \u2713" if bc.is_valid() else "INVALID")

    print("\n[3] Tampering: change data of block index 1 ('send 1 coin' -> 'send 100 coins')\n")
    bc.tamper(1, "Student A sends 100 coins to Student B")
    show_chain(bc)

    print("\n[4] Chain validity check after tampering: ", "VALID \u2713" if bc.is_valid() else "INVALID \u2717")
    print("\n    Because each block's hash is computed FROM its own data + previous hash,")
    print("    changing one block breaks the link for every block after it (tamper-evident).")


if __name__ == "__main__":
    main()
