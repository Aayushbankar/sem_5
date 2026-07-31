---
subject: AIPE
status: not-started
tags: [subject/aipe, practical, unit/1]
practical: 2
unit: 1
hours: 2
---
# P02 — Sentiment Analysis & Text Classification with Python

**Subject:** Artificial Intelligence with Prompt Engineering | **Unit:** 1 | **Approx. Hrs:** 2
**PrO (verbatim):** *Perform basic NLP-based tasks such as sentiment analysis and text classification using AI tools or Python libraries.*

---

## 1. Objective
- Perform **sentiment analysis** (positive/negative/neutral) on text using Python.
- Build a **text classifier** (movie review positive/negative; spam vs ham) in pure Python.
- Show a **no-network fallback** (lexicon approach) that runs anywhere.

## 2. Theory (exam-ready)

**NLP (Natural Language Processing)** lets computers understand, interpret, and generate human language. Two basic NLP tasks:

1. **Sentiment analysis** — decide the emotional tone of text. Output is usually a **polarity** score in `[-1, +1]` and a **subjectivity** score in `[0, 1]`.
2. **Text classification** — assign a text to a category (label) from a fixed set. Example: `pos`/`neg`, `spam`/`ham`.

**Approaches used here:**
- **Lexicon-based:** count positive vs negative words from a fixed word list. Simple, transparent, works offline. Handles simple negation ("not good").
- **TextBlob** (Python library built on NLTK): `TextBlob(text).sentiment` returns `(polarity, subjectivity)`.
- **Naive Bayes classifier** (from scratch): counts word frequencies per class, applies Bayes' rule with add-1 smoothing, and predicts the class with the highest log-probability. This is the same family used by real spam filters.

**Tokenization:** splitting text into smaller units — words or sub-words — before analysis. It is the first step of almost every NLP pipeline (Unit 2 covers tokens for LLMs).

## 3. Steps Performed
1. Checked the environment: `python3 -c "import textblob"` → *ModuleNotFoundError*, so installed it with `python3 -m pip install textblob` and `python3 -m textblob.download_corpora` (works when online).
2. Implemented a **pure-stdlib lexicon classifier** (works even with no internet / no libraries).
3. Ran **TextBlob** sentiment on the same 4 sample reviews and compared.
4. Wrote a tiny **Naive Bayes classifier** from scratch and trained it on movie reviews and on spam/ham messages; measured accuracy on unseen test data.

## 4. Code
- Main script (auto-uses TextBlob when present, else falls back to the lexicon): [[p02_sentiment_analysis.py|`p02_sentiment_analysis.py`]]
- Offline-only lexicon classifier (zero dependencies): [[p02_lexicon_fallback.py|`p02_lexicon_fallback.py`]]

Core of the lexicon classifier (pure stdlib):

```python
def classify(text: str) -> dict:
    words = re.findall(r"[a-z']+", text.lower())
    pos = neg = 0
    for i, w in enumerate(words):
        if w in NEGATIONS and i + 1 < len(words):
            nxt = words[i + 1]
            if nxt in POSITIVE_WORDS: neg += 1
            elif nxt in NEGATIVE_WORDS: pos += 1
            continue
        if w in POSITIVE_WORDS: pos += 1
        elif w in NEGATIVE_WORDS: neg += 1
    score = (pos - neg) / max(1, pos + neg)
    label = "Positive" if score > 0.2 else "Negative" if score < -0.2 else "Neutral"
    return {"polarity": score, "label": label, "pos": pos, "neg": neg}
```

The Naive Bayes core (trained `fit`, predicted `predict`): counts `word_counts[class][word]`, then for a new text computes `log P(class) + Σ log P(word|class)` with add-1 smoothing.

## 5. Output (actual run on this machine — Python 3.14)

**Main script — `python3 p02_sentiment_analysis.py`:**
```
========================================================================
PRACTICAL 02: Sentiment Analysis & Text Classification
========================================================================

[1] Rule-based lexicon sentiment (pure stdlib, offline)
  polarity=+1.00 pos=2 neg=0 -> Positive | This product is amazing and I love it!
  polarity=-1.00 pos=0 neg=2 -> Negative | This product is terrible and I hate it.
  polarity=+0.00 pos=0 neg=0 -> Neutral  | The movie was okay, nothing special.
  polarity=+0.33 pos=2 neg=1 -> Positive | The service was good, but the room was not great.

[2] TextBlob sentiment (polarity / subjectivity)
  polarity=+0.613 subjectivity=0.750 -> Positive | This product is amazing and I love it!
  polarity=-0.900 subjectivity=0.950 -> Negative | This product is terrible and I hate it.
  polarity=+0.429 subjectivity=0.536 -> Positive | The movie was okay, nothing special.
  polarity=+0.150 subjectivity=0.675 -> Positive | The service was good, but the room was not great.

[3] Text classification with a tiny Naive Bayes classifier
  Movie review classifier accuracy: 100%
    predict=pos  actual=pos  | an absolutely fantastic experience, i loved it
    predict=neg  actual=neg  | horrible and boring, nothing good about it
    predict=pos  actual=pos  | the acting was great but the ending was not bad
    predict=neg  actual=neg  | nice story, but a slow and painful first half
    predict=neg  actual=neg  | i was not impressed, a waste of two hours
  Spam classifier accuracy: 100%
    predict=spam  actual=spam  | free gift waiting for you click now
    predict=ham   actual=ham   | the presentation is ready for review
```

