---
subject: AIPD
status: not-started
tags: [subject/aipd, practical, unit/3]
practical: 7
unit: 3
hours: 2
---
# P07 — Business Model Canvas & AI Monetization Strategy

**Subject:** AI Product Design | **Unit:** 3 | **Approx. Hrs:** 2
**PrO (verbatim):** *Develop Business Model Canvas and identify AI monetization strategy.*

---

## 1. Objective
- Fill the **Business Model Canvas (BMC)** — all 9 blocks — for StudyMate.
- Choose and justify an **AI monetization model** (subscription / freemium / usage-based) with example pricing.

## 2. Filled Business Model Canvas — StudyMate

| BMC Block | Filled value |
|---|---|
| **1. Customer Segments** | Primary: diploma/college students (India, exam seasons). Secondary: teachers (quiz generation), tutorial centres (bulk). |
| **2. Value Propositions** | "Turn any class material into a tested revision pack in 10 minutes"; grounded-in-your-notes answers; weak-topic tracking; no coaching fees needed. |
| **3. Channels** | Web + PWA app; Google Play; Instagram/YouTube (organic); WhatsApp referrals; campus ambassadors. |
| **4. Customer Relationships** | Self-service onboarding; in-app help; automated exam-season nudges; human support on paid tier (priority email). |
| **5. Revenue Streams** | Freemium subscription (Pro) + optional bulk licence for tutorial centres. *(details in §3)* |
| **6. Key Resources** | LLM API access (OpenAI/Google), document-processing pipeline, user data + feedback signals, brand/community, 2–4 person team. |
| **7. Key Activities** | Model prompts & RAG tuning; quiz-generation quality checks (P08 evaluation); content safety; marketing around exam calendars; server & cost monitoring. |
| **8. Key Partnerships** | LLM API provider; cloud host; college/YouTube study channels; note-sharing communities (for organic reach, not data). |
| **9. Cost Structure** | API tokens (dominant, ~40–60% of COGS), cloud hosting, salaries, marketing, payment-gateway fees, support. |

## 3. AI monetization strategy (filled)

### 3.1 Model options (the exam table)

| Model | How it works | Pros | Cons | Best for |
|---|---|---|---|---|
| **Subscription (SaaS)** | Flat ₹/month for Pro features | Predictable revenue; user feels "unlimited" | Users churn after exams (seasonality!) | StudyMate primary |
| **Freemium** | Free core (1 upload, N questions) + paid Pro | Huge acquisition; low-friction trial | Conversion pressure; API cost leakage on free tier | StudyMate primary |
| **Usage-based (per token / per API call)** | Pay for what you consume | Fair pricing; scales with real cost | Unpredictable bills; billing complexity | Enterprise/white-label only |
| One-time licence | Pay once | Simple | No recurring revenue | Not suitable (API costs are recurring) |

### 3.2 Recommended hybrid for StudyMate

**Freemium + subscription**, with a hard daily cap to control API cost:

| Plan | Price | Includes | Why it works |
|---|---|---|---|
| **Free** | ₹0 | 1 upload, 10 quiz Qs/day, 5 chat msgs/day, standard model | Acquisition; lets Riya feel the core loop (P06 MVP) |
| **Pro (monthly)** | ₹199/month | Unlimited uploads, adaptive quizzes, weak-topic engine, priority model, export | Catches the exam-season surge; students already pay for coaching copies |
| **Pro (semester)** | ₹799 / semester (₹133/mo effective) | Everything + advance-pay discount | Fights the "exam-over churn" seasonality |
| **Tutorial centre bulk** | Custom / seat | 50+ seats, white-label, usage-based overage | Enterprise revenue, stable |

**Why not pure usage-based?** Students can't predict token bills and will panic-churn. **Why not pure subscription?** Seasonality — December/May exam spikes and dead months would kill the MRR curve. Freemium + subscription + one bulk seat = predictable base + seasonal spike.

## 4. Blank Template (copy into `../code/p07_bmc_template.md`)

