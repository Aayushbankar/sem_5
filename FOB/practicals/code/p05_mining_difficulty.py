import hashlib
import json
import time


def sha256(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()


def mine_block(block_data: dict, difficulty: int) -> tuple:
    """
    Find a nonce such that sha256(block + nonce) starts with `difficulty`
    zero hex characters (i.e. hash < 16^difficulty target).
    """
    prefix = "0" * difficulty
    nonce = 0
    start = time.time()
    while True:
        block_string = json.dumps({**block_data, "nonce": nonce}, sort_keys=True)
        h = sha256(block_string)
        if h.startswith(prefix):
            elapsed = time.time() - start
            return nonce, h, elapsed
        nonce += 1


def main() -> None:
    print("=" * 70)
    print("PRACTICAL: The 'Nonce' & Mining Difficulty (Proof-of-Work)")
    print("=" * 70)

    block = {
        "index": 1,
        "timestamp": "2026-07-31T10:00:00Z",
        "data": "Student A pays 1 coin to Student B",
        "previous_hash": "0" * 64,
    }

    for difficulty in range(1, 5):
        nonce, h, elapsed = mine_block(block, difficulty)
        print(f"\n[ Difficulty {difficulty} -> target: hash starts with '{'0'*difficulty}' ]")
        print(f"    Nonce found  : {nonce}")
        print(f"    Block hash   : {h}")
        print(f"    Time taken   : {elapsed:.3f} s")

    print("\n" + "=" * 70)
    print("OBSERVATION: each +1 difficulty multiplies work by ~16x (4 hex chars = 16^4)")
    print("=" * 70)


if __name__ == "__main__":
    main()