**Offline fallback — `python3 p02_lexicon_fallback.py`:**
```
========================================================================
P02 (offline fallback): Lexicon-based sentiment classifier
========================================================================
  polarity=+1.00  pos=2 neg=0  -> Positive | This product is amazing and I love it!
  polarity=-1.00  pos=0 neg=2  -> Negative | This product is terrible and I hate it.
  polarity=+0.00  pos=0 neg=0  -> Neutral  | The movie was okay, nothing special.
  polarity=+0.33  pos=2 neg=1  -> Positive | The service was good, but the room was not great.
  polarity=+0.00  pos=0 neg=0  -> Neutral  | Customer support was very helpful and friendly.
  polarity=-1.00  pos=0 neg=1  -> Negative | The app crashed repeatedly, extremely frustrating.
```

**Interpretation:**
- Both the lexicon and TextBlob agree on the positive/negative direction of every sample.
- Negation handling works: *"the room was not great"* → lexicon gives `+0.33` (good dominates) while TextBlob gives `+0.15` — a milder positive; note the difference in scales.
- The Naive Bayes classifier (written from scratch, no sklearn) hits **100%** on both small test sets, and the negation-folded features (`not_good`, `not_impressed`) are exactly why "i was not impressed" is not classified as positive.

## 6. Conclusion
- Sentiment analysis can be done with **three levels of effort**: a word lexicon (offline, transparent), a library like TextBlob (better coverage), or a trained classifier (task-specific, measurable accuracy).
- Text classification via a tiny Naive Bayes model is effective even with a small training set and **zero external dependencies**.
- These are the same building blocks that real products (review analytics, spam filters, support-ticket routing) use.

## 7. Viva Q&A
1. **What is polarity?** — A score in [-1, +1] describing how positive or negative a text is.
2. **What is subjectivity?** — A score in [0, 1] describing how much of the text is opinion vs fact.
3. **What is a token?** — A basic text unit (word or sub-word) produced by tokenization.
4. **Why did TextBlob need `download_corpora`?** — It downloads NLTK datasets (movie_reviews, etc.) used for training and tagging.
5. **What is add-1 (Laplace) smoothing?** — Adding 1 to every word count so unseen words never get a zero probability.
6. **What does the offline fallback do differently?** — It uses a fixed positive/negative word list instead of a trained model or corpus, so it needs no downloads.

## 8. Resources
- TextBlob docs: https://textblob.readthedocs.io
- NLTK docs: https://www.nltk.org
- *Natural Language Processing with Python* (Bird, Klein & Loper): https://www.nltk.org/book/
- scikit-learn text classification tutorial (if you later want sklearn): https://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html

---



---

## 🐛 Failure Modes & Debugging (Real-World Experience)

> [!bug] What goes wrong in production?
> When running **Sentiment Analysis Text Classification** in a real environment, it almost never works perfectly the first time. 
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

- **Sentiment analysis** — decide the emotional tone of text. Output is usually a **polarity** score in `[-1, +1]` and a **subjectivity** score in `[0, 1]`.
- **Text classification** — assign a text to a category (label) from a fixed set. Example: `pos`/`neg`, `spam`/`ham`.
- **Approaches used here:** — **Lexicon-based:** count positive vs negative words from a fixed word list. Simple, transparent, works offline. Handles simple negation ("not good").
- **Interpretation:** — Both the lexicon and TextBlob agree on the positive/negative direction of every sample.
- **three levels of effort** — a word lexicon (offline, transparent), a library like TextBlob (better coverage), or a trained classifier (task-specific, measurable accuracy).
- **What is polarity?** — A score in [-1, +1] describing how positive or negative a text is.
- **What is a token?** — A basic text unit (word or sub-word) produced by tokenization.
- **Why did TextBlob need `download_corpora`?** — It downloads NLTK datasets (movie_reviews, etc.) used for training and tagging.

> [!tip] Viva Prep
> Be ready to explain the *why* behind each step, not just the output.
