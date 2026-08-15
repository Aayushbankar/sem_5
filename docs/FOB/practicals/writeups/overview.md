**Note:** The syllabus does not provide a separate practical marks rubric. The criteria below are extracted directly from the stated **Practical Outcomes (PrOs)** and their **Course Outcome (CO)** mappings, optimized for the minimum work required to pass and demonstrate competence.

---

**Practical 1: Cryptographic Hash Functions & Avalanche Effect**

**[1. Objective]**
* Demonstrate that SHA-256 converts any input into a fixed-length output, and show that a tiny input change produces a drastically different hash (avalanche effect).

**[2. Key Stuff to Learn]**
* Python `hashlib.sha256`, UTF-8 encoding, hex digest output format, avalanche effect definition.

**[3. What to Code / Implement]**
* A Python script that: (a) takes an input string and prints its SHA-256 hash, (b) changes exactly one character in that string, (c) prints the new hash, (d) visually compares the two hashes.

**[4. Passing Criteria According to the Rubric]**
* **Must have** — Working script that generates SHA-256 hashes; side-by-side output proving the avalanche effect (hashes must look completely different); statement that output is always fixed-length.
* **Good to have** — Second example with a different input pair; brief mention of why this matters for blockchain integrity.
* **Necessary** — Use `hashlib`; do not call an online API.

**[5. Final Deliverable]**
* Python `.py` file + screenshot of terminal output showing original input, modified input, both hashes, and a one-line observation.

---

**Practical 2: Public/Private Key Pair & Digital Signatures**

**[1. Objective]**
* Generate an asymmetric key pair and prove that digital signatures ensure data authenticity (valid if untampered, invalid if tampered).

**[2. Key Stuff to Learn]**
* Python `cryptography` library (RSA or ECC), `private_key.sign()` / `public_key.verify()`, tamper detection logic.

**[3. What to Code / Implement]**
* Python script that: (a) generates a key pair, (b) signs a message with the private key, (c) verifies the signature with the public key, (d) modifies the message, (e) attempts verification again and shows it fails.

**[4. Passing Criteria According to the Rubric]**
* **Must have** — Evidence of key pair generation; successful verification on the original message; explicit failed verification after the message is altered.
* **Good to have** — Keys exported in PEM format; signature printed in hex.
* **Necessary** — Use an established library. Do not implement the cryptographic math manually.

**[5. Final Deliverable]**
* Python `.py` file + terminal output/screenshots showing sign → verify → tamper → fail.

---

**Practical 3: Basic Blockchain Structure in Python**

**[1. Objective]**
* Build a minimal blockchain where blocks are cryptographically linked to the previous block via hashes.

**[2. Key Stuff to Learn]**
* Block structure (`index`, `data`, `timestamp`, `previous_hash`, `hash`), SHA-256 chaining, chain validation.

**[3. What to Code / Implement]**
* A `Block` class and a `Blockchain` class with: `calculate_hash()` (must include `previous_hash` in the hashed data), `add_block()`, and `is_chain_valid()` that checks every link.

**[4. Passing Criteria According to the Rubric]**
* **Must have** — A chain of at least 3 blocks where each block stores the previous block's hash; `is_chain_valid()` returns `True` for an unmodified chain and `False` after you manually tamper with any block's data.
* **Good to have** — Auto-recalculation demonstration if a block's data changes.
* **Necessary** — The block hash must include `previous_hash` to create the cryptographic link.

**[5. Final Deliverable]**
* Python `.py` file + output showing the created chain, a tampered block, and the validation result (`False`).

---

**Practical 4: Simplified Merkle Tree**

**[1. Objective]**
* Manually construct a Merkle Tree from transaction data and demonstrate that the root hash acts as a tamper-evident summary.

**[2. Key Stuff to Learn]**
* Leaf node hashing, pairwise parent hashing, Merkle root computation, tamper detection via root change.

