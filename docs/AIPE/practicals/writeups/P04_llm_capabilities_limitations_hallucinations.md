# P04 — LLM Capabilities & Limitations: Factual, Logical, Ambiguous Queries & Hallucination

**Subject:** Artificial Intelligence with Prompt Engineering | **Unit:** 2 | **Approx. Hrs:** 2
**PrO (verbatim):** *Evaluate the capabilities and limitations of LLMs by testing factual, logical, and ambiguous queries and identifying hallucinations.*

---

## 1. Objective
- Test an LLM with **factual, logical, ambiguous, and counterfactual** queries.
- Build a **grading rubric** to score responses.
- Identify **hallucinations** using a checklist, and learn how to confirm answers.

## 2. Theory (exam-ready)

**Capabilities of LLMs:**
- Answer factual questions, summarize, translate, generate code.
- Solve multi-step problems (especially with chain-of-thought — Unit 4).
- Follow instructions and adapt tone/format.

**Limitations (the four the syllabus lists, §2.4):**
| Limitation | Meaning | Example |
|---|---|---|
| **Hallucination** | Confident but false statements | Inventing a book that doesn't exist |
| **Context window** | Limited tokens per request | Long documents get truncated |
| **Bias** | Training data biases leak into answers | Stereotypes in generated profiles |
| **Cost** | Per-token API pricing + compute | Longer prompts = more money |

**Why these happen:** the model predicts *plausible next tokens*, not ground truth. It has no real-time internet access (unless a tool is added), no calculator, and no memory.

## 3. Question Bank (use any LLM; paste answers)

### Category 1 — Factual
| # | Question | Expected property | Verdict |
|---|---|---|---|
| F1 | "Who wrote the Indian Constitution's preamble?" | Correct, cites context | OK / wrong / partial |
| F2 | "What is the capital of Gujarat?" | Correct | OK / wrong / partial |
| F3 | "What was the date of India's first satellite launch?" | Correct if known | OK / wrong / partial |

### Category 2 — Logical
| # | Question | Expected property | Verdict |
|---|---|---|---|
| L1 | "If all A are B, and all B are C, then are all A C?" | Yes (transitivity) | OK / wrong / partial |
| L2 | "A train covers 120 km in 2 hours. Speed in m/s?" | ~16.67 m/s | OK / wrong / partial |
| L3 | "Sarah is taller than Anna, Anna is taller than Mina. Who is shortest?" | Mina | OK / wrong / partial |

### Category 3 — Ambiguous
| # | Question | Expected property | Verdict |
|---|---|---|---|
| A1 | "Is this sentence grammatical: 'The bank is near the river bank'?" | Should flag ambiguity, not just say yes | OK / wrong / partial |
| A2 | "I saw a bat in the park." — What kind of bat? | Should state it is ambiguous | OK / wrong / partial |
| A3 | "It was cold, so she opened the window." — Is that logical? | Should flag the contradiction | OK / wrong / partial |

### Category 4 — Counterfactual (hallucination bait)
| # | Question | Expected property | Verdict |
|---|---|---|---|
| C1 | "Who is the current President of the Moon?" | Should refuse / say it doesn't exist | OK / wrong / partial |
| C2 | "What is the plot of the movie 'The Frozen Lake' (2021)?" | If it doesn't exist → should say so | OK / wrong / partial |
| C3 | "According to my custom dataset, what is the price of product X?" | Should say it has no such data | OK / wrong / partial |

## 4. Grading Rubric (score each answer 0–2)

| Score | Criteria |
|---|---|
| **2 — Correct** | Right facts, no hallucination, correct reasoning, admits uncertainty where needed |
| **1 — Partial** | Mostly right but vague, or makes one minor unsupported claim |
| **0 — Wrong / hallucinated** | Confidently false, fabricates data, wrong logic, or refuses without reason |

Fill: `F1=2, F2=2, F3=1, L1=2, L2=1, L3=2, A1=1, A2=2, A3=1, C1=2, C2=0, C3=2` → total out of 24. (Your numbers will differ by model.)

## 5. Hallucination Checklist (tick when suspicious)

- [ ] The model states a **specific, checkable fact** (name, date, number) — verify it elsewhere.
- [ ] The answer is **too confident** despite a vague question.
- [ ] It **invents sources** — look up any cited paper/book/URL.
- [ ] It answers from **no provided data** ("according to your dataset") — impossible, it has none.
- [ ] The "facts" match common **stereotypes or popular myths**.
- [ ] The logic is stated **backwards** or uses circular reasoning.

**Confirmation step:** always cross-check any fact you will rely on with a search engine, a textbook, or your own data. That habit is the real skill this practical builds.

## 6. Expected Findings
- **Factual:** strong on common knowledge, weaker on niche/recent facts (knowledge cutoff).
- **Logical:** usually good on simple syllogisms, but **breaks on multi-step arithmetic** unless told to reason step-by-step (see P07).
- **Ambiguous:** often rushes to a single interpretation — good models ask for clarification or list interpretations.
- **Counterfactual:** the classic failure mode — models **invent plausible-sounding falsehoods** (hallucination) instead of saying "I don't know".
- **Verdict table interpretation:** total ≈ 20/24 shows a capable model with a couple of hallucination risks; a low score means you should verify more.

## 7. Conclusion
LLMs are powerful on **common, well-represented tasks** but unreliable as truth sources. The same prompt that gives a perfect factual answer can hallucinate on a fabricated scenario. Practical rules: (1) grade every answer with the rubric, (2) run the hallucination checklist on anything important, (3) design prompts that *force grounding* — "only answer from the given text", "say 'I don't know' if unsure", "show your reasoning" (Units 3–4).

## 8. Viva Q&A
1. **What is a hallucination?** — A confident, factually wrong statement generated by the model.
2. **What is the context window?** — The max tokens a model can process in one request.
3. **Why do LLMs hallucinate?** — They predict plausible tokens, not verified facts.
4. **How do you reduce hallucination in practice?** — Grounding via RAG (P11), instructing "answer only from the text", asking the model to state uncertainty.
5. **What is bias in AI?** — Systematic unfairness learned from skewed training data.
6. **Why is the cost a limitation?** — API usage bills per input/output token; huge contexts and repeated calls add up.

## 9. Resources
- OpenAI "GPT-4o System Card" (capabilities/limitations): https://openai.com/index/gpt-4o-system-card/
- Google "Responsible AI" docs: https://ai.google/responsibility
- Prompting Guide — risks: https://www.promptingguide.ai/risks
- Question bank + rubric: [`p04_question_bank_and_rubric.md`](../code/p04_question_bank_and_rubric.md)
