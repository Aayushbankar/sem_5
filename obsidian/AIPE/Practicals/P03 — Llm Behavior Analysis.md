---
subject: AIPE
status: not-started
tags: [subject/aipe, practical, unit/2]
practical: 3
unit: 2
hours: 2
---
# P03 — LLM Behavior Analysis: Prompt Variation, Context Understanding, Response Consistency

**Subject:** Artificial Intelligence with Prompt Engineering | **Unit:** 2 | **Approx. Hrs:** 2
**PrO (verbatim):** *Perform experiments to analyze the behavior of LLM by testing prompt variations, context understanding and response consistency.*

---

## 1. Objective
- Observe how **rephrasing a prompt** changes the output.
- Observe how **adding/removing context** changes the output.
- Measure **response consistency** by repeating the exact same prompt 3 times.
- Record results in a standard **test matrix** and draw conclusions about LLM behavior.

## 2. Theory (exam-ready)

An LLM is a next-token predictor. Its output is influenced by:
- **The prompt** — instruction, context, input data, output format.
- **Sampling settings** — `temperature` (0 = near-deterministic, 1+ = creative/random), `top-p`.
- **The model itself** — training data, parameter count, system prompt.

Because generation is **probabilistic**, the same prompt can give different outputs on different runs. Understanding this is the basis of **prompt engineering** (Unit 3): small wording changes measurably change output quality.

Key behaviors to test:
| Behavior | What we look for |
|---|---|
| **Prompt variation** | Does rephrasing the *same request* change tone, length, or content? |
| **Context understanding** | Does extra context (role, examples, constraints) improve relevance? |
| **Response consistency** | Does repeating the identical prompt give the same answer 3 times? |

## 3. Experiment Design — the Test Matrix

Use any LLM (ChatGPT, Gemini, or Claude). Run each row, paste the outputs, and fill in the "observed" column. The matrix below is a filled example.

### Test A — Prompt variation (same task, 3 phrasings)

| # | Prompt | LLM output (paste) | Observed differences |
|---|---|---|---|
| A1 | "Explain machine learning." | *(paste)* | Baseline — generic, no audience |
| A2 | "Explain machine learning in 2 lines for a school student." | *(paste)* | Shorter, simpler words, analogy used |
| A3 | "Explain machine learning with a concrete example, in a formal tone." | *(paste)* | Longer, formal, technical example |

**Fillable template:**
```
A1 prompt:  ...
A1 output:  ...
A2 prompt:  ...
A2 output:  ...
A3 prompt:  ...
A3 output:  ...
What changed and why: ...
```

### Test B — Context understanding (add/remove context)

| # | Prompt | LLM output (paste) | Observed differences |
|---|---|---|---|
| B1 | "Summarize the meeting notes." | *(paste)* | Generic summary, invents structure |
| B2 | "Summarize: {3 lines of your real meeting notes}" | *(paste)* | Stays close to the given text |
| B3 | "Summarize: {same notes}. Focus only on action items, list them as bullets." | *(paste)* | Correct focus + format = most useful |

**Fillable template:**
```
B1 output: ...
B2 output: ...
B3 output: ...
Which context mattered most? ...
```

### Test C — Response consistency (same prompt × 3)

| # | Prompt (identical each time) | Output 1 | Output 2 | Output 3 | Same wording? |
|---|---|---|---|---|---|
| C1 | "Give me one career tip." | *(paste)* | *(paste)* | *(paste)* | Usually **no** |
| C2 | "1+1 = ? Answer with only the number." | *(paste)* | *(paste)* | *(paste)* | Usually **yes** |

**Fillable template:**
```
C1 (creative, temperature high)  → 3 different answers?  yes/no
C2 (factual, constrained format) → 3 identical answers? yes/no
Conclusion: ...
```

## 4. How to run (steps)
1. Open your chosen tool (e.g., https://chat.openai.com or https://gemini.google.com).
2. Copy the **three prompts of Test A**, send them one at a time, paste the outputs into the matrix.
3. Repeat for Test B — first without your data, then with it.
4. For Test C, send the **exact same prompt 3 times** (use "new chat" each time) and compare wording.
5. Fill the two "observed" columns and write a 5-line conclusion.

## 5. Expected Findings (what students typically observe)
- **Rephrasing changes style more than facts.** A2/A3 are shorter/more formal but the *core facts* stay the same.
- **Context matters more than wording.** B2 vs B1: feeding the actual text removes invented details. B3 shows output *format* follows the format instruction.
- **Consistency depends on the task.** Creative/opinion prompts vary a lot; constrained factual prompts ("answer with only the number") are stable. This is why production systems set low temperature and fixed formats.
- **LLMs do not have memory across chats** — each chat starts fresh unless you re-provide context (this is why RAG in P11 exists).

## 6. Conclusion
An LLM's output is a function of **(prompt + sampling settings + model)**, not a fixed database lookup. Two practical consequences: (1) iterate on prompts — wording and context are cheap to tune; (2) pin down expectations with format constraints if you need repeatable answers.

## 7. Viva Q&A
1. **Why do repeated prompts give different answers?** — Because the model samples the next token from a probability distribution (temperature > 0).
2. **Which affects output more: wording or context?** — Usually context (facts, constraints) changes correctness; wording changes style.
3. **What is temperature?** — A sampling knob; low = deterministic, high = creative/random.
4. **Does the model remember earlier chats?** — No; each session is independent unless context is re-provided.
5. **How would you get a repeatable answer?** — Set temperature ≈ 0 and constrain the output format.

## 8. Resources
- Prompt Engineering Guide — Behaviors & risks: https://www.promptingguide.ai/risks
- OpenAI prompt engineering docs: https://platform.openai.com/docs/guides/prompt-engineering
- Google Gemini prompt guide: https://developers.google.com/learn/pathways/prompt-engineering
- Template matrix: [[p03_llm_behavior_test_matrix.md|`p03_llm_behavior_test_matrix.md`]]

---



---

## 🐛 Failure Modes & Debugging (Real-World Experience)

> [!bug] What goes wrong in production?
> When running **Llm Behavior Analysis** in a real environment, it almost never works perfectly the first time. 
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

- **The prompt** — instruction, context, input data, output format.
- **Sampling settings** — `temperature` (0 = near-deterministic, 1+ = creative/random), `top-p`.
- **The model itself** — training data, parameter count, system prompt.
- **LLMs do not have memory across chats** — each chat starts fresh unless you re-provide context (this is why RAG in P11 exists).
- **Why do repeated prompts give different answers?** — Because the model samples the next token from a probability distribution (temperature > 0).
- **Which affects output more: wording or context?** — Usually context (facts, constraints) changes correctness; wording changes style.
- **What is temperature?** — A sampling knob; low = deterministic, high = creative/random.
- **Does the model remember earlier chats?** — No; each session is independent unless context is re-provided.

> [!tip] Viva Prep
> Be ready to explain the *why* behind each step, not just the output.
