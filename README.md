# Semester 5 Academic Archive

Welcome to the ultimate engineering knowledge base for Semester 5. This repository houses an interconnected, hyper-structured academic blueprint covering hyperscale cloud systems, cryptography, hardware/IoT, and generative artificial intelligence.

## 🏛️ Architecture Overview

This project is divided into two major components:

1. **`/obsidian` (The Knowledge Graph)**
   - A fully functional, bidirectional Zettelkasten-style Obsidian Vault.
   - Contains 27 MIT-grade textbook unit notes and 58 engineering practicals.
   - Every file features active recall spaced-repetition blocks, detailed case studies, and advanced system design explanations.
   - 169 custom Mermaid.js diagrams visualizing complex protocols, architectural state machines, and hardware mapping.
   - LaTeX (KaTeX) integration for all mathematical bounds and algorithm equations.

2. **`/web` (The "Editorial Blueprint" Web Portal)**
   - A lightning-fast, zero-JS-by-default static site built on **Astro (Starlight)**.
   - Features a completely bespoke "Tufte/Blueprint" aesthetic. 
   - Uses high-density, high-contrast, structural design emphasizing raw readability (Crimson Pro) and engineering precision (JetBrains Mono).
   - Abandons generic "SaaS marketing" aesthetics in favor of academic rigor and clarity.
   - Automatically parses Obsidian `[[wikilinks]]` into a seamless web-based graph.

## ⚙️ Automated Deployment (GitHub Pages)

This repository utilizes a full CI/CD pipeline via GitHub Actions.
- **Trigger:** Any `push` to the `main` branch.
- **Workflow (`.github/workflows/deploy.yml`):** Automatically boots an Ubuntu server, installs Astro dependencies, securely compiles the Markdown, Math, and Diagrams, and generates a static `dist` bundle.
- **Hosting:** It is natively deployed to **GitHub Pages** (absolutely free and permanently scalable).

## 📚 Core Subjects

* **CDCT:** Cloud and Data Center Technology (SDN, AWS Nitro, Clos Networks, K8s).
* **FOB:** Foundation of Blockchain (EVM execution, PBFT Consensus, Cryptographic Hashes).
* **IOT:** Hands-on Practice using IoT (ESP32 SRAM, MQTT Handshakes, Bare-metal protocols).
* **AIPE:** AI with Prompt Engineering (Transformers, RAG indexing, KV Caching).
* **AIPD:** AI Product Design (Vector DB routing, System telemetry, Privacy architectures).

## 🚀 How to Run Locally

If you wish to run the web portal locally:

```bash
cd web
npm install
npm run dev
```
Navigate to `http://localhost:4321` to view the live rendering.

*Note: You can also just open the `/obsidian` folder directly inside the Obsidian desktop application for the offline graph view.*
