"""Lightweight, transparent NLP scoring for diary works.

No heavy model downloads: everything here is lexical and rule-based, which is
robust to the noisy OCR of scanned handwriting and fully explainable. The goal is
to tell apart, at the *work* level:

  * English vs non-English            -> `english_ratio` (stopword density)
  * personal narrative vs field notes -> `firstperson`, `everyday`, `drama`
                                          vs `naturalist` (field-note markers)
  * substantial journal vs fragment   -> `n_words`

`score_text()` returns a Features object; `narrative_score()` combines the signals
with configurable weights. Densities are per 1,000 words so they compare across
works of different lengths.
"""
from __future__ import annotations

import re
from dataclasses import asdict, dataclass

# Core English function words — dense in any real English prose, rare elsewhere.
_STOPWORDS = {
    "the", "and", "of", "to", "a", "in", "that", "it", "is", "was", "i", "for",
    "on", "with", "as", "at", "by", "he", "she", "we", "they", "you", "this",
    "but", "his", "her", "had", "have", "not", "be", "are", "from", "or", "an",
    "were", "which", "our", "all", "my", "me", "so", "very", "there", "their",
    "when", "who", "them", "then", "would", "will", "no", "if", "out", "up",
    "into", "about", "some", "more", "one", "been", "has", "did", "do", "us",
}

_FIRSTPERSON = {"i", "me", "my", "mine", "we", "our", "ours", "us", "myself"}

# Everyday / domestic-social life.
_EVERYDAY = {
    "home", "house", "family", "mother", "father", "mama", "papa", "wife",
    "husband", "son", "daughter", "child", "children", "baby", "brother",
    "sister", "aunt", "uncle", "cousin", "friend", "friends", "neighbour",
    "neighbor", "dinner", "supper", "breakfast", "tea", "dine", "cooked",
    "kitchen", "church", "sermon", "prayer", "school", "lesson", "letter",
    "letters", "wrote", "write", "money", "shop", "market", "town", "village",
    "street", "work", "worked", "farm", "field", "garden", "married",
    "marriage", "wedding", "visit", "visited", "called", "company", "party",
    "danced", "sang", "talked", "walked", "rode", "bed", "morning", "evening",
    "night", "sunday", "monday", "husbandry", "servant", "washing", "sewing",
}

# Drama / emotional intensity / eventful.
_DRAMA = {
    "death", "died", "dead", "dying", "grave", "buried", "funeral", "ill",
    "illness", "sick", "sickness", "fever", "pain", "blood", "wound",
    "wounded", "fear", "afraid", "terror", "dread", "wept", "weeping", "cried",
    "crying", "tears", "grief", "sorrow", "misery", "despair", "love", "loved",
    "dear", "heart", "passion", "quarrel", "angry", "anger", "rage", "fight",
    "fought", "battle", "war", "enemy", "killed", "murder", "fire", "burned",
    "storm", "flood", "wreck", "escape", "danger", "terrible", "dreadful",
    "awful", "joy", "happy", "delight", "hope", "prayed", "god", "soul",
    "drunk", "drink", "poor", "starving", "hunger", "cold", "wretched",
}

# Naturalist field-note vocabulary (penalize).
_NATURALIST = {
    "specimen", "specimens", "species", "genus", "genera", "plumage",
    "nest", "nests", "eggs", "clutch", "migration", "migrant", "warbler",
    "warblers", "sparrow", "sparrows", "thrush", "hawk", "heron", "duck",
    "flycatcher", "plover", "sandpiper", "gull", "fern", "ferns", "moss",
    "lichen", "flora", "fauna", "foliage", "petals", "stamens", "leaflet",
    "botanical", "zoological", "ornithology", "naturalist", "collected",
    "observed", "observation", "measured", "length", "wing", "bill", "tail",
    "feathers", "breeding", "habitat", "flock", "flowering", "blossom",
    "pollen", "insect", "insects", "beetle", "larva", "moth", "butterfly",
    "frond", "seedling", "meadow", "swamp",
}

_WORD_RE = re.compile(r"[A-Za-z']+")
# A capitalized word followed by a lowercase word — approximates Latin binomials
# (Turdus migratorius) that pepper naturalist notes.
_BINOMIAL_RE = re.compile(r"\b[A-Z][a-z]{2,} [a-z]{3,}\b")
# Measurement / temperature tokens common in field notes.
_MEASURE_RE = re.compile(r"(\d+\s?°|\b\d+\s?(deg|mm|cm|in|ft|oz|lbs?)\b|\b\d+\.\d+\b)")


@dataclass
class Features:
    n_words: int
    english_ratio: float
    firstperson: float        # per 1000 words
    everyday: float           # per 1000 words
    drama: float              # per 1000 words
    naturalist: float         # per 1000 words (measurements/binomials folded in)

    def as_dict(self) -> dict:
        return asdict(self)


def score_text(text: str) -> Features:
    tokens = [t.lower() for t in _WORD_RE.findall(text)]
    n = len(tokens)
    if n == 0:
        return Features(0, 0.0, 0.0, 0.0, 0.0, 0.0)

    per_k = 1000.0 / n

    stop = sum(1 for t in tokens if t in _STOPWORDS)
    fp = sum(1 for t in tokens if t in _FIRSTPERSON)
    ev = sum(1 for t in tokens if t in _EVERYDAY)
    dr = sum(1 for t in tokens if t in _DRAMA)
    nat = sum(1 for t in tokens if t in _NATURALIST)

    # Fold structural field-note markers into the naturalist signal.
    binomials = len(_BINOMIAL_RE.findall(text))
    measures = len(_MEASURE_RE.findall(text))
    nat_total = nat + 0.5 * binomials + 0.5 * measures

    return Features(
        n_words=n,
        english_ratio=stop / n,
        firstperson=fp * per_k,
        everyday=ev * per_k,
        drama=dr * per_k,
        naturalist=nat_total * per_k,
    )


def narrative_score(f: Features, weights: dict) -> float:
    w_ev = float(weights.get("everyday", 1.0))
    w_dr = float(weights.get("drama", 1.0))
    w_fp = float(weights.get("firstperson", 0.5))
    w_nat = float(weights.get("naturalist", 1.0))
    return w_ev * f.everyday + w_dr * f.drama + w_fp * f.firstperson - w_nat * f.naturalist


def count_words(text: str) -> int:
    return len(_WORD_RE.findall(text))
