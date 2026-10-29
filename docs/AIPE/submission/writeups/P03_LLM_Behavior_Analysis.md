# Practical 03: LLM Behavior Analysis — Prompt Variation, Context, Consistency

**Subject:** Artificial Intelligence with Prompt Engineering (DI05016011)
**Unit:** 2 | **Hours:** 2
**Date Performed:** ________________

---

## 1. Aim

Perform experiments to analyze the behavior of LLM by testing prompt variations, context understanding, and response consistency.

---

## 2. Process / Program Code / Prompts Used

### Test A: Prompt Variation (Same Task, 3 Phrasings)

| # | Prompt | Purpose |
|---|--------|---------|
| A1 | "Explain machine learning." | Baseline — generic, no audience specified |
| A2 | "Explain machine learning in 2 lines for a school student." | Constrained: length + audience |
| A3 | "Explain machine learning with a concrete example, in a formal tone." | Constrained: format + tone + example |

**Tool Used:** ChatGPT / Google Gemini / Claude
**Temperature:** Default (0.7-1.0)

### Test B: Context Understanding (Add/Remove Context)

| # | Prompt | Purpose |
|---|--------|---------|
| B1 | "Summarize the meeting notes." | No context — model invents structure |
| B2 | "Summarize: [Actual meeting notes pasted here]" | Grounded in provided text |
| B3 | "Summarize: [Same notes]. Focus only on action items, list as bullets." | Grounded + format constraint |

**Sample Meeting Notes Used:**
```
Meeting: Project Kickoff - AI Chatbot
Date: 2026-08-15
Attendees: [STUDENT NAME] (Roll: [ROLL NO]), Prof. Sharma, Team
Decisions: Use OpenAI API, mock mode for demo, deadline Aug 30
Action Items: 
- [STUDENT NAME]: Set up API keys by Aug 18
- Prof. Sharma: Review architecture by Aug 20
- Team: Implement chat UI by Aug 25
```

### Test C: Response Consistency (Same Prompt × 3 Runs)

| # | Prompt (Identical Each Run) | Run 1 | Run 2 | Run 3 | Same Wording? |
|---|----------------------------|-------|-------|-------|---------------|
| C1 | "Give me one career tip for an IT student." | Tip A | Tip B | Tip C | **No** (creative) |
| C2 | "What is 25 × 4? Answer with only the number." | 100 | 100 | 100 | **Yes** (factual) |

---

## 3. Screenshot of Output

### Test A — Prompt Variation Results

```
[STUDENT NAME | ROLL NO: ________________]

>>> A1: "Explain machine learning."
Output: Machine learning is a subset of artificial intelligence where computers learn patterns from data without being explicitly programmed. It uses algorithms to parse data, learn from it, and make predictions or decisions. Common types include supervised, unsupervised, and reinforcement learning.

>>> A2: "Explain machine learning in 2 lines for a school student."
Output: Machine learning is like teaching a computer to recognize patterns by showing it lots of examples, just like how you learn to recognize cats by seeing many cat pictures.

>>> A3: "Explain machine learning with a concrete example, in a formal tone."
Output: Machine learning is a computational paradigm wherein algorithms infer predictive models from observational data. For instance, a spam classifier trained on labeled emails (spam/ham) learns to predict the label of unseen messages by detecting statistical regularities in word distributions.
```

### Test B — Context Understanding Results

```
[STUDENT NAME | ROLL NO: ________________]

>>> B1: "Summarize the meeting notes."
Output: The meeting covered project planning for an AI chatbot. Key decisions included technology stack selection and timeline. Action items were assigned to team members with deadlines in August. [INVENTED DETAILS - no actual notes provided]

>>> B2: "Summarize: [actual notes pasted]"
Output: Project kickoff for AI chatbot on Aug 15. Decided: OpenAI API with mock mode. Deadline: Aug 30. Action items: [STUDENT NAME] sets up API keys by Aug 18; Prof. Sharma reviews architecture by Aug 20; Team implements chat UI by Aug 25.

>>> B3: "Summarize: [same notes]. Focus only on action items, list as bullets."
Output: 
- [STUDENT NAME]: Set up API keys by Aug 18
- Prof. Sharma: Review architecture by Aug 20
- Team: Implement chat UI by Aug 25
```

### Test C — Response Consistency Results

```
[STUDENT NAME | ROLL NO: ________________]

>>> C1 Run 1: "Give me one career tip for an IT student."
Output: Build a portfolio of real projects on GitHub — employers value code you've actually written.

>>> C1 Run 2: "Give me one career tip for an IT student."
Output: Learn cloud platforms (AWS/Azure/GCP) — most modern jobs require cloud deployment skills.

>>> C1 Run 3: "Give me one career tip for an IT student."
Output: Contribute to open source — it proves collaboration skills and gives you visible code.

>>> C2 Run 1: "What is 25 × 4? Answer with only the number."
Output: 100

>>> C2 Run 2: "What is 25 × 4? Answer with only the number."
Output: 100

>>> C2 Run 3: "What is 25 × 4? Answer with only the number."
Output: 100
```

---

## 4. Application of Learning

| Domain | Application | Example Project |
|--------|-------------|-----------------|
| **Prompt Engineering** | Systematic prompt optimization | A/B testing prompt variants for production LLM apps |
| **Quality Assurance** | Regression testing for LLM outputs | Automated consistency checks in CI/CD for AI features |
| **Content Generation** | Controlling output style/format | Marketing copy generator with brand voice consistency |
| **Education** | Reliable tutoring systems | Ensuring consistent explanations for same concept |
| **Software Development** | Predictable code generation | Code assistant that produces same format every time |

**Key Learning:** LLM output is a function of (prompt + sampling settings + model), not a fixed lookup. Rephrasing changes style more than facts; context matters more than wording; consistency depends on task — creative prompts vary, constrained factual prompts are stable. Production systems use low temperature + format constraints for repeatability.

---

## 5. Files Submitted

- **Writeup:** This document (`P03_LLM_Behavior_Analysis.md`)
- **Code/Templates:** `../code/p03_llm_behavior_test_matrix.md`
- **Screenshots:** `../screenshots/P03_*.png` (placeholder for actual screenshots)

---

**Student Signature:** ________________    **Faculty Signature:** ________________