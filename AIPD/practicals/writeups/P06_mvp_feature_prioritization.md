# P06 — MVP Features & Feature Prioritization Matrix

**Subject:** AI Product Design | **Unit:** 3 | **Approx. Hrs:** 2
**PrO (verbatim):** *Define Minimum Viable Product (MVP) features and prepare feature prioritization matrix.*

---

## 1. Objective
- Define the **MVP scope** for StudyMate: the smallest feature set that still delivers the core value.
- Prioritise the full feature backlog with **MoSCoW** (Must/Should/Could/Won't).
- Rank features on an **Effort × Impact** matrix to justify the MVP choice.

## 2. Feature backlog (candidate list for StudyMate — from P01, P04, P05)

| ID | Feature | Source |
|---|---|---|
| F1 | Smart Notes Summarizer (PDF → summary + key points) | P01 F1 |
| F2 | Conversational Doubt Assistant (grounded chat) | P01 F2 |
| F3 | Practice Quiz Generator (MCQ + short answers) | P01 F3 |
| F4 | Study Plan Builder (dates → schedule) | P01 F4 |
| F5 | Weak-topic tagging from quiz results | P04 feedback loop |
| F6 | "Explain my mistakes" remediation | P05 |
| F7 | Export flashcards (Anki/PDF) | P04 Kunal |
| F8 | Guest / no-email try-before-upload | P04 opportunity |
| F9 | Streaks + revision reminders | P04 retention |
| F10 | Hindi/Gujarati explanation toggle | P04 (local students) |
| F11 | Multi-subject dashboards | P01 |
| F12 | Shareable score-card images | P04 marketing |

## 3. MoSCoW prioritization (filled)

| Priority | Features | Rationale |
|---|---|---|
| **M — Must have** | F1, F2, F3, F5 | The core loop: upload → understand → test → improve. Without these, StudyMate is not an AI study product. F5 makes the loop adaptive. |
| **S — Should have** | F6, F8, F10 | F6 deepens quiz value; F8 removes first-use friction; F10 is the localisation moat. High value, medium effort — ship right after MVP. |
| **C — Could have** | F4, F7, F11, F9 | Nice-to-haves. F4 is powerful but needs a scheduler engine (effort); F7/F9 are retention boosts, not core. |
| **W — Won't have (now)** | F12 | Marketing asset, not product value; defer to the campaign (P09) which can create it with Canva instead. |

> **Rule of thumb:** the MVP = **Must** column only (2–4 features). "Should/Could" are roadmap, not launch. Kill or defer "Won't" without guilt — scope discipline *is* the deliverable.

## 4. Effort × Impact matrix (filled)

| Feature | Effort (1–5) | Impact (1–5) | Quadrant |
|---|---|---|---|
| F1 Summarizer | 2 | 5 | ⭐ **Quick win** |
| F2 Doubt Assistant | 4 | 5 | 🚀 Strategic bet |
| F3 Quiz Generator | 3 | 5 | ⭐ **Quick win** |
| F5 Weak-topic tags | 2 | 4 | ⭐ **Quick win** |
| F6 Explain mistakes | 2 | 4 | ⭐ **Quick win** |
| F8 Guest mode | 2 | 3 | Quick win (marketing aid) |
| F10 Local language | 3 | 4 | Strategic (moat) |
| F4 Study Plan Builder | 5 | 5 | Big bet (post-MVP) |
| F7 Flashcards export | 3 | 3 | Fill-in |
| F9 Streaks | 2 | 2 | Fill-in |
| F11 Dashboards | 4 | 2 | **Money pit — cut** |
| F12 Share scorecard | 1 | 3 | Quick win (defer to P09) |

```text
        HIGH IMPACT
             ▲
   F1 ⭐     │     F2 🚀     F4
   F3 ⭐     │     F10
   F5 ⭐     │
   F6 ⭐     │
   F8        │
   F12       │     F7  F9
   LOW EFFORT└──────────────► HIGH EFFORT
             F11 (money pit)
```

**MVP recommendation:** ship **F1 + F3 + F5** in week 1 (three quick wins = fastest value), add **F2** in week 2 once document grounding is proven. Defer F4 (big bet) until you have retention data. Cut F11.

## 5. Blank Template (copy into `../code/p06_prioritization_matrix_template.md`)

```
# <Product> — MVP & Prioritization (blank)

## Feature backlog
| ID | Feature | Source (persona/journey pain point) |

## MoSCoW
| Priority | Features | Rationale |
| Must | | |
| Should | | |
| Could | | |
| Won't (now) | | |

## Effort × Impact
| Feature | Effort 1–5 | Impact 1–5 | Quadrant |
| | | | |

## MVP scope (final)
Ship: ____  (features, in order)
Defer: ____  Next milestone: ____
```

## 6. Field-by-field explanation (how to redo for your idea)
- **Feature source** — every feature must trace back to a persona goal or a journey pain point (P04). Orphan features are scope creep.
- **MoSCoW is a consensus tool, not a taxonomy.** Debate lives in the *rationale* column; the label is the output. Must ≠ "everything important" — it's *"product fails without it"*.
- **Effort** = engineering + data + ops cost on 1–5. **Impact** = effect on the core metric (for StudyMate: *time-to-feel-prepared* or weekly quizzes completed).
- **Quadrant names** (memorise): Quick win (low effort, high impact) → ship first · Strategic bet (high effort, high impact) → plan carefully · Fill-in (low effort, low impact) → ship when idle · **Money pit** (high effort, low impact) → cut.
- **MVP ≠ smallest possible** — it's the smallest set that *proves the value hypothesis*. If Riya won't re-use StudyMate after F1+F3+F5, the concept fails — and that's what an MVP is for: fail fast, cheaply.

## 7. Expected Deliverable (report skeleton)
1. Title, aim, date.
2. Backlog table with sources.
3. MoSCoW table with rationale.
4. Effort×Impact matrix + quadrant diagram.
5. Final MVP scope paragraph (ship / defer / cut).
6. Conclusion.

## 8. Viva Q&A
1. **What is an MVP?** — The minimum feature set that delivers core value to early users and lets you test the riskiest assumptions with the least effort.
2. **Why are F1/F3/F5 the MVP and not F2?** — They are quick wins with the same core value (convert material → testable understanding); F2 needs heavier RAG plumbing, so it ships a sprint later.
3. **What's a "money pit" feature?** — High effort, low impact (F11 dashboards) — cut, because it consumes budget the MVP can't afford.
4. **How does the matrix link to P04?** — Impact scores come from the journey's pain-point frequency/intensity; a feature nobody's pain demanded scores low.

## 9. Resources
- MoSCoW method (Agile Business Consortium): search *moscow method agile business consortium*
- RICE / effort-impact scoring (Intercom blog): search *rice scoring model prioritization intercom*
- Y Combinator "MVP" guidance: search *ycombinator minimum viable product talk*
- Template file: [`p06_prioritization_matrix_template.md`](../code/p06_prioritization_matrix_template.md)
