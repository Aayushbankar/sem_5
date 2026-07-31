"""P10 - Simple AI chatbot using an API (OpenAI-compatible or Gemini) + Python.

Features
  * Reads the API key from the environment variable AI_API_KEY (never hard-coded).
  * --mock : runs fully offline with canned responses, no key required.
  * --provider openai|gemini : select the backend (default openai).
  * Exposes a reusable ChatClient so P11 (RAG) can import it.

Usage
  export AI_API_KEY=sk-...            # real key
  python3 p10_chatbot.py              # live OpenAI-compatible chat
  python3 p10_chatbot.py --provider gemini
  python3 p10_chatbot.py --mock       # offline demo (works anywhere)
"""

import argparse
import os
import sys

MOCK_RESPONSES = {
    "hello": "Hello! I am your AI study assistant. Ask me about prompt "
             "engineering, LLMs, or ask me to explain a concept.",
    "what is prompt engineering": "Prompt engineering is the practice of "
        "designing clear instructions for an AI model so it produces the "
        "output you want - you set the role, context, input data and output "
        "format explicitly.",
    "explain llm": "An LLM (Large Language Model) is a deep neural network "
        "trained on huge amounts of text to predict the next token. It is "
        "what powers tools like ChatGPT, Claude and Gemini.",
}


class ChatClient:
    """Thin wrapper around an HTTP chat API.

    mock=True -> canned replies, no network, no key.
    Otherwise it calls a chat/completions style REST endpoint using requests.
    """

    def __init__(self, provider: str = "openai", mock: bool = False,
                 model: str | None = None):
        self.provider = provider
        self.mock = mock
        if mock:
            self.model = "mock-1"
            return
        self.api_key = os.environ.get("AI_API_KEY", "").strip()
        if not self.api_key:
            raise RuntimeError(
                "AI_API_KEY is not set. Run with --mock for an offline demo, "
                "or set the key first:  export AI_API_KEY=your_key"
            )
        if provider == "openai":
            self.base_url = "https://api.openai.com/v1/chat/completions"
            self.model = model or "gpt-4o-mini"
        elif provider == "gemini":
            self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/" \
                            + (model or "gemini-2.0-flash") + ":generateContent"
            self.model = model or "gemini-2.0-flash"
        else:
            raise ValueError(f"Unknown provider: {provider}")
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    def respond(self, user_message: str) -> str:
        if self.mock:
            key = user_message.strip().lower().rstrip("?!.")
            if key in MOCK_RESPONSES:
                return MOCK_RESPONSES[key]
            for known, reply in MOCK_RESPONSES.items():
                if known in key:
                    return reply
            return (f"[mock] I heard: \"{user_message}\". In live mode this "
                    f"would go to the {self.provider} API and return a real "
                    "model-generated answer.")
        import requests  # imported lazily so --mock needs no extra deps

        if self.provider == "openai":
            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": user_message}],
            }
            resp = requests.post(self.base_url, headers=self.headers,
                                 json=payload, timeout=60)
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"]
        else:
            payload = {"contents": [{"parts": [{"text": user_message}]}]}
            resp = requests.post(self.base_url, headers=self.headers,
                                 json=payload, timeout=60)
            resp.raise_for_status()
            return resp.json()["candidates"][0]["content"]["parts"][0]["text"]


def main() -> int:
    parser = argparse.ArgumentParser(description="Simple API chatbot (P10)")
    parser.add_argument("--provider", choices=["openai", "gemini"],
                        default="openai", help="which API backend to use")
    parser.add_argument("--mock", action="store_true",
                        help="run offline with canned responses (no API key)")
    args = parser.parse_args()

    try:
        client = ChatClient(provider=args.provider, mock=args.mock)
    except RuntimeError as e:
        print(f"[error] {e}", file=sys.stderr)
        return 1

    print("=" * 72)
    print(f"AI CHATBOT (provider={args.provider}, mock={args.mock})")
    print("Type 'quit' to exit. " + ("[OFFLINE DEMO - no API key needed]" if args.mock else ""))
    print("=" * 72)

    demo_questions = [
        "Hello",
        "What is prompt engineering?",
        "Explain LLM",
    ]
    for q in demo_questions:
        print(f"\nYou   : {q}")
        print(f"Bot   : {client.respond(q)}")

    if args.mock:
        print("\n(mock mode: interactive loop skipped; type 'quit' if you "
              "re-run interactively)")
        return 0

    print("\n(live mode: interactive chat - type 'quit' to exit)")
    while True:
        try:
            user_input = input("\nYou: ").strip()
        except EOFError:
            break
        if user_input.lower() in {"quit", "exit", "q"}:
            break
        print(f"Bot: {client.respond(user_input)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
