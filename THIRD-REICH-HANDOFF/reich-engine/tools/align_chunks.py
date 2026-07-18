#!/usr/bin/env python3
"""Map each transcribed audio chunk to a span of the bracket-tagged script,
using fuzzy block matching (robust to pocketsphinx noise). Reports coverage + gaps."""
import json, os, re, difflib

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CHUNKS = os.path.join(BASE, "public", "audio", "special-legal-coup-1919-1933", "_chunks")
SCRIPT = os.path.abspath(os.path.join(BASE, "..", "episodes", "special-legal-coup-1919-1933", "script-final.md"))
TRANS = json.load(open(os.path.join(CHUNKS, "_transcripts.json")))

def norm(w): return re.sub(r"[^a-z0-9]", "", w.lower())

# Build script word list with per-word beat tag
raw = open(SCRIPT, encoding="utf-8").read()
# keep body between first (1) and Sources
body = raw[raw.find("(1)"): raw.find("## Sources")]
tokens = []   # (word_norm, beat_tag)
cur = None
i = 0
for m in re.finditer(r"\(((?:\d+|Q\d+|H\d+))\)|([A-Za-z0-9']+)", body):
    if m.group(1) is not None:
        tag = m.group(1)
        cur = tag if cur != tag else None  # toggle open/close
        # opening tag sets current; closing (same tag) clears
        cur = tag if (cur is not None) else None
        # simpler: track open span
    else:
        w = norm(m.group(2))
        if w: tokens.append((w, cur))
# Recompute beat tags cleanly with an explicit open/close scan
tokens = []
open_tag = None
pos = 0
for m in re.finditer(r"\(((?:\d+|Q\d+|H\d+))\)|([A-Za-z0-9']+)", body):
    if m.group(1) is not None:
        t = m.group(1)
        open_tag = None if open_tag == t else t
    else:
        w = norm(m.group(2))
        if w: tokens.append((w, open_tag))
script_words = [w for w, _ in tokens]

def beat_at(idx):
    return tokens[idx][1] if 0 <= idx < len(tokens) else None

# order chunks by filename timestamp
names = sorted(TRANS.keys())
results = []
for name in names:
    cw = [norm(x["w"]) for x in TRANS[name]["words"] if norm(x["w"])]
    sm = difflib.SequenceMatcher(None, script_words, cw, autojunk=False)
    blocks = [b for b in sm.get_matching_blocks() if b.size >= 2]
    if not blocks:
        results.append((name, None, None, 0)); continue
    # script coverage = from first matched script idx to last matched script idx+size
    a0 = min(b.a for b in blocks)
    a1 = max(b.a + b.size for b in blocks)
    matched = sum(b.size for b in blocks)
    results.append((name, a0, a1, matched, len(cw)))

print(f"script total words: {len(script_words)}")
print(f"{'chunk':<42} {'begins~beat':>11} {'ends~beat':>9} {'matched':>8} {'asr_w':>6}")
covered_beats = set()
for r in results:
    name = r[0]
    if r[1] is None:
        print(f"{name:<42} {'NO MATCH':>11}"); continue
    a0, a1, matched, asrw = r[1], r[2], r[3], r[4]
    b0, b1 = beat_at(a0), beat_at(a1-1)
    for i in range(a0, a1):
        t = beat_at(i)
        if t: covered_beats.add(t)
    print(f"{name:<42} {str(b0):>11} {str(b1):>9} {matched:>8} {asrw:>6}")

# coverage report over all numeric+Q+H beats present in script
all_beats = []
seen=set()
for _, t in tokens:
    if t and t not in seen:
        seen.add(t); all_beats.append(t)
missing = [b for b in all_beats if b not in covered_beats]
print(f"\nBEATS IN SCRIPT: {len(all_beats)} | COVERED: {len(covered_beats)} | MISSING: {len(missing)}")
print("MISSING beats:", ", ".join(missing))