**[3. What to Code / Implement]**
* Python script that: (a) accepts an even list of transaction strings as leaves, (b) hashes them bottom-up to a single Merkle root, (c) prints the root, (d) changes one leaf and prints the new root to show it differs.

**[4. Passing Criteria According to the Rubric]**
* **Must have** — Correct Merkle root computed from a set of leaves; printed root values; proof that altering any leaf changes the root.
* **Good to have** — A function that returns a Merkle proof path for a specific leaf.
* **Necessary** — Handle an odd number of leaves by duplicating the last leaf so pairing works.

**[5. Final Deliverable]**
* Python `.py` file + terminal output showing leaf hashes, intermediate hashes, original root, modified root, and a brief note.

---

**Practical 5: Nonce and Mining Difficulty**

**[1. Objective]**
* Simulate proof-of-work by finding a nonce that produces a hash with a required number of leading zeros, showing that higher difficulty requires more work.

**[2. Key Stuff to Learn]**
* Nonce definition, difficulty as leading-zero requirement, brute-force hash loop, basic time measurement.

**[3. What to Code / Implement]**
* Python miner function: inputs `data` and `difficulty` (integer). Iterates nonce from `0` until `hash(data + str(nonce))` starts with `difficulty` zeros. Run it for at least two difficulty levels (e.g., 2 and 4 zeros). Print the nonce, final hash, and time taken for each.

**[4. Passing Criteria According to the Rubric]**
* **Must have** — Working nonce finder that outputs a hash meeting the difficulty target; clear evidence that higher difficulty requires significantly more iterations or time.
* **Good to have** — A simple table comparing difficulty, nonce, hash, and elapsed time.
* **Necessary** — Difficulty must be a configurable parameter, not hardcoded to a single value.

**[5. Final Deliverable]**
* Python `.py` file + output/screenshot showing results for at least two difficulty levels.

---

**Practical 6: Wallets and Mnemonic Seed Phrases**

**[1. Objective]**
* Show how a wallet deterministically generates cryptographic keys from a human-readable BIP-39 mnemonic seed phrase.

**[2. Key Stuff to Learn]**
* BIP-39 mnemonic generation, seed derivation, deterministic key generation; Python `mnemonic` library or equivalent.

**[3. What to Code / Implement]**
* Python script that: (a) generates a random 12-word mnemonic, (b) converts it to a seed, (c) derives a private key and corresponding public key/address from that seed, (d) re-runs the same mnemonic to prove the keys are identical.

**[4. Passing Criteria According to the Rubric]**
* **Must have** — Valid mnemonic phrase output; derived key pair; proof of determinism (same mnemonic yields exactly the same keys).
* **Good to have** — Derivation of multiple addresses from the same seed using a basic HD path.
* **Necessary** — Use a standard BIP-39 library and wordlist. Do not invent your own word list.

**[5. Final Deliverable]**
* Python `.py` file + output showing the mnemonic, derived keys, and a confirmation note that re-running produces identical results.

---

**Practical 7: Write, Compile, and Deploy a Basic Smart Contract**

**[1. Objective]**
* Write a simple Solidity smart contract, compile it in Remix, deploy it to an EVM environment, and interact with it.

**[2. Key Stuff to Learn]**
* Solidity basics (`pragma`, `contract`, state variables, functions), Remix IDE workflow (Compile → Deploy → Interact), MetaMask basics (from syllabus Unit 3.2.4).

**[3. What to Code / Implement]**
* One simple Solidity contract (e.g., `SimpleStorage` with a `uint` variable, a setter, and a getter). Compile in Remix. Deploy to Remix VM (JavaScript London). Call the setter and then the getter to show the state change.

**[4. Passing Criteria According to the Rubric]**
* **Must have** — Valid `.sol` code; successful compilation with no errors; deployed contract instance visible in Remix; screenshot or log of a function call that changes state and a call that reads state.
* **Good to have** — Deployment on a public testnet via MetaMask with a transaction hash.
* **Necessary** — Remix screenshots proving compile, deploy, and interaction steps.

