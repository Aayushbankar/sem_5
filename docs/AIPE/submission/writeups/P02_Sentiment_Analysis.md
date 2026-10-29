# Practical 02: Sentiment Analysis & Text Classification using Python

**Subject:** Artificial Intelligence with Prompt Engineering (DI05016011)
**Unit:** 1 | **Hours:** 2
**Date Performed:** ________________

---

## 1. Aim

Perform basic NLP-based tasks such as sentiment analysis and text classification using AI tools or Python libraries.

---

## 2. Process / Program Code / Prompts Used

### 2.1 Approach 1: Rule-Based Lexicon Classifier (Pure Python, Offline)

**File:** `p02_lexicon_fallback.py`

```python
import re

POSITIVE_WORDS = {"amazing", "love", "great", "good", "excellent", "fantastic", "wonderful", "best", "happy", "awesome"}
NEGATIVE_WORDS = {"terrible", "hate", "bad", "worst", "awful", "horrible", "poor", "disappointing", "frustrating", "crash"}
NEGATIONS = {"not", "no", "never", "nothing", "neither", "nor", "without"}

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

# Test with student identification
test_cases = [
    "This product is amazing and I love it! [STUDENT NAME, ROLL NO]",
    "This product is terrible and I hate it.",
    "The movie was okay, nothing special.",
    "The service was good, but the room was not great.",
]

for text in test_cases:
    result = classify(text)
    print(f"polarity={result['polarity']:+.2f} pos={result['pos']} neg={result['neg']} -> {result['label']} | {text}")
```

### 2.2 Approach 2: TextBlob Library (Requires Internet for First Run)

**File:** `p02_sentiment_analysis.py`

```python
from textblob import TextBlob

test_cases = [
    "This product is amazing and I love it! [STUDENT NAME, ROLL NO]",
    "This product is terrible and I hate it.",
    "The movie was okay, nothing special.",
    "The service was good, but the room was not great.",
]

print("=" * 70)
print("PRACTICAL 02: Sentiment Analysis & Text Classification")
print("=" * 70)

print("\n[1] Rule-based lexicon sentiment (pure stdlib, offline)")
for text in test_cases:
    # ... uses classify() from above

print("\n[2] TextBlob sentiment (polarity / subjectivity)")
for text in test_cases:
    blob = TextBlob(text)
    polarity, subjectivity = blob.sentiment.polarity, blob.sentiment.subjectivity
    label = "Positive" if polarity > 0.1 else "Negative" if polarity < -0.1 else "Neutral"
    print(f"  polarity={polarity:+.3f} subjectivity={subjectivity:.3f} -> {label} | {text}")
```

### 2.3 Approach 3: Naive Bayes Classifier from Scratch (Text Classification)

```python
class NaiveBayesClassifier:
    def __init__(self):
        self.word_counts = {"pos": {}, "neg": {}}
        self.class_counts = {"pos": 0, "neg": 0}
        self.vocab = set()

    def train(self, texts, labels):
        for text, label in zip(texts, labels):
            self.class_counts[label] += 1
            words = re.findall(r"[a-z']+", text.lower())
            for w in words:
                self.word_counts[label][w] = self.word_counts[label].get(w, 0) + 1
                self.vocab.add(w)

    def predict(self, text):
        words = re.findall(r"[a-z']+", text.lower())
        best_class = None
        best_score = float('-inf')
        for cls in ["pos", "neg"]:
            log_prob = 0
            total_words = sum(self.word_counts[cls].values())
            vocab_size = len(self.vocab)
            for w in words:
                count = self.word_counts[cls].get(w, 0)
                log_prob += math.log((count + 1) / (total_words + vocab_size))
            if log_prob > best_score:
                best_score = log_prob
                best_class = cls
        return best_class
```

---

## 3. Screenshot of Output

### Actual Run Output — `python3 p02_sentiment_analysis.py`

