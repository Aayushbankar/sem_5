"""P02 - Sentiment analysis and text classification.

Three self-contained demos:
  [1] Rule-based lexicon sentiment analysis (pure stdlib, works offline).
  [2] TextBlob sentiment (polarity + subjectivity) when the library is present.
  [3] A tiny Naive Bayes text classifier written from scratch (no sklearn).

Run:  python3 p02_sentiment_analysis.py
"""

import re
import sys

POSITIVE_WORDS = {
    "amazing", "awesome", "best", "brilliant", "delicious", "excellent",
    "fantastic", "good", "great", "happy", "impressive", "incredible",
    "loved", "love", "nice", "outstanding", "perfect", "recommend",
    "superb", "terrific", "wonderful", "wow", "beautiful", "enjoyed",
}
NEGATIVE_WORDS = {
    "awful", "bad", "boring", "broken", "disappointing", "dreadful",
    "hated", "hate", "horrible", "poor", "terrible", "worst", "waste",
    "useless", "unhelpful", "laggy", "slow", "confusing", "painful",
    "refund", "disgusting", "frustrating", "buggy",
}
NEGATIONS = {"not", "no", "never", "neither", "nor", "hardly"}


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z']+", text.lower())


def tokenize_nb(text: str) -> list[str]:
    """Tokenizer with negation folding: 'not good' becomes 'not_good'."""
    words = tokenize(text)
    out = []
    i = 0
    while i < len(words):
        w = words[i]
        if w in NEGATIONS and i + 1 < len(words):
            out.append(w + "_" + words[i + 1])
            i += 2
        else:
            out.append(w)
            i += 1
    return out


def lexicon_sentiment(text: str):
    """Pure-stdlib sentiment: counts positive vs negative words.

    Handles simple negation: 'not good' flips one following positive word.
    """
    words = tokenize(text)
    pos = neg = 0
    for i, w in enumerate(words):
        if w in NEGATIONS and i + 1 < len(words):
            nxt = words[i + 1]
            if nxt in POSITIVE_WORDS:
                neg += 1
            elif nxt in NEGATIVE_WORDS:
                pos += 1
            continue
        if w in POSITIVE_WORDS:
            pos += 1
        elif w in NEGATIVE_WORDS:
            neg += 1
    score = (pos - neg) / max(1, pos + neg)
    label = "Positive" if score > 0.2 else "Negative" if score < -0.2 else "Neutral"
    return score, label, pos, neg


def textblob_sentiment(text: str):
    from textblob import TextBlob  # lazy import: only if installed

    s = TextBlob(text).sentiment
    label = "Positive" if s.polarity > 0.1 else "Negative" if s.polarity < -0.1 else "Neutral"
    return s.polarity, s.subjectivity, label


# ---------------------------------------------------------------------------
# Tiny Naive Bayes classifier (multinomial, add-1 smoothing) - no external deps
# ---------------------------------------------------------------------------
class NaiveBayes:
    def __init__(self):
        self.classes = []
        self.vocab = set()
        self.priors = {}
        self.word_counts = {}
        self.class_totals = {}

    def fit(self, X, y):
        self.classes = sorted(set(y))
        docs_per_class = {c: 0 for c in self.classes}
        for c in y:
            docs_per_class[c] += 1
        n_docs = len(y)
        self.priors = {c: docs_per_class[c] / n_docs for c in self.classes}
        self.word_counts = {c: {} for c in self.classes}
        self.class_totals = {c: 0 for c in self.classes}
        for text, c in zip(X, y):
            for w in tokenize_nb(text):
                self.vocab.add(w)
                self.word_counts[c][w] = self.word_counts[c].get(w, 0) + 1
                self.class_totals[c] += 1

    def _log_prob(self, w, c):
        return __import__("math").log(
            (self.word_counts[c].get(w, 0) + 1) / (self.class_totals[c] + len(self.vocab))
        )

    def predict(self, text):
        best_c, best_p = None, float("-inf")
        for c in self.classes:
            p = __import__("math").log(self.priors[c])
            for w in tokenize_nb(text):
                p += self._log_prob(w, c)
            if p > best_p:
                best_c, best_p = c, p
        return best_c

    def accuracy(self, X, y):
        correct = sum(1 for t, c in zip(X, y) if self.predict(t) == c)
        return correct / len(y)


