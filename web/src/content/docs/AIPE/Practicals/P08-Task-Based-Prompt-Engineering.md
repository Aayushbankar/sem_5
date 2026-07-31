---
title: "P08 — Task Based Prompt Engineering"
sidebar:
  order: 8
---

# P08 — Task-Based Prompt Engineering: Summarization, Blog Generation, Code Generation

**Subject:** Artificial Intelligence with Prompt Engineering | **Unit:** 4 | **Approx. Hrs:** 2
**PrO (verbatim):** *Perform task-based prompt engineering for summarization, blog generation, and code generation. Optimize prompts for better output.*

---

## 1. Objective
- Perform three tasks — **summarization, blog generation, code generation** — with prompts.
- Show **before/after** outputs after optimizing each prompt.
- Produce an **optimization checklist** per task.

## 2. Theory (exam-ready)

Task-based prompt engineering means choosing the right *prompt structure* for each task (syllabus §4.3). The four components (instruction, context, input data, output format) map onto tasks as:

| Task | Key instruction | Critical context | Typical output format |
|---|---|---|---|
| **Summarization** | "Summarize…" | audience, length, what to keep | bullets / N lines / one paragraph |
| **Content (blog) generation** | "Write a blog post…" | topic, audience, tone, SEO needs | heading + paragraphs + CTA |
| **Code generation** | "Write a function…" | language, inputs/outputs, edge cases | code block + tests + docstring |
| **Question answering** | "Answer…" | grounding source | short answer / table |
| **Translation** | "Translate…" | language pair, register | text |

**Optimization loop:** run → evaluate against criteria → fix → rerun. Measure with: correctness, completeness, format fit, and effort-to-use.

## 3. Task 1 — Summarization

**Before (bad prompt):**
```
Prompt: Summarize this article.
Output: A vague 1-line summary that misses the numbers and the main argument.
```
**Diagnosis:** no length, no focus, no audience.

**After (optimized):**
```
Prompt: Summarize the article below for a busy manager.
- Exactly 4 bullet points, max 20 words each.
- Keep all numbers, dates, and names.
- End with one sentence: the article's main conclusion.
{article pasted here}
Output: 4 tight bullets + a one-sentence conclusion, all key figures intact.
```

**Optimization checklist — summarization**
- [ ] Say *what* to summarize (input data supplied, not "this article").
- [ ] Set length and format (bullets / N lines / one paragraph).
- [ ] Say what to *keep* ("all numbers", "the main argument").
- [ ] Say what to *drop* ("no marketing language").
- [ ] Specify audience → controls detail level.
- [ ] For long docs, chain: chunk → summarize each → merge (P07).

## 4. Task 2 — Blog generation

**Before:**
```
Prompt: Write a blog about AI.
Output: Generic 200-word filler, no structure, no audience, no hook.
```
**Diagnosis:** no topic angle, no audience, no structure, no CTA.

**After:**
```
Prompt: You are a tech blogger. Write a 500-word blog post titled
"5 Ways Students Can Use AI for Exams (Ethically)".
- Target audience: 18-year-old engineering students.
- Structure: hook paragraph, 5 numbered sections with one example each,
  a short "risks to avoid" box, and a closing call to action.
- Tone: friendly, practical, zero hype.
- Include the exact title as an H1.
Output: structured, scannable post ready for editing.
```

**Optimization checklist — blog generation**
- [ ] Title + topic angle given.
- [ ] Audience + tone specified.
- [ ] Structure demanded (H1, numbered sections, CTA).
- [ ] Word count set.
- [ ] Instructions to avoid filler/hype.
- [ ] Ask for examples ("one real example per section").
- [ ] Follow-up pass: "Rewrite the hook 3 ways" / "Add an FAQ".

## 5. Task 3 — Code generation

**Before:**
```
Prompt: Write code to reverse a list.
Output: Works, but no type hints, no docstring, and fails on empty input
visibility — fine for a demo, unusable for a project.
```
**Diagnosis:** no language, no edge cases, no style, no tests.

**After:**
```
Prompt: Write a Python function `flatten(nested)` that flattens a nested list
into a single list.
- Input example: [1, [2, 3](./1,%20[2,%203.md), [4]] -> Output: [1, 2, 3, 4].
- Handle: empty list, one level deep, strings inside (keep them as strings).
- Style: type hints, docstring, one helper at most.
- Then write 3 unit-test-style assert statements for the edge cases.
Output: clean function + tests.
```

**Optimization checklist — code generation**
- [ ] Language + function signature named.
- [ ] Example input → output given (few-shot for behaviour).
- [ ] Edge cases listed (empty, types, large input).
- [ ] Style demanded (docstring, type hints, naming).
- [ ] Ask for tests / asserts.
- [ ] Ask for explanation ("add a one-line comment per block").
- [ ] Verify before trusting — **always run the code** (this practical series does!).

## 6. Before/After summary table (fill from your own runs)

| Task | Before quality (1-5) | After quality (1-5) | Biggest single fix |
|---|---|---|---|
| Summarization | 2 | 5 | length+format constraint |
| Blog | 1 | 4 | audience + structure |
| Code | 3 | 5 | example + edge cases |

## 7. Deliverable — report skeleton
1. One "before" prompt + output per task.
2. One "after" prompt + output per task.
3. Filled before/after table with your own scores.
4. The three optimization checklists ticked.
5. Conclusion: which prompt component mattered most per task.

## 8. Conclusion
Across all three tasks the pattern is the same: **vague prompts → vague outputs**. The biggest single lever per task was *format control* (summarization), *audience + structure* (blog), and *input/output examples + edge cases* (code). The optimization loop — run, evaluate, fix one thing, rerun — is universal.

## 9. Viva Q&A
1. **How do you make a summary trustworthy?** — Keep numbers/dates, set length, ground it in the given text.
2. **Why do blogs need structure in the prompt?** — LLMs write generic essays by default; headings + CTA make it publishable.
3. **Why give input/output examples for code?** — They define the exact behaviour; text descriptions alone are ambiguous.
4. **What is "optimization" in prompt engineering?** — Iterating the prompt until output meets evaluation criteria.
5. **Name the 4 prompt components used in each task.** — Instruction, context, input data, output format.

## 10. Resources
- OpenAI prompt engineering guide (task recipes): https://platform.openai.com/docs/guides/prompt-engineering
- DAIR.AI — applications: https://www.promptingguide.ai/applications
- Google Prompting guide — summarization recipes: https://developers.google.com/learn/pathways/prompt-engineering
- Template: [`p08_optimization_checklists.md`](./p08_optimization_checklists.md.md)

---



---

## 🐛 Failure Modes & Debugging (Real-World Experience)

> [!bug] What goes wrong in production?
> When running **Task Based Prompt Engineering** in a real environment, it almost never works perfectly the first time. 
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

- **How do you make a summary trustworthy?** — Keep numbers/dates, set length, ground it in the given text.
- **Why do blogs need structure in the prompt?** — LLMs write generic essays by default; headings + CTA make it publishable.
- **Why give input/output examples for code?** — They define the exact behaviour; text descriptions alone are ambiguous.
- **What is "optimization" in prompt engineering?** — Iterating the prompt until output meets evaluation criteria.
- **Name the 4 prompt components used in each task.** — Instruction, context, input data, output format.

> [!tip] Viva Prep
> Be ready to explain the *why* behind each step, not just the output.
