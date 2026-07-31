---
subject: AIPD
status: not-started
tags: [subject/aipd, practical, unit/1]
practical: 3
unit: 1
hours: 2
---
# P03 — Data Components: Inventory, Classification & Risk Identification

**Subject:** AI Product Design | **Unit:** 1 | **Approx. Hrs:** 2
**PrO (verbatim):** *Identify and describe Data components, classify data types, and identify risks.*

---

## 1. Objective
- List **every piece of data** StudyMate needs — for *training* (indirectly, via the base model) and for *inference* (running the product).
- Classify each data type as **structured / unstructured** and **personal / sensitive / non-personal**.
- Identify the **risks** attached to holding each type (see P11 and P12 for the full plans).

## 2. Why data is the foundation (exam framing)

An AI product has no value without data, and data is where most product risk lives:
- **Unstructured** data (PDFs, chat, audio) is what LLMs consume; it is harder to secure and search than rows in a table.
- **Personal** data (things tied to a person) triggers privacy law; **sensitive** data triggers much stricter rules (see P11, Unit 5).
- A data inventory is the first document a data-protection officer or GTU viva examiner will ask for.

## 3. Filled Data Inventory — StudyMate

### 3.1 Inference data (the data your product actually processes)

| Data item | Example | Structured / Unstructured | Personal? | Sensitive? | Where it lives | Risk level |
|---|---|---|---|---|---|---|
| Uploaded study material | Student's PDF notes, slides | Unstructured (text/images) | No (usually) | Can be (if it contains personal details) | Cloud storage, indexed copy | 🟡 Medium |
| User profile | Name, email, college, semester | Structured | ✅ Yes | No | Account DB | 🟡 Medium |
| Chat messages | "Explain Kirchhoff's law" | Unstructured text | ✅ Yes | No | Chat history DB | 🟡 Medium |
| Quiz answers & scores | MCQ choices, % score | Structured | ✅ Yes (linked to account) | No | Progress DB | 🟢 Low |
| Study plan | Exam date, chapters left | Structured | ✅ Yes | No | Progress DB | 🟢 Low |
| Device / usage telemetry | App-opened timestamps, device type | Structured | No | No | Analytics | 🟢 Low |

### 3.2 Training data (conceptual — StudyMate uses a pre-trained LLM API)

| Data item | How it's used | Structured / Unstructured | Notes |
|---|---|---|---|
| Base LLM training corpus (handled by the API provider, not us) | The model's general knowledge | Unstructured | We do **not** train; we fine-tune/prompt over student docs (inference-time learning) |
| User feedback signals | Quality of generated quizzes (implicit training signal) | Structured | Aggregated; never raw student content in shared models |

### 3.3 Risk identification

| Risk | Data affected | Why it's a risk | Severity | Where handled |
|---|---|---|---|---|
| **Over-storage** — keeping old uploads forever | All user data | More data = bigger breach surface + legal obligation | 🟠 High | P11 retention policy |
| **Sensitive content inside uploads** — notes containing exam hall tickets, Aadhaar numbers, medical info | Uploaded docs | Student didn't intend it as "sensitive", but law treats it as such | 🟠 High | P03 §4 mitigation + P11 |
| **Training-data leakage** — model answers from other students' material | Uploaded docs | Cross-user contamination; a student sees someone else's private notes | 🟠 High | Per-user document isolation (P02, P08) |
| **Prompt/content privacy** — chat sent to third-party API | Chat + docs | API provider may log; student's material leaves our servers | 🟠 High | P08 data-processing agreement |
| **Re-identification** — analytics could single out a student | Telemetry + profile | Combining rows can re-identify even "anonymous" data | 🟡 Medium | Anonymise, aggregate, P11 |
| **Rogue employee / breach** — internal access | All | Human error or insider misuse | 🟡 Medium | Access control (P08) |

## 4. Blank Template (copy into `../code/p03_data_inventory_template.md`)

```
# Data Components — <Product>

## Inference data
| Data item | Example | Structured/Unstructured | Personal? | Sensitive? | Where it lives | Risk level |

## Training data
| Data item | How it's used | Structured/Unstructured | Notes |

## Risk identification
| Risk | Data affected | Why it's a risk | Severity | Where handled |
```

