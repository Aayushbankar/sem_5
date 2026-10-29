# AIPE Practical Submission Package

**Subject:** Artificial Intelligence with Prompt Engineering (DI05016011)
**Semester:** 5 · **Branch:** IT · **Academic Year:** 2026-27

---

## Submission Structure

```
submission/
├── INDEX.md                              # Practical index with student details
├── README.md                             # This guide
├── writeups/                             # 12 practical writeups (faculty format)
│   ├── P01_GenAI_Tools_Tasks_Domains.md
│   ├── P02_Sentiment_Analysis.md
│   ├── P03_LLM_Behavior_Analysis.md
│   ├── P04_LLM_Capabilities_Limitations.md
│   ├── P05_Prompt_Design_Refinement.md
│   ├── P06_Zero_Few_Shot_Role.md
│   ├── P07_CoT_Prompt_Chaining.md
│   ├── P08_Task_Based_Prompt_Eng.md
│   ├── P09_AI_Tools_Software_Dev.md
│   ├── P10_AI_Chatbot_API.md
│   ├── P11_Document_QA_RAG.md            # ← Privata (real RAG, not mock)
│   └── P12_AI_Study_Assistant.md         # ← Security Research Assistant
├── code/                                 # All practical code files
│   ├── p01_genai_task_templates.txt
│   ├── p02_lexicon_fallback.py
│   ├── p02_sentiment_analysis.py
│   ├── p03_llm_behavior_test_matrix.md
│   ├── p04_question_bank_and_rubric.md
│   ├── p05_before_after_template.md
│   ├── p06_prompting_technique_templates.md
│   ├── p07_cot_and_chaining_templates.md
│   ├── p08_optimization_checklists.md
│   ├── p09_code_gen_debugging_cases.py
│   ├── p10_chatbot.py
│   ├── p11_rag_document_qa.py            # Original mock RAG (kept for reference)
│   ├── p11_sample_document.txt
│   ├── p12_security_research_assistant.py  # ← NEW: Real security research tool
│   ├── p12_study_assistant.py            # Original mock (kept for reference)
│   └── privata/                          # ← NEW: Privata RAG project (real implementation)
│       ├── main.py
│       ├── ingest.py
│       ├── chat.py
│       ├── config.py
│       ├── requirements.txt
│       ├── models/llm_loader.py
│       ├── retriever/embedder.py
│       ├── retriever/vectordb.py
│       └── utils/doc_loader.py
└── screenshots/                          # Placeholder for terminal screenshots
```

---

## Key Changes from Original

| Practical | Original | Updated To |
|-----------|----------|------------|
| **P11** | Mock RAG (character n-grams, no deps) | **Privata** — Real RAG with HuggingFace MiniLM embeddings, ChromaDB, Gemini 1.5-flash |
| **P12** | Generic Study Assistant | **Security Research Assistant** — CVE analysis, exploit chains, kernel offsets, forensic analysis, whitepaper generation |

---

## Faculty Guidelines Compliance

Per faculty message, each practical writeup includes:

| Required Element | Location in Writeup |
|-----------------|---------------------|
| **1. Aim** | Section 1 of each writeup |
| **2. Process / Program Code / Prompts Used** | Section 2 — full prompts, code snippets, theory |
| **3. Screenshot of Output with Name & Roll No** | Section 3 — actual run outputs with `[STUDENT NAME, ROLL NO]` placeholders |
| **4. Application of Learning** | Section 4/5 — domain applications table with example projects |

**Additional Requirements:**
- ✅ Index page with practical number and aim (INDEX.md)
- ✅ Print copy ready (all Markdown → printable)
- ✅ Soft copy ready (this folder structure)
- ✅ Practical-wise code/prompt files in `code/`

---

## How to Complete Before Submission

1. **Fill Student Details** in `INDEX.md` and each writeup's header
2. **Replace Placeholders** `[STUDENT NAME]` and `[ROLL NO]` throughout all writeups with actual values
3. **Add Screenshots** — Run each practical, capture terminal output screenshots, save as `P01_*.png`, `P02_*.png`, etc. in `screenshots/`

### Key Scripts to Run for Screenshots

