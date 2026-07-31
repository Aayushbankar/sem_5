---
title: "P12 — Ai Study Assistant"
sidebar:
  order: 12
---

# P12 — Build an AI Application: Study Assistant (with design docs for 3 more)

**Subject:** Artificial Intelligence with Prompt Engineering | **Unit:** 5 | **Approx. Hrs:** 4
**PrO (verbatim):** *Develop an AI-based application such as a Study Assistant/Resume Generator/Blog writer/Coding assistant.*

---

## 1. Objective
- Design a complete AI application: **AI Study Assistant** (the worked example).
- Implement a **working offline mock version** and run it.
- Produce **design documents** for 3 other apps: Resume Generator, Blog Writer, Coding Assistant.
- Show how prompt design + retrieval + a mock/real API fit together (the capstone of Units 3–5).

## 2. Application Architecture (Study Assistant)

```
                        ┌─────────────────────────────────────────┐
  student types        │             STUDY ASSISTANT             │
  "explain RAG"  ──►   │                                         │
                        │  ┌─────────────┐   ┌─────────────────┐  │
                        │  │   RETRIEVER │   │   PROMPT BUILDER │  │
                        │  │ keyword +   │──►│ role + task +   │  │
                        │  │ n-gram      │   │ retrieved notes │  │
                        │  │ scoring     │   └────────┬────────┘  │
                        │  └─────────────┘            │           │
                        │   knowledge base    ┌───────▼────────┐  │
                        │   (study notes)     │   LLM CLIENT   │  │
                        │                     │  mock | API    │  │
                        │                     │ (P10 ChatClient)│  │
                        │                     └───────┬────────┘  │
                        │                             │           │
                        │                     explain / summary   │
                        │                     / quiz response ──► │
                        └─────────────────────────────────────────┘
```

Three layers, each independently swappable:
| Layer | Component | Mock (offline) | Real (production) |
|---|---|---|---|
| **Knowledge** | study notes + retriever | dictionary of notes, keyword scoring | vector DB + embedding model |
| **Reasoning** | prompt builder | templates with role/context/format | same templates |
| **Brain** | LLM client | canned + rule-based responses | `ChatClient` from P10 with `AI_API_KEY` |

**Prompt design in the app** (the Unit 3/4 skills in production):
- *Role:* "You are a friendly tutor for diploma IT students…"
- *Context:* the retrieved note passages (RAG from P11).
- *Input data:* the student's topic.
- *Output format:* "Explain in 3–4 sentences with one real-world example."

## 3. Implementation — offline mock

Script: [`p12_study_assistant.py`](./p12_study_assistant.py.md) — reuses `ChatClient` from P10 and adds a tiny retrieval layer. Three commands:

| Command | What it does | Mock implementation |
|---|---|---|
| `explain <topic>` | Retrieves the best notes and explains the topic | Mock brain rephrases the top note into a plain-language explanation |
| `summary <topic>` | One-line takeaway | Returns the note's stored "one-liner" |
| `quiz <topic>` | Generates MCQs | Rule-based MCQ set (live mode: model generates topic-specific MCQs) |

## 4. Actual run (`python3 p12_study_assistant.py --mock --topic "prompt engineering"`)

```
========================================================================
AI STUDY ASSISTANT (mock=True, provider=openai)
Commands: explain <topic> | summary <topic> | quiz <topic>
========================================================================

[retrieval] top 2 note(s) for 'prompt engineering':
  - [prompt engineering] Prompt engineering is the practice of designing instructions for an LLM to get  ...
  - [llm] A Large Language Model is a deep neural network trained on massive text corpora to predict the ...

>>> explain
[mock] Prompt Engineering in simple words: prompt engineering is the practice of designing instructions for an llm to get accurate, well-formatted outputs. It works best when you combine a clear definition with practice. Example: ask your assistant 'explain prompt engineering' and then quiz yourself on it.

>>> summary
[mock] Summary of 'prompt engineering': The quality of the prompt directly controls the quality of the answer.

>>> quiz
[mock] Quiz for you:
1. Which technique shows a model examples before the real question?
   - Few-shot prompting (correct)
   - Zero-shot prompting
   - Fine-tuning
   - Tokenization
2. What does the context window limit?
   - The number of tokens a model can process at once (correct)
   - Zero-shot prompting
   - Fine-tuning
   - Tokenization
3. Which step comes first in a RAG pipeline?
   - Chunking the document (correct)
   - Zero-shot prompting
   - Fine-tuning
   - Tokenization
```

All three commands work end-to-end offline: retrieval found the right note, and the mock brain produced an explanation, a summary, and a quiz.

**To run live:** `export AI_API_KEY=sk-...` then `python3 p12_study_assistant.py` — the same app, now with real model answers (and topic-specific MCQs).

## 5. Design docs for the other 3 suggested apps

