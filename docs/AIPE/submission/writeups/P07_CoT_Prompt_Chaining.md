# Practical 07: Chain-of-Thought & Prompt Chaining for Multi-Step Problems

**Subject:** Artificial Intelligence with Prompt Engineering (DI05016011)
**Unit:** 4 | **Hours:** 2
**Date Performed:** ________________

---

## 1. Aim

Apply advanced prompting techniques such as chain-of-thought and prompt chaining to solve multi-step problems.

---

## 2. Process / Program Code / Prompts Used

### Theory Reference

**Chain-of-Thought (CoT):** Asking the model to "think step by step" before giving the answer. Instead of jumping to a conclusion, the model produces an intermediate reasoning trace, dramatically improving accuracy on arithmetic/logical problems.

**Key Paper:** "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models" (Wei et al., 2022)

**Variants:**
- **Self-Consistency:** Sample several reasoning paths, take majority answer
- **ReAct:** Interleave Reasoning and Action — call tools, observe, continue

**Prompt Chaining:** Break a big task into smaller sequential prompts, each feeding its output to the next.
```
[Prompt 1 output] → [Prompt 2 input] → [Prompt 3 input] → Final result
```

### 2.1 Worked Example 1: Math Word Problem with CoT

**Task:** "A shop sells notebooks at ₹45 each. Riya buys 4 notebooks and a pen for ₹27. She pays with a ₹500 note. How much change does she get?"

#### Without CoT (Baseline)
```
Prompt: A shop sells notebooks at ₹45 each. Riya buys 4 notebooks and a pen for ₹27. She pays with a ₹500 note. How much change?
Output: ₹293.
```
Correct but only final number — no way to verify steps. On harder problems, LLMs silently slip into wrong answers.

#### With CoT
```
Prompt: A shop sells notebooks at ₹45 each. Riya buys 4 notebooks and a pen for ₹27. She pays with a ₹500 note. How much change does she get?
Think step by step, then give the final answer as: "Change = ₹X"
Output:
Step 1: Cost of 4 notebooks = 4 × 45 = ₹180
Step 2: Add the pen = 180 + 27 = ₹207
Step 3: Change = 500 − 207 = ₹293
Change = ₹293
```
**Why it helps:** Model must do arithmetic in the open. If a step is wrong, you can see where and fix the prompt.

**CoT Templates:**
```
Template 1: "Solve step by step. Show every intermediate calculation. Final line: 'Answer: …'"
Template 2: "Let's work this out carefully. For each step state the formula and the numbers."
```

### 2.2 Worked Example 2: Prompt Chaining — Summarize → Extract → Format

**Task:** Turn a messy project report into a polished one-page handover document.

#### Chain Execution

**PROMPT 1 (Summarize):**
```
Prompt: You are an editorial assistant. Summarize the report below into 5 bullet points. Keep all numbers and dates.
[Full project report pasted here — includes [STUDENT NAME], [ROLL NO], deadlines, team members]
→ OUTPUT 1: 5 bullets with dates & numbers
```

**PROMPT 2 (Extract Action Items):**
```
Prompt: From these 5 bullets, list the ACTION ITEMS as 'Who | What | By when'. If a date is missing, write TBD.
[OUTPUT 1 pasted here]
→ OUTPUT 2: "[STUDENT NAME] | fix login bug | 12 Aug", "Aarav | write tests | TBD", ...
```

**PROMPT 3 (Format):**
```
Prompt: You are a project manager. Turn these action items into a clean handover document with a title, one-line status, the action table, and a short risks section.
[OUTPUT 2 pasted here]
→ OUTPUT 3: Polished one-page handover document
```

| Step | Input | Output | Failure Visible At |
|------|-------|--------|-------------------|
| Summarize | Full report | 5 bullets | Step 1 (bad summary) |
| Extract | Bullets | Action table | Step 2 (wrong fields) |
| Format | Action table | Handover doc | Step 3 (bad layout) |

**Why chaining beats one mega-prompt:**
- Each step gets short, focused prompt → fewer instruction conflicts
- Swap/retry one step without rerunning others
- Each step's output can be checked before flowing on
- Cheaper: no need to repeat whole report in every call

### 2.3 Self-Consistency & ReAct (Exam Reference)

