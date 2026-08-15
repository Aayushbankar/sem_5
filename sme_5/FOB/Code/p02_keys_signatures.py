from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature


def to_hex(data: bytes) -> str:
    return data.hex()


def main() -> None:
    print("=" * 70)
    print("PRACTICAL: Public/Private Key Pair & Digital Signatures (ECDSA)")
    print("=" * 70)

    # 1. Generate an ECDSA key pair (secp256k1 is the curve used by Bitcoin/Ethereum)
    private_key = ec.generate_private_key(ec.SECP256K1())
    public_key = private_key.public_key()

    # 2. Serialize keys (PEM) so they can be viewed/saved
    priv_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    pub_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    print("\n[1] Private key (PEM, keep SECRET):")
    print(priv_pem.decode())
    print("\n[2] Public key (PEM, share freely):")
    print(pub_pem.decode())

    # 3. Sign a message
    message = b"Transfer 5 ETH to StudentB - transaction #1001"
    signature = private_key.sign(message, ec.ECDSA(hashes.SHA256()))
    r, s = decode_dss_signature(signature)
    print("[3] Message to sign:")
    print("   ", message.decode())
    print(f"\n    Signature (DER, hex): {to_hex(signature)}")
    print(f"    Signature r (hex)  : {r.to_bytes(32, 'big').hex()}")
    print(f"    Signature s (hex)  : {s.to_bytes(32, 'big').hex()}")

    # 4. Verify with the PUBLIC key (works)
    try:
        public_key.verify(signature, message, ec.ECDSA(hashes.SHA256()))
        print("\n[4] Verification with PUBLIC key : VALID \u2713 (message unchanged)")
    except Exception:
        print("\n[4] Verification with PUBLIC key : INVALID")

    # 5. Tampered message -> verification FAILS
    tampered = b"Transfer 50 ETH to StudentB - transaction #1001"
    try:
        public_key.verify(signature, tampered, ec.ECDSA(hashes.SHA256()))
        print("[5] Verification of TAMPERED msg  : VALID (BAD \u2717)")
    except Exception:
        print("[5] Verification of TAMPERED msg  : INVALID \u2713 (signature rejected)")

    # 6. Sign with a different (wrong) key -> verification FAILS
    wrong_key = ec.generate_private_key(ec.SECP256K1()).public_key()
    try:
        wrong_key.verify(signature, message, ec.ECDSA(hashes.SHA256()))
        print("[6] Verification with WRONG pubkey : VALID (BAD \u2717)")
    except Exception:
        print("[6] Verification with WRONG pubkey : INVALID \u2713 (signature rejected)")


if __name__ == "__main__":
    main()
