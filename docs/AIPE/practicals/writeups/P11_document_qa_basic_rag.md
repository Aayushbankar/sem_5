# P11 — Document-Based Q&A (Basic RAG)

**Subject:** Artificial Intelligence with Prompt Engineering | **Unit:** 5 | **Approx. Hrs:** 4
**PrO (verbatim):** *Build a document-based question-answering system using AI APIs. (Basic RAG concept)*

---

## 1. Objective
- Build a **Retrieval Augmented Generation (RAG)** pipeline in Python:
  **chunk → embed → retrieve → answer**.
- Make it run **fully offline** with a `--mock` flag (no API key, no network).
- Reuse the `ChatClient` from P10 so the same code works live with a key.
- Keep dependencies to **stdlib only** (embeddings use character n-gram hashing).

## 2. Theory (exam-ready)

**The problem:** an LLM knows only its training data and can't answer questions about *your* document. **Retrieval Augmented Generation (RAG)** fixes this by retrieving relevant text from the document and giving it to the model as context (syllabus §4.4).

**The four steps:**
| Step | What happens | Our implementation |
|---|---|---|
| 1. **Chunk** | Split the document into small overlapping passages | Sentence-based chunks of ~300 chars with 50-char overlap |
| 2. **Embed** | Convert each chunk into a vector of numbers | Character **n-gram hashing** → 256-dim TF vector |
| 3. **Retrieve** | Rank chunks by similarity to the question | **Cosine similarity** with the question's vector |
| 4. **Answer** | Feed top-k chunks + question to the LLM | `ChatClient` from P10 (mock or live) |

**Why RAG matters:** (a) answers are **grounded in real text** → fewer hallucinations; (b) the model can discuss documents it never saw; (c) no retraining needed — just swap the document.

**Embeddings (conceptual):** a vector that captures a text's meaning; similar texts get similar vectors, so "how close is this chunk to the question?" becomes a simple geometry question (cosine of the angle between vectors). Real systems use trained embedding models; for this practical we use a cheap hashed-char-gram approximation that needs no downloads.

## 3. Code

Script: [`p11_rag_document_qa.py`](../code/p11_rag_document_qa.py), sample doc: [`p11_sample_document.txt`](../code/p11_sample_document.txt)

Core of the offline retrieval (stdlib only):
```python
def embed(text: str, n: int = 3, dim: int = 256) -> list[float]:
    vec = [0.0] * dim
    norm = text.lower()
    for i in range(len(norm) - n + 1):
        gram = norm[i:i + n]
        vec[hash(gram) % dim] += 1.0
    mag = math.sqrt(sum(v * v for v in vec)) or 1.0
    return [v / mag for v in vec]

def cosine_sim(a, b):
    return sum(x * y for x, y in zip(a, b))

def retrieve(question, chunks, k=2):
    q_vec = embed(question)
    scored = sorted(((cosine_sim(q_vec, embed(c)), c) for c in chunks),
                    key=lambda t: t[0], reverse=True)
    return scored[:k]
```
The mock "answerer" returns the excerpt sentence with the most question-word overlap (an *extractive* answer); with `AI_API_KEY` set, the same excerpts go to the real model instead.

## 4. Actual run (`python3 p11_rag_document_qa.py --mock`)

```
========================================================================
P11: DOCUMENT Q&A WITH BASIC RAG (mock=True, provider=openai)
========================================================================
Document : p11_sample_document.txt
Chunks   : 14
  chunk 1: 213 chars | Introduction to Large Language Models
...
------------------------------------------------------------------------
Q: What is a Large Language Model?
  [retrieved score=0.636] Introduction to Large Language Models
...
  [retrieved score=0.413] Scaling up the number of parameters ...
A: Introduction to Large Language Models

A Large Language Model, or LLM, is a deep neural network trained on very large
amounts of text data. [extracted by the offline mock brain]

------------------------------------------------------------------------
Q: How does the transformer architecture work?
  [retrieved score=0.604] Transformers and attention
...
  [retrieved score=0.463] Retrieval Augmented Generation ...
A: Transformers and attention

The transformer architecture was introduced in 2017 in the paper "Attention is
All You Need". [extracted by the offline mock brain]

------------------------------------------------------------------------
Q: What is prompt engineering?
  [retrieved score=0.528] What is prompt engineering? Prompt engineering is the practice of ...
  [retrieved score=0.475] Scaling up the number of parameters ...
A: Prompt engineering is the practice of designing the instruction given to an LLM
so that the output is accurate, useful, and correctly formatted.
[extracted by the offline mock brain]

Note: with a live AI_API_KEY (no --mock), the same pipeline sends the retrieved
excerpts to the real model for a better answer.
```

**How to interpret:** for each question the system found the *correct* chunks (top score is the matching section), and the answer text was extracted straight from the retrieved passage — proving the retrieval is doing its job. With a real key, the LLM would rephrase that passage into a natural answer instead.

## 5. How to run
```
# offline (no deps, no key)
python3 p11_rag_document_qa.py --mock

# live (needs P10's ChatClient + requests + a key)
python3 -m pip install requests
export AI_API_KEY=sk-...                    # or a Gemini key
python3 p11_rag_document_qa.py
python3 p11_rag_document_qa.py --doc my_notes.txt     # any .txt file
```
Requirements: Python 3.8+; `p10_chatbot.py` must be in the same folder (it's imported).

## 6. Experiment ideas (record your results)
1. **Change k** (retrieved chunks): `k=1` vs `k=3` — does the answer improve?
2. **Change chunk size** in `chunk_text()` — too small = lost context, too big = noise.
3. **Ask an out-of-document question** (e.g., "recipes for biryani") — mock returns "Not found in the document." That *groundedness* is the whole point of RAG.
4. **Swap the document** — any `.txt` becomes a Q&A subject.

## 7. Deliverable — report skeleton
1. Theory + the 4-step pipeline diagram.
2. Code listing with each step labelled (chunk/embed/retrieve/answer).
3. Pasted real `--mock` output.
4. Result of one experiment (change k or chunk size).
5. Conclusion: how RAG reduces hallucination vs plain prompting.

## 8. Conclusion
The mock run demonstrates the complete RAG loop — chunking 14 passages, embedding them, ranking by cosine similarity, and answering from the retrieved text — with zero external dependencies. The same pipeline upgrades to a real LLM simply by removing `--mock`. This is the exact architecture behind "chat with your PDF" products.

## 9. Viva Q&A
1. **What does RAG stand for and what does it add?** — Retrieval Augmented Generation; it adds external documents as context to the model.
2. **What is a chunk?** — A small overlapping passage of the document; the retrieval unit.
3. **What is an embedding?** — A vector of numbers representing a text's meaning.
4. **How are chunks ranked?** — Cosine similarity between question vector and chunk vector.
5. **Why does RAG reduce hallucinations?** — The answer is grounded in the retrieved text instead of the model's memory.
6. **Why use hashed character n-grams instead of a real embedding model?** — Zero downloads, works offline; real products use trained embedding models.
7. **What role does P10's ChatClient play?** — It is reused to call the API (or mock) — same client, new application.

## 10. Resources
- *"Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"* (Lewis et al., 2020): https://arxiv.org/abs/2005.11401
- OpenAI cookbook — RAG patterns: https://cookbook.openai.com/examples/vector_databases/readme
- Google AI — grounding with Gemini: https://ai.google.dev/gemini-api/docs/grounding
- Script + sample doc: [`p11_rag_document_qa.py`](../code/p11_rag_document_qa.py) · [`p11_sample_document.txt`](../code/p11_sample_document.txt)