MOVIE_TRAIN = [
    ("this film was amazing and i loved every scene", "pos"),
    ("a brilliant movie with great acting", "pos"),
    ("wonderful story, i really enjoyed it", "pos"),
    ("fantastic soundtrack and superb direction", "pos"),
    ("the ending was perfect, truly impressive", "pos"),
    ("an outstanding performance from the whole cast", "pos"),
    ("this movie was terrible and boring", "neg"),
    ("awful acting, a complete waste of time", "neg"),
    ("the plot was confusing and the pace was slow", "neg"),
    ("i hated this film, disappointing from start to finish", "neg"),
    ("poor script, dreadful performances", "neg"),
    ("not a good film, really disappointing", "neg"),
    ("not bad at all, surprisingly enjoyable", "pos"),
]
MOVIE_TEST = [
    ("an absolutely fantastic experience, i loved it", "pos"),
    ("horrible and boring, nothing good about it", "neg"),
    ("the acting was great but the ending was not bad", "pos"),
    ("nice story, but a slow and painful first half", "neg"),
    ("i was not impressed, a waste of two hours", "neg"),
]

SPAM_TRAIN = [
    ("win a free iphone now click this link", "spam"),
    ("congratulations you have won a lottery prize", "spam"),
    ("cheap pills for sale limited time offer", "spam"),
    ("claim your reward before midnight today", "spam"),
    ("urgent transfer needed from your bank account", "spam"),
    ("meeting at 4pm tomorrow in room 12", "ham"),
    ("the assignment is due on friday please submit", "ham"),
    ("can you review the slides before class", "ham"),
    ("lunch with the team at the usual place", "ham"),
    ("here are the minutes of the last meeting", "ham"),
]
SPAM_TEST = [
    ("free gift waiting for you click now", "spam"),
    ("the presentation is ready for review", "ham"),
]


def main() -> None:
    print("=" * 72)
    print("PRACTICAL 02: Sentiment Analysis & Text Classification")
    print("=" * 72)

    print("\n[1] Rule-based lexicon sentiment (pure stdlib, offline)")
    samples = [
        "This product is amazing and I love it!",
        "This product is terrible and I hate it.",
        "The movie was okay, nothing special.",
        "The service was good, but the room was not great.",
    ]
    for s in samples:
        score, label, pos, neg = lexicon_sentiment(s)
        print(f"  polarity={score:+.2f} pos={pos} neg={neg} -> {label:<8} | {s}")

    print("\n[2] TextBlob sentiment (polarity / subjectivity)")
    try:
        textblob_sentiment("test")
        for s in samples:
            pol, subj, label = textblob_sentiment(s)
            print(f"  polarity={pol:+.3f} subjectivity={subj:.3f} -> {label:<8} | {s}")
    except ImportError:
        print("  [!] textblob not installed - skipping (lexicon fallback still works)")

    print("\n[3] Text classification with a tiny Naive Bayes classifier")
    movie_nb = NaiveBayes()
    movie_nb.fit(*zip(*MOVIE_TRAIN))
    print(f"  Movie review classifier accuracy: "
          f"{movie_nb.accuracy(*zip(*MOVIE_TEST)):.0%}")
    for text, _ in MOVIE_TEST:
        print(f"    predict={movie_nb.predict(text):<4} actual={_:<4} | {text}")

    spam_nb = NaiveBayes()
    spam_nb.fit(*zip(*SPAM_TRAIN))
    print(f"  Spam classifier accuracy: {spam_nb.accuracy(*zip(*SPAM_TEST)):.0%}")
    for text, _ in SPAM_TEST:
        print(f"    predict={spam_nb.predict(text):<5} actual={_:<5} | {text}")


if __name__ == "__main__":
    sys.exit(main())
