"""Curation: score every work and select long, English, narrative journals.

Runs after `segment`. For each work it concatenates its entry text, computes NLP
features (diarycorpus/nlp.py), writes them to the store, and marks the work
`selected` when it passes the gates:

    english_ratio >= english_min      (it's really English)
    n_words       >= min_words        (a substantial journal, not a fragment)
    naturalist    <= naturalist_max   (not a field notebook)
    narrative_score >= narrative_min  (reads as everyday-life / dramatic narrative)

Per the user's choice, there is no top-N cap: every work clearing the gates is
kept. Micro-entries within a kept work are pruned (min_entry_words).
"""
from __future__ import annotations

from .config import Config
from .nlp import Features, narrative_score, score_text
from .store import Store


def curate(config: Config) -> dict:
    opts = config.curate or {}
    min_words = int(opts.get("min_words", 2000))
    min_entry_words = int(opts.get("min_entry_words", 40))
    english_min = float(opts.get("english_min", 0.16))
    naturalist_max = float(opts.get("naturalist_max", 12.0))
    narrative_min = float(opts.get("narrative_min", 0.0))
    weights = opts.get("weights", {}) or {}

    selected, rejected = 0, 0
    reasons: dict[str, int] = {}
    kept_rows = []

    with Store(config.db_path) as store:
        works = store.all_works()
        if not works:
            print("[curate] no works in store — run harvest + segment first")
            return {"selected": 0, "total": 0}

        for w in works:
            entries = store.get_entries(w["id"])
            text = "\n".join(e["text"] for e in entries)
            f = score_text(text)
            ns = narrative_score(f, weights)

            ok, why = _passes(f, ns, min_words, english_min, naturalist_max, narrative_min)
            scores = {**f.as_dict(), "narrative_score": ns}
            store.set_work_scores(w["id"], scores, selected=ok)

            if ok:
                store.delete_entries_below(w["id"], min_entry_words)
                selected += 1
                kept_rows.append((ns, w["title"], f))
            else:
                rejected += 1
                reasons[why] = reasons.get(why, 0) + 1

    # Report, best first.
    kept_rows.sort(reverse=True, key=lambda r: r[0])
    print(f"[curate] selected {selected} / {len(works)} works "
          f"(gates: words>={min_words}, english>={english_min}, "
          f"naturalist<={naturalist_max})")
    if reasons:
        print("  rejected because: " +
              ", ".join(f"{k}={v}" for k, v in sorted(reasons.items())))
    for ns, title, f in kept_rows[:12]:
        print(f"  [keep] score={ns:6.1f}  words={f.n_words:>6}  "
              f"ev={f.everyday:4.1f} dr={f.drama:4.1f} nat={f.naturalist:4.1f}  "
              f"{(title or '')[:48]}")
    return {"selected": selected, "total": len(works)}


def _passes(f: Features, ns: float, min_words: int, english_min: float,
            naturalist_max: float, narrative_min: float) -> tuple[bool, str]:
    if f.n_words < min_words:
        return False, "too_short"
    if f.english_ratio < english_min:
        return False, "not_english"
    if f.naturalist > naturalist_max:
        return False, "naturalist"
    if ns < narrative_min:
        return False, "low_narrative"
    return True, ""
