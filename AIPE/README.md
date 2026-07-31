# AIPE — Artificial Intelligence with Prompt Engineering (DI05016011)

> **w.e.f. 2026-27** · GTU Diploma Engineering · Information Technology · Sem 5

Complete study kit: solved practicals (with runnable code), 5 gold theory chapters, and curated resources.

## 📊 Progress
- Practicals: **[tracker](./PRACTICALS.md)** · 12 practicals / 30 hrs

## 🧪 Practicals (12)
| # | Practical | Solution | Code |
|---|-----------|----------|------|
| P01 | Use Generative AI tools for different task types & domains | [P01](./practicals/writeups/P01_genai_tools_tasks_and_domains.md) | [prompt templates](./practicals/code/p01_genai_task_templates.txt) |
| P02 | Sentiment analysis & text classification with Python | [P02](./practicals/writeups/P02_sentiment_analysis_text_classification.md) | [p02_sentiment_analysis.py](./practicals/code/p02_sentiment_analysis.py) + [lexicon fallback](./practicals/code/p02_lexicon_fallback.py) |
| P03 | LLM behavior: prompt variation, context, consistency | [P03](./practicals/writeups/P03_llm_behavior_analysis.md) | [test matrix](./practicals/code/p03_llm_behavior_test_matrix.md) |
| P04 | LLM capabilities & limitations, hallucination ID | [P04](./practicals/writeups/P04_llm_capabilities_limitations_hallucinations.md) | [question bank + rubric](./practicals/code/p04_question_bank_and_rubric.md) |
| P05 | Design & refine prompts (email, concept) | [P05](./practicals/writeups/P05_prompt_design_and_refinement.md) | [before/after template](./practicals/code/p05_before_after_template.md) |
| P06 | Zero-shot, few-shot, role-based prompting | [P06](./practicals/writeups/P06_zero_shot_few_shot_role_based.md) | [technique templates](./practicals/code/p06_prompting_technique_templates.md) |
| P07 | Chain-of-thought & prompt chaining | [P07](./practicals/writeups/P07_chain_of_thought_prompt_chaining.md) | [CoT + chaining templates](./practicals/code/p07_cot_and_chaining_templates.md) |
| P08 | Task-based prompt engineering (summary/blog/code) | [P08](./practicals/writeups/P08_task_based_prompt_engineering.md) | [optimization checklists](./practicals/code/p08_optimization_checklists.md) |
| P09 | AI tools for software development (gen/debug/explain) | [P09](./practicals/writeups/P09_ai_tools_for_software_development.md) | [p09_code_gen_debugging_cases.py](./practicals/code/p09_code_gen_debugging_cases.py) |
| P10 | AI chatbot via API (OpenAI/Gemini) with Python | [P10](./practicals/writeups/P10_ai_chatbot_api_python.md) | [p10_chatbot.py](./practicals/code/p10_chatbot.py) |
| P11 | Document-based Q&A (basic RAG) | [P11](./practicals/writeups/P11_document_qa_basic_rag.md) | [p11_rag_document_qa.py](./practicals/code/p11_rag_document_qa.py) + [sample doc](./practicals/code/p11_sample_document.txt) |
| P12 | Build an AI application (Study Assistant) | [P12](./practicals/writeups/P12_ai_study_assistant.md) | [p12_study_assistant.py](./practicals/code/p12_study_assistant.py) |

## 📚 Theory Notes (per unit)
| Unit | Title | Weightage | Notes |
|------|-------|-----------|-------|
| 1 | Foundations of Artificial Intelligence & Generative AI | 15% (6h) | [UNIT_1](./notes/UNIT_1_Foundations_of_AI_and_Generative_AI.md) |
| 2 | Basics of Large Language Models (LLMs) | 15% (6h) | [UNIT_2](./notes/UNIT_2_Basics_of_Large_Language_Models.md) |
| 3 | Prompt Engineering Fundamentals | 20% (9h) | [UNIT_3](./notes/UNIT_3_Prompt_Engineering_Fundamentals.md) |
| 4 | Prompt Engineering Techniques | 20% (9h) | [UNIT_4](./notes/UNIT_4_Prompt_Engineering_Techniques.md) |
| 5 | AI Application Development: Generative AI, Agentic AI | 30% (15h) | [UNIT_5](./notes/UNIT_5_AI_Application_Development_Agentic_AI.md) |

## 🔗 Resources
- [Curated links (docs, papers, courses, tools, books, videos)](./notes/RESOURCES.md)

## 🛠 Requirements
- **Python practicals (P02, P09–P12):** Python 3.8+. Stdlib-only scripts; optional `pip install textblob` (P02) and `pip install requests` (P10–P12 live mode).
- **Tool-based practicals (P01, P03–P08):** any LLM tool of your choice — ChatGPT, Google Gemini, or Claude.
- **P10–P12 live API mode:** optional `AI_API_KEY` environment variable (OpenAI or Gemini key). Every script has a `--mock` flag that runs **fully offline** — no key, no network.
- **P02 note:** if `textblob` corpora can't download (offline), use the pure-stdlib lexicon fallback script — it runs anywhere.

## ⚠️ Exam tips
- Unit 5 (30%) is the heaviest — master the 4 app architectures, the API request/response shape, agentic AI, and Responsible AI.
- "Short notes" favorites: Narrow vs General AI, tokens/embeddings, hallucination, CoT, prompt chaining, RAG, OpenAI vs Gemini API, AI agents, AutoGPT/CrewAI, bias & fairness.
- Definition-heavy units (1–2) repay memorizing the glossaries and the 3 solved model answers in each chapter.
- Practical viva: know the *why* behind each code line (e.g., why the key is an env var in P10, why RAG grounds answers in P11, why mock-first in P10–P12).
