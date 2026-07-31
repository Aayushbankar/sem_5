---
title: "Unit 1 — Foundations of AI and Generative AI"
sidebar:
  order: 1
---

# UNIT 1 — Foundations of Artificial Intelligence & Generative AI 🤖

> **Artificial Intelligence with Prompt Engineering (DI05016011)** · **6 hrs · 15% weightage**
> **Covers syllabus sections:** 1.1 Introduction to AI · 1.2 Types of AI · 1.3 Applications of AI · 1.4 Introduction to Generative AI · 1.5 Generative AI tools · 1.6 Basics of NLP
> **Related practicals:** [P01](./P01%20—%20Genai%20Tools%20Tasks%20And%20Domains.md), [P02](./P02%20—%20Sentiment%20Analysis%20Text%20Classification.md)

---

## 🧭 Chapter Roadmap

This unit answers two questions the whole subject depends on: *"What is AI and where did it come from?"* and *"What is Generative AI, and what can it do?"*. Everything later — LLMs (Unit 2), prompting (Units 3–4), and applications (Unit 5) — is a build-up from here. It is the highest "definition-heavy" unit: lots of 2–3 mark definitions.

| # | Concept | Exam importance | Code demo |
|---|---------|-----------------|-----------|
| 1.1 | Definition & history of AI | ★★★ | — |
| 1.2 | AI vs ML vs Deep Learning | ★★★★ | — |
| 1.3 | Narrow AI vs General AI | ★★★ | — |
| 1.4 | Applications of AI (daily life, education, healthcare, cybersecurity) | ★★★★ | — |
| 1.5 | Concept & types of Generative AI | ★★★★★ | P01 |
| 1.6 | Generative AI tools (ChatGPT, Gemini, DALL·E) | ★★★★ | P01 |
| 1.7 | Text / Image / Code generation | ★★★★ | P01 |
| 1.8 | NLP basics & its role in chatbots/LLMs | ★★★★ | P02 |

