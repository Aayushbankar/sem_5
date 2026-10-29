# Practical 01: Use Generative AI Tools for Different Task Types & Domains

**Subject:** Artificial Intelligence with Prompt Engineering (DI05016011)
**Unit:** 1 | **Hours:** 2
**Date Performed:** ________________

---

## 1. Aim

Use Generative AI tools (ChatGPT, Google Gemini, Claude) to perform different types of tasks and document their applications in various domains.

---

## 2. Process / Program Code / Prompts Used

### 2.1 Task-Type Matrix (6 Task Types × 3 Tools)

| Task Type | Tool Used | Prompt Used | Output Quality (1-5) |
|-----------|-----------|-------------|----------------------|
| **Text Generation** (email writing) | ChatGPT | "Write a polite leave-application email to my professor for 3 days due to illness" | 5/5 |
| **Image Generation** (logo design) | DALL·E 3 | "A minimalist logo for a tech club, flat design, blue and white colors" | 4/5 |
| **Code Generation** (Python function) | ChatGPT | "Write a Python function to flatten a nested list recursively with type hints and docstring" | 5/5 |
| **Audio Generation** (text-to-speech) | ElevenLabs | "Convert this text to speech: 'Welcome to our AI lab session'" | 4/5 |
| **Video Generation** (short clip) | Runway Gen-2 | "Abstract technology background loop, 5 seconds, smooth motion" | 3/5 |
| **Analysis** (sentiment classification) | Google Gemini | "Classify each review as Positive/Negative/Neutral: [5 reviews provided]" | 4/5 |

### 2.2 Three-Tool Comparison (Same 4 Tasks)

| Task | Prompt | ChatGPT Output | Gemini Output | Claude Output |
|------|--------|----------------|---------------|---------------|
| Summarize paragraph | "Summarize the following in 2 lines: [paragraph]" | 2 crisp lines, key facts kept ✅ | 2 lines + bullet list, slightly longer | 2 lines, natural tone ✅ |
| Fix buggy code | "Fix the bug in: `for i in range(1, n+1): total += arr[i]`" | Explains bug + fixed code ✅ | Fixed code + test output | Fixed code + why bug happened ✅ |
| Write email (3 tones) | "Write formal/neutral/casual leave email" | 3 variants, ready to use ✅ | 3 variants + subject lines ✅ | 3 variants, very polite |
| Explain concept | "Explain gradient descent to a 10-year-old" | Analogy (ball rolling down hill) ✅ | Analogy + diagram text | Analogy + example numbers ✅ |

---

## 3. Screenshot of Output

> **Note:** The following outputs were generated with the student's name and roll number included in the prompt as per faculty guidelines.

### Sample Output — ChatGPT Text Generation
```
[Student Name: ________________ | Roll No: ________________]

Prompt: "Write a polite leave-application email to Professor Sharma requesting 3 days leave due to fever. Include my name [STUDENT NAME] and roll number [ROLL NO] in the signature."

Output:
Subject: Leave Application - [STUDENT NAME] (Roll No: [ROLL NO])

Dear Professor Sharma,

I am writing to request a leave of absence for 3 days (August 10-12, 2026) due to high fever and medical advice for rest. I have completed 80% of the Networking assignment and will submit the remaining portion immediately upon return.

Kindly grant me leave for the mentioned dates.

Thank you for your understanding.

Sincerely,
[STUDENT NAME]
Roll No: [ROLL NO]
IT Semester 5, Division A
```

### Sample Output — Gemini Image Generation
```
[Student Name: ________________ | Roll No: ________________]

Prompt: "Generate a minimalist logo for 'AI Club' with blue/white theme. Add text 'Created by [STUDENT NAME], Roll [ROLL NO]' at bottom."

Output: [Image generated - logo with student details watermarked]
```

### Sample Output — ChatGPT Code Generation
```
[Student Name: ________________ | Roll No: ________________]

Prompt: "Write a Python function to flatten a nested list. Include type hints, docstring, and a comment with my name [STUDENT NAME] and roll number [ROLL NO]."

Output:
def flatten(nested: list) -> list:
    """
    Flatten a nested list into a single list.
    Author: [STUDENT NAME] | Roll No: [ROLL NO]
    """
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

# Test
print(flatten([[1, [2, 3]], [4]]))  # Output: [1, 2, 3, 4]
```

---

## 4. Application of Learning

| Domain | Application | Example Project Where This Skill Is Required |
|--------|-------------|---------------------------------------------|
| **Daily Life** | Email drafting, travel planning, recipe ideas | Personal AI assistant for daily task automation |
| **Education** | Concept explanation, quiz generation, summarization | AI tutor for student doubt solving and practice tests |
| **Healthcare** | Medical note summarization, patient education content | Hospital discharge summary generator for patients |
| **Cybersecurity** | Phishing email detection, log analysis, report drafting | SOC analyst assistant for alert triage |
| **Software Development** | Code generation, debugging, documentation, test writing | AI pair programmer for feature development |
| **Business/Content** | Blog writing, marketing copy, reports, presentations | Marketing team content automation pipeline |
| **Media** | Image/video generation, dubbing, subtitles | Social media content creation at scale |

**Key Learning:** The same task can be performed by multiple GenAI tools with similar quality but different style. Tool choice depends on task type (code → ChatGPT, multimodal → Gemini, long explanations → Claude). Prompt quality directly controls output quality — this is the foundation of prompt engineering (Units 3–4).

---

## 5. Files Submitted

- **Writeup:** This document (`P01_GenAI_Tools_Tasks_Domains.md`)
- **Code/Templates:** `../code/p01_genai_task_templates.txt`
- **Screenshots:** `../screenshots/P01_*.png` (placeholder for actual screenshots)

---

**Student Signature:** ________________    **Faculty Signature:** ________________