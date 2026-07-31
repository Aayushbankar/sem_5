---
title: "P11 — Data Protection Ethics Policy"
sidebar:
  order: 11
---

# P11 — Data Protection Plan & AI Ethical Usage Policy

**Subject:** AI Product Design | **Unit:** 5 | **Approx. Hrs:** 2
**PrO (verbatim):** *Draft Data Protection Plan and AI Ethical Usage Policy.*

---

## 1. Objective
- Draft a **Data Protection Plan (DPP)** for StudyMate: data inventory, consent, retention, breach response.
- Draft an **AI Ethical Usage Policy**: bias, transparency, accountability, fairness.

## 2. Filled Data Protection Plan — StudyMate

### 2.1 Data inventory (summary — full detail in P03)

| Dataset | Type | Purpose | Lawful basis (DPDP framing) |
|---|---|---|---|
| Uploaded study PDFs | Non-personal (usually) | Summarisation, Q&A, quiz | Service contract; user instruction |
| Profile (name, email, college) | Personal | Account, billing, support | Consent |
| Chat & quiz history | Personal (linked) | Product improvement | Consent |
| Device/analytics | Aggregated | Product analytics | Consent (opt-in) |

### 2.2 Consent
- **Clear, specific, informed:** one plain-language sentence per use, shown *before* upload ("We read your PDF only to answer you. We never sell it. We don't train models on it.").
- **Separate toggles:** (a) analytics, (b) "improve my questions with my history", (c) marketing email. No bundled "accept everything" checkbox.
- **Revocable:** every toggle live in Settings (see P05 wireframe 3.4); withdraw = stop using that data for that purpose going forward.
- **Children:** if a user indicates age < 18 (diploma students are often 17+), follow the **parental-consent** route required by DPDP for children's data.

