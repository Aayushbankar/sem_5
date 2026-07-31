# P07 — CoT & Prompt-Chaining Templates

## Chain-of-thought templates
```
Solve this step by step. Show every intermediate calculation.
Final line must be exactly: "Answer: ..."
```

```
Let's work this out carefully. For each step, state the formula you use and
the numbers you plug in. Double-check your final step.
```

```
You are a maths tutor. Explain each step to the student, then give the answer.
```

### Self-consistency recipe (3 runs)
1. Run the CoT prompt 3 times (or with temperature ~0.7).
2. Collect the 3 answers.
3. Report the majority answer + note any disagreement.
Example: `[₹293, ₹293, ₹250]` → majority ₹293, and you know run 3 was off.

## Prompt-chaining templates

### Chain: summarize → extract → format
```
PROMPT 1 — Summarize
You are an editorial assistant. Summarize the text below into 5 bullet
points. Keep all numbers and dates.
{source text}

PROMPT 2 — Extract
From these bullets, list the action items as: Who | What | By when.
Write TBD for any missing date.
{output of prompt 1}

PROMPT 3 — Format
You are a project manager. Turn the action items into a clean document:
title, one-line status, action table, and a short risks section.
{output of prompt 2}
```

### Chain: brainstorm → select → write
```
PROMPT 1: List 10 blog post ideas about {topic}.
PROMPT 2: Pick the 3 most original ideas; give one-line hooks.
PROMPT 3: Write a 400-word post for idea #1, outline first, then prose.
```

### Chain debugging rules
- If step 2 output is wrong, fix step 2's prompt only — steps 1 and 3 stay valid.
- Keep each step's output in plain text/tables so the next step can parse it.
- Add a final "reviewer" step: "Check the document for errors against the original; list corrections."

## When to chain vs one-shot
| Situation | Use |
|---|---|
| Short single-goal task | One prompt |
| Multi-stage output (report, app, article) | Chain |
| Reasoning-heavy math/logic | CoT (+ self-consistency) |
| Needs tools/data lookups | ReAct loop |
| Both long + multi-step | Chain where every step also asks for CoT-style justification |
