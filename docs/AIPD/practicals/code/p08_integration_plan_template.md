# AI Integration Plan Template — <Your Product>

> Reusable blank for [P08](../writeups/P08_ai_integration_plan.md). API choice → token cost math → security → latency/fallbacks.

## 1. API selection
| Need | Model/API | Why this choice | Typical input/output size (tokens) |
|---|---|---|---|
| | | | |
| | | | |
| | | | |

## 2. Cost estimate (worked example — show the arithmetic!)
| Activity | Tokens in + out | Price per 1M tokens | Cost per request |
|---|---|---|---|
| | | | |

Monthly model:
- Requests / heavy user / month: ____
- Cost to serve / user: ____ vs plan price: ____ → margin: ____
- Free-tier daily cap (why): ____

## 3. Security
| Concern | Mitigation |
|---|---|
| API key leakage | (keys must be server-side only) |
| Key rotation & scoping | |
| Data handling (TLS, encryption, no training on user data) | |
| Input hygiene (file validation, prompt-injection guard) | |
| Rate limiting & quotas | |
| Access control (per-user namespacing, 2FA) | |
| Audit logging | |

## 4. Latency & fallbacks
| Failure | Target | Plan |
|---|---|---|
| Normal latency (name seconds per interaction) | | |
| API down / 5xx | | |
| Rate limited (429) | | |
| Document too long for model | | |
| Toxic / off-topic request | | |
