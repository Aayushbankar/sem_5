# Practical 05: Design & Refine Prompts — Email Writing & Concept Explanation

**Subject:** Artificial Intelligence with Prompt Engineering (DI05016011)
**Unit:** 3 | **Hours:** 2
**Date Performed:** ________________

---

## 1. Aim

Design and refine prompts for tasks such as email writing and concept explanation. Compare outputs before and after prompt refinement.

---

## 2. Process / Program Code / Prompts Used

### Task 1: Email Writing — 3 Iterations

#### Iteration 1 (First Try)
```
Prompt: Write an email asking for a deadline extension.
```
**Output:** Generic, no recipient, no reason, no dates. Usable as skeleton only.
**Problem Diagnosed:** No audience, no reason, no clear ask.

#### Iteration 2 (Add Audience + Reason)
```
Prompt: Write an email to my professor asking to extend the project submission deadline by 5 days because I was hospitalised for a week.
```
**Output:** Polite, includes reason, but invents dates and has no clear closing ask.
**Problem Diagnosed:** Needs exact dates + clear request sentence + subject line.

#### Iteration 3 (Full Structure — Final)
```
Prompt: Act as a professional writing coach. Write a polite email to my professor, Dr. Sharma, asking to extend the "Networking" assignment deadline from 5 August to 10 August. Reason: I was hospitalised from 25 July to 2 August. Requirements:
- Subject line that mentions the extension request.
- 3 short paragraphs: greeting + reason, current status, clear request with dates.
- A closing line thanking the professor.
- Formal but warm tone.
- Include my name [STUDENT NAME] and roll number [ROLL NO] in signature.
```
**Output:** Complete, ready-to-send email with subject line, dates, and polite closing. ✅

### Task 2: Concept Explanation — 3 Iterations

#### Iteration 1
```
Prompt: Explain an API.
```
**Output:** Correct but long, vague, no audience.
**Problem Diagnosed:** No audience → wrong level of detail.

#### Iteration 2
```
Prompt: Explain an API to a non-technical person, like a hotel manager.
```
**Output:** Better — uses "restaurant waiter" analogy. Still no length limit or concrete examples.
**Problem Diagnosed:** Add length limit + concrete example + why it matters.

#### Iteration 3 (Final)
```
Prompt: Explain what an API is to a hotel manager (non-technical).
- Use the analogy of a waiter passing orders between kitchen and guest.
- Max 150 words.
- End with 2 examples of APIs used in hospitality booking software.
- Simple English, no jargon.
- Add a footer: "Explained by [STUDENT NAME], Roll No: [ROLL NO]"
```
**Output:** Tight analogy, exactly 2 examples, jargon-free. ✅

### Before/After Comparison Tables

| Aspect | Iteration 1 | Iteration 2 | Iteration 3 |
|--------|-------------|-------------|-------------|
| **Email — Length** | ~50 words | ~70 words | ~90 words |
| **Email — Dates** | none | invented | correct |
| **Email — Clear Request** | no | weak | explicit |
| **Email — Subject Line** | none | none | yes |
| **Email — Tone Control** | default | polite | warm + formal |

| Aspect | Iteration 1 | Iteration 2 | Iteration 3 |
|--------|-------------|-------------|-------------|
| **Concept — Audience** | none | hotel manager | hotel manager |
| **Concept — Analogy** | none | waiter | waiter + kitchen |
| **Concept — Length** | ~200 words | ~120 words | ~140 words |
| **Concept — Examples** | none | none | 2 booking APIs |
| **Concept — Jargon** | yes | some | none |

### Why Each Refinement Helps

| Refinement | Effect on the Model |
|------------|---------------------|
| Adding a role ("Act as...") | Biases model toward domain-appropriate tone and knowledge |
| Adding audience | Fixes the "level of detail" the model guesses at |
| Supplying exact data (dates, names) | Stops model from inventing facts (hallucination control) |
| Formatting instructions (subject, bullets, length) | Makes output predictable and directly usable |
| Constraints (max words, tone) | Shrinks the search space of possible answers |
| Self-review round ("critique then rewrite") | Second pass removes model's own errors |

---

## 3. Screenshot of Output

### Task 1 — Email Writing: Final Output (Iteration 3)

```
[STUDENT NAME | ROLL NO: ________________]

Prompt: Act as a professional writing coach. Write a polite email to my professor, Dr. Sharma, asking to extend the "Networking" assignment deadline from 5 August to 10 August. Reason: I was hospitalised from 25 July to 2 August. Requirements: Subject line mentioning extension, 3 short paragraphs, closing thanks, formal but warm tone, include [STUDENT NAME] and [ROLL NO].

Output:
Subject: Extension Request — Networking Assignment — [STUDENT NAME] (Roll No: [ROLL NO])

Dear Dr. Sharma,

I am writing to request an extension for the Networking assignment, currently due on 5 August. I was hospitalised from 25 July to 2 August due to a severe viral infection, which prevented me from working on the project during that period. I have attached the medical certificate for your reference.

As of today, the project is approximately 80% complete. The remaining work involves final testing and documentation, which I estimate will take 2–3 days. I am fully committed to submitting a high-quality deliverable.

I kindly request an extension until 10 August 2026. I will ensure submission by end of day on that date. Thank you for your understanding and consideration.

Sincerely,
[STUDENT NAME]
Roll No: [ROLL NO]
IT Semester 5, Division A
```

### Task 2 — Concept Explanation: Final Output (Iteration 3)

```
[STUDENT NAME | ROLL NO: ________________]

Prompt: Explain what an API is to a hotel manager (non-technical). Use waiter analogy, max 150 words, end with 2 hospitality API examples, no jargon, add footer with student details.

Output:
Think of an API like a waiter in a restaurant. You (the guest) tell the waiter what you want from the menu. The waiter takes your order to the kitchen (the system), the kitchen prepares it, and the waiter brings back your food. You don't need to know how the kitchen works — you just get what you ordered.

In software, an API is that waiter. Your booking website asks the hotel's system for room availability. The API carries that request, the system checks its database, and the API returns the answer — available rooms and prices. Your website shows this to the guest without them ever seeing the hotel's internal system.

Two real examples in hospitality:
1. **Booking.com API** — lets travel sites show your hotel's live rates and availability.
2. **Cloudbeds API** — connects your property management system to online travel agencies automatically.

— Explained by [STUDENT NAME], Roll No: [ROLL NO]
```

---

## 4. Application of Learning

| Domain | Application | Example Project |
|--------|-------------|-----------------|
| **Business Communication** | Professional email drafting | AI assistant for corporate communication templates |
| **Technical Documentation** | Concept explanation for non-technical stakeholders | API documentation generator for product teams |
| **Customer Support** | Response templating with personalization | Support ticket auto-reply with customer-specific details |
| **Education** | Adaptive explanation generator | Tutoring system that adjusts complexity to student level |
| **Marketing** | Copy iteration and refinement | Ad copy A/B testing with prompt-controlled variations |
| **Legal/Compliance** | Formal letter generation with constraints | Legal notice generator with required clauses |

**Key Learning:** The biggest quality jumps came from adding missing input data (dates/reason) and fixing the audience, not from fancier words. Formatting instructions made output directly usable. Prompt design is an iteration loop: every output is feedback for the next prompt.

---

## 5. Files Submitted

- **Writeup:** This document (`P05_Prompt_Design_Refinement.md`)
- **Code/Templates:** `../code/p05_before_after_template.md`
- **Screenshots:** `../screenshots/P05_*.png` (placeholder for actual screenshots)

---

**Student Signature:** ________________    **Faculty Signature:** ________________