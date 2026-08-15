"""P02 - Offline fallback: pure-Python lexicon sentiment classifier.

No external libraries and no network needed. Use this on a machine where
`textblob` / its corpora cannot be installed or downloaded.

Run:  python3 p02_lexicon_fallback.py
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


def classify(text: str) -> dict:
    """Return {'polarity', 'label', 'pos', 'neg'} for a text."""
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
    return {"polarity": score, "label": label, "pos": pos, "neg": neg}


def main() -> None:
    print("=" * 72)
    print("P02 (offline fallback): Lexicon-based sentiment classifier")
    print("=" * 72)
    samples = [
        "This product is amazing and I love it!",
        "This product is terrible and I hate it.",
        "The movie was okay, nothing special.",
        "The service was good, but the room was not great.",
        "Customer support was very helpful and friendly.",
        "The app crashed repeatedly, extremely frustrating.",
    ]
    for s in samples:
        r = classify(s)
        print(f"  polarity={r['polarity']:+.2f}  pos={r['pos']} neg={r['neg']}"
              f"  -> {r['label']:<8} | {s}")


if __name__ == "__main__":
    sys.exit(main())