## 5. How to classify (the rules you need in an exam)

**Structured vs Unstructured**
- **Structured** = fits rows/columns, searchable by queries → profile table, scores, timestamps.
- **Unstructured** = free text, images, audio, PDFs → notes, chat, diagrams. LLMs exist because most human knowledge is unstructured.
- Rule of thumb: *if a spreadsheet can hold it naturally, it's structured.*

**Personal vs Sensitive (DPDP Act 2023 — see Unit 5)**
- **Personal data** = any data identifying a person: name, email, roll number.
- **Sensitive personal data** (Indian law / DPDP context) = financial data, health data, biometrics, caste/religious/political info, and (DPDP's key addition) **children's data**.
- A student's uploaded notes are *unstructured*, *usually non-personal* — but you must scan and classify them because you cannot guarantee that. **Classification is a policy decision, not just a technical one.**

**Risk level judgement**
- 🟢 Low — can't identify a person, no legal exposure.
- 🟡 Medium — identifies a person but not sensitive; loss is embarrassing, not catastrophic.
- 🟠 High — sensitive OR large volume OR legally regulated OR could harm a person if leaked.

## 6. Expected Deliverable (report skeleton)
1. Title, aim, date.
2. Inference data inventory (3.1) — full table.
3. Training data note (3.2) — explain "we use a pre-trained API, we don't train".
4. Risk table (3.3) with severity.
5. Two-sentence mitigation summary per High risk.
6. Conclusion.

## 7. Viva Q&A
1. **Structured vs unstructured?** — Rows/columns vs free-form text/media; LLMs consume unstructured data.
2. **Why is an upload risky even if it's "just notes"?** — Notes can accidentally contain sensitive/personal data (IDs, certificates, medical letters), and any data sent to a third-party API leaves your control.
3. **Do you train the model?** — No; StudyMate uses a pre-trained LLM API and grounds answers in per-user documents (RAG). User data is not used to train the shared model.
4. **What's the first thing you'd audit?** — Retention: what we store, how long, and who can access it (ties to P11).

## 8. Resources
- Data types & classification (NIST guide): search *nist data classification guidelines confidential sensitive*
- India DPDP Act 2023 summary: search *dpdp act 2023 summary personal data sensitive data*
- "Data Inventory" how-to (privacy frameworks): search *data inventory and mapping gdpr guide*
- Template file: [[p03_data_inventory_template.md|`p03_data_inventory_template.md`]]

---



---

## 🐛 Failure Modes & Debugging (Real-World Experience)

> [!bug] What goes wrong in production?
> When running **Data Components** in a real environment, it almost never works perfectly the first time. 
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

- **Over-storage** — keeping old uploads forever | All user data | More data = bigger breach surface + legal obligation | 🟠 High | P11 retention policy |
- **Sensitive content inside uploads** — notes containing exam hall tickets, Aadhaar numbers, medical info | Uploaded docs | Student didn't intend it as "sensitive", but law treats it as such | 🟠 High | P03 §4 mitigation + P11 |
- **Training-data leakage** — model answers from other students' material | Uploaded docs | Cross-user contamination; a student sees someone else's private notes | 🟠 High | Per-user document isolation (P02, P08) |
- **Prompt/content privacy** — chat sent to third-party API | Chat + docs | API provider may log; student's material leaves our servers | 🟠 High | P08 data-processing agreement |
- **Re-identification** — analytics could single out a student | Telemetry + profile | Combining rows can re-identify even "anonymous" data | 🟡 Medium | Anonymise, aggregate, P11 |
- **Rogue employee / breach** — internal access | All | Human error or insider misuse | 🟡 Medium | Access control (P08) |
- **Structured vs Unstructured** — **Structured** = fits rows/columns, searchable by queries → profile table, scores, timestamps.
- **Risk level judgement** — 🟢 Low — can't identify a person, no legal exposure.

> [!tip] Viva Prep
> Be ready to explain the *why* behind each step, not just the output.
