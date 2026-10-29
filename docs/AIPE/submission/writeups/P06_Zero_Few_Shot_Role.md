# Practical 06: Zero-Shot, Few-Shot & Role-Based Prompting

**Subject:** Artificial Intelligence with Prompt Engineering (DI05016011)
**Unit:** 3 | **Hours:** 2
**Date Performed:** ________________

---

## 1. Aim

Apply prompting techniques such as zero-shot, few-shot, and role-based prompting.

---

## 2. Process / Program Code / Prompts Used

### Theory Reference

| Technique | Definition | When to Use |
|-----------|------------|-------------|
| **Zero-shot** | One instruction, no examples. Model does task from prompt alone. | Simple, common tasks; quick tests |
| **Few-shot** | Show 2–5 examples of input→output before real task. Teaches pattern/format. | Odd formats, new tasks, improving consistency |
| **Role-based** | Assign a role ("act as a teacher, doctor, editor...") to set tone, knowledge, constraints. | Domain-specific tone & vocabulary |

### 2.1 Zero-Shot Examples (2)

#### Example 1: Sentiment Label
```
Prompt: Classify the sentiment of this review as Positive, Negative, or Neutral.
Review: "The battery drains really fast after the update."
Output: Negative.
```

#### Example 2: Table Extraction
```
Prompt: Convert the sentence into a table with columns Name, Age, City.
Sentence: "Riya, 21, lives in Ahmedabad; Aarav, 22, lives in Vadodara."
Output: 
| Name | Age | City |
|------|-----|------|
| Riya | 21 | Ahmedabad |
| Aarav | 22 | Vadodara |
```

### 2.2 Few-Shot Examples (2)

#### Example 1: Custom Tone/Format (FACT vs OPINION)
```
Prompt: Classify each text as FACT or OPINION.

"The Earth orbits the Sun." -> FACT
"Pizza is the best food." -> OPINION
"Python is easier than Java." -> OPINION
"Water boils at 100 °C at sea level." -> FACT

"IPL matches are more entertaining than test cricket." ->
Output: OPINION
```
**Why examples matter:** Without examples, model may answer "SUBJECTIVE/OBJECTIVE"; examples pin the exact labels.

#### Example 2: Specific Output Shape (Support Ticket)
```
Prompt: Turn each complaint into a ticket with fields: ID, ISSUE, PRIORITY.

"App crashes when I upload photos." -> ID: T-001, ISSUE: crash-on-upload, PRIORITY: high
"The search bar is slow." -> ID: T-002, ISSUE: slow-search, PRIORITY: medium

"My account shows a wrong balance." ->
Output: ID: T-003, ISSUE: wrong-balance, PRIORITY: high
```
**Why:** Model now knows exact field names and 3-level priority scale instead of inventing its own.

### 2.3 Role-Based Examples (2)

#### Example 1: Primary School Teacher
```
Prompt: You are a primary-school science teacher. Explain why the sky is blue using only words a 7-year-old understands, and end with one fun question.
Output: (Simple explanation using "light bouncing like balls", ends with a question like "Have you ever seen a rainbow in a sprinkler?")
```

#### Example 2: Senior Python Code Reviewer
```
Prompt: You are a senior Python code reviewer. Review this function for bugs, naming, and performance. Give a verdict and 3 numbered suggestions.
(code snippet provided)
Output: Verdict + 3 numbered suggestions in strict checklist format
```

---

## 3. Screenshot of Output

### Zero-Shot Results

```
[STUDENT NAME | ROLL NO: ________________]

>>> Zero-Shot Example 1
Prompt: Classify the sentiment of this review as Positive, Negative, or Neutral.
Review: "The battery drains really fast after the update. [STUDENT NAME, ROLL NO]"
Output: Negative

>>> Zero-Shot Example 2
Prompt: Convert the sentence into a table with columns Name, Age, City.
Sentence: "Riya, 21, lives in Ahmedabad; Aarav, 22, lives in Vadodara. [STUDENT NAME, ROLL NO]"
Output:
| Name  | Age | City       |
|-------|-----|------------|
| Riya  | 21  | Ahmedabad  |
| Aarav | 22  | Vadodara   |
```