| Technique | What It Is | One-Line Use |
|-----------|------------|--------------|
| **Self-Consistency** | Run CoT 3–5 times (different temps), take majority answer | Improves reliability of math/logic answers |
| **ReAct** | Interleave Reasoning and Action — "I need X → search X → observe → continue" | Building agents/tools (Unit 5: AutoGPT, CrewAI) |

---

## 3. Screenshot of Output

### Example 1: CoT Math Problem

```
[STUDENT NAME | ROLL NO: ________________]

>>> Without CoT
Prompt: A shop sells notebooks at ₹45 each. Riya buys 4 notebooks and a pen for ₹27. She pays with a ₹500 note. How much change?
Output: ₹293

>>> With CoT
Prompt: A shop sells notebooks at ₹45 each. Riya buys 4 notebooks and a pen for ₹27. She pays with a ₹500 note. How much change does she get? Think step by step, then give the final answer as: "Change = ₹X"
Output:
Step 1: Cost of 4 notebooks = 4 × 45 = ₹180
Step 2: Add the pen = 180 + 27 = ₹207
Step 3: Change = 500 − 207 = ₹293
Change = ₹293

>>> Self-Consistency Check (3 runs at temp=0.7)
Run 1: Change = ₹293
Run 2: Change = ₹293
Run 3: Change = ₹293
Majority: ₹293 ✅
```

### Example 2: Prompt Chaining (3 Steps)

```
[STUDENT NAME | ROLL NO: ________________]

>>> PROMPT 1: Summarize
Input: [Project report with student details, deadlines, bugs, team]
Output 1:
- Project: AI Chatbot API Integration (P10)
- Team: [STUDENT NAME] (Roll: [ROLL NO]), Aarav, Priya
- Deadline: Aug 30, 2026
- Current: API client done, mock mode working, UI pending
- Blocker: OpenAI key approval pending

>>> PROMPT 2: Extract Action Items
Input: [Output 1 above]
Output 2:
[STUDENT NAME] | Get OpenAI key approval | 12 Aug
Aarav | Implement chat UI | 20 Aug
Priya | Write unit tests | 18 Aug
[STUDENT NAME] | Deploy to staging | 25 Aug

>>> PROMPT 3: Format Handover
Input: [Output 2 above]
Output 3:
# HANDOVER DOCUMENT — AI Chatbot Project (P10)
**Status:** On track — API layer complete, UI in progress
**Deadline:** 30 Aug 2026

## Action Items
| Owner | Task | Due | Status |
|-------|------|-----|--------|
| [STUDENT NAME] | Get OpenAI key approval | 12 Aug | Pending |
| Aarav | Implement chat UI | 20 Aug | In Progress |
| Priya | Write unit tests | 18 Aug | Not Started |
| [STUDENT NAME] | Deploy to staging | 25 Aug | Not Started |

## Risks
- Key approval delay → blocks live testing
- UI complexity underestimated → may need 2 extra days
```

---

## 4. Application of Learning

| Domain | Application | Example Project |
|--------|-------------|-----------------|
| **Financial Analysis** | Multi-step calculation verification | Tax computation with audit trail |
| **Legal Reasoning** | Case law analysis with steps | Contract clause interpretation with reasoning trace |
| **Medical Diagnosis** | Differential diagnosis reasoning | Symptom → hypothesis → test → conclusion chain |
| **Software Debugging** | Root cause analysis | Error → hypothesis → test → fix verification chain |
| **Project Management** | Report → action items → tracker | Automated sprint handover generation |
| **Education** | Step-by-step tutoring | Math solver that shows work for student learning |

**Key Learning:** CoT turns "give me the answer" into "show me how you got there", improving correctness and making errors auditable. Prompt chaining decomposes complex tasks into small, testable steps — the same idea that powers modern agent pipelines (Unit 5). Together they are the core of reliable multi-step prompt engineering.

---

## 5. Files Submitted

- **Writeup:** This document (`P07_CoT_Prompt_Chaining.md`)
- **Code/Templates:** `../code/p07_cot_and_chaining_templates.md`
- **Screenshots:** `../screenshots/P07_*.png` (placeholder for actual screenshots)

---

**Student Signature:** ________________    **Faculty Signature:** ________________