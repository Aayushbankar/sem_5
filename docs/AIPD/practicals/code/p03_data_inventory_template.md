# Data Components Template — <Your Product>

> Reusable blank for [P03](../writeups/P03_data_components.md). Classify every dataset you can name; if you can't classify it, you can't protect it.

## 1. Inference data (what the product processes at run-time)
| Data item | Example | Structured / Unstructured | Personal? (Y/N) | Sensitive? (Y/N) | Where it lives | Risk level 🟢🟡🟠 |
|---|---|---|---|---|---|---|
| | | | | | | |
| | | | | | | |
| | | | | | | |

## 2. Training data (conceptual)
| Data item | How it's used | Structured / Unstructured | Notes |
|---|---|---|---|
| Base model corpus (if using a pre-trained API, state who owns it) | | | |
| User feedback signals | | | |

## 3. Risk identification
| Risk | Data affected | Why it's a risk | Severity | Where handled (P08/P11/P12) |
|---|---|---|---|---|
| | | | | |
| | | | | |

## 4. Classification rules (copy-paste reminders)
- **Structured** = fits rows/columns (profile table, scores). **Unstructured** = free text/images/audio (PDFs, chat).
- **Personal** = identifies a person (name, email). **Sensitive** = health, financial, biometrics, children's data — triggers stricter rules.
- Risk: 🟢 low (can't identify anyone) · 🟡 medium (personal but not sensitive) · 🟠 high (sensitive OR large volume OR legally regulated).
