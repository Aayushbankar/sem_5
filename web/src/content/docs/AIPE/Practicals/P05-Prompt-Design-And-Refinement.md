---
title: "P05 — Prompt Design And Refinement"
sidebar:
  order: 5
---

# P05 — Design & Refine Prompts: Email Writing & Concept Explanation

**Subject:** Artificial Intelligence with Prompt Engineering | **Unit:** 3 | **Approx. Hrs:** 2
**PrO (verbatim):** *Design and refine prompts for tasks such as email writing and concept explanation. Compare outputs before and after prompt refinement.*

---

## 1. Objective
- Write a prompt **quickly**, observe the output.
- **Refine it through 3 iterations** using feedback, and observe improvement each time.
- Produce a **before/after comparison** that shows *why* each refinement helps.

## 2. Theory (exam-ready)

A complete prompt has four parts (syllabus §3.2):
| Component | What it is | Example |
|---|---|---|
| **Instruction** | The task verb + goal | "Write an email…" |
| **Context** | Background, audience, constraints | "…to your professor asking for a deadline extension." |
| **Input data** | The material to work on | "Our project is 80% complete, delay due to illness." |
| **Output format** | How the result must look | "3 short paragraphs, polite tone, subject line." |

**The refinement loop (§3.4):** write → test → evaluate against your goal → identify what's missing → edit one thing → retest. Iterative prompt improvement is the core skill of prompt engineering.

**Common refinement moves:**
1. Add a **role** ("act as a career counsellor").
2. Add **constraints** (length, tone, audience).
3. Add **input data** (the actual facts, not placeholders).
4. Specify the **output format** (subject line, bullet list, 2 sentences).
5. Give a **good/bad example** (few-shot).
6. Ask the model to **review/improve its own draft** (self-refine).

## 3. Worked Example 1 — Email Writing

### Iteration 1 (first try)
```
Prompt: Write an email asking for a deadline extension.
```
**Observed output:** Generic, no recipient, no reason, no dates. Usable as a skeleton only.
**Problem diagnosed:** no audience, no reason, no ask.

### Iteration 2 (add audience + reason)
```
Prompt: Write an email to my professor asking to extend the project submission
deadline by 5 days because I was hospitalised for a week.
```
**Observed output:** Polite, includes the reason, but *invents dates* and has no clear closing ask.
**Problem diagnosed:** needs exact dates + a clear request sentence + subject line.

### Iteration 3 (full structure — final)
```
Prompt: Act as a professional writing coach. Write a polite email to my
professor, Dr. Sharma, asking to extend the "Networking" assignment deadline
from 5 August to 10 August. Reason: I was hospitalised from 25 July to 2 August.
Requirements:
- Subject line that mentions the extension request.
- 3 short paragraphs: greeting + reason, current status, clear request with dates.
- A closing line thanking the professor.
- Formal but warm tone.
```
**Observed output:** Complete, ready-to-send email with subject line, dates, and a polite closing. ✅

| Aspect | Iteration 1 | Iteration 2 | Iteration 3 |
|---|---|---|---|
| Length | ~50 words | ~70 words | ~90 words |
| Dates | none | invented | correct |
| Clear request | no | weak | explicit |
| Subject line | none | none | yes |
| Tone control | default | polite | warm + formal |

## 4. Worked Example 2 — Concept Explanation

### Iteration 1
```
Prompt: Explain an API.
```
**Observed output:** Correct but long, vague, no audience.
**Problem diagnosed:** no audience → wrong level of detail.

### Iteration 2
```
Prompt: Explain an API to a non-technical person, like a hotel manager.
```
**Observed output:** Better — uses a "restaurant waiter" analogy. Still no example of actual API calls or limits on length.
**Problem diagnosed:** add length limit + concrete example + why it matters.

### Iteration 3 (final)
```
Prompt: Explain what an API is to a hotel manager (non-technical).
- Use the analogy of a waiter passing orders between kitchen and guest.
- Max 150 words.
- End with 2 examples of APIs used in hospitality booking software.
- Simple English, no jargon.
```
**Observed output:** Tight analogy, exactly 2 examples, jargon-free. ✅

| Aspect | Iteration 1 | Iteration 2 | Iteration 3 |
|---|---|---|---|
| Audience | none | hotel manager | hotel manager |
| Analogy | none | waiter | waiter + kitchen |
| Length | ~200 words | ~120 words | ~140 words |
| Examples | none | none | 2 booking-software APIs |
| Jargon | yes | some | none |

## 5. Why Each Refinement Helps (the "why" table)
| Refinement | Effect on the model |
|---|---|
| Adding a role | Biases the model toward domain-appropriate tone and knowledge |
| Adding audience | Fixes the "level of detail" the model guesses at |
| Supplying exact data (dates, names) | Stops the model from inventing facts (hallucination control) |
| Formatting instructions (subject, bullets, length) | Makes output predictable and directly usable |
| Constraints (max words, tone) | Shrinks the search space of possible answers |
| Self-review round ("critique then rewrite") | Second pass removes the model's own errors |

## 6. Deliverable — report skeleton
1. Task 1: 3 iterations with prompt → output → diagnosed problem → fix.
2. Task 2: 3 iterations with prompt → output → diagnosed problem → fix.
3. A before/after table for each (like Sections 3–4).
4. The "why each refinement helps" table with 3 of your own examples.
5. Conclusion: which single refinement gave the biggest quality jump in your runs.

## 7. Conclusion
The biggest quality jumps came from **adding the missing input data** (dates/reason) and **fixing the audience**, not from fancier words. Formatting instructions made output *directly usable*. Prompt design is an iteration loop: every output is feedback for the next prompt.

## 8. Viva Q&A
1. **What are the 4 prompt components?** — Instruction, context, input data, output format.
2. **Which component prevents hallucinated facts?** — Supplying the input data yourself.
3. **What is the refinement loop?** — Write → test → evaluate → edit → retest.
4. **Why does "act as a …" help?** — It steers the model toward the role's conventions.
5. **How do you make an email prompt ready-to-send?** — Add recipient, reason, exact dates, subject line, tone, and closing.

## 9. Resources
- Google Prompt Engineering guide: https://developers.google.com/learn/pathways/prompt-engineering
- OpenAI prompt engineering guide: https://platform.openai.com/docs/guides/prompt-engineering
- DAIR.AI Prompt Engineering Guide: https://www.promptingguide.ai
- Template: [`p05_before_after_template.md`](./p05_before_after_template.md.md)

---



---

## 🐛 Failure Modes & Debugging (Real-World Experience)

> [!bug] What goes wrong in production?
> When running **Prompt Design And Refinement** in a real environment, it almost never works perfectly the first time. 
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

- **What are the 4 prompt components?** — Instruction, context, input data, output format.
- **Which component prevents hallucinated facts?** — Supplying the input data yourself.
- **What is the refinement loop?** — Write → test → evaluate → edit → retest.
- **Why does "act as a …" help?** — It steers the model toward the role's conventions.
- **How do you make an email prompt ready-to-send?** — Add recipient, reason, exact dates, subject line, tone, and closing.

> [!tip] Viva Prep
> Be ready to explain the *why* behind each step, not just the output.