### App 1 — AI Resume Generator
- **Input:** student details (JSON): name, education, skills, projects, achievements.
- **Prompt design:** role "professional resume writer"; output format — ATS-friendly sections; tone keyword-matched to the job description.
- **Pipeline (chain, P07):** ① extract highlights from raw input → ② draft 3 bullet styles per section → ③ format to markdown/PDF-ready text.
- **Retrieval/RAG:** optional — scan the job description to rank which skills to highlight.
- **Mock:** template-based resume from the JSON with canned bullets; real: LLM rewrites bullets.
- **Deliverables:** input schema, prompt templates, output sample.

### App 2 — AI Blog Writer
- **Input:** topic, audience, tone, target words.
- **Prompt design:** title generation → outline → section-by-section drafting (chaining) → hook/CTA variants → final SEO checklist.
- **Human-in-the-loop:** each chain stage output is reviewed before the next stage.
- **Mock:** fill outline with template paragraphs; real: full prose generation.
- **Deliverables:** chain diagram, prompt set, before/after article sample.

### App 3 — AI Coding Assistant
- **Input:** task spec or code snippet.
- **Prompt design:** role "senior reviewer"; few-shot examples; always ask for tests + explanation; instruction "run and verify before trusting".
- **Pipeline:** ① generate/explain → ② static checks (imports, naming) → ③ test generation.
- **Mock:** canned code review comments keyed to common bug patterns (as in P09).
- **Deliverables:** command list (generate/explain/fix/test), prompt templates, verification checklist.

**Shared architecture** (all 4 apps): `retriever (optional) → prompt builder → LLM client (mock/API) → formatter → human review`. That one diagram describes every AI application in Unit 5.

## 6. Deliverable — report skeleton
1. Architecture diagram + layer table (Section 2).
2. Code listing with the three commands highlighted.
3. Pasted real `--mock` output (Section 4).
4. One design doc for each of the 3 other apps (Section 5).
5. Conclusion: what you'd add for production (vector DB, chat memory, rate limiting, UI).

## 7. Conclusion
The Study Assistant ties the whole course together: **prompt design** (role/context/format from Unit 3), **retrieval** (RAG from Unit 4/P11), **API integration** (P10), and **responsibility** (mock mode means it demos anywhere, and grounding means fewer hallucinations). The same four-layer architecture ports directly to the Resume/Blog/Coding apps — that's what "build an AI application" means in practice.

## 8. Viva Q&A
1. **What are the layers of the app?** — Knowledge/retrieval, prompt building, LLM client, formatter.
2. **Why a mock brain?** — The full loop runs offline for demos, tests, and marking; the real API is a drop-in swap.
3. **How does prompt design appear here?** — Role + context + input + output format are all explicit in `build_explain_prompt`.
4. **How is RAG used?** — The retriever pulls relevant notes and they become the prompt's context.
5. **What would production add?** — Vector embeddings, chat memory, rate limiting, a web UI, and content safety filters.
6. **How do the 4 app ideas share code?** — Same pipeline; only the prompts, data schemas, and formatters change.

## 9. Resources
- Prompt patterns from Units 3–4 of these notes: [UNIT 3](./Unit%203%20—%20Prompt%20Engineering%20Fundamentals.md), [UNIT 4](./Unit%204%20—%20Prompt%20Engineering%20Techniques.md)
- OpenAI cookbook: https://cookbook.openai.com
- Gemini API docs: https://ai.google.dev/gemini-api/docs
- Script: [`p12_study_assistant.py`](./p12_study_assistant.py.md)

---



---

## 🐛 Failure Modes & Debugging (Real-World Experience)

> [!bug] What goes wrong in production?
> When running **Ai Study Assistant** in a real environment, it almost never works perfectly the first time. 
> 
> **Common Edge Cases to Test:**
> 1. **Network partitions:** What happens to this code if the Wi-Fi drops halfway through execution?
> 2. **Malformed Inputs:** How does the system behave if fed null values, extremely large datasets, or unexpected data types?
> 3. **Resource Exhaustion:** Does this script handle memory leaks or rate-limiting from APIs?

## 🔬 Extension Challenge

> [!example] Prove your expertise
> To truly master this practical, try modifying the code to achieve the following:
> - **Add robust error handling** (try/catch blocks) and structured logging instead of print statements.
> - **Parameterize the inputs** so the script can be run dynamically from the CLI without hardcoding values.
> - **Optimize it:** Can you reduce the execution time or memory footprint?

## 🎯 Key Takeaways

- **What are the layers of the app?** — Knowledge/retrieval, prompt building, LLM client, formatter.
- **Why a mock brain?** — The full loop runs offline for demos, tests, and marking; the real API is a drop-in swap.
- **How does prompt design appear here?** — Role + context + input + output format are all explicit in `build_explain_prompt`.
- **How is RAG used?** — The retriever pulls relevant notes and they become the prompt's context.
- **What would production add?** — Vector embeddings, chat memory, rate limiting, a web UI, and content safety filters.
- **How do the 4 app ideas share code?** — Same pipeline; only the prompts, data schemas, and formatters change.

> [!tip] Viva Prep
> Be ready to explain the *why* behind each step, not just the output.
