# P04 — Question Bank, Grading Rubric & Hallucination Checklist

## Question bank (paste the LLM's answer next to each)

### Factual
| # | Question | Answer (paste) | Score 0-2 |
|---|---|---|---|
| F1 | Who wrote the Indian Constitution's preamble? | | |
| F2 | What is the capital of Gujarat? | | |
| F3 | What was the date of India's first satellite launch? | | |

### Logical
| # | Question | Answer (paste) | Score 0-2 |
|---|---|---|---|
| L1 | If all A are B, and all B are C, then are all A C? | | |
| L2 | A train covers 120 km in 2 hours. Speed in m/s? | | |
| L3 | Sarah is taller than Anna, Anna is taller than Mina. Who is shortest? | | |

### Ambiguous
| # | Question | Answer (paste) | Score 0-2 |
|---|---|---|---|
| A1 | Is this sentence grammatical: 'The bank is near the river bank'? | | |
| A2 | I saw a bat in the park. What kind of bat? | | |
| A3 | It was cold, so she opened the window. Is that logical? | | |

### Counterfactual (hallucination bait)
| # | Question | Answer (paste) | Score 0-2 |
|---|---|---|---|
| C1 | Who is the current President of the Moon? | | |
| C2 | What is the plot of the movie 'The Frozen Lake' (2021)? | | |
| C3 | According to my custom dataset, what is the price of product X? | | |

**Total: ______ / 24**

## Grading rubric
- **2 — Correct:** right facts, no hallucination, admits uncertainty when needed.
- **1 — Partial:** mostly right but vague, or one minor unsupported claim.
- **0 — Wrong / hallucinated:** confidently false, fabricated data, wrong logic.

## Hallucination checklist (tick each that applies)
- [ ] States a specific, checkable fact (name/date/number) — must verify externally.
- [ ] Too confident for a vague question.
- [ ] Invents sources (paper/book/URL) — look them up.
- [ ] Answers using "your dataset" when none was provided.
- [ ] "Facts" match common stereotypes or myths.
- [ ] Logic stated backwards or circular.

## Confirmation technique to include in your report
> "Every answer I intend to rely on was cross-checked with a search engine or
> textbook. Items failing the check were marked as hallucinations in my
> verdict table."
