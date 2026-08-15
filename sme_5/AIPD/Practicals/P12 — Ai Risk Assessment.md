---
subject: AIPD
status: not-started
tags: [subject/aipd, practical, unit/6]
practical: 12
unit: 6
hours: 2
---
# P12 — AI Risk Assessment & Mitigation Strategy

**Subject:** AI Product Design | **Unit:** 6 | **Approx. Hrs:** 2
**PrO (verbatim):** *Perform AI risk assessment and design mitigation strategy.*

---

## 1. Objective
- Identify **8 AI-specific risks** for StudyMate.
- Score each on **likelihood × impact** in a risk matrix.
- Write a **mitigation plan per risk** (owner, control, detection, contingency).

## 2. Risk matrix (filled)

| # | Risk | Likelihood (1–5) | Impact (1–5) | Score | Zone |
|---|---|---|---|---|---|
| R1 | **Hallucination** — quiz/summary invents facts ("Faraday's law says…") | 4 | 4 | **16** | 🔴 Critical |
| R2 | **Privacy breach** — student notes/chat leak (cloud or third-party API) | 3 | 5 | **15** | 🔴 Critical |
| R3 | **Bias & discrimination** — content unfairly favours/harms groups; model refuses regional-language material | 3 | 4 | 12 | 🟠 High |
| R4 | **Prompt injection** — a malicious document/query hijacks the model | 3 | 4 | 12 | 🟠 High |
| R5 | **Regulatory** — DPDP non-compliance (children's consent, no breach notice) | 2 | 5 | 10 | 🟠 High |
| R6 | **Model drift / API change** — provider updates model, quality drops or costs jump | 4 | 2 | 8 | 🟡 Medium |
| R7 | **Adversarial / abuse** — bots or rivals burn API budget; content farmed at scale | 3 | 2 | 6 | 🟡 Medium |
| R8 | **AI-generated misinformation spread** — students share fake "model papers" made with our tool | 2 | 3 | 6 | 🟡 Medium |

### 2.1 Visual matrix
```text
Impact  5 │      R2          R1   ← top-right = act NOW
        4 │      R3 R4        R3/R4
        3 │      R8
        2 │      R7
        1 │  R6
         └───┬──────┬──────┬──────► Likelihood
             1      2      3      4      5
```
> **Reading:** anything in the red zone (score ≥ 12) gets a **mitigation owner and a control this sprint**; yellow gets a control on the roadmap; green (≤ 5) gets monitoring.

## 3. Mitigation plan per risk (filled)

| # | Risk | Preventive control | Detection | Contingency | Owner |
|---|---|---|---|---|---|
| R1 | Hallucination | **RAG grounding** (answers cite the page/chunk, P02/P08); "not in your notes" fallback; temperature ≤ 0.3 for quizzes | Random sample of 20 outputs/week checked against source | "Explain my mistakes" surface shows the source quote; user can flag | ML engineer |
| R2 | Privacy breach | Encryption at rest/in transit; per-user namespacing; **server-side keys**; data-processing terms with API vendor | Audit logs + alert on unusual access; annual security review | **72-h user notification** (P11 runbook); key rotation; isolate store | Security lead |
| R3 | Bias | Grounding in user's own material; never rank/sort students; multi-language evaluation set | Quarterly fairness sampling of generated questions | Human review lane for flagged content | Product lead |
| R4 | Prompt injection | System prompt marks uploaded docs as **untrusted data**; separate instructions from content; input sanitisation | Probe tests (red-team prompts) in CI | Degrade to "no file access" mode; block offending doc | ML engineer |
| R5 | Regulatory | DPDP checklist: children consent flow, 72-h breach notice, retention schedule (P11) | Pre-release compliance review | Legal counsel call; regulator notification | CEO/founder |
| R6 | Model drift | Pin model versions; benchmark quizzes against a fixed eval set monthly | Per-output quality score monitor | Rollback to pinned version; re-tune prompts | ML engineer |
| R7 | Abuse | Free-tier daily caps (P07); rate limiting; anomaly detection on token usage | Cost/usage dashboard + budget alerts | Suspend account; CAPTCHA on signup | Backend |
| R8 | Misinfo spread | Watermark AI outputs ("Made with StudyMate"); forbid "real model paper" claims in generated content | Social listening on exam-season keywords | Takedown requests + guidance page | Marketing |

## 4. Blank Template (copy into `../code/p12_risk_matrix_template.md`)

```
# <Product> — AI Risk Assessment (blank)

## Risk register
| # | Risk | Likelihood 1–5 | Impact 1–5 | Score | Zone |

## Risk matrix diagram (draw 5×5 grid, place each risk)

## Mitigation plan
| # | Risk | Preventive control | Detection | Contingency | Owner |

## Top 3 actions this sprint
1. ____  (owner: ____)
2. ____
3. ____
```

## 5. Field-by-field explanation (how to redo for your idea)
- **Likelihood** — how often you expect it (1 = rarely, 5 = weekly). Use your own usage data if you have it; otherwise the team's best estimate *written down*.
- **Impact** — severity if it happens (1 = nuisance, 5 = regulatory fine / user harm / product death). **Impact 5 risks get controls even at low likelihood** (R5).
- **Score = Likelihood × Impact** — this number is what sorts the matrix. Red ≥ 12, yellow 6–11, green ≤ 5 (calibrate to your product).
- **Preventive control** — stops it happening; **Detection** — proves you'd notice it in hours, not months; **Contingency** — what you do when it *does* happen. A risk with only "prevent" is half a plan.
- **Owner** — every red risk needs a *named person*. "The team" owns nothing.
- **Don't pad** — 6–8 real risks beat 20 invented ones. Each must be *specific to an AI product* (bias, hallucination, injection, drift) — "server crash" alone isn't an *AI* risk.

## 6. Expected Deliverable (report skeleton)
1. Title, aim, date.
2. Risk register table (8 risks) + matrix diagram.
3. Mitigation table — every red/high risk has control + detection + contingency + owner.
4. "Top 3 actions this sprint" list.
5. Residual risk paragraph: what risk remains after mitigation and why it's acceptable.
6. Conclusion.

## 7. Viva Q&A
1. **What is model drift?** — The API provider updates the model and your previously-good outputs degrade (or cost rises). Mitigation: pin versions + a fixed evaluation set run monthly.
2. **What is prompt injection?** — A crafted instruction inside uploaded data (e.g., a PDF containing "ignore all rules and…") that hijacks the model. Mitigation: treat document content as untrusted data, keep instructions separate.
3. **How does RAG reduce hallucination?** — The model must answer from retrieved chunks and can say "not in your notes" — grounded outputs cite evidence, and out-of-scope questions are refused instead of guessed.
4. **Why does R2 (privacy) get a 72-hour notification contingency?** — Because impact is 5 (regulatory fine + loss of trust); the runbook (P11) guarantees the user-visible action, not just internal fixes.
5. **Which risk would you tackle first?** — R1: hallucination — it's the highest score (16) and it *directly* undermines the product's core promise ("answers from your notes").

## 8. Resources
- OWASP LLM Top 10 (2025): https://owasp.org/www-project-top-10-for-large-language-model-applications/
- EU AI Act risk tiers overview: search *eu ai act risk levels unacceptable high limited minimal* (official: https://artificialintelligenceact.eu)
- NIST AI Risk Management Framework: https://www.nist.gov/itl/ai-risk-management-framework
- "AI red-teaming" guides: search *llm red teaming prompt injection testing*
- Template file: [[p12_risk_matrix_template.md|`p12_risk_matrix_template.md`]]

---



---

## 🐛 Failure Modes & Debugging (Real-World Experience)

> [!bug] What goes wrong in production?
> When running **Ai Risk Assessment** in a real environment, it almost never works perfectly the first time. 
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

- **Hallucination** — quiz/summary invents facts ("Faraday's law says…") | 4 | 4 | **16** | 🔴 Critical |
- **Privacy breach** — student notes/chat leak (cloud or third-party API) | 3 | 5 | **15** | 🔴 Critical |
- **Bias & discrimination** — content unfairly favours/harms groups; model refuses regional-language material | 3 | 4 | 12 | 🟠 High |
- **Prompt injection** — a malicious document/query hijacks the model | 3 | 4 | 12 | 🟠 High |
- **Regulatory** — DPDP non-compliance (children's consent, no breach notice) | 2 | 5 | 10 | 🟠 High |
- **Model drift / API change** — provider updates model, quality drops or costs jump | 4 | 2 | 8 | 🟡 Medium |
- **Adversarial / abuse** — bots or rivals burn API budget; content farmed at scale | 3 | 2 | 6 | 🟡 Medium |
- **AI-generated misinformation spread** — students share fake "model papers" made with our tool | 2 | 3 | 6 | 🟡 Medium |

> [!tip] Viva Prep
> Be ready to explain the *why* behind each step, not just the output.
