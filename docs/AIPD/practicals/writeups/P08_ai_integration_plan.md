# P08 — AI Integration Plan: API Usage, Cost Awareness & Security

**Subject:** AI Product Design | **Unit:** 3 | **Approx. Hrs:** 2
**PrO (verbatim):** *Prepare AI integration plan including API usage, cost awareness, and security.*

---

## 1. Objective
- Choose concrete **AI APIs** for StudyMate and justify the choice.
- Estimate **token costs** with example numbers (cost awareness is a syllabus outcome).
- Plan **security** (key management, data handling), **latency**, and **fallbacks** when the API fails.

## 2. API selection (filled)

| Need | Model/API (example) | Why this choice | Input/output (for a typical request) |
|---|---|---|---|
| Summaries & quiz generation | **OpenAI GPT-4o-mini** (chat completions) | Cheapest capable LLM; good Hindi/Gujarati support; simple API | Input ~4,000 tokens (a chapter); output ~800 tokens (summary) |
| Long-document grounding | **RAG pipeline** (embedding model e.g. `text-embedding-3-small` + a vector store) | Answers cite the student's own pages; cuts hallucination | Embed each chunk (≈150 tokens/chunk) |
| Optional speech (read aloud) | TTS API (e.g., OpenAI `tts-1`) | Exam-time listening revision | Input text; output audio |
| UI / non-AI stack | PWA (React/Flutter) + cloud backend | Scales with student count | — |

> **Rule:** for an MVP, prefer a **managed API over self-hosted models** — no GPU ops, pay-per-use, and your cost = usage (P07). Self-hosting only wins at huge, predictable scale.

## 3. Cost awareness — worked token estimate (the exam-ready numbers)

**Token math (must know):** 1 token ≈ 0.75 English words. Billing = prompt tokens + completion tokens.

| Activity | Tokens per request | Price (example: GPT-4o-mini ≈ ₹0.63/M prompt, ₹2.5/M completion) | Cost |
|---|---|---|---|
| Summarise a 10-page PDF | ~8,000 in + ~900 out | 8,000/1M×0.63 + 900/1M×2.5 | ≈ ₹0.007 |
| Generate a 10-question quiz | ~2,500 in + ~1,200 out | same pricing | ≈ ₹0.005 |
| 5 chat turns (grounded) | ~4,000 in + ~400 out | same | ≈ ₹0.004 |

**Monthly cost model (pro User, heavy use):**
```
~200 requests × ₹0.006 avg  ≈ ₹1.2  (token cost per heavy user/month)
+ hosting/shared ops        ≈ ₹5.0
────────────────────────────
≈ ₹6.2 cost-to-serve  vs  ₹199/month Pro  → gross margin ≈ 97%
```
> **Lesson for the viva:** AI products are *token-priced*, so unit economics are great *only if* you cap free-tier usage (P07's daily caps) — the cost of a malicious user hammering your API is your biggest unit-economics risk (see also P12: adversarial inputs).

## 4. Security plan (filled)

| Concern | Mitigation in StudyMate |
|---|---|
| **API key leakage** | Keys live **server-side only**; never in the mobile/web bundle. Server proxies every call; students never touch the key. |
| **Key rotation & scoping** | Per-environment keys (dev/prod); rotate on a schedule or on suspicion; restrict key to the one endpoint it needs. |
| **Data handling** | TLS in transit; encryption at rest; *no* training on user data (API provider agreement must state user content isn't used to train); regional data residency where possible. |
| **Input hygiene** | Validate file type/size; reject executables; **prompt-injection guard**: system prompt marks uploaded docs as untrusted content (see P12). |
| **Rate limiting & quotas** | Per-user caps (P07 free-tier caps) + per-key monthly budget alerts — stops a runaway/bot bill. |
| **Access control** | Users see only their own documents (per-user namespacing); internal staff need 2FA + least privilege. |
| **Audit log** | Log every API call (user, tokens, latency, result) for cost + abuse monitoring. |

## 5. Latency & fallbacks (filled)

| Failure | Target | Plan |
|---|---|---|
| **Normal latency** | Summary < 30 s (async job + progress bar); chat < 3 s | Stream chat tokens; cache repeated requests |
| **API down / 5xx** | Retry with exponential backoff (2×, max 3 retries); then **fallback**: show cached summary or a polite "try again in a minute" | Message to the student; no silent failure |
| **Rate limited (429)** | Queue + retry later; degrade to free-tier model temporarily | Monitor via alerts |
| **Long document (>model limit)** | Chunk + map-reduce summarisation (summarise per chunk, then combine) | Never let a PDF crash the request |
| **Toxic / off-topic request** | Output moderation filter → block + friendly notice | Prevents policy violations (P11) |

## 6. Blank Template (copy into `../code/p08_integration_plan_template.md`)

```
# <Product> — AI Integration Plan (blank)

## API selection
| Need | Model/API | Why | Typical input/output size |

## Cost estimate
| Activity | Tokens in/out | Price | Cost per request |
| Monthly cost model | cost-to-serve/user | plan price | margin |
| Free-tier cap | ____ | (why: ____) |

## Security
| Concern | Mitigation |
| API key leakage | |
| Data handling | |
| Input hygiene | |
| Rate limiting | |
| Access control | |

## Latency & fallbacks
| Failure | Target | Plan |
```

## 7. Field-by-field explanation (how to redo for your idea)
- **API choice** — justify with 3 axes: *cost per request, quality of output, data/region compliance*. Copying "because it's popular" is zero marks.
- **Token cost** — always show a *worked example* with numbers, then a monthly model. Examiners mark the arithmetic, not the guess.
- **Key security** — the single non-negotiable: **keys never ship in the client**. Everything else (rotation, scoping) follows from that.
- **Latency target** — name a number per interaction and a fallback per failure mode. "It'll probably be fine" is not a plan.
- **Fallback** — every API-dependent product needs a *degraded mode* (cache, retry, friendly error). A plan without fallbacks is a plan to lose users.

## 8. Expected Deliverable (report skeleton)
1. Title, aim, date.
2. API selection table with justification.
3. Worked token-cost example + monthly unit-economics.
4. Security table (7+ rows).
5. Latency/fallback table.
6. Conclusion: 2 risks this plan reduces and the residual risk left.

## 9. Viva Q&A
1. **Why server-side API keys?** — A key in a mobile bundle can be extracted by anyone (APK reverse engineering); a server-side proxy is the only way to keep it secret + add rate limits/logging.
2. **What is a token?** — The pricing unit of LLM APIs (~3–4 chars of English); you pay for both input and output tokens.
3. **What's RAG doing in the integration plan?** — It's the grounding step: embed chunks of the student's PDF, retrieve relevant chunks, inject them into the prompt — cutting cost (fewer tokens) and hallucination.
4. **Your API is down at exam week. What happens?** — Retry with backoff, serve cached summaries/quizzes, and show an honest status message; monitor and alert the team.

## 10. Resources
- OpenAI pricing page (token costs): https://openai.com/api/pricing/
- "How to build a RAG system" guides: search *rag retrieval augmented generation explained*
- OpenAI API security best practices: https://platform.openai.com/docs/guides/safety-best-practices
- OWASP LLM Top 10 (security for LLM apps): https://owasp.org/www-project-top-10-for-large-language-model-applications/
- Template file: [`p08_integration_plan_template.md`](../code/p08_integration_plan_template.md)
