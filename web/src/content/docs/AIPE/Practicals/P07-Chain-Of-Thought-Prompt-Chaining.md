---
title: "P07 — Chain Of Thought Prompt Chaining"
sidebar:
  order: 7
---

# P07 — Chain-of-Thought & Prompt Chaining for Multi-Step Problems

**Subject:** Artificial Intelligence with Prompt Engineering | **Unit:** 4 | **Approx. Hrs:** 2
**PrO (verbatim):** *Apply advanced prompting techniques such as chain-of-thought and prompt chaining to solve multi-step problems.*

---

## 1. Objective
- Use **chain-of-thought (CoT)** prompting to make an LLM solve multi-step reasoning problems step by step.
- Use **prompt chaining** to split a complex task into a pipeline of small prompts.
- Provide **2 worked multi-step examples** with prompts and observed outputs.

## 2. Theory (exam-ready)

**Chain-of-Thought (CoT):** asking the model to "think step by step" before giving the answer. Instead of jumping to a conclusion, the model produces an intermediate reasoning trace, which dramatically improves accuracy on arithmetic/logical problems.

- *Paper:* "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models" (Wei et al., 2022) — showed large gains on math, commonsense, and symbolic tasks.
- **Variants** (syllabus §4.1): **Self-consistency** (sample several reasoning paths, take the majority answer) and **ReAct** (interleave *Reasoning* and *Act*ion — call tools, observe, continue).

**Prompt chaining:** break a big task into **smaller sequential prompts**, each feeding its output to the next. Benefits: each step is testable, the model handles less context per call, and a mistake in one step is easy to fix.

```
[Prompt 1 output] ──► [Prompt 2 input] ──► [Prompt 3 input] ──► Final result
```

## 3. Worked Example 1 — Math word problem with CoT

**Task:** "A shop sells notebooks at ₹45 each. Riya buys 3 notebooks and a pen for ₹30. She pays with a ₹500 note. How much change does she get?"

**Without CoT:**
```
Prompt: A shop sells notebooks at ₹45 each. Riya buys 4 notebooks and a pen
for ₹27. She pays with a ₹500 note. How much change?
Output: ₹293.
```
Correct here (4×45 = 180; +27 = 207; 500 − 207 = 293) — but we get **only the final number with no way to check it**. On harder or larger-number variants this is exactly where LLMs silently slip into wrong answers.

**With CoT:**
```
Prompt: A shop sells notebooks at ₹45 each. Riya buys 4 notebooks and a pen
for ₹27. She pays with a ₹500 note. How much change does she get?
Think step by step, then give the final answer as: "Change = ₹X"
Output:
Step 1: Cost of 4 notebooks = 4 × 45 = ₹180
Step 2: Add the pen = 180 + 27 = ₹207
Step 3: Change = 500 − 207 = ₹293
Change = ₹293
```
**Why it helps:** the model *must* do arithmetic in the open. If a step is wrong you can see where and fix the prompt ("double-check step 1"). This is the single biggest accuracy lever for math.

**Templates:**
```
Solve step by step. Show every intermediate calculation. Final line: "Answer: …"
```
```
Let's work this out carefully. For each step state the formula and the numbers.
```

## 4. Worked Example 2 — Prompt chaining: summarize → extract → format

**Task:** turn a messy project report into a polished one-page handover document.

**Chain:**
```
PROMPT 1 (summarize)
"You are an editorial assistant. Summarize the report below into 5 bullet
points. Keep all numbers and dates."
[report pasted here]
──► OUTPUT 1: 5 bullets with dates & numbers

PROMPT 2 (extract action items)
"From these 5 bullets, list the ACTION ITEMS as 'Who | What | By when'.
If a date is missing, write TBD."
[OUTPUT 1 pasted here]
──► OUTPUT 2: "Riya | fix login bug | 12 Aug", "Aarav | write tests | TBD", …

PROMPT 3 (format)
"You are a project manager. Turn these action items into a clean handover
document with a title, one-line status, the action table, and a short risks
section."
[OUTPUT 2 pasted here]
──► OUTPUT 3: polished one-page handover document
```