```bash
# P02 - Sentiment Analysis
python3 code/p02_sentiment_analysis.py
python3 code/p02_lexicon_fallback.py

# P09 - AI Tools for Software Dev
python3 code/p09_code_gen_debugging_cases.py

# P10 - Chatbot API (mock mode)
python3 code/p10_chatbot.py --mock

# P11 - Privata RAG (requires Gemini API key for live mode)
# Offline ingestion (no key needed):
cd code/privata && python3 main.py
# Select [1] Ingest Documents → point to your notes folder
# Select [2] Start Chatbot → ask questions

# P12 - Security Research Assistant (mock mode)
python3 code/p12_security_research_assistant.py --mock cve CVE-2026-28576
python3 code/p12_security_research_assistant.py --mock chain "kernel uaf to root"
python3 code/p12_security_research_assistant.py --mock exploit CVE-2026-28576
python3 code/p12_security_research_assistant.py --mock forensic "ebpf trace"
python3 code/p12_security_research_assistant.py --mock report "CVE-2026-28576 disclosure"
python3 code/p12_security_research_assistant.py --mock offsets 5.15
```

4. **Print** — Export all `.md` files to PDF or print directly
5. **Verify Code Runs** — Test key scripts (see above)

---

## Practical Mapping to Syllabus

| # | Practical | Unit | Hrs | Syllabus PrO |
|---|-----------|------|-----|--------------|
| 1 | GenAI Tools: Tasks & Domains | 1 | 2 | Use GenAI tools for different tasks, document domain applications |
| 2 | Sentiment Analysis & Text Classification | 1 | 2 | Perform NLP tasks using AI tools/Python libraries |
| 3 | LLM Behavior Analysis | 2 | 2 | Test prompt variations, context understanding, response consistency |
| 4 | LLM Capabilities & Limitations | 2 | 2 | Test factual/logical/ambiguous/counterfactual queries, ID hallucinations |
| 5 | Prompt Design & Refinement | 3 | 2 | Design/refine prompts for email & concept explanation, compare before/after |
| 6 | Zero/Few-Shot & Role-Based Prompting | 3 | 2 | Apply zero-shot, few-shot, role-based prompting techniques |
| 7 | Chain-of-Thought & Prompt Chaining | 4 | 2 | Apply CoT and prompt chaining for multi-step problems |
| 8 | Task-Based Prompt Engineering | 4 | 2 | Summarization, blog generation, code generation with optimization |
| 9 | AI Tools for Software Development | 5 | 2 | Code generation, debugging, explanation using AI tools |
| 10 | AI Chatbot via API | 5 | 4 | Develop chatbot with OpenAI/Gemini API in Python |
| 11 | Document Q&A (RAG) — **Privata** | 5 | 4 | Build document-based Q&A system using RAG (real implementation) |
| 12 | AI Application — **Security Research Assistant** | 5 | 4 | Develop AI application for vulnerability research |

---

## Why These Changes?

### P11 — Privata (Real RAG)
- Your actual project: https://github.com/Aayushbankar/Privata
- Uses **local embeddings** (HuggingFace `all-MiniLM-L6-v2`) — privacy, no embedding API costs
- Uses **ChromaDB** — persistent local vector store
- Uses **Gemini 1.5-flash** — fast, accurate generation
- **Grounded answers** — explicitly refuses when context insufficient (anti-hallucination)
- Production architecture: `load → chunk → embed → store → retrieve → generate`

### P12 — Security Research Assistant
- **Directly applicable to your work:**
  - CVE-2026-28576 (Android Contacts Provider SQLi) — first-to-publish analysis
  - spectre-prism (eBPF/kernel forensics)
  - cve-chaining-hunter (app→kernel exploit chains)
  - novel-exploit-chain-builder (reliable kernel exploit chains)
  - about_me/ (Obsidian knowledge vault)
- **Reuses Privata infrastructure** — same ChromaDB + MiniLM + Gemini pipeline
- **Commands you'll actually use daily:**
  - `cve CVE-2026-28576` → instant full analysis + PoC + chaining map
  - `chain "kernel uaf to root"` → exploit chain with offsets, reliability
  - `exploit <vuln-class>` → PoC skeleton
  - `forensic "ebpf trace"` → tracing patterns + analysis scripts
  - `report <topic>` → technical whitepaper / disclosure draft
  - `offsets 5.15` → kernel symbol offsets for exploit dev

---

## Quick Verification Checklist

- [ ] All 12 writeups present in `writeups/`
- [ ] All code files present in `code/` (including `privata/` subdirectory)
- [ ] Student name & roll number filled in INDEX.md and all writeups
- [ ] Screenshots captured and placed in `screenshots/`
- [ ] Code verified to run (at least mock modes)
- [ ] Print copies generated
- [ ] Soft copy (this folder) ready for submission

---

**Prepared by:** [STUDENT NAME]  
**Roll No:** [ROLL NO]  
**Date:** ________________