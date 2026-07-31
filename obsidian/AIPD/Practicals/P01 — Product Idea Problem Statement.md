---
subject: AIPD
status: not-started
tags: [subject/aipd, practical, unit/1]
practical: 1
unit: 1
hours: 4
---
# P01 — Product Idea, Problem Statement, Target Users & Core Features

**Subject:** AI Product Design | **Unit:** 1 | **Approx. Hrs:** 4
**PrO (verbatim):** *Define AI product idea, problem statement, target users, and minimum 3 core features.*

> 🧪 **The running example for ALL 12 practicals is StudyMate — an AI Study Assistant for diploma students.** Every practical in this folder builds on the same product so the kit forms one continuous design story. When you redo a practical for *your own* idea, use the blank template (section 4) and the field explanations (section 5).

---

## 1. Objective
- Pick a real-world problem that an **AI product** can solve better than a plain app.
- Write a **problem statement** that is specific, user-centred, and testable.
- Name the **target users** and their needs.
- Propose **3+ core features** and justify why each one needs AI.

## 2. The Example Product — StudyMate

**StudyMate** is an AI study assistant that helps a diploma/college student turn their own notes, PDFs, and lecture material into summaries, practice questions, and a personalised study plan — in under a minute, instead of an evening.

It is an **AI product** (not just an AI tool) because it has a full product wrapper: a target user, a persistent data store (your uploaded material), a feedback loop (quiz scores → better questions), and a subscription business model (see P07).

## 3. Filled Template (StudyMate)

### 3.1 Product idea

| Field | Filled value (StudyMate) |
|---|---|
| **Product name** | StudyMate |
| **One-line description** | An AI study assistant that turns your class notes, PDFs and slides into summaries, practice quizzes and a personalised revision plan. |
| **Category** | EdTech — AI productivity assistant for students |
| **Platform** | Web + mobile (PWA); chatbot-style interface |
| **"AI in one sentence"** | StudyMate uses a Large Language Model (LLM) over the *student's own* documents so answers are grounded in their course material, not generic internet text. |
| **Differentiator vs existing tools** | Generic chatbots answer from the internet; StudyMate answers only from *your* syllabus, marks key diagrams as "study targets", and tracks what you still don't know. |

### 3.2 Problem statement

> "Final-year diploma students lose up to 4–5 hours per exam week re-reading scattered notes, writing question papers by hand, and deciding *what to study next*. They have no fast way to turn their own study material into self-test questions, so they discover gaps only on exam day."

**Why it's a good statement** (see §5 checklist): it names **who** (diploma students), **what** (wasted revision hours, no self-testing), the **evidence** (up to 4–5 hrs/week, gaps discovered late), and implies the **opportunity** (an AI that converts material → tests in minutes).

### 3.3 Target users

| Segment | Description | Need | Priority |
|---|---|---|---|
| **Primary — Diploma student (Y2–Y3)** | 17–20 yrs, preparing for board/GTU semester exams, uses phone + free Wi-Fi, budget-limited | Turn notes into revision material fast; self-test before exams | ⭐⭐⭐ |
| **Secondary — Course teacher** | Wants students to arrive prepared | Quick class quiz generation from their slides | ⭐⭐ |
| **Tertiary — Coaching/tutorial centres** | Run batches of 50–100 students | Bulk practice-paper generation, white-labelled | ⭐ |

### 3.4 Core features (minimum 3)

| # | Feature | What it does | Why it needs AI |
|---|---|---|---|
| 1 | **📄 Smart Notes Summarizer** | Upload PDF/notes/slides → get a 1-page summary, key definitions, and "exam likely" points. | LLM summarisation + extraction over an arbitrary document |
| 2 | **💬 Conversational Doubt Assistant** | Chat with your uploaded material: "Explain Faraday's law in the way my notes do." | Retrieval-augmented Q&A grounded in the student's own docs |
| 3 | **❓ Practice Quiz Generator** | One click → 10 MCQs + short answers from your material, with a marking key. | Question generation from domain content, difficulty tuning |
| 4 | **🗓️ Study Plan Builder** | Input exam date + subjects → AI schedule that balances chapters, with daily targets. *(stretch / "Should-have" in P06)* | Personalised sequencing/timetabling logic |

## 4. Blank Template (copy into `../code/p01_product_idea_template.md`)

