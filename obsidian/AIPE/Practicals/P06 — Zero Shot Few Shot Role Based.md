---
subject: AIPE
status: not-started
tags: [subject/aipe, practical, unit/3]
practical: 6
unit: 3
hours: 2
---
# P06 — Zero-Shot, Few-Shot & Role-Based Prompting

**Subject:** Artificial Intelligence with Prompt Engineering | **Unit:** 3 | **Approx. Hrs:** 2
**PrO (verbatim):** *Apply prompting techniques such as zero-shot, few-shot, and role-based prompting.*

---

## 1. Objective
- Apply **zero-shot**, **few-shot**, and **role-based** prompting to real tasks.
- Provide **2 worked examples per technique** with prompt + observed output.
- Compare the techniques and note when each is the right tool.

## 2. Theory (exam-ready)

| Technique | Definition | When to use |
|---|---|---|
| **Zero-shot** | One instruction, no examples. The model must do the task from the prompt alone. | Simple, common tasks; quick tests |
| **Few-shot** | Show the model **2–5 examples** of input → output before the real task. The examples teach the *pattern/format*. | Odd formats, new tasks, improving consistency |
| **Role-based** | Assign a role ("act as a teacher, doctor, editor…") to set tone, knowledge domain, and constraints. | Domain-specific tone & vocabulary |

**Why few-shot works:** LLMs are in-context learners — they pick up patterns from the examples in the prompt (this is the finding of *"Language Models are Few-Shot Learners"*, Brown et al. 2020). Zero-shot sometimes fails on unfamiliar formats; a few examples fix it without retraining.

## 3. Worked Examples

### 3.1 Zero-shot (2 examples)

**Example 1 — Sentiment label:**
```
Prompt: Classify the sentiment of this review as Positive, Negative, or Neutral.
Review: "The battery drains really fast after the update."
Output: Negative. 
```
**Example 2 — Table extraction:**
```
Prompt: Convert the sentence into a table with columns Name, Age, City.
Sentence: "Riya, 21, lives in Ahmedabad; Aarav, 22, lives in Vadodara."
Output: | Name | Age | City | |---|---|---| | Riya | 21 | Ahmedabad | | Aarav | 22 | Vadodara |
```

### 3.2 Few-shot (2 examples)

**Example 1 — Custom tone/format:**
```
Prompt: Classify each text as FACT or OPINION.

"The Earth orbits the Sun." -> FACT
"Pizza is the best food." -> OPINION
"Python is easier than Java." -> OPINION
"Water boils at 100 °C at sea level." -> FACT

"IPL matches are more entertaining than test cricket." ->
Output: OPINION
```
*Why the example matters:* without examples the model may answer "SUBJECTIVE/OBJECTIVE"; the examples pin the exact labels.

**Example 2 — Specific output shape (customer support ticket):**
```
Prompt: Turn each complaint into a ticket with fields: ID, ISSUE, PRIORITY.

"App crashes when I upload photos." -> ID: T-001, ISSUE: crash-on-upload, PRIORITY: high
"The search bar is slow." -> ID: T-002, ISSUE: slow-search, PRIORITY: medium

"My account shows a wrong balance." ->
Output: ID: T-003, ISSUE: wrong-balance, PRIORITY: high
```
*Why:* the model now knows the exact field names and the 3-level priority scale instead of inventing its own.

### 3.3 Role-based (2 examples)

**Example 1 — Teacher:**
```
Prompt: You are a primary-school science teacher. Explain why the sky is blue
using only words a 7-year-old understands, and end with one fun question.
Output: (simple explanation using "light bouncing like balls", ends with a question)
```

**Example 2 — Technical reviewer:**
```
Prompt: You are a senior Python code reviewer. Review this function for bugs,
naming, and performance. Give a verdict and 3 numbered suggestions.
(code snippet goes here)
Output: verdict + 3 numbered suggestions in a strict checklist format
```

## 4. Comparison Table (fill with your own runs)

| Criterion | Zero-shot | Few-shot | Role-based |
|---|---|---|---|
| Prompt effort | Lowest | Medium (write examples) | Low |
| Consistency | Varies | Highest | Medium |
| Best for | Quick/common tasks | Exact formats & labels | Tone & domain depth |
| Example risk | — | Bad examples mislead | Over-roleplay verbosity |
| When to choose | Simple instruction | Format must match | Domain voice matters |

**Rule of thumb:** zero-shot to prototype → add few-shot if the format is off → add a role if the tone/domain is off. Combine them freely ("Act as a teacher and use these 3 examples…").

## 5. Deliverable — report skeleton
1. Theory table (Section 2).
2. Your 2 worked examples per technique: prompt → output → one-line "why this worked".
3. Comparison table filled from your own runs.
4. One **combined** prompt showing all three techniques used together.
5. Conclusion: pick your favourite technique per task type.

## 6. Conclusion
Zero-shot is the fastest but least controlled; few-shot trades a few example tokens for high format consistency; role-based is the cheapest way to inject domain expertise and tone. The best prompts mix all three — a role, examples, and a clear instruction.

## 7. Viva Q&A
1. **What is zero-shot prompting?** — Asking the model to perform a task with no examples.
2. **What is few-shot prompting?** — Giving 2–5 example input/output pairs before the real task.
3. **Why does few-shot improve consistency?** — In-context learning: the model copies the pattern of the examples.
4. **What is role-based prompting?** — "Act as X" to set tone, knowledge, and constraints.
5. **How many examples is "few"?** — Typically 2–5; too many bloat the context (cost).

## 8. Resources
- *"Language Models are Few-Shot Learners"* (Brown et al., 2020): https://arxiv.org/abs/2005.14165
- Google Prompt Engineering guide — zero/few-shot: https://developers.google.com/learn/pathways/prompt-engineering
- DAIR.AI — techniques: https://www.promptingguide.ai/techniques
- Template: [[p06_prompting_technique_templates.md|`p06_prompting_technique_templates.md`]]

---



---

## 🐛 Failure Modes & Debugging (Real-World Experience)

> [!bug] What goes wrong in production?
> When running **Zero Shot Few Shot Role Based** in a real environment, it almost never works perfectly the first time. 
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

- **What is zero-shot prompting?** — Asking the model to perform a task with no examples.
- **What is few-shot prompting?** — Giving 2–5 example input/output pairs before the real task.
- **Why does few-shot improve consistency?** — In-context learning: the model copies the pattern of the examples.
- **What is role-based prompting?** — "Act as X" to set tone, knowledge, and constraints.
- **How many examples is "few"?** — Typically 2–5; too many bloat the context (cost).

> [!tip] Viva Prep
> Be ready to explain the *why* behind each step, not just the output.
