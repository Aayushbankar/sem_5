# UNIT 5 — AI Application Development: Generative AI & Agentic AI 🚀

> **Artificial Intelligence with Prompt Engineering (DI05016011)** · **15 hrs · 30% weightage**
> **Covers syllabus sections:** 5.1 AI Tools for Productivity · 5.2 AI in Software Development · 5.3 AI for Debugging Code · 5.4 Introduction to AI APIs · 5.5 Developing AI Applications · 5.6 Introduction to Agentic AI · 5.7 Responsible AI
> **Related practicals:** [P09](../practicals/writeups/P09_ai_tools_for_software_development.md), [P10](../practicals/writeups/P10_ai_chatbot_api_python.md), [P11](../practicals/writeups/P11_document_qa_basic_rag.md), [P12](../practicals/writeups/P12_ai_study_assistant.md)

---

## 🧭 Chapter Roadmap

The **biggest unit in the paper (30%)** and the most application-heavy: productivity tools, AI-assisted development, APIs, four app types, agentic AI, and Responsible AI. Practicals P09–P12 (the capstone quarter of the 12) live here. Exams favour "explain the architecture of app X", "what is an AI agent", "OpenAI vs Gemini API", and ethical essays.

| # | Concept | Exam importance | Code demo |
|---|---------|-----------------|-----------|
| 5.1 | AI tools: emails, reports, presentations | ★★★ | — |
| 5.2 | AI in software dev: generate/explain/document | ★★★★ | P09 |
| 5.3 | AI for debugging | ★★★★ | P09 |
| 5.4 | Concept of APIs; OpenAI & Gemini APIs | ★★★★★ | P10 |
| 5.5 | Apps: chatbot, blog writer, summarizer, question generator | ★★★★★ | P10–P12 |
| 5.6 | Agentic AI: agents, autonomy, AutoGPT/CrewAI | ★★★★★ | P12 |
| 5.7 | Responsible AI: ethics, bias, privacy, risks | ★★★★ | — |

### Learning outcomes — after this unit you can:
1. Describe how AI tools speed up emails, reports, and presentations — with do's and don'ts.
2. Explain AI's roles in software development: generation, explanation, documentation, debugging.
3. Define an **API**, explain request/response, and compare **OpenAI vs Gemini** APIs.
4. Describe the architecture of an **AI chatbot, blog writer, document summarizer, and question generator**.
5. Explain **agentic AI**: what an agent is, autonomous execution, and examples (AutoGPT, CrewAI).
6. Discuss **Responsible AI**: ethics, bias/fairness, data privacy, and risks.
7. Apply everything in P09–P12 (including the capstone Study Assistant).

---

## 5.1 Using AI Tools for Productivity ⭐

| Task | How AI helps | Do | Don't |
|---|---|---|---|
| **Writing emails** | Drafts, tone-switching, summarizing threads | Give recipient, purpose, dates (P05 recipe); pick tone | Send without checking names/dates — the model invents them |
| **Generating reports** | Outlines, data summarization, formatting | Provide the real data; ask for bullet sections (chaining, P07) | Let it invent numbers |
| **Creating presentations** | Slide outlines, talking points, speaker notes | "Create 10 slides on X: one idea per slide, speaker notes each" | Generate without a story — ask for narrative first |

**The productivity rule:** AI drafts; the **human** verifies facts, adds judgment, and owns the result. Tools save 60–80% of drafting time, but only for writers who can review.

> ⚠️ **Exam note:** the syllabus lists these as "using AI tools for productivity" — answer with *which prompt makes each task work*, not just "AI writes it".

## 5.2 AI in Software Development ⭐⭐

### 5.2.1 Code Generation
- Prompt with signature + example + edge cases (Unit 4 §4.3.3).
- **Golden rule:** always **run and test** generated code — it can be wrong while looking perfect.

### 5.2.2 Code Explanation
```
Prompt: Explain this function line by line. Then state its time and space
        complexity, and suggest one improvement.
```
- Use for legacy/unknown code; verify the explanation with a manual trace.