### Few-Shot Results

```
[STUDENT NAME | ROLL NO: ________________]

>>> Few-Shot Example 1 (FACT/OPINION)
Prompt: [2 examples provided]
"IPL matches are more entertaining than test cricket." ->
Output: OPINION

>>> Few-Shot Example 2 (Support Ticket)
Prompt: [2 examples provided]
"My account shows a wrong balance." ->
Output: ID: T-003, ISSUE: wrong-balance, PRIORITY: high
```

### Role-Based Results

```
[STUDENT NAME | ROLL NO: ________________]

>>> Role-Based Example 1 (Teacher)
Prompt: You are a primary-school science teacher. Explain why the sky is blue using only words a 7-year-old understands, and end with one fun question.
Output: Sunlight looks white but it's really made of all colors mixed together. When sunlight hits the air, the blue part bounces around the most and goes in all directions. That's why the sky looks blue! The other colors go straight through. Fun question: Have you ever seen a rainbow in a sprinkler on a sunny day?

>>> Role-Based Example 2 (Code Reviewer)
Prompt: You are a senior Python code reviewer. Review this function for bugs, naming, and performance. Give a verdict and 3 numbered suggestions.
def buggy_func(lst):
    for i in range(len(lst)):
        if lst[i] % 2 == 0:
            lst.remove(lst[i])  # BUG: modifies list during iteration
    return lst

Output:
**Verdict:** Buggy — modifies list during iteration causing skipped elements.

1. **Bug Fix:** Use list comprehension `[x for x in lst if x % 2 != 0]` instead of in-place removal.
2. **Naming:** Rename `buggy_func` to `filter_odd_numbers` for clarity.
3. **Performance:** Current approach is O(n²) due to `remove()`; comprehension is O(n).
```

---

## 4. Comparison Table

| Criterion | Zero-Shot | Few-Shot | Role-Based |
|-----------|-----------|----------|------------|
| Prompt Effort | Lowest | Medium (write examples) | Low |
| Consistency | Varies | Highest | Medium |
| Best For | Quick/common tasks | Exact formats & labels | Tone & domain depth |
| Risk | Format drift | Bad examples mislead | Over-roleplay verbosity |
| When to Choose | Simple instruction | Format must match | Domain voice matters |

**Rule of Thumb:** Zero-shot to prototype → add few-shot if format is off → add role if tone/domain is off. Combine freely ("Act as a teacher and use these 3 examples...").

---

## 5. Application of Learning

| Domain | Application | Example Project |
|--------|-------------|-----------------|
| **Data Labeling** | Consistent annotation at scale | Few-shot for custom label schemas in NLP pipelines |
| **Content Moderation** | Policy-compliant classification | Role-based "safety reviewer" with few-shot policy examples |
| **Code Generation** | Style-consistent code output | Role-based "senior engineer" + few-shot style guide |
| **Customer Service** | Brand-voice responses | Role-based "support agent" + few-shot approved responses |
| **Education** | Level-appropriate explanations | Role-based "tutor for grade X" + few-shot examples |
| **Legal/Compliance** | Format-standardized documents | Few-shot for contract clause templates |

**Key Learning:** Zero-shot is fastest but least controlled; few-shot trades a few example tokens for high format consistency; role-based is the cheapest way to inject domain expertise and tone. Best prompts mix all three — a role, examples, and a clear instruction.

---

## 6. Files Submitted

- **Writeup:** This document (`P06_Zero_Few_Shot_Role.md`)
- **Code/Templates:** `../code/p06_prompting_technique_templates.md`
- **Screenshots:** `../screenshots/P06_*.png` (placeholder for actual screenshots)

---

**Student Signature:** ________________    **Faculty Signature:** ________________