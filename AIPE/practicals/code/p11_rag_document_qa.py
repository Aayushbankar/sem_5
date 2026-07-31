"""P11 - Document-based question answering (basic RAG), fully offline.

Pipeline
  1. Chunk  a .txt file into overlapping passages.
  2. Embed  each chunk with character n-gram hashing (TF vectors).
  3. Rank   chunks by cosine similarity to the question.
  4. Answer using the top chunks as context via the ChatClient from P10.

No external dependencies are required for embedding (pure stdlib).
Use --mock to answer from canned responses (no API key). With AI_API_KEY set
and without --mock it calls the real API through the P10 client.

Run:  python3 p11_rag_document_qa.py --mock
"""

import argparse
import math
import re
import sys
from collections import Counter
from pathlib import Path

from p10_chatbot import ChatClient

DEFAULT_DOC = Path(__file__).parent / "p11_sample_document.txt"


# ---------------------------------------------------------------------------
# 1) Chunking
# ---------------------------------------------------------------------------
def chunk_text(text: str, chunk_size: int = 300, overlap: int = 50) -> list[str]:
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    chunks, current, current_len = [], [], 0
    for s in sentences:
        if current_len + len(s) > chunk_size and current:
            chunks.append(" ".join(current))
            keep = []
            kept = 0
            for prev in reversed(current):
                if kept + len(prev) > overlap:
                    break
                keep.append(prev)
                kept += len(prev)
            current = list(reversed(keep))
            current_len = kept
        current.append(s)
        current_len += len(s)
    if current:
        chunks.append(" ".join(current))
    return chunks


# ---------------------------------------------------------------------------
# 2) Embedding: character n-gram hashing (pure stdlib, no network)
# ---------------------------------------------------------------------------
def embed(text: str, n: int = 3, dim: int = 256) -> list[float]:
    vec = [0.0] * dim
    norm = text.lower()
    for i in range(len(norm) - n + 1):
        gram = norm[i:i + n]
        idx = hash(gram) % dim
        vec[idx] += 1.0
    mag = math.sqrt(sum(v * v for v in vec)) or 1.0
    return [v / mag for v in vec]


def cosine_sim(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


# ---------------------------------------------------------------------------
# 3) Retrieval
# ---------------------------------------------------------------------------
def retrieve(question: str, chunks: list[str], k: int = 2) -> list[tuple[float, str]]:
    q_vec = embed(question)
    scored = [(cosine_sim(q_vec, embed(c)), c) for c in chunks]
    scored.sort(key=lambda t: t[0], reverse=True)
    return scored[:k]


# ---------------------------------------------------------------------------
# 4) Answering
# ---------------------------------------------------------------------------
def build_prompt(question: str, contexts: list[str]) -> str:
    ctx_block = "\n\n".join(f"[Excerpt {i + 1}]\n{c}" for i, c in enumerate(contexts))
    return (
        "You are a document-answering assistant. Answer the question using "
        "ONLY the excerpts below. If the answer is not in the excerpts, say "
        "'Not found in the document.'\n\n"
        f"QUESTION: {question}\n\n"
        f"EXCERPTS:\n{ctx_block}\n\n"
        "ANSWER:"
    )


def extractive_answer(question: str, contexts: list[str]) -> str:
    """Offline answer: return the excerpt sentence with most question-word
    overlap. Stands in for the LLM so the full RAG loop runs without a key."""
    q_words = set(re.findall(r"[a-z']+", question.lower()))
    best_sentence, best_score = None, -1
    for ctx in contexts:
        for sent in re.split(r"(?<=[.!?])\s+", ctx):
            sent_words = re.findall(r"[a-z']+", sent.lower())
            if not sent_words:
                continue
            overlap = len(q_words & set(sent_words))
            if overlap / len(sent_words) > 0.8:
                continue  # the "sentence" is just the question itself
            if overlap > best_score:
                best_sentence, best_score = sent, overlap
    if best_sentence is None or best_score == 0:
        return "Not found in the document."
    return best_sentence + " [extracted by the offline mock brain]"


# ---------------------------------------------------------------------------
# 5) Pipeline
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description="Document Q&A with basic RAG")
    parser.add_argument("--doc", default=str(DEFAULT_DOC),
                        help="path to the source .txt document")
    parser.add_argument("--mock", action="store_true",
                        help="answer offline with canned responses")
    parser.add_argument("--provider", choices=["openai", "gemini"],
                        default="openai")
    args = parser.parse_args()

    doc_path = Path(args.doc)
    if not doc_path.exists():
        print(f"[error] document not found: {doc_path}", file=sys.stderr)
        return 1

    try:
        client = ChatClient(provider=args.provider, mock=args.mock)
    except RuntimeError as e:
        print(f"[error] {e}", file=sys.stderr)
        return 1

    text = doc_path.read_text(encoding="utf-8")
    chunks = chunk_text(text)

    print("=" * 72)
    print("P11: DOCUMENT Q&A WITH BASIC RAG "
          f"(mock={args.mock}, provider={args.provider})")
    print("=" * 72)
    print(f"Document : {doc_path.name}")
    print(f"Chunks   : {len(chunks)}")
    for i, c in enumerate(chunks):
        print(f"  chunk {i + 1}: {len(c)} chars | {c[:60]}...")

    questions = [
        "What is a Large Language Model?",
        "How does the transformer architecture work?",
        "What is prompt engineering?",
    ]
    for q in questions:
        top = retrieve(q, chunks)
        print("\n" + "-" * 72)
        print(f"Q: {q}")
        for score, chunk in top:
            print(f"  [retrieved score={score:.3f}] {chunk[:80]}...")
        contexts = [c for _, c in top]
        if args.mock:
            answer = extractive_answer(q, contexts)
        else:
            answer = client.respond(build_prompt(q, contexts))
        print(f"A: {answer}")

    print("\nNote: with a live AI_API_KEY (no --mock), the same pipeline "
          "sends the retrieved excerpts to the real model for a better answer.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
