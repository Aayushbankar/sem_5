---
subject: AIPE
full_name: Artificial Intelligence with Prompt Engineering
code: DI05016011
units: 5
practicals: 12
status: not-started
tags: [subject/aipe, dashboard]
---
# 🤖 Artificial Intelligence with Prompt Engineering

> **DI05016011** · w.e.f. 2026-27 · GTU Diploma IT · Sem 5

---

## 📚 Theory Units

| Unit | Note | Status |
|---|---|---|
| Unit 1 | [[Unit 1 — Foundations of AI and Generative AI]] | ⬜ |
| Unit 2 | [[Unit 2 — Basics of Large Language Models]] | ⬜ |
| Unit 3 | [[Unit 3 — Prompt Engineering Fundamentals]] | ⬜ |
| Unit 4 | [[Unit 4 — Prompt Engineering Techniques]] | ⬜ |
| Unit 5 | [[Unit 5 — AI Application Development Agentic AI]] | ⬜ |

---

## 🧪 Practicals (12)

| # | Practical | Status |
|---|---|---|
| P01 | [[P01 — Genai Tools Tasks And Domains]] | ⬜ |
| P02 | [[P02 — Sentiment Analysis Text Classification]] | ⬜ |
| P03 | [[P03 — Llm Behavior Analysis]] | ⬜ |
| P04 | [[P04 — Llm Capabilities Limitations Hallucinations]] | ⬜ |
| P05 | [[P05 — Prompt Design And Refinement]] | ⬜ |
| P06 | [[P06 — Zero Shot Few Shot Role Based]] | ⬜ |
| P07 | [[P07 — Chain Of Thought Prompt Chaining]] | ⬜ |
| P08 | [[P08 — Task Based Prompt Engineering]] | ⬜ |
| P09 | [[P09 — Ai Tools For Software Development]] | ⬜ |
| P10 | [[P10 — Ai Chatbot Api Python]] | ⬜ |
| P11 | [[P11 — Document Qa Basic Rag]] | ⬜ |
| P12 | [[P12 — Ai Study Assistant]] | ⬜ |

---

## 💻 Code Files

- [[p01_genai_task_templates.txt]]
- [[p02_lexicon_fallback.py]]
- [[p02_sentiment_analysis.py]]
- [[p03_llm_behavior_test_matrix.md]]
- [[p04_question_bank_and_rubric.md]]
- [[p05_before_after_template.md]]
- [[p06_prompting_technique_templates.md]]
- [[p07_cot_and_chaining_templates.md]]
- [[p08_optimization_checklists.md]]
- [[p09_code_gen_debugging_cases.py]]
- [[p10_chatbot.py]]
- [[p11_rag_document_qa.py]]
- [[p11_sample_document.txt]]
- [[p12_study_assistant.py]]

---

## 🔗 Quick Links

- [[AIPE Resources|🔗 Resources]]
- [[AIPE Practical Tracker|📋 Practical Tracker]]
- [[DI05016011-AIPE.pdf|📄 Syllabus (PDF)]]

---

## ⚠️ Exam Tips

- Unit 5 (30%) is the heaviest — master the 4 app architectures, the API request/response shape, agentic AI, and Responsible AI.
- "Short notes" favorites: Narrow vs General AI, tokens/embeddings, hallucination, CoT, prompt chaining, RAG, OpenAI vs Gemini API, AI agents, AutoGPT/CrewAI, bias & fairness.
- Definition-heavy units (1–2) repay memorizing the glossaries and the 3 solved model answers in each chapter.
- Practical viva: know the *why* behind each code line (e.g., why the key is an env var in P10, why RAG grounds answers in P11, why mock-first in P10–P12).

---

## 🛠️ Requirements

- **Python practicals (P02, P09–P12):** Python 3.8+. Stdlib-only scripts; optional `pip install textblob` (P02) and `pip install requests` (P10–P12 live mode).
- **Tool-based practicals (P01, P03–P08):** any LLM tool of your choice — ChatGPT, Google Gemini, or Claude.
- **P10–P12 live API mode:** optional `AI_API_KEY` environment variable (OpenAI or Gemini key). Every script has a `--mock` flag that runs **fully offline** — no key, no network.
- **P02 note:** if `textblob` corpora can't download (offline), use the pure-stdlib lexicon fallback script — it runs anywhere.
