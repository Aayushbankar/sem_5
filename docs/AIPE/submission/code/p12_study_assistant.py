"""P12 - AI Study Assistant (capstone, offline mock version).

An end-to-end AI application that combines:
  * a small knowledge base (study_notes) with retrieval,
  * a mock LLM client (or the live API client from P10 when AI_API_KEY is set),
  * three commands: explain / summary / quiz.

Design (see writeup for the full architecture diagram)
  prompt design  ->  retrieval (keyword + n-gram scoring)  ->  mock/real API

Run (offline):   python3 p12_study_assistant.py --mock
Run (live):      export AI_API_KEY=sk-...; python3 p12_study_assistant.py
"""

import argparse
import random
import re
import sys
from pathlib import Path

try:
    from p10_chatbot import ChatClient
except ImportError:  # allow running from a different cwd
    sys.path.insert(0, str(Path(__file__).parent))
    from p10_chatbot import ChatClient

NOTES = {
    "prompt engineering": (
        "Prompt engineering is the practice of designing instructions for an "
        "LLM to get accurate, well-formatted outputs. Key components: "
        "instruction, context, input data, output format. Core techniques: "
        "zero-shot, few-shot, role-based, chain-of-thought, prompt chaining.",
        "The quality of the prompt directly controls the quality of the answer.",
    ),
    "llm": (
        "A Large Language Model is a deep neural network trained on massive "
        "text corpora to predict the next token. It uses the transformer "
        "architecture with attention. LLMs power chatbots, summarizers, and "
        "code assistants. Known limits: hallucination, context window, bias.",
        "LLMs predict the next token based on the previous context.",
    ),
    "rag": (
        "Retrieval Augmented Generation grounds LLM answers in external "
        "documents. Pipeline: chunk the document, embed chunks as vectors, "
        "rank the chunks closest to the question, feed them to the LLM as "
        "context. RAG reduces hallucination and enables document Q&A.",
        "RAG = retrieve first, then generate with retrieved context.",
    ),
    "token": (
        "A token is a unit of text that an LLM reads and writes, typically a "
        "sub-word like 'prompt' or 'ing'. The context window is the maximum "
        "number of tokens a model can handle in one request. Longer prompts "
        "cost more because API billing is per token.",
        "Tokenization converts raw text into a sequence of tokens.",
    ),
    "agentic ai": (
        "An AI agent is a system that uses an LLM plus tools to act "
        "autonomously: it plans, calls tools (search, code, APIs), observes "
        "results, and iterates. Examples: AutoGPT, CrewAI. RAG adds knowledge; "
        "agents add action.",
        "Agents combine reasoning (LLM) with action (tools).",
    ),
}


def retrieve(topic: str, k: int = 2) -> list[str]:
    """Rank note entries by how many query words they share."""
    topic_words = set(re.findall(r"[a-z']+", topic.lower()))
    scored = []
    for key, (body, summary) in NOTES.items():
        hay = set(re.findall(r"[a-z']+", key + " " + body.lower()))
        scored.append((len(topic_words & hay), key, body, summary))
    scored.sort(key=lambda t: t[0], reverse=True)
    return [f"[{key}] {body} (one-liner: {summary})"
            for _, key, body, summary in scored[:k]]


def build_explain_prompt(topic: str, context: list[str]) -> str:
    return (
        "You are a friendly tutor for diploma IT students. Explain the topic "
        f"below in simple words in 3-4 sentences, with one real-world example.\n\n"
        f"TOPIC: {topic}\n\n"
        f"REFERENCE NOTES:\n" + "\n".join(context) + "\n\nEXPLANATION:"
    )


def build_quiz_prompt(topic: str) -> str:
    return (
        f"Generate 3 multiple-choice quiz questions (4 options each) about "
        f"'{topic}'. Give the correct answer after each question with a "
        "one-line reason."
    )


def mock_explain(topic: str, context: list[str]) -> str:
    top_key = context[0].split("]", 1)[0].strip("[]") if context else topic
    body = NOTES.get(top_key, (topic, ""))[0]
    first = body.split(".", 1)[0].lower()
    return (f"[mock] {topic.title()} in simple words: {first}. "
            f"It works best when you combine a clear definition with practice. "
            f"Example: ask your assistant 'explain {top_key}' and then quiz "
            "yourself on it.")


def mock_summary(topic: str, context: list[str]) -> str:
    top_key = context[0].split("]", 1)[0].strip("[]") if context else topic
    summary = NOTES.get(top_key, ("", ""))[1] or "No summary available."
    return f"[mock] Summary of '{top_key}': {summary}"


def mock_quiz(topic: str) -> str:
    questions = [
        ("Which technique shows a model examples before the real question?",
         "Few-shot prompting"),
        ("What does the context window limit?",
         "The number of tokens a model can process at once"),
        ("Which step comes first in a RAG pipeline?",
         "Chunking the document"),
    ]
    lines = []
    for i, (q, a) in enumerate(questions, 1):
        lines.append(f"{i}. {q}")
        for opt in (a, "Zero-shot prompting", "Fine-tuning", "Tokenization"):
            marker = " (correct)" if opt == a else ""
            lines.append(f"   - {opt}{marker}")
    lines.append("\n[Note: in live mode the model generates topic-specific MCQs.]")
    return "[mock] Quiz for you:\n" + "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="AI Study Assistant (P12)")
    parser.add_argument("--mock", action="store_true",
                        help="use the offline mock brain (no API key)")
    parser.add_argument("--topic", default="prompt engineering",
                        help="topic to study")
    parser.add_argument("--provider", choices=["openai", "gemini"],
                        default="openai")
    args = parser.parse_args()

    try:
        client = ChatClient(provider=args.provider, mock=args.mock)
    except RuntimeError as e:
        print(f"[error] {e}", file=sys.stderr)
        return 1

    print("=" * 72)
    print(f"AI STUDY ASSISTANT (mock={args.mock}, provider={args.provider})")
    print("Commands: explain <topic> | summary <topic> | quiz <topic>")
    print("=" * 72)

    topic = args.topic
    context = retrieve(topic)
    print(f"\n[retrieval] top {len(context)} note(s) for '{topic}':")
    for c in context:
        print("  -", c[:100], "...")

    if args.mock:
        print("\n>>> explain")
        print(mock_explain(topic, context))
        print("\n>>> summary")
        print(mock_summary(topic, context))
        print("\n>>> quiz")
        print(mock_quiz(topic))
        return 0

    commands = [
        (f"explain {topic}", build_explain_prompt(topic, context)),
        (f"summary of {topic}",
         f"Summarize the key points of '{topic}' in exactly 3 bullets."),
        (f"quiz on {topic}", build_quiz_prompt(topic)),
    ]
    for name, prompt in commands:
        print(f"\n>>> {name}")
        print(client.respond(prompt))
    return 0


if __name__ == "__main__":
    sys.exit(main())
