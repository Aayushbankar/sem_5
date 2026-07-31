---
title: "P01 — Genai Tools Tasks And Domains"
sidebar:
  order: 1
---

# P01 — Generative AI Tools for Different Task Types & Applications Across Domains

**Subject:** Artificial Intelligence with Prompt Engineering | **Unit:** 1 | **Approx. Hrs:** 2
**PrO (verbatim):** *Use Generative AI tools to perform different types of tasks and document their applications in various domains.*

---

## 1. Objective
- Use Generative AI tools (e.g., ChatGPT, Google Gemini, Claude) to perform **different types of tasks**.
- Build a **task-type matrix** covering text, image, code, audio, video, and analysis.
- Compare 3 tools (ChatGPT, Gemini, Claude) on 4 sample tasks.
- Document real-world applications of Generative AI across **domains**.

## 2. Theory (exam-ready)

### What is Generative AI?
Generative AI is a branch of AI that **creates new content** — text, images, code, audio, video — rather than only classifying or predicting. It learns the *underlying patterns and distribution* of training data and samples from it to produce novel outputs.

| Traditional AI (Discriminative) | Generative AI |
|---|---|
| Predicts a label/class (spam / not-spam) | Generates new examples (an email, an image) |
| Learns decision boundaries | Learns the data distribution *p(x)* |
| E.g., spam filter, fraud detection | E.g., ChatGPT, DALL·E, Stable Diffusion |

### Types of Generative AI systems
| System | Output | Examples |
|---|---|---|
| **Text generation** (LLMs) | Text | ChatGPT, Gemini, Claude, LLaMA |
| **Image generation** | Images | DALL·E, Midjourney, Stable Diffusion |
| **Code generation** | Source code | GitHub Copilot, Codeium, ChatGPT |
| **Audio generation** | Speech/music | ElevenLabs, Suno, Whisper (speech→text) |
| **Video generation** | Video clips | Runway, Pika, Sora |
| **Analysis / reasoning** | Insights, summaries | Any LLM with data (analysis of CSV, logs) |

### Popular tools covered by the syllabus
- **ChatGPT** (OpenAI) — general-purpose chatbot, strong reasoning & code.
- **Google Gemini** (Google DeepMind) — multimodal (text, image, audio), integrated with Google Workspace.
- **DALL·E** (OpenAI) — text-to-image generation.

## 3. Task-Type Matrix (the core deliverable)

Fill rows with your own observed results; the table below is a filled example.

| Task type | Tool used | Prompt (shortened) | Output quality | Best tool in class |
|---|---|---|---|---|
| **Text** (email, essay, summary) | ChatGPT | "Write a polite leave-application email" | 4/5 — clean, ready to send | ChatGPT / Claude |
| **Image** (generate a logo) | Gemini / DALL·E | "A minimalist logo for a tech club, flat design" | 3/5 — needs 2-3 iterations | DALL·E |
| **Code** (function) | ChatGPT | "Write a Python function to flatten a nested list" | 5/5 — correct + docstring | ChatGPT / Copilot |
| **Audio** (text-to-speech) | ElevenLabs (optional) | Paste text, pick a voice | 4/5 — natural voice | ElevenLabs |
| **Video** (short explainer) | Runway / Pika | "Abstract background loop, 5 s" | 3/5 — good for B-roll | Runway |
| **Analysis** (sentiment of 5 reviews) | Gemini | "Classify each review as positive/negative/neutral" | 4/5 — consistent labels | Gemini |

## 4. Worked Comparison — 3 tools × 4 tasks

Same task, same prompt, three tools. Fill your own rows; example rows show what a good comparison looks like.

| Task | Prompt | ChatGPT | Gemini | Claude |
|---|---|---|---|---|
| **Summarize** a paragraph (2 lines) | "Summarize: … in 2 lines" | 2 crisp lines, key facts kept ✅ | 2 lines + bullet list, slightly longer | 2 lines, natural tone ✅ |
| **Fix** a buggy snippet | "Fix the bug in: `for i in range(1, n+1): …`" | Explains bug + fixed code ✅ | Fixed code + test output | Fixed code + why the bug happened ✅ |
| **Write** an email (3 tones) | "Formal/neutral/casual leave email" | 3 variants, ready to use ✅ | 3 variants + subject lines ✅ | 3 variants, very polite |
| **Explain** a concept | "Explain gradient descent to a 10-year-old" | Analogy (ball rolling down a hill) ✅ | Analogy + small diagram text | Analogy + example numbers ✅ |