```
# Product Idea — <Your Product Name>

## 4.1 Product idea
- Product name: ____
- One-line description: ____
- Category: ____
- Platform: ____
- "AI in one sentence": ____
- Differentiator vs existing tools: ____

## 4.2 Problem statement
"<Who> + <what painful situation> + <evidence/impact> + <implied opportunity>"

## 4.3 Target users
| Segment | Description | Need | Priority |

## 4.4 Core features (3+)
| # | Feature | What it does | Why it needs AI |
|---|---|---|---|
```

## 5. How to define a good problem statement (exam + viva guidance)

A weak statement is vague ("students find studies hard"). A strong one is **P.R.O.B.E.**-shaped:

| Letter | Stands for | Ask yourself | StudyMate example |
|---|---|---|---|
| **P** | Person | *Who exactly suffers?* | Final-year diploma students |
| **R** | Root cause | *What underlying behaviour causes it?* | They re-read notes passively; they don't self-test |
| **O** | Outcome | *What bad outcome results?* | Gaps found only on exam day; 4–5 lost hrs/week |
| **B** | Benchmark | *Can you measure it?* | "up to 4–5 hours per week", "discover gaps late" |
| **E** | End state | *What would good look like?* | 10-min upload → ready-to-test revision pack |

**Quick checks before you finalise:**
1. ✅ It names a **specific user**, not "everyone".
2. ✅ It describes a **behaviour**, not just an emotion.
3. ✅ It has **measurable impact** (time, money, errors).
4. ✅ It is **solvable by AI** — i.e., the problem involves converting/understanding language, images, or speech at scale (that's what LLMs do).
5. ✅ It does **not** name a solution yet ("we need a chatbot" is a solution, not a problem).
6. 🚫 Avoid: "The problem is lack of X app" — apps are solutions. Problems live *before* the app.

**Why each core feature must "need AI":** a product is an *AI product* only if removing the AI collapses the value. "Store notes" is not an AI feature; "turn notes into an exam-style quiz" is. In viva, you will be asked *"which feature could you build without AI, and why did you keep it anyway?"* — be ready to say StudyMate's login/library pages are non-AI, but summarizer/quiz/chat are the AI core.

## 6. Expected Deliverable (report skeleton)
1. Title, aim, date.
2. Product idea table (3.1) with the one-line description.
3. Problem statement in one sentence (bold) + PROBE walk-through.
4. Target-user table with the primary segment highlighted.
5. Core-feature table (3.4) with "why AI" column.
6. Conclusion: 2–3 sentences on *why this is an AI product*.

## 7. Viva Q&A
1. **Difference between an AI tool and an AI product?** — A tool does one task (e.g., ChatGPT answering); a product wraps AI in a solution for a specific user with data, workflow, and feedback loop. StudyMate is a product; a single chatbot endpoint is a tool.
2. **Why 3 features minimum?** — Enough to show a usable loop (input → AI value → output) without over-scoping an MVP.
3. **Can a problem statement name a solution?** — No; it should describe the user's pain, not a proposed fix.
4. **What makes a problem "AI-solvable"?** — It involves unstructured data (text/images/speech) or pattern recognition that a model can process at scale/automatically.

## 8. Resources
- Problem statement toolkit (Nielsen Norman Group): search *nngroup problem statements UX*
- "How to define a problem statement" — Interaction Design Foundation: https://www.interaction-design.org/literature/article/problem-statements
- Y Combinator "How to find product ideas": search *ycombinator how to get and evaluate startup ideas*
- Template file: [[p01_product_idea_template.md|`p01_product_idea_template.md`]]

---



---

## 🐛 Failure Modes & Debugging (Real-World Experience)

> [!bug] What goes wrong in production?
> When running **Product Idea Problem Statement** in a real environment, it almost never works perfectly the first time. 
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

- **solvable by AI** — i.e., the problem involves converting/understanding language, images, or speech at scale (that's what LLMs do).
- **Difference between an AI tool and an AI product?** — A tool does one task (e.g., ChatGPT answering); a product wraps AI in a solution for a specific user with data, workflow, and feedback loop. StudyMate is a product; a single chatbot endpoint is a tool.
- **Why 3 features minimum?** — Enough to show a usable loop (input → AI value → output) without over-scoping an MVP.
- **Can a problem statement name a solution?** — No; it should describe the user's pain, not a proposed fix.
- **What makes a problem "AI-solvable"?** — It involves unstructured data (text/images/speech) or pattern recognition that a model can process at scale/automatically.

> [!tip] Viva Prep
> Be ready to explain the *why* behind each step, not just the output.
