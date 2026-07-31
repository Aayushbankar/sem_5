# FOB — Foundation of Blockchain (DI05016051)

> **w.e.f. 2026-27** · GTU Diploma Engineering · Information Technology

Complete study kit: solved practicals, theory notes, and curated resources.

## 📊 Progress
- Practicals: **[tracker](./PRACTICALS.md)**

## 🧪 Practicals (10)
| # | Practical | Solution | Code |
|---|-----------|----------|------|
| P01 | Cryptographic hash functions & Avalanche Effect | [P01](./practicals/writeups/P01_cryptographic_hash_avalanche.md) | [p01_hash_avalanche.py](./practicals/code/p01_hash_avalanche.py) |
| P02 | Public/private keys & digital signatures | [P02](./practicals/writeups/P02_public_private_keys_digital_signatures.md) | [p02_keys_signatures.py](./practicals/code/p02_keys_signatures.py) |
| P03 | Basic blockchain structure in Python | [P03](./practicals/writeups/P03_basic_blockchain_python.md) | [p03_blockchain.py](./practicals/code/p03_blockchain.py) |
| P04 | Simplified Merkle tree | [P04](./practicals/writeups/P04_merkle_tree.md) | [p04_merkle_tree.py](./practicals/code/p04_merkle_tree.py) |
| P05 | Nonce & mining difficulty (PoW) | [P05](./practicals/writeups/P05_nonce_mining_difficulty.md) | [p05_mining_difficulty.py](./practicals/code/p05_mining_difficulty.py) |
| P06 | Wallets: keys from mnemonic (BIP39) | [P06](./practicals/writeups/P06_wallets_mnemonic_bip39.md) | [p06_bip39_wallet.py](./practicals/code/p06_bip39_wallet.py) + [wordlist](./practicals/code/p06_bip39_wordlist.txt) |
| P07 | Smart contract on the EVM | [P07](./practicals/writeups/P07_smart_contract_evm.md) | [P07_SimpleStorage.sol](./practicals/code/P07_SimpleStorage.sol) |
| P08 | ERC-20 token (Remix) | [P08](./practicals/writeups/P08_erc20_token.md) | [P08_GreenEnergyToken.sol](./practicals/code/P08_GreenEnergyToken.sol) |
| P09 | Case Study 1: Public vs Private + Hyperledger Fabric | [P09](./practicals/writeups/P09_case_study_public_vs_private_hyperledger.md) | — |
| P10 | Case Study 2: Security + Green Energy DAO | [P10](./practicals/writeups/P10_case_study_security_green_energy_dao.md) | — |

## 📚 Theory Notes (per unit)
| Unit | Title | Weightage | Notes |
|------|-------|-----------|-------|
| 1 | Foundations of Decentralization | 20% (10h) | [UNIT_1](./notes/UNIT_1_Foundations_of_Decentralization.md) |
| 2 | Bitcoin & The Proof-of-Work Era | 15% (8h) | [UNIT_2](./notes/UNIT_2_Bitcoin_and_PoW.md) |
| 3 | Ethereum & Smart Contracts | 30% (12h) | [UNIT_3](./notes/UNIT_3_Ethereum_and_Smart_Contracts.md) |
| 4 | Enterprise & Private Blockchains | 20% (7h) | [UNIT_4](./notes/UNIT_4_Enterprise_and_Private_Blockchains.md) |
| 5 | Security, Emerging Trends & Green Energy | 15% (8h) | [UNIT_5](./notes/UNIT_5_Security_Emerging_Trends_Green_Energy.md) |

## 🔗 Resources
- [Curated links (docs, courses, tools, books, videos)](./notes/RESOURCES.md)

## 🛠 Requirements
- **Python practicals (P01–P06):** Python 3.8+, `pip install cryptography` (P02 only), stdlib otherwise.
- **Solidity practicals (P07–P08):** Remix IDE (browser) + MetaMask for Sepolia.
- **P09 optional hands-on:** Docker Desktop to run the Fabric test network.

## ⚠️ Exam tips
- Unit 3 (30%) is the heaviest — master Solidity syntax + gas + Remix flow.
- "Write short notes" favorites: CAP theorem, UTXO vs account, PoW vs PoS, 51% attack, oracle problem, re-entrancy, SSI.
- Practical viva: know the *why* behind each code line, not just output.