**Evaluation notes to document:**
1. All three tools produced usable output — differences were in **style**, not correctness.
2. ChatGPT was fastest to converge on code tasks; Claude gave the best *explanations*; Gemini was strongest on multimodal inputs (an image + text question).
3. Repeating the same prompt gives **different wording** (non-determinism) — expected for LLMs.
4. **Human-in-the-loop is required**: outputs need review for facts, tone, and safety.

## 5. Applications Across Domains (documentation table)

| Domain | Applications | Example |
|---|---|---|
| **Daily life** | Chatbots, recipe ideas, travel planning, email drafting | Ask an assistant to plan a 3-day trip |
| **Education** | Explanation, quiz generation, summarization, doubt solving | "Generate 5 MCQs on photosynthesis" |
| **Healthcare** | Summarizing medical notes, patient-education content, triage support (not diagnosis) | Summarize a doctor's prescription in plain language |
| **Cybersecurity** | Phishing-email detection, log analysis, security report drafting | "What does this log line indicate?" |
| **Software** | Code generation, debugging, documentation, test writing | Copilot suggesting a sort function |
| **Business/Content** | Blogs, marketing copy, reports, presentations | "Write a 300-word product description" |
| **Media** | Image/video generation, dubbing, subtitles | Auto-captions for a short video |

> [!warning] Responsible-use note
> GenAI can **hallucinate** and reflect **bias**; outputs in medicine/security must be verified by a human expert. (Detailed in Unit 2 §2.4 and Unit 5 §5.7.)

## 6. Deliverable — report skeleton
1. Title, aim, tools used.
2. Completed **task-type matrix** (Section 3) with your own observations.
3. Completed **3-tool comparison** (Section 4) with 2-3 sentences of evaluation.
4. **Domain table** (Section 5) with one example output pasted per domain.
5. Conclusion: which tool you'd pick for which task, and why a human still reviews.

## 7. Conclusion
Generative AI tools are general-purpose "content engines" that cover text, image, code, audio, video, and analysis. The **same task** can be done by ChatGPT, Gemini, or Claude with similar quality but different style, so choosing a tool depends on the task (code → ChatGPT, multimodal → Gemini, long explanations → Claude). The quality of the result is controlled by the **prompt** — which is exactly what the rest of this subject (Units 3–4) teaches.

## 8. Viva Q&A
1. **What is Generative AI?** — AI that creates new content (text/image/code/audio/video) by learning patterns in training data.
2. **Text generation vs image generation tool example?** — ChatGPT (text), DALL·E (image).
3. **Why are repeated prompts not identical?** — LLMs sample from a probability distribution (temperature), so output varies.
4. **What is a hallucination?** — A confident but factually wrong statement.
5. **Which tool for analyzing an uploaded image?** — Gemini (multimodal).

## 9. Resources
- ChatGPT: https://chat.openai.com
- Google Gemini: https://gemini.google.com
- DALL·E: https://openai.com/dall-e
- Prompt Engineering Guide (DAIR.AI): https://www.promptingguide.ai
- Template file: [`p01_genai_task_templates.txt`](./p01_genai_task_templates.txt.md)

---



---

## 🐛 Failure Modes & Debugging (Real-World Experience)

> [!bug] What goes wrong in production?
> When running **Genai Tools Tasks And Domains** in a real environment, it almost never works perfectly the first time. 
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

- **creates new content** — text, images, code, audio, video — rather than only classifying or predicting. It learns the *underlying patterns and distribution* of training data and samples from it to produce novel outputs.
- **Human-in-the-loop is required** — outputs need review for facts, tone, and safety.
- **prompt** — which is exactly what the rest of this subject (Units 3–4) teaches.
- **What is Generative AI?** — AI that creates new content (text/image/code/audio/video) by learning patterns in training data.
- **Text generation vs image generation tool example?** — ChatGPT (text), DALL·E (image).
- **Why are repeated prompts not identical?** — LLMs sample from a probability distribution (temperature), so output varies.
- **What is a hallucination?** — A confident but factually wrong statement.
- **Which tool for analyzing an uploaded image?** — Gemini (multimodal).

> [!tip] Viva Prep
> Be ready to explain the *why* behind each step, not just the output.