```
# <Product> — Business Model Canvas (blank)

| BMC Block | Filled value |
| Customer Segments | |
| Value Propositions | |
| Channels | |
| Customer Relationships | |
| Revenue Streams | |
| Key Resources | |
| Key Activities | |
| Key Partnerships | |
| Cost Structure | |

# Monetization plan
## Model options | Choice | Why
## Pricing table | Plan | Price | Includes | Why it works
## Unit economics (simple)
- Revenue / active user / month: ____
- Cost to serve / user / month (tokens + hosting): ____
- Gross margin: ____
```

## 5. Field-by-field explanation (so you can redo for your idea)
- **Customer Segments** — who pays *and* who uses (they may differ — students use, tutorial centres pay).
- **Value Proposition** — the *one sentence* a customer would repeat. Must be a measurable outcome ("10-minute revision pack"), not a feature list.
- **Channels** — acquisition (Instagram), distribution (Play Store), service (in-app). One row per *kind* of channel.
- **Customer Relationships** — the *depth* of service: automated (self-serve) → assisted (email) → manual (campus ambassador).
- **Revenue Streams** — where money *actually* comes from; name pricing model(s).
- **Key Resources / Activities / Partnerships** — Resources = what you *own* (API, data, brand); Activities = what you *do* daily (prompt tuning, moderation, cost watch); Partnerships = who you *borrow* capability from.
- **Cost Structure** — for an AI product, name the **dominant cost explicitly**: it's usually **API tokens** (see P08 for numbers). A BMC without a token-cost line fails in viva.

## 6. Expected Deliverable (report skeleton)
1. Title, aim, date.
2. Completed BMC (9 blocks).
3. Monetization model comparison table + the **choice** with justification.
4. Pricing table (3.2) with the per-plan "why".
5. Simple unit economics line (revenue vs cost-to-serve vs margin).
6. Conclusion.

## 7. Viva Q&A
1. **What is a Business Model Canvas?** — A one-page, 9-block strategic template (Osterwalder) describing how a business creates, delivers, and captures value.
2. **Why is token cost the dominant cost for StudyMate?** — Every summary/quiz/answer is an LLM API call; unlike hosting, token cost grows with every *feature use*, not with user count alone.
3. **Why freemium over pure subscription?** — Free tier drives acquisition and proves value; the Pro tier monetises the exam-season spike; the semester plan reduces churn.
4. **What's a "usage-based" model?** — Billing per unit consumed (per token/per API call) — fair but unpredictable; StudyMate keeps it only for bulk enterprise seats.

## 8. Resources
- Business Model Canvas (Strategyzer, official): https://www.strategyzer.com/library/the-business-model-canvas
- *Business Model Generation* — Osterwalder & Pigneur (the BMC book)
- "How to price AI features" essays: search *how to price ai products tokens saas* (a16z / Lenny's Newsletter)
- Free BMC template: https://www.strategyzer.com/library/the-business-model-canvas (downloadable canvas PDF)
- Template file: [[p07_bmc_template.md|`p07_bmc_template.md`]]

---



---

## 🐛 Failure Modes & Debugging (Real-World Experience)

> [!bug] What goes wrong in production?
> When running **Business Model Canvas** in a real environment, it almost never works perfectly the first time. 
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

- **Business Model Canvas (BMC)** — all 9 blocks — for StudyMate.
- **Customer Segments** — who pays *and* who uses (they may differ — students use, tutorial centres pay).
- **Value Proposition** — the *one sentence* a customer would repeat. Must be a measurable outcome ("10-minute revision pack"), not a feature list.
- **Channels** — acquisition (Instagram), distribution (Play Store), service (in-app). One row per *kind* of channel.
- **Customer Relationships** — the *depth* of service: automated (self-serve) → assisted (email) → manual (campus ambassador).
- **Revenue Streams** — where money *actually* comes from; name pricing model(s).
- **Key Resources / Activities / Partnerships** — Resources = what you *own* (API, data, brand); Activities = what you *do* daily (prompt tuning, moderation, cost watch); Partnerships = who you *borrow* capability from.
- **Cost Structure** — for an AI product, name the **dominant cost explicitly**: it's usually **API tokens** (see P08 for numbers). A BMC without a token-cost line fails in viva.

> [!tip] Viva Prep
> Be ready to explain the *why* behind each step, not just the output.
