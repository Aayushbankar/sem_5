# P10 — Simple AI Chatbot via API (OpenAI/Gemini) with Python

**Subject:** Artificial Intelligence with Prompt Engineering | **Unit:** 5 | **Approx. Hrs:** 4
**PrO (verbatim):** *Develop a simple AI chatbot using API integration (OpenAI/Gemini) with Python.*

---

## 1. Objective
- Build a **command-line chatbot** in Python that calls an LLM API.
- Support **both** OpenAI-compatible and Gemini endpoints.
- Read the secret key from an environment variable (`AI_API_KEY`) — **never** hard-code it.
- Provide a `--mock` mode so the chatbot can be **demonstrated offline** with no key.

## 2. Theory (exam-ready)

**What is an API?** An Application Programming Interface is a contract that lets one program request data/computation from another over HTTP. LLM providers (OpenAI, Google) expose **REST APIs**: you send a JSON `POST` request with your prompt, and get back the model's generated text.

**How the chatbot works:**
```
User input ──► build JSON payload ──► POST to /chat/completions ──► parse choices[0].message.content ──► print
```
**Key API concepts (syllabus §5.4):**
| Concept | Meaning |
|---|---|
| **Endpoint / URL** | The address you POST to (e.g., `https://api.openai.com/v1/chat/completions`) |
| **API key** | Secret credential sent in the `Authorization` header |
| **Model** | Which model to use (e.g., `gpt-4o-mini`, `gemini-2.0-flash`) |
| **Payload / request body** | `{model, messages:[{role, content}], …}` |
| **Message roles** | `system` (instructions), `user` (input), `assistant` (replies) |
| **Token cost** | Billing is per input + output token |

**Security:** the key must live in the environment (`export AI_API_KEY=…`), not in source code. Committing a key to git leaks money and access.

## 3. Code

Script: [`p10_chatbot.py`](../code/p10_chatbot.py) — key parts:

```python
class ChatClient:
    def __init__(self, provider="openai", mock=False, model=None):
        if mock:
            self.mock = True
            return
        self.api_key = os.environ.get("AI_API_KEY", "").strip()
        if not self.api_key:
            raise RuntimeError("AI_API_KEY is not set …")
        if provider == "openai":
            self.base_url = "https://api.openai.com/v1/chat/completions"
            self.model = model or "gpt-4o-mini"
        elif provider == "gemini":
            self.base_url = "…/generativelanguage.googleapis.com/v1beta/models/" \
                            + (model or "gemini-2.0-flash") + ":generateContent"

    def respond(self, user_message: str) -> str:
        if self.mock:
            return MOCK_RESPONSES.get(user_message.strip().lower().rstrip("?!."),
                                      "[mock] …canned answer…")
        import requests
        payload = {"model": self.model,
                   "messages": [{"role": "user", "content": user_message}]}
        resp = requests.post(self.base_url,
                             headers={"Authorization": f"Bearer {self.api_key}"},
                             json=payload, timeout=60)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
```

Note the mock path imports `requests` *lazily*, so `--mock` works with zero extra dependencies.

## 4. How to run

**Offline demo (no key, no network) — actual run:**
```
$ python3 p10_chatbot.py --mock
========================================================================
AI CHATBOT (provider=openai, mock=True)
Type 'quit' to exit. [OFFLINE DEMO - no API key needed]
========================================================================

You   : Hello
Bot   : Hello! I am your AI study assistant. Ask me about prompt engineering, LLMs, or ask me to explain a concept.

You   : What is prompt engineering?
Bot   : Prompt engineering is the practice of designing clear instructions for an AI model so it produces the output you want - you set the role, context, input data and output format explicitly.

You   : Explain LLM
Bot   : An LLM (Large Language Model) is a deep neural network trained on huge amounts of text to predict the next token. It is what powers tools like ChatGPT, Claude and Gemini.

(mock mode: interactive loop skipped; type 'quit' if you re-run interactively)
```

**Live mode (real key):**
```
export AI_API_KEY=sk-...                # OpenAI key (or AIza... for Gemini)
python3 p10_chatbot.py                  # OpenAI backend
python3 p10_chatbot.py --provider gemini
```
Interactive loop: type messages, `quit` to exit. In live mode the app runs the exact same demo questions against the real API.

**Setup steps for a real key**
1. Create an account at https://platform.openai.com (or https://aistudio.google.com/apikey for Gemini).
2. Create an API key; copy it.
3. `export AI_API_KEY="your_key_here"` (macOS/Linux) or `set AI_API_KEY=your_key_here` (Windows).
4. Install the only dependency: `python3 -m pip install requests`.
5. Run the script (optionally with `--provider gemini`).

> ⚠️ **Never** paste the key into the script or commit it. The script refuses to start if `AI_API_KEY` is missing.

## 5. Expected output explanation
- In mock mode the canned answers prove the full **request → response → print** loop works end-to-end without external access.
- In live mode the same three demo questions go over HTTPS to the provider and the real model text is printed.
- Because the client is a separate class, P11 (RAG) and P12 (Study Assistant) **reuse** `ChatClient` instead of re-writing API code.

## 6. Deliverable — report skeleton
1. Theory: what an API is + the request/response flow diagram.
2. The code with the key read from `AI_API_KEY` (point it out).
3. Real output of the `--mock` run (paste it).
4. Setup steps for a real key (don't paste the key).
5. Conclusion: what changes when `mock=False`.

## 7. Conclusion
A chatbot is a loop: **collect input → build a prompt → call an API → print the response**. The important engineering choices are *where the key lives* (environment variable), *how the payload is shaped* (roles + model + messages), and *how failures are surfaced* (`raise_for_status`). The `--mock` flag makes the whole loop testable offline — the same pattern used in P11 and P12.

## 8. Viva Q&A
1. **What is an API key?** — A secret credential that identifies you to the provider; sent in the Authorization header.
2. **Why read the key from an environment variable?** — So it never lives in source code and can't be committed to git.
3. **What is the endpoint?** — The URL your client POSTs the request to.
4. **What is a system message/role?** — The role that sets the model's behaviour ("you are a study assistant").
5. **What is `--mock` for?** — Running the full loop offline with canned answers, for demos/tests with no key.
6. **Which header carries the key?** — `Authorization: Bearer <key>`.

## 9. Resources
- OpenAI chat completions API docs: https://platform.openai.com/docs/api-reference/chat
- Gemini API docs: https://ai.google.dev/gemini-api/docs
- `requests` library: https://requests.readthedocs.io
- Script: [`p10_chatbot.py`](../code/p10_chatbot.py)