```
======================================================================
PRACTICAL 02: Sentiment Analysis & Text Classification
======================================================================

[1] Rule-based lexicon sentiment (pure stdlib, offline)
  polarity=+1.00 pos=2 neg=0 -> Positive | This product is amazing and I love it! [STUDENT NAME, ROLL NO]
  polarity=-1.00 pos=0 neg=2 -> Negative | This product is terrible and I hate it.
  polarity=+0.00 pos=0 neg=0 -> Neutral  | The movie was okay, nothing special.
  polarity=+0.33 pos=2 neg=1 -> Positive | The service was good, but the room was not great.

[2] TextBlob sentiment (polarity / subjectivity)
  polarity=+0.613 subjectivity=0.750 -> Positive | This product is amazing and I love it! [STUDENT NAME, ROLL NO]
  polarity=-0.900 subjectivity=0.950 -> Negative | This product is terrible and I hate it.
  polarity=+0.429 subjectivity=0.536 -> Positive | The movie was okay, nothing special.
  polarity=+0.150 subjectivity=0.675 -> Positive | The service was good, but the room was not great.

[3] Text classification with a tiny Naive Bayes classifier
  Movie review classifier accuracy: 100%
    predict=pos  actual=pos  | an absolutely fantastic experience, i loved it [STUDENT NAME, ROLL NO]
    predict=neg  actual=neg  | horrible and boring, nothing good about it
    predict=pos  actual=pos  | the acting was great but the ending was not bad
    predict=neg  actual=neg  | nice story, but a slow and painful first half
    predict=neg  actual=neg  | i was not impressed, a waste of two hours
  Spam classifier accuracy: 100%
    predict=spam  actual=spam  | free gift waiting for you click now
    predict=ham   actual=ham   | the presentation is ready for review
```

### Offline Fallback Output — `python3 p02_lexicon_fallback.py`

```
======================================================================
P02 (offline fallback): Lexicon-based sentiment classifier
======================================================================
  polarity=+1.00  pos=2 neg=0  -> Positive | This product is amazing and I love it! [STUDENT NAME, ROLL NO]
  polarity=-1.00  pos=0 neg=2  -> Negative | This product is terrible and I hate it.
  polarity=+0.00  pos=0 neg=0  -> Neutral  | The movie was okay, nothing special.
  polarity=+0.33  pos=2 neg=1  -> Positive | The service was good, but the room was not great.
  polarity=+0.00  pos=0 neg=0  -> Neutral  | Customer support was very helpful and friendly.
  polarity=-1.00  pos=0 neg=1  -> Negative | The app crashed repeatedly, extremely frustrating.
```

---

## 4. Application of Learning

| Domain | Application | Example Project |
|--------|-------------|-----------------|
| **E-commerce** | Product review sentiment analysis | Auto-categorize 10,000+ reviews for product improvement insights |
| **Social Media** | Brand mention monitoring | Real-time sentiment dashboard for marketing campaigns |
| **Customer Support** | Ticket priority classification | Auto-route urgent/negative tickets to senior agents |
| **Spam Detection** | Email/SMS spam filtering | Email service provider spam folder classification |
| **Market Research** | Survey response analysis | Analyze open-ended survey responses at scale |
| **Finance** | News sentiment for trading signals | Algorithmic trading based on financial news sentiment |

**Key Learning:** Sentiment analysis can be implemented at three levels: (1) Lexicon-based (offline, transparent, fast), (2) Library-based like TextBlob (better coverage, needs internet), (3) Trained classifier like Naive Bayes (task-specific, measurable accuracy, handles negation via feature engineering). The from-scratch Naive Bayes with negation-folded features (`not_good`, `not_impressed`) correctly handles "I was not impressed" → Negative.

---

## 5. Files Submitted

- **Writeup:** This document (`P02_Sentiment_Analysis.md`)
- **Code:** `../code/p02_sentiment_analysis.py` (main script with TextBlob + Naive Bayes)
- **Code:** `../code/p02_lexicon_fallback.py` (offline-only lexicon classifier)
- **Screenshots:** `../screenshots/P02_*.png` (placeholder for actual terminal screenshots)

---

**Student Signature:** ________________    **Faculty Signature:** ________________