| Step | Input | Output | Failure is visible at |
|---|---|---|---|
| Summarize | full report | 5 bullets | step 1 (bad summary) |
| Extract | bullets | action table | step 2 (wrong fields) |
| Format | action table | handover doc | step 3 (bad layout) |

**Why chaining beats one mega-prompt:**
- Each step gets a short, focused prompt → fewer instruction conflicts.
- You can *swap or retry one step* without rerunning the others.
- Each step's output can be **checked** (dates correct? items complete?) before it flows on.
- Cheaper: no need to repeat the whole report in every call.

## 5. Self-Consistency & ReAct (know these for exams)

| Technique | What it is | One-line use |
|---|---|---|
| **Self-consistency** | Run CoT 3–5 times (different temperatures), take the **majority** answer | Improves reliability of math/logic answers |
| **ReAct** | Interleave Reasoning and Action — "I need X → search X → observe → continue" | Building agents/tools (Unit 5: AutoGPT, CrewAI) |

## 6. Deliverable — report skeleton
1. Theory of CoT + chaining (with the Wei et al. paper reference).
2. Worked example 1: same math problem with and without CoT, plus your own prompt.
3. Worked example 2: run the 3-step chain on your own text, paste each intermediate output.
4. A table: one-shot vs CoT vs chained — accuracy/effort/troubleshooting.
5. Conclusion.

## 7. Conclusion
CoT turns "give me the answer" into "show me how you got there", which improves correctness and makes errors *auditable*. Prompt chaining decomposes complex tasks into small, testable steps — the same idea that powers modern agent pipelines (Unit 5). Together they are the core of reliable multi-step prompt engineering.

## 8. Viva Q&A
1. **What is chain-of-thought prompting?** — Asking the model to reason step by step before answering.
2. **What paper introduced it?** — "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models" (Wei et al., 2022).
3. **What is prompt chaining?** — Splitting a task into sequential prompts where each output feeds the next.
4. **What is self-consistency?** — Sampling multiple reasoning paths and taking the majority answer.
5. **What is ReAct?** — Interleaving reasoning and actions (tool calls) in one loop.
6. **Why is chaining cheaper?** — Each prompt sees only its small input, not the whole document.

## 9. Resources
- *"Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"* (Wei et al., 2022): https://arxiv.org/abs/2201.11903
- *"Self-Consistency Improves Chain of Thought Reasoning in Language Models"* (Wang et al., 2022): https://arxiv.org/abs/2203.11171
- *"ReAct: Synergizing Reasoning and Acting in Language Models"* (Yao et al., 2022): https://arxiv.org/abs/2210.03629
- DAIR.AI — CoT & chaining: https://www.promptingguide.ai/techniques
- Template: [`p07_cot_and_chaining_templates.md`](./p07_cot_and_chaining_templates.md.md)

---



---

## 🐛 Failure Modes & Debugging (Real-World Experience)

> [!bug] What goes wrong in production?
> When running **Chain Of Thought Prompt Chaining** in a real environment, it almost never works perfectly the first time. 
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

- **Why chaining beats one mega-prompt:** — Each step gets a short, focused prompt → fewer instruction conflicts.
- **What is chain-of-thought prompting?** — Asking the model to reason step by step before answering.
- **What paper introduced it?** — "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models" (Wei et al., 2022).
- **What is prompt chaining?** — Splitting a task into sequential prompts where each output feeds the next.
- **What is self-consistency?** — Sampling multiple reasoning paths and taking the majority answer.
- **What is ReAct?** — Interleaving reasoning and actions (tool calls) in one loop.
- **Why is chaining cheaper?** — Each prompt sees only its small input, not the whole document.

> [!tip] Viva Prep
> Be ready to explain the *why* behind each step, not just the output.