### 2.3 Retention (the "delete" story)
| Data | Retention | After retention |
|---|---|---|
| Uploaded PDFs | 6 months after last login, or exam-season end | Purged + index deleted |
| Chat history | 90 days | Purged |
| Quizzes/scores | Kept while account active (they're the value) | Deleted on account deletion |
| Analytics | 12 months, aggregated only | De-identified |

### 2.4 Breach response (for a student-data product)
1. **Contain** — revoke API keys, isolate the affected store (≤15 min).
2. **Assess** — what leaked, whose data, how many records (P03 inventory makes this fast).
3. **Notify** — inform affected users (email/in-app) **within 72 h**; explain what happened and what they should do (e.g., "reset password").
4. **Report** — notify the regulator where required (DPDP breach-notification duty); keep a written incident log.
5. **Remediate** — fix the root cause, re-run the risk matrix (P12), document lessons.

## 3. Filled AI Ethical Usage Policy — StudyMate

| Principle | Policy statement (what StudyMate commits to) |
|---|---|
| **Bias** | We don't let the model decide a student's worth: no ranking/sorting of students, no "predicted score" that locks them out. Quiz content is generated from the student's *own* material to avoid one-size-fits-all cultural bias. We periodically sample generated questions for stereotypes (esp. regional language examples). |
| **Transparency** | Every AI output is labelled as AI-generated. Chat answers show the citation (which page/chunk they came from). We never pretend a mock quiz is a real model paper. |
| **Accountability** | A named human owner per AI surface (Summarizer, Chat, Quiz). Final answers on flagged content are reviewed by a human. We publish a simple "what we do when the AI is wrong" note. |
| **Fairness** | Free tier gives genuine core value (not an unusable teaser). Pricing doesn't depend on a student's predicted score. Same quality for all languages we support. |
| **Privacy by design** | Data minimisation (we don't collect what we don't need — P03), purpose limitation, and user-controlled deletion are defaults, not features. |
| **Safety** | Output moderation on chat/quiz (block harmful or self-harm content with a help redirect); no data used to train shared models without opt-in. |

## 4. Blank Templates (copy into `../code/p11_data_protection_ethics_template.md`)

```
# <Product> — Data Protection Plan (blank)

## Data inventory
| Dataset | Type | Purpose | Lawful basis |

## Consent
| Use | Consent copy (plain language) | Toggle location |
## Retention
| Data | Retention | After retention |
## Breach response
1 Contain  2 Assess  3 Notify (72h)  4 Report  5 Remediate

# <Product> — AI Ethical Usage Policy (blank)

| Principle | Policy statement |
| Bias | |
| Transparency | |
| Accountability | |
| Fairness | |
| Privacy by design | |
| Safety | |
```

## 5. Field-by-field explanation (how to redo for your idea)
- **Data inventory** — reuse your P03 table; the DPP is the *governance* layer on top of it. If a dataset isn't in the inventory, you can't protect it.
- **Consent** — the test is *"could a 17-year-old read this sentence and know exactly what happens to their PDF?"* If not, rewrite. Consent ≠ a long privacy policy nobody reads.
- **Retention** — name **a number per dataset** ("6 months", "90 days"). "When we feel like it" is not a policy. Deletion must include derived artifacts (indexes, cached summaries).
- **Breach response** — 5 steps in order, with a **72-hour user notification** target (aligns with DPDP breach duty). Practise the runbook once before the viva.
- **Ethics policy ≠ marketing.** Each principle needs a *concrete, testable commitment* ("answers carry a citation", "human owner named"). Vague virtue words earn no marks.
- **Bias is a design constraint** for an AI study product: the AI must never *sort students* or produce a single "predicted score" — that's where bias becomes discrimination.

## 6. Expected Deliverable (report skeleton)
1. Title, aim, date.
2. Data inventory + consent + retention + breach response (§2).
3. Ethics policy table (§3), 5+ principles with concrete commitments.
4. One paragraph: which two commitments are hardest to keep and why.
5. Conclusion.

## 7. Viva Q&A
1. **What is data minimisation?** — Collect only what the product truly needs (P03): StudyMate doesn't need your phone contacts or location to summarise notes.
2. **What's the difference between consent and notice?** — Notice tells you what will happen; consent is your *active agreement*. GDPR/DPDP generally require real consent for personal data, not just disclosure.
3. **Why 72 hours for breach notification?** — It's the practical/regulatory benchmark (GDPR; DPDP has a breach-notification duty) — enough time to assess, not enough to hide.
4. **How does StudyMate avoid bias if the underlying LLM is biased?** — It grounds answers in the student's own material, refuses to rank students, and runs periodic fairness sampling on generated content — bias controls live at the *product layer*, not just the model layer.

## 8. Resources
- India DPDP Act 2023 (official): https://www.meity.gov.in/data-protection-framework
- DPDP explainer: search *dpdp act 2023 explained consent data fiduciary children data*
- Google People + AI Guidebook (transparency, explainability): https://pair.withgoogle.com
- "Building Trust in AI" resources (IBM): search *ibm trust in ai transparency accountability*
- Template file: [`p11_data_protection_ethics_template.md`](./p11_data_protection_ethics_template.md.md)

---



---

## 🐛 Failure Modes & Debugging (Real-World Experience)

> [!bug] What goes wrong in production?
> When running **Data Protection Ethics Policy** in a real environment, it almost never works perfectly the first time. 
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

- **AI Ethical Usage Policy** — bias, transparency, accountability, fairness.
- **Contain** — revoke API keys, isolate the affected store (≤15 min).
- **Assess** — what leaked, whose data, how many records (P03 inventory makes this fast).
- **Notify** — inform affected users (email/in-app) **within 72 h**; explain what happened and what they should do (e.g., "reset password").
- **Report** — notify the regulator where required (DPDP breach-notification duty); keep a written incident log.
- **Remediate** — fix the root cause, re-run the risk matrix (P12), document lessons.
- **Data inventory** — reuse your P03 table; the DPP is the *governance* layer on top of it. If a dataset isn't in the inventory, you can't protect it.
- **Consent** — the test is *"could a 17-year-old read this sentence and know exactly what happens to their PDF?"* If not, rewrite. Consent ≠ a long privacy policy nobody reads.

> [!tip] Viva Prep
> Be ready to explain the *why* behind each step, not just the output.