### 5.2.3 Code Documentation
```
Prompt: Add a docstring, inline comments, and a README section for this
        function. Keep comments one line each.
```
- **Trap:** AI comments can describe what it *thinks* the code does — compare against actual behaviour.

## 5.3 AI for Debugging Code ⭐⭐

**Workflow (from P09's worked cases):**
```
1. REPRODUCE  : run the buggy code, capture the exact error/output
2. PASTE      : buggy code + error message + expected output
3. ASK WHY    : "why is this happening?" before "fix it"
4. FIX        : have it apply the fix
5. VERIFY     : run again, including edge cases
6. LEARN      : ask "what caused this bug class?" to build understanding
```

| Bug type | What AI finds | Classic fix |
|---|---|---|
| **append vs extend** in recursion | Sub-lists stay nested | `extend()` instead of `append()` |
| **Off-by-one** `range(1, n+1)` | Silently skips index 0 → wrong-but-crash-free | slice `values[:n]` + a clear `ValueError` |
| Type errors | `.upper()` on ints crashes | `str()` cast |

> 💡 **Beyond the textbook:** the *scariest* AI-debugging result is a fix that runs but is still wrong. That's why step 5 (verify) is non-negotiable, and why P09's code ships with `assert`-style checks.

## 5.4 Introduction to AI APIs ⭐⭐⭐

### 5.4.1 Concept of APIs ⭐

**Definition (exam-ready):** An API (Application Programming Interface) is a **defined set of rules/endpoints** that lets one program request data or computation from another over HTTP. In AI, the LLM provider hosts the model and exposes a REST API: you send a **JSON request** with your prompt and get a **JSON response** with generated text.

```mermaid
sequenceDiagram
    participant App as Your Python app
    participant API as LLM API (OpenAI/Gemini)
    App->>API: POST /chat/completions<br/>Authorization: Bearer KEY<br/>{model, messages}
    API-->>App: 200 OK<br/>{choices[0].message.content}
    App->>App: parse & print reply
```

| API concept | Meaning |
|---|---|
| **Endpoint** | The URL you POST to |
| **API key** | Secret credential in the `Authorization` header |
| **Model** | Which model serves the request |
| **Messages/roles** | `system` (behaviour) · `user` (input) · `assistant` (history) |
| **Parameters** | `temperature`, `max_tokens`, `top_p` |
| **Response** | JSON with generated content + usage (token counts) |

### 5.4.2 Examples: OpenAI API and Gemini API ⭐

| Aspect | OpenAI API | Gemini API |
|---|---|---|
| **Endpoint** | `https://api.openai.com/v1/chat/completions` | `https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent` |
| **Request body** | `{model, messages:[{role, content}]}` | `{contents:[{parts:[{text}]}]}` |
| **Model example** | `gpt-4o-mini`, `gpt-4o` | `gemini-2.0-flash`, `gemini-1.5-pro` |
| **Key header** | `Authorization: Bearer <key>` | `x-goog-api-key: <key>` (or Bearer) |
| **Response shape** | `choices[0].message.content` | `candidates[0].content.parts[0].text` |
| **Signature strength** | Ecosystem, tooling, function calling | Native **multimodal** input, Google ecosystem |

**Security rules (memorize):**
1. Store the key in an **environment variable** (`AI_API_KEY`), never in code.
2. Never commit keys to git (P10's script refuses to run without the env var).
3. Treat keys as passwords; rotate if leaked; scope keys to minimal permissions.

## 5.5 Developing AI Applications ⭐⭐⭐

The four syllabus apps share one architecture (P12 builds all of them):

```
User input → [optional retrieval] → prompt builder → LLM API (mock/real) → formatter → output
```

### 5.5.1 AI Chatbot
- **Loop:** read input → build messages → call API → print reply → repeat.
- **Extras:** system prompt for persona; history for multi-turn memory; safety filters.
- **P10 builds this** — including a `--mock` mode so it runs offline.

### 5.5.2 AI Blog Writer
- **Pipeline (chaining, Unit 4):** title → outline → section drafts → hook/CTA variants → SEO check.
- **Prompt:** audience + tone + structure + word count (P08's recipe).
- **Human-in-the-loop:** review each stage.

### 5.5.3 AI Document Summarizer
- **Short docs:** one summarization prompt (P08).
- **Long docs:** **RAG** approach — chunk, retrieve relevant parts, summarize each, merge (P11).

### 5.5.4 AI Question Generator
- **Prompt:** "Generate N MCQs on topic X: 4 options each, correct answer + one-line reason, GTU style."
- **Extras:** few-shot with one example MCQ to fix format; difficulty filter.
- **P12's quiz command** demonstrates the offline version.

**Production concerns for all four:** rate limiting, chat memory, cost control (token budgets), input/output safety, and **the mock-first pattern** — develop against `--mock`, swap in the real API for deployment.

## 5.6 Introduction to Agentic AI ⭐⭐⭐

### 5.6.1 Concept of AI Agents ⭐

**Definition (exam-ready):** an **AI agent** is a system in which an LLM **autonomously decides and executes multi-step actions** using tools (search, code execution, APIs), observes results, and iterates until the goal is complete. An agent = **LLM (reasoning) + tools (actions) + a loop (observe → decide → act)**.

| Ordinary LLM app | Agentic AI |
|---|---|
| One request → one response | Multiple steps with tool calls |
| Model chooses only *words* | Model chooses *actions* |
| User drives the conversation | Agent plans and drives |
| Static prompt → output | Loop until goal done |
| Example: chatbot | Example: AutoGPT researching and writing a report |

```mermaid
flowchart LR
    GOAL[Goal from user] --> LLM[LLM reasons<br/>Thinks: what next?]
    LLM --> TOOL[Tool: search / code / API / file]
    TOOL --> OBS[Observe result]
    OBS --> LLM
    LLM -->|goal reached| DONE[Final answer]
```

### 5.6.2 Autonomous Task Execution ⭐
The ReAct loop (Unit 4 §4.1.4) is the engine: **Thought → Action → Observation → repeat**. Autonomy is *bounded* — the agent still operates within a defined goal, tools, and safety limits; it is not free will.

### 5.6.3 Examples: AutoGPT, CrewAI ⭐
| Tool | What it is | One-liner |
|---|---|---|
| **AutoGPT** | An open-source autonomous agent | Give it a goal; it plans, searches, writes code, and iterates to finish it |
| **CrewAI** | A framework for **multi-agent** teams | Define *roles* (researcher, writer, reviewer) — agents collaborate like a crew |
| (LangChain/LangGraph) | Building blocks for agent pipelines | The "glue" many agents are built on |

**Limits (exam-ready):** agents can loop/overspend (many API calls), act on bad observations, or produce wrong results confidently — human oversight and **tool permissioning** are essential.

## 5.7 Responsible AI ⭐⭐

### 5.7.1 Ethical AI Usage
**Definition:** using AI systems honestly, safely, and fairly — transparency about AI-generated content, avoiding deception (deepfakes, fake reviews), respecting intellectual property, and keeping humans accountable for AI-assisted decisions.

### 5.7.2 Bias and Fairness
- **Bias** = systematic unfairness learned from training data (gender/region/culture stereotypes).
- **Fairness** = designing/testing so outcomes don't disadvantage groups.
- **Mitigation:** diverse, curated data; bias testing; human review; feedback loops.

### 5.7.3 Data Privacy
- Personal data in prompts can leak into training or logs — **never paste sensitive data** into public tools.
- Respect consent, minimisation ("only send what's needed"), and compliance (data-protection laws).
- P10/P11's env-var key pattern is a *privacy* practice, not just convenience.

### 5.7.4 Risks and Limitations of AI Systems
| Risk | Example | Mitigation |
|---|---|---|
| **Hallucination** | Invented facts in a legal document | Grounding/RAG, verification |
| **Misinformation / deepfakes** | Fake images/videos of people | Provenance labels, detection, human verification |
| **Bias** | Biased hiring suggestions | Fairness testing, human review |
| **Privacy** | Prompt leaks | Data minimisation, no secrets in prompts |
| **Dependence / deskilling** | Copy-pasting without understanding | Education, verification culture |
| **Security** | Prompt injection, poisoned tools | Input validation, least-privilege tools |

**The one-sentence exam summary:** AI is a powerful tool whose outputs must be **verified by humans**, whose **data must be protected**, and whose **biases must be tested** — responsible use is part of the engineering, not an afterthought.

---

## 🧠 Deep-Dive Topics

### Deep Dive A: The mock-first development pattern
Build every AI app against a **mock client** (canned responses), then swap in the real API. Benefits: (1) tests/demos run offline and for free; (2) the UI/logic is debugged independently of network failures; (3) demos at practical time never fail on missing keys. P10–P12 all implement `--mock`, and P11/P12 *reuse* P10's `ChatClient` — one API layer, three apps.

### Deep Dive B: From chatbot to agent in three upgrades
```
Level 1 — Chatbot (P10):     input → API → output.
Level 2 — RAG app (P11):     input → retrieve → API with context → output.
Level 3 — Agent (P12/§5.6):  goal → loop{ think → act → observe } → output.
```
Each level adds autonomy. Knowing this ladder answers "what is the difference between a chatbot and an agent?" in one breath.

### Deep Dive C: The 4-app shared architecture (P12)
`retriever → prompt builder → LLM client → formatter → human review`. Chatbot, blog writer, summarizer, and question generator all follow it; only the prompts, data schemas, and formatters change. This is the reusable insight Unit 5 wants you to carry out of the course.

---

## 🚀 Beyond the Textbook (what most classes won't tell you)

1. **"Agentic" is a spectrum, not a binary.** Every tool call added to a chatbot makes it *more* agentic; AutoGPT and CrewAI just push autonomy further. Don't write exam answers as if agents are a totally separate species.
2. **Prompt injection is the new OWASP topic.** Untrusted text inside a prompt can hijack an agent ("ignore previous instructions…"). Real apps sanitize inputs and give tools least privilege.
3. **Mock-first is industry practice**, not a student shortcut. Test-driven development with a stubbed LLM is how serious teams ship; P10–P12 teach it.
4. **The API layer is thin.** Once you can make one chat-completions call, you can call any provider — the differences are endpoint shapes (see §5.4.2 table). This is why the course teaches *one* client reused across apps.
5. **Responsible AI is examinable as application, not philosophy.** "A student copies a full essay from an AI without checking it — discuss" is a classic application-style question. Answer with *verification, disclosure, privacy, bias*.
6. **Memory aid — the 7 sections:** **"P-D-C-A-4-A-R"** ≈ Productivity, Development, Debugging, APIs, the 4 Apps, Agents, Responsible AI. And the agent formula: **"agent = LLM + tools + loop"**.

---

## 🎯 High-Yield Exam Topics (likely GTU-style — no PYQ papers exist yet)

1. **Explain how AI tools help in writing emails, generating reports, and creating presentations.** (4/7)
2. **Explain the role of AI in code generation, explanation, and documentation.** (4/7)
3. **Explain the AI-based debugging workflow with an example.** (7)
4. **What is an API? Explain the components of an API request/response.** (4/7)
5. **Compare the OpenAI API and the Gemini API.** (4)
6. **Explain the architecture of an AI chatbot / blog writer / document summarizer / question generator.** (7)
7. **What is an AI agent? Explain autonomous task execution.** (4/7)
8. **Write a short note on AutoGPT and CrewAI.** (4/7)
9. **Explain Responsible AI: ethics, bias & fairness, data privacy.** (7)
10. **Explain the risks and limitations of AI systems.** (4/7)
11. **Why must an API key never be hard-coded in source code?** (3)
12. **Differentiate a chatbot from an agentic AI system.** (4)

### ✅ Solved model answers (exam style)

**Q. (7 marks) Explain the architecture of an AI chatbot and a document summarizer.**
> **AI chatbot:** a loop: (1) **collect input** — the user types a message; (2) **build the request** — a JSON payload with the model name and messages (system prompt for persona + user message); (3) **call the API** — POST to the chat/completions endpoint with the key in the Authorization header; (4) **parse the response** — extract `choices[0].message.content`; (5) **print the reply** and repeat. A Python implementation of this is P10, which also supports a `--mock` client for offline testing. **Document summarizer:** for short documents, a single summarization prompt (instruction + length + "keep all numbers" + the text). For long documents, the **RAG** pipeline (P11): chunk the document into overlapping passages, embed each chunk, embed the user's request, retrieve the top-k similar chunks, and pass them to the model as context so the summary is grounded in the actual text. Both apps share the same core: prompt building → LLM API → formatting, with retrieval added when the document is large.

**Q. (4 marks) What is an AI agent? Explain with an example.**
> An **AI agent** is a system in which an LLM autonomously decides and executes multi-step actions using tools, observes the results, and iterates until the goal is complete. The formula is **agent = LLM (reasoning) + tools (actions) + a loop (thought → action → observation → repeat)**. Unlike a plain chatbot that answers one request, an agent *plans* a series of steps. Example: AutoGPT given the goal "compare three smartphones and write a report" will break it into steps — search for specs, compute comparisons, draft sections, write the file — calling tools and feeding results back into its reasoning each round. Example of a crew: CrewAI lets you define roles (a researcher, a writer, a reviewer) that collaborate. Agents reduce human effort on multi-step work but need limits: tool permissioning, cost budgets, and human oversight because they can loop, overspend, or act on wrong observations.

**Q. (7 marks) Explain Responsible AI: ethics, bias and fairness, data privacy.**
> **Ethical AI usage:** use AI transparently and honestly — disclose AI-generated content, avoid deepfakes and fake reviews, respect intellectual property, and keep humans accountable for AI-assisted decisions (a human reviews and owns the final output). **Bias and fairness:** bias is systematic unfairness learned from training data (e.g., gender or regional stereotypes). Fairness means designing and testing systems so outcomes do not disadvantage any group. Mitigation: curate diverse training data, run bias/fairness tests, involve diverse reviewers, and provide feedback channels. **Data privacy:** protect personal data at every stage — don't paste sensitive or personal information into public AI tools (it may be logged or used for training), collect only the minimum data needed, obtain consent, and follow data-protection regulations. Engineering practices such as reading API keys from environment variables (P10) are also privacy practices. Overall, Responsible AI treats safety, fairness, and privacy as core requirements of an AI system, not optional extras.

---

## ✍️ Practice Problems (self-test — answers upside-down)

1. Write the 6-step AI debugging workflow.
2. Give one difference in the request body shape between OpenAI and Gemini APIs.
3. What three things does an "agent" combine?
4. A student copies an AI-written assignment without checking it. Which Responsible AI principles does this violate?
5. Which app would you build with (a) just a summarization prompt, (b) RAG, (c) a mock-first chatbot, and why?
6. Name two risks of autonomous agents and their mitigations.

<details>
<summary>📌 Model solutions</summary>

1. Reproduce → paste code + error → ask why → apply fix → verify (incl. edge cases) → learn what caused the bug class.
2. OpenAI sends `{model, messages:[{role, content}]}`; Gemini sends `{contents:[{parts:[{text}]}]}` (response shapes differ too: `choices[0].message.content` vs `candidates[0].content.parts[0].text`).
3. **LLM (reasoning) + tools (actions) + a loop (thought → action → observation → repeat)**.
4. Transparency/honesty (undisclosed AI use), accountability (no human verification), and possibly plagiarism — the right practice is to use AI as a drafting aid, disclose it, and verify every fact.
5. (a) short-document summarizer; (b) long-document/PDF Q&A (chunking + retrieval); (c) any production chatbot — mock-first lets it be tested and demonstrated offline before wiring the real API (the P10 pattern).
6. Loops/overspending (runaway API calls) → cost budgets and step limits; acting on wrong observations → human oversight and tool permissioning; prompt injection → input sanitisation.
</details>

---

## 📖 Glossary of Key Terms

| Term | Definition |
|---|---|
| **API** | Defined interface for one program to request computation/data from another over HTTP |
| **Endpoint** | The URL a client POSTs to |
| **API key** | Secret credential sent in the request header |
| **Request/Response body** | JSON payload sent / JSON result received |
| **Messages (roles)** | `system`/`user`/`assistant` turns in a chat request |
| **Model parameter** | `temperature`, `max_tokens` etc. that shape generation |
| **Chatbot** | App that loops user input → API → reply |
| **Document summarizer** | App that condenses text; RAG for long documents |
| **Question generator** | App that creates MCQs/short questions from a topic |
| **Agent** | LLM + tools + loop that executes multi-step tasks |
| **Autonomous execution** | Agent plans and acts without step-by-step user guidance |
| **AutoGPT** | Open-source autonomous agent |
| **CrewAI** | Multi-agent collaboration framework |
| **Mock client** | Canned-response stand-in for the API for offline testing |
| **Responsible AI** | Ethics, fairness, privacy, and safety in AI systems |
| **Bias** | Systematic unfairness from training data |
| **Fairness** | Design/testing so outcomes don't disadvantage groups |
| **Data privacy** | Protecting personal data in prompts, logs, training |
| **Prompt injection** | Malicious text that hijacks a prompt/agent's instructions |
| **Deepfake** | AI-generated fake media of real people |

---

## 🔗 Curated Resources (per concept)

**Productivity & software dev**
- GitHub Copilot docs: https://docs.github.com/en/copilot
- OpenAI cookbook (code generation, debugging patterns): https://cookbook.openai.com

**APIs**
- OpenAI API reference: https://platform.openai.com/docs/api-reference/chat
- Gemini API docs: https://ai.google.dev/gemini-api/docs
- `requests` library: https://requests.readthedocs.io

**Applications**
- [P10](../practicals/writeups/P10_ai_chatbot_api_python.md) — chatbot + `--mock` + real-key setup
- [P11](../practicals/writeups/P11_document_qa_basic_rag.md) — RAG document Q&A (offline)
- [P12](../practicals/writeups/P12_ai_study_assistant.md) — capstone Study Assistant + 3 design docs

**Agentic AI**
- ReAct paper (Yao et al., 2022): https://arxiv.org/abs/2210.03629
- AutoGPT: https://github.com/Significant-Gravitas/AutoGPT
- CrewAI: https://www.crewai.com · docs: https://docs.crewai.com

**Responsible AI**
- Google Responsible AI: https://ai.google/responsibility
- OpenAI safety & system cards: https://openai.com/safety
- NIST AI Risk Management Framework: https://www.nist.gov/itl/ai-risk-management-framework
- Anthropic responsible scaling: https://www.anthropic.com/research

---

## 🎥 Video Study Guide (YouTube)

> Don't like reading? Me neither. This is your **structured video path** for the whole unit — better than the syllabus because it tells you *exactly what to search* and *what to watch first*, in a sensible order. Everything below is search keywords (they never rot like links do) + channels you can trust.

### 🧑‍🎓 Step 0 — Pick your learning style

| Style | You learn best by | Your path through this unit |
|---|---|---|
| 🎧 **Listener** | short, clear explainers | Watch 1 explainer per topic from the table below (3–8 min each) |
| 🛠️ **Builder** | writing code yourself | Run [P10](../practicals/writeups/P10_ai_chatbot_api_python.md) → [P11](../practicals/writeups/P11_document_qa_basic_rag.md) → [P12](../practicals/writeups/P12_ai_study_assistant.md) with `--mock` |
| 🔧 **Tinkerer** | experimenting & demos | Use a chatbot to generate/debug/explain one of your own scripts (P09-style) |
| 🧠 **Deep Diver** | full theory, "why" | Watch the agent/RAG deep dives; read the ReAct abstract |
| 🧭 **Explorer** | breadth & curiosity | Watch "what are AI agents" and "responsible AI" explainers first |
| 🎓 **Academic** | exam marks | Watch revision videos, then grind the High-Yield Topics above |

### 🎬 Step 1 — Watch by topic (search these on YouTube)

| Topic | YouTube search keywords (copy-paste ready) | Best channels | Style served |
|---|---|---|---|
| AI productivity tools | `ai for email writing` · `ai for presentations` · `best ai productivity tools` | The AI Advantage, IBM Technology | 🧭 Explorer |
| AI in software development | `github copilot for beginners` · `ai code generation best practices` · `explain code with ai` | freeCodeCamp, Fireship | 🛠️ Builder |
| AI debugging | `debugging with chatgpt` · `ai debugging python example` · `find bugs with ai` | Tech With Tim, NetworkChuck | 🛠️ + 🔧 |
| APIs explained | `what is an api in 5 minutes` · `rest api explained` · `how to call openai api python` | IBM Technology, Mosh, freeCodeCamp | 🎧 + 🛠️ |
| OpenAI vs Gemini API | `openai api vs gemini api` · `gemini api python tutorial` · `chatgpt api tutorial python` | Tech With Tim, Google for Developers | 🛠️ Builder |
| Building chatbots | `build chatbot python openai` · `create chatbot with gemini api` · `python chatbot tutorial` | freeCodeCamp, Tech With Tim, AssemblyAI | 🛠️ Builder |
| RAG apps (summarizer/QA) | `build rag application python` · `chat with your pdf python` · `document summarizer llm` | freeCodeCamp, LangChain (official), James Briggs | 🛠️ + 🧠 |
| AI agents | `what are ai agents` · `ai agents explained for beginners` · `agentic ai explained` | IBM Technology, AI Explained, Two Minute Papers | 🧭 + 🎧 |
| AutoGPT & CrewAI | `autogpt explained` · `crewai tutorial` · `multi agent framework` | Two Minute Papers, Nicholas Renotte, AI Jason | 🛠️ + 🧠 |
| Responsible AI | `responsible ai explained` · `ai ethics bias fairness` · `risks of ai systems` | IBM Technology, TED-Ed, Sabine Hossenfelder | 🧭 + 🎓 |
| Whole-unit revision | `ai applications full course` · `generative ai apps python` · `agentic ai crash course` | freeCodeCamp, Gate Smashers, Neso Academy | 🎓 Academic |

### 🎬 Step 2 — Full playlists (for Deep Divers & Academics)

1. **"Andrej Karpathy — intro to LLMs / agents"** — the authoritative "how far can models go" talk that grounds the agent chapter.
2. **"freeCodeCamp — Build an AI chatbot / RAG apps in Python"** — hands-on build-alongs matching P10–P12 exactly.
3. **"Andrew Ng — Agentic AI short course (DeepLearning.AI)"** — short, credible, directly on §5.6.

### 🎬 Step 3 — Proof you got it (5 min)

- Run [P10](../practicals/writeups/P10_ai_chatbot_api_python.md) `--mock`, then [P11](../practicals/writeups/P11_document_qa_basic_rag.md) `--mock`, then [P12](../practicals/writeups/P12_ai_study_assistant.md) `--mock` — you have now built the app ladder chatbot → RAG → study assistant.
- Explain "agent = LLM + tools + loop" to a friend using AutoGPT as the example.
- Answer the P12 viva: "how do the 4 app ideas share code?" — *one pipeline, different prompts*.

---

*🎓 You've finished the 5 units. Next steps: run the practicals, then revise via [RESOURCES](./RESOURCES.md).*