### Learning outcomes — after this unit you can:
1. Define AI and narrate its history (from Turing to today's GenAI boom).
2. Distinguish **AI → ML → Deep Learning** and **Narrow → General AI** in one table each.
3. Give 2–3 real examples of AI per domain: daily life, education, healthcare, cybersecurity.
4. Explain what **Generative AI** is and classify GenAI systems by output type.
5. Name the big GenAI tools and what each does best (ChatGPT, Gemini, DALL·E).
6. Explain **NLP** and its role in chatbots and LLMs.
7. Relate this unit to the practicals: P01 (task-type matrix) and P02 (sentiment analysis/NLP).

---

## 1.1 Introduction to Artificial Intelligence

### 1.1.1 Definition and History of AI ⭐

**Definition (exam-ready):** Artificial Intelligence is the branch of computer science concerned with building **machines/systems that can perform tasks that normally require human intelligence** — such as understanding language, recognizing images, making decisions, and solving problems. Alternatively: "AI is the study and design of intelligent agents that perceive their environment and take actions to achieve goals."

**The history in 6 lines (memorize the dates + names):**

```
1950 Turing's "Computing Machinery and Intelligence" ──► Turing Test proposed
1956 Dartmouth workshop (McCarthy) ──► the term "Artificial Intelligence" coined
1950s–70s Symbolic AI ──► rule-based systems, expert systems (MYCIN, 1970s)
1980s–90s ML + neural nets return ──► backpropagation popularized; Deep Blue beats Kasparov (1997)
2010s Deep Learning era ──► AlexNet (2012), AlphaGo (2016), GPT-1 (2018)
2020s Generative AI era ──► GPT-3 (2020), ChatGPT (2022), Gemini, Claude, Sora
```

| Era | Key event | Significance |
|---|---|---|
| **1950** | Turing proposes the **Turing Test** | First test of machine "intelligence" |
| **1956** | Dartmouth workshop | Birth of AI as a field |
| **1970s** | Expert systems (MYCIN) | Rule-based AI reaches real use |
| **1997** | Deep Blue beats Kasparov | Narrow AI beats a world champion in chess |
| **2012** | AlexNet wins ImageNet | Deep learning breakthrough (GPUs + big data) |
| **2020–2022** | GPT-3 → ChatGPT | Generative AI goes mainstream |

> [!tip] Beyond the textbook
> AI has had two "winters" — periods (1974–80, 1987–93) when funding and hype collapsed because the promised results didn't arrive. The current era avoids this partly because LLMs are genuinely useful and commercially valuable, not just demos.

### 1.1.2 AI vs Machine Learning vs Deep Learning ⭐⭐

The three are **nested** — ML is a subset of AI; Deep Learning is a subset of ML.

```mermaid
graph TD
    subgraph AI["Artificial Intelligence (Umbrella Domain)"]
        RAI["Rule-Based & Symbolic AI<br/>• Expert Systems (MYCIN)<br/>• Search Trees (A*, Minimax)<br/>• Knowledge Graphs"]
        ML["Machine Learning (Data-Driven Paradigm)<br/>Learns mapping f: X → Y from data"]
    end

    subgraph MLSub["Machine Learning Subfields"]
        CML["Classical Machine Learning<br/>• Feature Engineering required<br/>• SVMs, Decision Trees, Random Forests"]
        DL["Deep Learning (Hierarchical Representation)<br/>Multi-layer Neural Networks (Automatic Feature Extraction)"]
    end

    subgraph DLSub["Deep Learning Architectures"]
        DiscDL["Discriminative Models P(Y|X)<br/>• ResNet (Computer Vision)<br/>• BERT (Text Classification)"]
        GenAI["Generative AI P(X) / P(X,Y)<br/>Learns data distribution density"]
    end

    subgraph GenAISub["Generative AI Paradigms"]
        AR["Auto-Regressive Transformers<br/>• Next-Token Prediction<br/>• GPT-4, Gemini, LLaMA"]
        Diff["Score-Based Diffusion<br/>• Latent Noise Denoising<br/>• Stable Diffusion, DALL·E 3"]
    end

    AI --> ML
    ML --> CML
    ML --> DL
    DL --> DiscDL
    DL --> GenAI
    GenAI --> AR
    GenAI --> Diff

    classDef aiStyle fill:#1e1e2e,stroke:#89b4fa,stroke-width:2px,color:#cdd6f4;
    classDef mlStyle fill:#181825,stroke:#a6e3a1,stroke-width:2px,color:#cdd6f4;
    classDef dlStyle fill:#313244,stroke:#fab387,stroke-width:2px,color:#cdd6f4;
    classDef genStyle fill:#45475a,stroke:#f38ba8,stroke-width:2px,color:#cdd6f4;

    class AI,RAI,ML aiStyle;
    class CML,DL mlStyle;
    class DiscDL,GenAI dlStyle;
    class AR,Diff genStyle;
```

| Criterion | AI | Machine Learning | Deep Learning |
|---|---|---|---|
| **Definition** | Making machines intelligent | Computers learn from data | Neural networks with many layers |
| **How it "knows"** | Rules / search / logic / learned | Patterns in data | Hierarchical features (edges → shapes → objects) |
| **Human effort** | Hand-craft rules | Feature engineering still needed | Features learned automatically |
| **Data needed** | Little | Moderate | Very large |
| **Example** | Chess engine with rules, Siri, chatbots | Spam filter, credit scoring | Image recognition, ChatGPT |
| **Relation** | Umbrella term | Subset of AI | Subset of ML |

> [!warning] Exam trap
> "Is a spam filter AI?" — Yes (it is ML-based AI). "Is ChatGPT deep learning?" — Yes (an LLM is a deep neural network). "Is a decision-tree spam filter deep learning?" — **No** — it's ML but not deep learning.

## 1.2 Types of AI ⭐

### 1.2.1 Narrow AI vs General AI

| Criterion | Narrow (Weak) AI | General (Strong) AI |
|---|---|---|
| **Scope** | One specific task | Any intellectual task a human can do |
| **Learning** | Trained for that task only | Learns and transfers across tasks |
| **Today?** | ✅ Everywhere (all current AI) | ❌ Not yet achieved (research goal) |
| **Awareness** | None — no consciousness | Hypothetical self-aware systems |
| **Examples** | Chess engine, spam filter, ChatGPT, face recognition | Human-level robot assistants in sci-fi (JARVIS, HAL) |
| **Memory aid** | "Narrow = one job" | "General = like a person" |

> [!tip] Beyond the textbook
> some books add a third label, **Artificial Superintelligence (ASI)** — intelligence far beyond the best human in every domain. A common exam phrase: "current GenAI systems like ChatGPT are *narrow* AI, despite looking broad, because they have no understanding, no world model, and can't do arbitrary tasks."

## 1.3 Applications of AI

A guaranteed "name applications" question — know **2–3 per domain** with one concrete example each.

| Domain | Applications | Concrete example |
|---|---|---|
| **Daily life** | Virtual assistants, recommendation systems, smart keyboards, maps, smart home | Siri/Alexa; YouTube/Netflix recommendations; Google Maps traffic prediction |
| **Education** | Adaptive learning, auto-grading, doubt-solving chatbots, study assistants | Duolingo adapting difficulty; AI that generates quizzes (P12!) |
| **Healthcare** | Medical imaging analysis, disease prediction, drug discovery, clinical support | AI screening X-rays/CT for tuberculosis; predicting diabetic risk |
| **Cybersecurity** | Intrusion detection, phishing detection, malware analysis, log analysis | AI flagging a phishing email; anomaly detection in network traffic |

> [!warning] Exam note
> "AI in healthcare" — be careful to say AI is a **decision-support** tool, not a replacement for doctors; it can be biased or wrong, so humans review.

## 1.4 Introduction to Generative AI ⭐⭐

### 1.4.1 Concept of Generative AI

**Definition (exam-ready):** Generative AI is a branch of AI that **creates new content** — text, images, code, audio, video — rather than just classifying or predicting. It learns the **statistical patterns and distribution of training data**, then **samples** from that learned distribution to produce novel outputs.

```
Traditional AI:   input ──► MODEL ──► label/decision   (e.g., spam/not-spam)
Generative AI:    prompt ──► MODEL ──► new content      (e.g., a new essay, image, song)
```

**Key properties:**
- **Generative** = produces something *new*, not a stored copy.
- **Learns patterns** from massive data (text, images, audio).
- **Probabilistic** — the same prompt can yield different outputs (this is central to Units 2–3).
- Powered today mostly by **foundation models** — huge neural networks pre-trained on internet-scale data and fine-tuned/adjusted for tasks.

### 1.4.2 Types of Generative AI Systems ⭐

| Type | Output produced | Example models/tools |
|---|---|---|
| **Text generation (LLMs)** | Sentences, essays, code, summaries | ChatGPT, Gemini, Claude, LLaMA |
| **Image generation** | New images from a text description | DALL·E, Midjourney, Stable Diffusion |
| **Code generation** | Source code from a description | GitHub Copilot, Codeium, ChatGPT |
| **Audio generation** | Speech, music, voices | ElevenLabs (voice), Suno (music) |
| **Video generation** | Short video clips | Runway, Pika, Sora |
| **Multimodal** | Mixes text + image + audio understanding/generation | Gemini, GPT-4o |

### 1.4.3 Text, Image, and Code Generation ⭐

| Task | How it works (conceptual) | Example prompt → output |
|---|---|---|
| **Text generation** | LLM predicts the next token given the prompt | "Write a haiku about rain" → 5-7-5 poem |
| **Image generation** | Diffusion models start from noise and iteratively denoise toward the text description | "A cat astronaut, watercolor" → image |
| **Code generation** | LLM trained partly on code predicts code tokens | "Python function to check if a number is prime" → function |

> [!tip] Beyond the textbook
> most text-to-image models today are **diffusion models** (trained by progressively adding noise to images, then learning to reverse it), while LLMs are **transformer** models predicting tokens (Unit 2). "Two model families, one word: generative."

## 1.5 Generative AI Tools ⭐

| Tool | Company | Strength | Notes for exams |
|---|---|---|---|
| **ChatGPT** | OpenAI | General-purpose chatbot, excellent reasoning & code | Released Nov 2022; powered by GPT models |
| **Google Gemini** | Google DeepMind | **Multimodal** (text + image + audio + video), integrated with Google Workspace | Successor to Bard |
| **DALL·E** | OpenAI | Text-to-**image** generation | Named after surrealist painter Salvador Dalí + WALL·E |

**Choosing a tool (practical mindset — from P01):**
- Code & reasoning → **ChatGPT**.
- Multimodal input (analyze an uploaded image) → **Gemini**.
- Generating an image → **DALL·E / Midjourney / Stable Diffusion**.
- Long, nuanced writing → **Claude**.

> [!warning] Exam note
> "Name 3 GenAI tools" — be able to say who makes each and one signature capability. Also: tools are *complements*, not replacements — outputs need human review.

## 1.6 Basics of Natural Language Processing ⭐

### 1.6.1 Concept of NLP

**Definition (exam-ready):** Natural Language Processing (NLP) is the branch of AI that enables computers to **understand, interpret, and generate human language**.

**Core NLP tasks:**
| Task | What it does | Example |
|---|---|---|
| **Tokenization** | Split text into tokens (words/subwords) | "AI is fun" → `["AI", "is", "fun"]` |
| **Sentiment analysis** | Detect emotional tone | "Great product" → positive |
| **Text classification** | Assign a category | Email → spam/ham |
| **Named-entity recognition** | Find names, dates, places | "Riya met Aarav in Ahmedabad" |
| **Machine translation** | Convert between languages | English ↔ Gujarati |
| **Text generation / summarization** | Produce/shorten text | Summarize a news article |

**NLP pipeline (simplified):** raw text → clean → tokenize → represent as numbers (embeddings) → model → output.

### 1.6.2 Role of NLP in Chatbots and LLMs ⭐

```mermaid
graph LR
    subgraph InputStage["(1) Text Processing & Tokenization"]
        Raw["Raw User Text Input<br/>'AI is transforming modern code'"] --> BPE["Byte-Pair Encoding (BPE)<br/>Subword Tokenizer"]
        BPE --> Tokens["Token ID Sequence<br/>[9552, 374, 14073, ...]"]
    end

    subgraph VectorStage["(2) Semantic Vector Space"]
        Tokens --> LookUp["Token Embedding Matrix<br/>E ∈ ℝ^{|V| × d_model}"]
        LookUp --> PosEnc["Positional Encoding Addition<br/>E_tok + PE(pos)"]
    end

    subgraph ModelStage["(3) Deep Transformer Architecture"]
        PosEnc --> MHA["Multi-Head Self-Attention<br/>Q, K, V Projections"]
        MHA --> FFN["Feed-Forward Networks & LayerNorm"]
        FFN --> ContextVec["Contextual Hidden Vectors h_T"]
    end

    subgraph DecodingStage["(4) Probability Decoding"]
        ContextVec --> LinearHead["Vocab Projection Head W_v"]
        LinearHead --> Softmax["Softmax Layer P(x_t | x_<t)"]
        Softmax --> Sampling["Sampling Strategy<br/>(Temperature / Top-p)"]
        Sampling --> Detok["Detokenization"] --> Response["Final Generated Response"]
    end

    style InputStage fill:#1e1e2e,stroke:#89b4fa;
    style VectorStage fill:#181825,stroke:#a6e3a1;
    style ModelStage fill:#313244,stroke:#fab387;
    style DecodingStage fill:#45475a,stroke:#f38ba8;
```

- **Chatbots:** NLP lets the bot understand what the user wrote (parse, intent) and produce a natural reply. Rule-based bots (old) matched keywords; modern LLM chatbots *generate* replies.
- **LLMs:** NLP is the *front end* of an LLM — tokenization + embeddings convert language into numbers the network can process; the model's output is converted back to text.
- In short: **NLP is the bridge between human language and machine math** — the same bridge P02's practical walks across (tokenize → represent → classify).

---

## 🧠 Deep-Dive Topics

### Deep Dive A: The "is it AI?" decision tree
```
Does it mimic human intelligence?  ──No──► it's just software
   │Yes
   Does it learn from data? ──No──► Rule-based AI (expert systems, search bots)
   │Yes
   Does it use multi-layer neural networks? ──No──► Classical ML (trees, SVMs)
   │Yes
   Deep Learning ── generates new content? ──Yes──► Generative AI (LLMs, diffusion)
```
Use this to answer "classify this system" viva questions with confidence.

### Deep Dive B: Why Generative AI is probabilistic (the seed of Unit 2)
A generative model does **not** memorize answers; it assigns probabilities to possible next tokens/images and *samples* from them. Consequences: (1) same prompt → different outputs; (2) confident-but-wrong outputs (hallucination) are intrinsic, not bugs; (3) prompt engineering works because better instructions narrow the probability distribution. This single idea explains Units 2, 3, and 4.

### Deep Dive C: Generative vs Discriminative, in one sentence
- **Discriminative model:** learns the boundary between classes → *"Given input X, the label is Y."* (spam filter)
- **Generative model:** learns how the data is produced → *"Given the pattern I learned, here is new X."* (image generator)
A one-sentence exam answer: *"Discriminative models classify; generative models create."*

---

## 🚀 Beyond the Textbook (what most classes won't tell you)

1. **ChatGPT did not invent LLMs.** GPT-1/2 (2018–19) and Google's Transformer paper (2017) came first; ChatGPT was the *product* that made them usable by everyone. Exams reward the history timeline over brand worship.
2. **"Generative" ≠ "original".** A GenAI model samples from patterns in its training data — it can produce text/images that *look* original but are statistical recombinations. This is why copyright and deep-fake debates exist.
3. **Narrow AI is a spectrum, not a line.** A model like ChatGPT looks broad, but it still fails basic real-world reasoning — it has no body, no senses, and no world model. "General AI" remains a research goal, not a product.
4. **The current era is "capability without understanding."** LLMs pass many tests while being deeply unreliable on facts they haven't memorized. That's exactly why the rest of this subject teaches *prompting* (control the output) and *RAG* (ground the output).
5. **Memorization aid for history:** **"Turing 1950, Dartmouth 1956, Deep Blue 1997, AlexNet 2012, ChatGPT 2022"** — five dates = the whole story.
6. **GenAI tool accuracy varies by task type** (P01 finding): code generation is remarkably reliable; image generation needs many iterations; factual answers must be verified. Never quote a tool's answer as truth in an exam answer unless you'd verify it.

---

## 🎯 High-Yield Exam Topics (likely GTU-style — no PYQ papers exist yet)

> This subject is new for 2026-27, so there are no previous papers to map. Below are the **questions most likely to appear**, written in GTU style, with mark hints.

1. **Define Artificial Intelligence.** (3)
2. **State the difference between AI, Machine Learning, and Deep Learning with examples.** (4)
3. **Write a short note on the history of AI.** (4)
4. **Distinguish between Narrow AI and General AI.** (3/4)
5. **Explain any four applications of AI (daily life, education, healthcare, cybersecurity).** (7)
6. **What is Generative AI? Explain its types.** (4/7)
7. **Explain text generation, image generation, and code generation with examples.** (4)
8. **Write a short note on: ChatGPT, Google Gemini, and DALL·E.** (7)
9. **What is NLP? List the tasks performed by NLP.** (3/4)
10. **Explain the role of NLP in chatbots and LLMs.** (4)
11. **Short note: Diffusion models vs LLMs.** (4)
12. **Explain why Generative AI outputs can differ each time.** (3)

### ✅ Solved model answers (exam style)

**Q. (7 marks) What is Generative AI? Explain its types.**
> Generative AI is a branch of artificial intelligence that **creates new content** — text, images, code, audio, video — by learning the statistical patterns of its training data and then **sampling** from that learned distribution. Unlike traditional (discriminative) AI, which classifies or predicts a label from an input, generative systems produce *novel outputs* from a prompt. Types: **(1) Text generation (LLMs)** — models such as ChatGPT, Claude, and Gemini generate coherent sentences, essays, and summaries by predicting the next token. **(2) Image generation** — diffusion-based models such as DALL·E, Midjourney, and Stable Diffusion create images from text descriptions. **(3) Code generation** — tools like GitHub Copilot and ChatGPT write source code from a natural-language specification. **(4) Audio generation** — tools such as ElevenLabs and Suno synthesize speech and music. **(5) Video generation** — tools such as Runway and Sora produce short video clips. **(6) Multimodal systems** — such as Gemini and GPT-4o, which understand and generate multiple modalities together. Example: the prompt "a cat astronaut, watercolor" produces a new image; the prompt "write a haiku about rain" produces a new poem.

**Q. (4 marks) Distinguish between AI, Machine Learning, and Deep Learning.**
> AI is the umbrella field of building machines that mimic human intelligence (perception, language, reasoning, problem-solving). **Machine Learning (ML)** is a subset of AI in which systems **learn patterns from data** instead of following hand-written rules — e.g., a spam filter trained on labelled emails. **Deep Learning (DL)** is a subset of ML that uses **multi-layer neural networks** to automatically learn hierarchical features, requiring large datasets and high compute — e.g., image recognition and ChatGPT. The three are nested: every DL system is ML, every ML system is AI, but not vice versa. Example: a rule-based chess program is AI but not ML; a decision-tree credit scorer is ML but not DL; a neural-network image classifier is DL.

**Q. (3 marks) Define AI. Give the significance of the Turing Test and the Dartmouth workshop.**
> **AI** is the branch of computer science concerned with building systems that perform tasks normally requiring human intelligence — understanding language, recognizing images, making decisions, solving problems. The **Turing Test**, proposed by Alan Turing in 1950, was the first practical proposal for judging machine intelligence: a machine is "intelligent" if a human interrogator cannot reliably tell it apart from a human in a conversation. The **Dartmouth workshop (1956)**, organized by John McCarthy and colleagues, coined the term "Artificial Intelligence" and formally established AI as a research field.

---

## ✍️ Practice Problems (self-test — answers upside-down)

1. Order the timeline: ChatGPT, AlexNet, Deep Blue, Dartmouth workshop, Turing Test.
2. A system uses a fixed set of if-then rules to answer customer queries. Is it AI? Is it ML? Is it DL?
3. Give one example each of text, image, and code generation by GenAI tools.
4. Why is ChatGPT called "Narrow AI" despite doing many tasks?
5. List the six NLP tasks from §1.6 and give an example of each.
6. Name the tool you'd choose to (a) analyze an uploaded X-ray image, (b) generate a logo, (c) fix a buggy Python function. Justify.

<details>
<summary>📌 Model solutions</summary>

1. Turing Test (1950) → Dartmouth (1956) → Deep Blue (1997) → AlexNet (2012) → ChatGPT (2022).
2. It is **AI** (mimics human answering) but **not ML** (no learning from data) and therefore **not DL**.
3. Text: "Write a haiku about rain" → poem (ChatGPT). Image: "a cat astronaut, watercolor" → image (DALL·E). Code: "Python function to check if a number is prime" → function (Copilot/ChatGPT).
4. Because it has **no general understanding** — it is trained for language tasks, has no world model, no senses, and fails on arbitrary tasks; "narrow" refers to task scope and lack of general reasoning, not how many tasks a product offers.
5. Tokenization (split into words), sentiment analysis (positive/negative), text classification (spam/ham), named-entity recognition (find "Riya", "Ahmedabad"), machine translation (EN↔GU), text generation/summarization (shorten an article).
6. (a) **Gemini** (multimodal — reads images), (b) **DALL·E** (text-to-image), (c) **ChatGPT/Copilot** (strongest at code).
</details>

---

## 📖 Glossary of Key Terms

| Term | Definition |
|---|---|
| **Artificial Intelligence** | Building machines that perform tasks requiring human intelligence |
| **Turing Test** | Conversational test of machine intelligence (Turing, 1950) |
| **Dartmouth workshop** | 1956 event that founded AI as a field |
| **Machine Learning** | Learning patterns from data instead of hand-written rules |
| **Deep Learning** | Multi-layer neural networks that learn features automatically |
| **Narrow AI** | AI limited to one task (all current systems) |
| **General AI** | Hypothetical AI matching human intellectual ability |
| **Generative AI** | AI that creates new content by sampling a learned distribution |
| **Foundation model** | Large pre-trained model adapted to many tasks |
| **Diffusion model** | Image-generating model that reverses added noise |
| **LLM** | Large Language Model — next-token predicting text model |
| **ChatGPT** | OpenAI's general-purpose chatbot |
| **Gemini** | Google's multimodal GenAI model family |
| **DALL·E** | OpenAI's text-to-image model |
| **NLP** | Branch of AI for understanding/generating human language |
| **Tokenization** | Splitting text into tokens (words/subwords) |
| **Sentiment analysis** | Detecting the emotional tone of text |
| **Embedding** | Vector of numbers representing a word/text's meaning |

---

## 🔗 Curated Resources (per concept)

**AI basics & history**
- *Artificial Intelligence: A Modern Approach* — Russell & Norvig (GTU-suggested book)
- AI history timeline: https://en.wikipedia.org/wiki/History_of_artificial_intelligence
- Turing's 1950 paper: https://academic.oup.com/mind/article/LIX/236/433/986238

**Generative AI**
- OpenAI "What is Generative AI?" explainers: https://openai.com
- DALL·E product page: https://openai.com/dall-e
- Google Gemini: https://gemini.google.com · developers: https://ai.google.dev
- DAIR.AI Prompt Engineering Guide: https://www.promptingguide.ai

**NLP**
- NLTK book (free, GTU-suggested): https://www.nltk.org/book/
- TextBlob docs: https://textblob.readthedocs.io
- *Natural Language Processing with Python* — Bird, Klein & Loper (GTU book)

**Practical tie-ins**
- [P01](./P01%20—%20Genai%20Tools%20Tasks%20And%20Domains.md) — GenAI task-type matrix + tool comparison
- [P02](./P02%20—%20Sentiment%20Analysis%20Text%20Classification.md) — NLP in code: sentiment + classification

---

## 🎥 Video Study Guide (YouTube)

> Don't like reading? Me neither. This is your **structured video path** for the whole unit — better than the syllabus because it tells you *exactly what to search* and *what to watch first*, in a sensible order. Everything below is search keywords (they never rot like links do) + channels you can trust.

### 🧑‍🎓 Step 0 — Pick your learning style

| Style | You learn best by | Your path through this unit |
|---|---|---|
| 🎧 **Listener** | short, clear explainers | Watch 1 explainer per topic from the table below (3–8 min each) |
| 🛠️ **Builder** | writing code yourself | Watch the NLP/Python intro video → then run [P02](./P02%20—%20Sentiment%20Analysis%20Text%20Classification.md) code |
| 🔧 **Tinkerer** | experimenting & demos | Open ChatGPT/Gemini and re-run the P01 task matrix for yourself |
| 🧠 **Deep Diver** | full theory, "why" | Watch the full AI-intro playlists at the bottom (university-level depth) |
| 🧭 **Explorer** | breadth & curiosity | Watch the "how generative AI works" explainers first, then follow your curiosity |
| 🎓 **Academic** | exam marks | Watch the GTU-style/revision videos, then grind the High-Yield Topics above |

### 🎬 Step 1 — Watch by topic (search these on YouTube)

| Topic | YouTube search keywords (copy-paste ready) | Best channels | Style served |
|---|---|---|---|
| What is AI (mental model) | `artificial intelligence explained` · `what is ai in 5 minutes` · `introduction to artificial intelligence` | freeCodeCamp, Simplilearn, IBM Technology | 🧭 Explorer |
| History of AI | `history of artificial intelligence timeline` · `ai winters explained` · `turing test explained` | Computerphile, IEEE, The Royal Institution | 🎧 + 🧠 |
| AI vs ML vs Deep Learning | `ai vs machine learning vs deep learning` · `machine learning explained simply` | Simplilearn, IBM Technology, 3Blue1Brown (neural nets) | 🎓 Academic |
| Narrow vs General AI | `narrow ai vs general ai vs superintelligence` · `what is agi` | Two Minute Papers, ColdFusion | 🧭 + 🎧 |
| Applications of AI | `ai in daily life examples` · `ai in healthcare` · `ai in cybersecurity` | IBM Technology, TED-Ed, freeCodeCamp | 🧭 Explorer |
| Generative AI explained | `what is generative ai` · `generative ai explained` · `diffusion models explained` | IBM Technology, Two Minute Papers, Andrej Karpathy | 🧠 Deep Diver |
| Text-to-image (diffusion) | `stable diffusion explained` · `how dall-e works` · `diffusion models from scratch` | Two Minute Papers, Andrej Karpathy, Computerphile | 🧠 + 🛠️ |
| LLMs / ChatGPT basics | `how chatgpt works for beginners` · `large language models explained` | Andrej Karpathy, 3Blue1Brown, Fireship | 🧠 Deep Diver |
| NLP fundamentals | `natural language processing explained` · `nlp tutorial for beginners` · `textblob sentiment analysis python` | freeCodeCamp, DeepLearning.AI, Tech With Tim | 🛠️ Builder |
| AI tools overview | `chatgpt vs gemini vs claude` · `best ai tools 2026 comparison` | Fireship, The AI Advantage | 🔧 Tinkerer |
| Whole-unit revision | `artificial intelligence full course diploma` · `ai fundamentals one shot revision` · `generative ai crash course` | freeCodeCamp, Gate Smashers, Neso Academy | 🎓 Academic |

### 🎬 Step 2 — Full playlists (for Deep Divers & Academics)

1. **"freeCodeCamp — AI / Machine Learning for Beginners full course"** — structured, covers AI→ML→DL and hands-on Python; ideal companion for this unit.
2. **"Andrej Karpathy — Neural Networks: Zero to Hero"** — the deepest intuition for how deep learning actually works; watch the first 2 videos here.
3. **"DeepLearning.AI — short courses on generative AI & prompt engineering"** (Andrew Ng) — short, credible, directly relevant to the rest of this subject.

### 🎬 Step 3 — Proof you got it (5 min)

- Can you explain the AI→ML→DL nesting to a friend in two sentences?
- Open any GenAI tool and generate one text, one image, and one code output (the P01 trio) — did each behave differently?
- Run [P02](./P02%20—%20Sentiment%20Analysis%20Text%20Classification.md) and predict which review is positive before the script prints it.

---

*Next: [UNIT 2 — Basics of Large Language Models](./Unit%202%20—%20Basics%20of%20Large%20Language%20Models.md)*

---



---

## 📖 Historical Context & Motivation

For decades, artificial intelligence was dominated by the **symbolic paradigm** (often termed "Good Old-Fashioned AI" or GOFAI). Systems such as MYCIN (1970s) and expert rule-engines operated on hand-crafted formal logic, production rules ($\text{IF } \text{condition} \text{ THEN } \text{action}$), and deterministic search trees over discrete state spaces. While symbolic AI excelled at constrained formal domains like chess or axiomatic logic, it succumbed to the **Brittleness Obstacle** and the **Curse of Dimensionality**. Human intelligence relies on implicit perceptual knowledge—recognizing a handwritten digit, interpreting semantic ambiguity, or synthesizing natural language—which defies complete manual rule specification.

The transition to **statistical machine learning** swapped manual rule-writing for optimization over parameterized function approximators. Instead of hardcoding rules, algorithms learned mapping functions $f_\theta: \mathcal{X} \to \mathcal{Y}$ from labeled training data. However, classical ML (e.g., Support Vector Machines, Random Forests) required labor-intensive **feature engineering**, where domain experts manually extracted vector representations. 

The **Deep Learning Revolution (2012–present)**, triggered by GPU-accelerated training of AlexNet on ImageNet, eliminated manual feature engineering by learning hierarchical representations directly from raw perceptual signals. Yet, early deep learning models were fundamentally **discriminative**: given an input $X$, they calculated conditional class distributions $P(Y \mid X)$. 

The emergence of **Generative AI** represents a structural paradigm shift from modeling conditional boundaries to modeling joint probability distributions $P(X, Y)$ or marginal distributions $P(X)$ over complex, high-dimensional manifolds (such as text, code, or images). By sampling from these learned probability density functions, generative models synthesize entirely novel data artifacts that preserve the underlying statistical structure of natural human distribution, establishing the foundation for modern autonomous systems and Large Language Models.

---

## 🔬 Deep Dive: System Architecture & Mathematical Foundations

### 1. Discriminative vs. Generative Latent Density Estimation
Mathematically, a discriminative model estimates the posterior distribution $P(Y \mid X)$, partitioning the input space $\mathcal{X}$ into decision regions separated by boundaries defined by parameters $\theta$. A generative model, conversely, models the true data-generating distribution $p_{\text{data}}(X)$. 

For continuous high-dimensional data (e.g., images), exact density estimation is intractable. Generative models construct a mapping function $g_\theta: \mathcal{Z} \to \mathcal{X}$ that transforms a simple prior distribution $p(Z)$ (e.g., isotropic Gaussian $\mathcal{N}(\mathbf{0}, \mathbf{I})$) over a low-dimensional latent space $\mathcal{Z}$ into a complex distribution $p_\theta(X)$ over the high-dimensional data manifold $\mathcal{X}$.

```mermaid
graph TD
    subgraph ParadigmA["Paradigm A: Auto-Regressive Discrete Generation (LLMs)"]
        A_Input["Discrete Token Sequence X = (x_1, ..., x_t)"] --> A_Chain["Chain Rule Factorization:<br/>P(X) = ∏ P(x_t | x_<t)"]
        A_Chain --> A_Dec["Transformer Decoder Stack<br/>Hidden State h_t = Decoder(x_<t)"]
        A_Dec --> A_Softmax["Logits Vector z_t → Softmax P(x_t | x_<t)"]
        A_Softmax --> A_Sample["Token Sampling & Feedback Loop"]
        A_Sample -->|Append Next Token| A_Input
    end

    subgraph ParadigmB["Paradigm B: Continuous Score-Based Diffusion Models (Images)"]
        B_Forward["Forward Process q(x_t | x_0):<br/>Iterative Gaussian Noise Addition"] 
        B_Forward --> B_Noise["Latent Noise Space x_T ~ N(0, I)"]
        B_Noise --> B_Reverse["Reverse Denoising Process:<br/>Time-Conditioned U-Net ε_θ(x_t, t)"]
        B_Reverse --> B_Cond["Cross-Attention Guidance<br/>(Text Condition Embedding c via CLIP)"]
        B_Cond --> B_Denoise["Iterative Denoising Steps<br/>x_{t-1} = μ_θ(x_t, t) + σ_t z"]
        B_Denoise --> B_Output["Synthesized Continuous Output x_0"]
    end

    style ParadigmA fill:#1e1e2e,stroke:#89b4fa,stroke-width:2px;
    style ParadigmB fill:#181825,stroke:#f38ba8,stroke-width:2px;
```

### 2. Deep Generative Architectures: Auto-regressive Transformers vs. Score-Based Diffusion Models

Modern Generative AI is partitioned into two primary mathematical families based on data modality:

#### A. Auto-regressive Probability Factorization (Text & Discrete Sequences)
For discrete sequential data $X = (x_1, x_2, \dots, x_T)$, generative language models utilize the chain rule of probability to factorize the joint density into a product of conditional probabilities:
$$P(X; \theta) = \prod_{t=1}^{T} P(x_t \mid x_1, x_2, \dots, x_{t-1}; \theta)$$

Each conditional token distribution is parameterized via a Transformer decoder network:
$$\mathbf{h}_t = \text{TransformerDecoder}(x_1, \dots, x_{t-1})$$
$$P(x_t \mid x_{<t}) = \text{Softmax}\left(\mathbf{W}_{\text{vocab}} \mathbf{h}_t + \mathbf{b}\right)$$

Training minimizes the Negative Log-Likelihood (NLL) over corpus $\mathcal{D}$ via Empirical Risk Minimization:
$$\mathcal{L}_{\text{NLL}}(\theta) = -\sum_{i=1}^{|\mathcal{D}|} \sum_{t=1}^{T_i} \log P_\theta\left(x_{i,t} \mid x_{i,<t}\right)$$

#### B. Score-Based Continuous Diffusion Models (Images & Continuous Media)
For continuous data like images $x_0 \sim q(x)$, diffusion models formulate generation as the reverse process of a Stochastic Differential Equation (SDE). 

1. **Forward Stochastic Process (Denoising Diffusion Probabilistic Models - DDPM)**:
   Progressively degrades data by adding Gaussian noise over time steps $t \in [0, T]$ according to a variance schedule $\beta_1, \dots, \beta_T$:
   $$q(x_t \mid x_{t-1}) = \mathcal{N}\left(x_t; \sqrt{1 - \beta_t} x_{t-1}, \beta_t \mathbf{I}\right)$$
   Exploiting the reparameterization trick, any arbitrary step $x_t$ can be sampled in closed form given $x_0$:
   $$q(x_t \mid x_0) = \mathcal{N}\left(x_t; \sqrt{\bar{\alpha}_t} x_0, (1 - \bar{\alpha}_t) \mathbf{I}\right) \quad \text{where } \alpha_t = 1 - \beta_t, \; \bar{\alpha}_t = \prod_{s=1}^t \alpha_s$$

2. **Reverse Denoising Process**:
   A deep neural network (typically a Time-Conditioned U-Net with Cross-Attention) parameterizes $\epsilon_\theta(x_t, t)$ to predict the Gaussian noise added at step $t$. The objective minimizes the mean-squared error:
   $$\mathcal{L}_{\text{simple}}(\theta) = \mathbb{E}_{t, x_0, \epsilon}\left[ \left\| \epsilon - \epsilon_\theta\left( \sqrt{\bar{\alpha}_t} x_0 + \sqrt{1 - \bar{\alpha}_t} \epsilon, t \right) \right\|^2 \right]$$

Sampling starts from pure noise $x_T \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$ and iteratively denoises down to $x_0$, generating sharp, high-fidelity images conditioned on text embeddings (e.g., via CLIP text encoders).

---

## 🏢 Real-World Case Study: GitHub Copilot Enterprise Code Synthesis Pipeline

### Enterprise Code Completion & Telemetry Architecture
GitHub Copilot processes tens of billions of code completion queries daily across millions of active developer sessions. The system architecture does not simply query a raw LLM API; it operates an end-to-end continuous generative software engineering pipeline:

1. **Context Harvesting**: When a developer types in an IDE (e.g., VS Code), a local telemetry agent constructs a prompt payload containing active file context, open sibling tabs, import statements, and cursor positioning.
2. **Prompt Orchestration & Truncation**: Context is tokenized locally using Byte-Pair Encoding (BPE). Prompts exceeding the model's target context budget are dynamically trimmed using semantic relevance heuristics (AST-based extraction).
3. **Low-Latency Inference Pipeline**: Requests hit proxy routing clusters that dispatch to Triton Inference Servers backed by GPU clusters. Models employ **Speculative Decoding** (drafting candidate tokens with a lightweight 1B parameter model and verifying in parallel with a 70B model) to achieve sub-50ms latency per token.
4. **Post-Processing & Filtering**: Output streams are intercepted in real-time by compliance layers:
   - **Verbatim Code Matcher**: Queries a Bloom filter index of public GitHub repositories to flag and block code blocks >150 matching characters to avoid GPL license infringement.
   - **Secret Detection Engine**: Scans generated outputs via regular expressions and entropy checks to prevent echoing leaked AWS keys or passwords.

```mermaid
sequenceDiagram
    autonumber
    actor Dev as Developer (IDE)
    participant Telemetry as Local AST Harvester
    participant Proxy as Edge Proxy & Router
    participant SpecEngine as Speculative Decoding Cluster
    participant DraftModel as 1B Draft Model
    participant TargetModel as 70B Target Model
    participant Guard as Real-Time Compliance Guard
    participant Bloom as Repository Bloom Filter

    Dev->>Telemetry: User Types Code / Pauses Cursor
    Telemetry->>Telemetry: Extract AST Context, Open Tabs & Imports
    Telemetry->>Proxy: Send Tokenized Payload (BPE)
    Proxy->>SpecEngine: Route Request to GPU Cluster
    
    rect rgb(30, 30, 46)
        note over SpecEngine, TargetModel: Low-Latency Speculative Decoding Loop
        SpecEngine->>DraftModel: Draft K Candidate Tokens (Fast)
        DraftModel-->>SpecEngine: Candidate Tokens K
        SpecEngine->>TargetModel: Parallel Verification of K Tokens
        TargetModel-->>SpecEngine: Validated Tokens Vector
    end

    SpecEngine->>Guard: Stream Output Tokens
    
    rect rgb(40, 40, 60)
        note over Guard, Bloom: Security & Compliance Post-Processing
        Guard->>Bloom: Scan Code against Public Repos (>150 chars)
        Bloom-->>Guard: License Match Result (Clear/Blocked)
        Guard->>Guard: Regex & Entropy Scan for Secret Keys
    end

    alt Security & License Clear
        Guard-->>Dev: Render Ghost Text Suggestion (Inline)
    else Violation Detected
        Guard-->>Dev: Suppress Suggestion / Retrain Filter
    end
```

---

## 📝 End-of-Chapter Exercises

### Exercise 1: Probability Calculation in Generative Sequence Models
Given a vocabulary $\mathcal{V} = \{\text{"AI"}, \text{"is"}, \text{"powerful"}, \text{"fun"}\}$, suppose an auto-regressive model outputs the following unnormalized logit vectors $\mathbf{z}_t$ for successive sequence steps:
- Step 1 (given `<s>`): $\mathbf{z}_1 = [4.0, 1.0, 0.5, 0.5]$
- Step 2 (given `<s> AI`): $\mathbf{z}_2 = [0.2, 5.0, 1.0, 0.8]$
- Step 3 (given `<s> AI is`): $\mathbf{z}_3 = [0.1, 0.1, 3.0, 4.0]$

1. Compute the Softmax probability distributions $P(x_t \mid x_{<t})$ for each step $t \in \{1, 2, 3\}$.
2. Calculate the exact probability $P(X)$ of generating the specific sequence `"AI is fun"`.
3. Calculate the Cross-Entropy Loss $\mathcal{L}$ of this sequence if the ground truth text was `"AI is powerful"`.

### Exercise 2: Architectural Trade-off Design for Medical Diagnostics
Design an enterprise AI application architecture for an emergency room triage system. The system receives high-resolution chest X-rays, patient vital signs (numerical data), and historical medical narratives (unstructured text).
1. Classify which sub-components of this diagnostic system must be **Discriminative** (e.g., fracture classification, vital status prediction) and which should be **Generative** (e.g., discharge summary drafting, patient consultation translation).
2. Formulate a fail-safe hybrid system architecture diagram illustrating data flow, model boundaries, human-in-the-loop fallback triggers, and safety guardrails to mitigate generative hallucination in critical patient diagnostics.

### Exercise 3: Derivation of Diffusion Denoising Step
Given the forward diffusion equation $x_t = \sqrt{\bar{\alpha}_t} x_0 + \sqrt{1 - \bar{\alpha}_t} \epsilon$ where $\epsilon \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$:
1. Express the clean data sample $x_0$ explicitly as a function of noisy image $x_t$, time step parameter $\bar{\alpha}_t$, and predicted noise $\epsilon_\theta(x_t, t)$.
2. Explain physically why attempting to reverse the forward process directly without predicting noise $\epsilon_\theta$ or score functions $\nabla_{x_t} \log p(x_t)$ is computationally intractable for high-resolution $1024 \times 1024$ pixel images.

### Exercise 4: Vulnerability Analysis of Code Generation Pipelines
Analyze a scenario where an enterprise integrates an un-sanitized open-source Generative Code Model into its internal CI/CD pipeline.
1. Identify how a **Data Poisoning Attack** on public GitHub repositories could inject arbitrary backdoors (e.g., hardcoded SSH keys or vulnerable dependencies) into the model's next-token generation distribution.
2. Formulate a multi-stage automated verification pipeline (static analysis, dynamic sandboxing, AST parsing, and prompt restriction) to neutralize generated code vulnerabilities before deployment to production servers.