**[5. Final Deliverable]**
* `.sol` file + Remix screenshots showing the Compile tab, Deployed Contracts panel, and the interaction result.

---

**Practical 8: Deploy a Basic ERC-20 Token Contract**

**[1. Objective]**
* Understand tokenization by deploying a standard ERC-20 token using Remix IDE.

**[2. Key Stuff to Learn]**
* ERC-20 interface (`totalSupply`, `balanceOf`, `transfer`), OpenZeppelin `ERC20` contract, constructor minting, Remix deployment.

**[3. What to Code / Implement]**
* A Solidity contract that imports OpenZeppelin's `ERC20` and mints an initial supply to the deployer in the constructor. Compile and deploy in Remix. Query `balanceOf` for the deployer address. Optionally execute a `transfer`.

**[4. Passing Criteria According to the Rubric]**
* **Must have** — Contract inheriting from a standard ERC-20 implementation; successful Remix deployment; `balanceOf` query showing the initial minted supply; evidence of a working `transfer` or `balanceOf` call.
* **Good to have** — Custom `name`, `symbol`, and `decimals`; testnet deployment via MetaMask.
* **Necessary** — Use OpenZeppelin or equivalent standard library. Do not rewrite the ERC-20 standard from scratch.

**[5. Final Deliverable]**
* `.sol` file + Remix screenshots showing token deployment, the deployer's balance, and a transfer transaction/balance update.

---

**Practical 9: Public vs Private Blockchains (Hyperledger Fabric Case Study)**

**[1. Objective]**
* Differentiate public and private (permissioned) blockchains by explaining Hyperledger Fabric's architecture and components.

**[2. Key Stuff to Learn]**
* Permissionless vs permissioned differences (access, identity, speed, privacy), Fabric components (peers, orderers, channels, chaincode).

**[3. What to Code / Implement]**
* No code required. Produce: (a) a comparison table covering at least 5 criteria (access control, consensus, transaction speed, data privacy, identity management), (b) a simple diagram or bullet list explaining Fabric's peer-orderer-channel model, (c) a one-line conclusion on when to use which type.

**[4. Passing Criteria According to the Rubric]**
* **Must have** — Accurate differentiation across at least 5 criteria; correct description of Fabric peers, orderers, and channels; a clear conclusion.
* **Good to have** — Screenshot of the Hyperledger Fabric documentation or a local test-network execution.
* **Necessary** — Reference official Hyperledger Fabric architecture sources.

**[5. Final Deliverable]**
* 2–3 page report or presentation slides containing the comparison table, Fabric architecture diagram, and conclusion.

---

**Practical 10: Security Vulnerability & Green Energy DAO/Token Concept**

**[1. Objective]**
* Identify the re-entrancy vulnerability and conceptualize a Green Energy DAO/Token system.

**[2. Key Stuff to Learn]**
* Re-entrancy attack flow (syllabus 5.1.1), `checks-effects-interactions` mitigation, DAO governance basics, token utility, green energy oracle context (syllabus 5.3.2/5.3.3).

**[3. What to Code / Implement]**
* **Part A:** Minimal before/after Solidity snippets showing a re-entrancy vulnerability (e.g., a withdraw function that calls external address before updating balance) and the fixed version.
* **Part B:** A 1-page conceptual design for a Green Energy DAO/Token: token purpose, governance/voting mechanism, how energy data enters the system (oracle), and participant roles. No full implementation required.

**[4. Passing Criteria According to the Rubric]**
* **Must have** — Correct identification and explanation of re-entrancy (the attack flow); a valid mitigation shown; a plausible Green Energy DAO/token concept with defined token utility and basic governance.
* **Good to have** — Sequence diagram of the re-entrancy attack; mock Solidity for the DAO.
* **Necessary** — Explicitly reference syllabus topics: re-entrancy attacks, greenwashing problem, and oracle problem.

**[5. Final Deliverable]**
* Document containing: (a) re-entrancy explanation + before/after code snippets, (b) DAO/token concept description + diagram.