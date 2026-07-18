#!/usr/bin/env python3
"""Concatenate the 17 narration chunks (chronological = script order) and compute
per-beat timing on the global timeline, anchored per-chunk (drift resets each chunk).

Method: each chunk's start beat is found by matching its ASR words to the script;
beats are partitioned to chunks accordingly; within a chunk each beat's duration is
its share of the chunk's real audio duration, weighted by script word count.
Outputs beat_timing.json and concatenates narration.mp3.
"""
import json, os, re, difflib, subprocess, imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
BASE = os.path.abspath("..")
CH = os.path.join(BASE, "public", "audio", "special-legal-coup-1919-1933", "_chunks")
OUTDIR = os.path.join(BASE, "public", "audio", "special-legal-coup-1919-1933")
SCRIPT = os.path.abspath(os.path.join(BASE, "..", "episodes", "special-legal-coup-1919-1933", "script-final.md"))
TR = json.load(open(os.path.join(CH, "_transcripts.json")))

def norm(w): return re.sub(r"[^a-z0-9]", "", w.lower())

# --- script tokens with beat tag + ordered beat list with word counts ---
raw = open(SCRIPT, encoding="utf-8").read()
body = raw[raw.find("(1)"): raw.find("## Sources")]
tokens = []; open_tag = None
for m in re.finditer(r"\(((?:\d+|Q\d+|H\d+))\)|([A-Za-z0-9']+)", body):
    if m.group(1) is not None:
        t = m.group(1); open_tag = None if open_tag == t else t
    else:
        w = norm(m.group(2))
        if w: tokens.append((w, open_tag))
sw = [w for w, _ in tokens]
beat_order = []; beat_wc = {}
for w, t in tokens:
    if t is None: continue
    if t not in beat_wc: beat_wc[t] = 0; beat_order.append(t)
    beat_wc[t] += 1
first_idx = {}
for i, (w, t) in enumerate(tokens):
    if t and t not in first_idx: first_idx[t] = i

def dur(mp3):
    s = subprocess.run([FF, "-i", mp3], capture_output=True, text=True).stderr
    d = s.split("Duration:")[1].split(",")[0].strip(); h, m, se = d.split(":")
    return int(h)*3600 + int(m)*60 + float(se)

# --- order chunks chronologically (filename timestamp) & find each start beat ---
names = sorted(TR.keys())  # ISO timestamp in name sorts chronologically
def start_word_idx(asr_words):
    cw = [norm(x["w"]) for x in asr_words if norm(x["w"])]
    sm = difflib.SequenceMatcher(None, sw, cw, autojunk=False)
    big = [b for b in sm.get_matching_blocks() if b.size >= 4]
    if not big: big = [max(sm.get_matching_blocks(), key=lambda x: x.size)]
    # earliest robust anchor whose asr position is also near the start
    big.sort(key=lambda b: b.b)  # by asr order
    return min(b.a for b in big[:3])  # script idx of one of the first anchors

chunks = []
for nm in names:
    swi = start_word_idx(TR[nm]["words"])
    chunks.append({"name": nm, "start_word": swi, "dur": dur(os.path.join(CH, nm))})
# enforce monotonic start_word (chronological should already be increasing)
for i in range(1, len(chunks)):
    if chunks[i]["start_word"] <= chunks[i-1]["start_word"]:
        chunks[i]["start_word"] = chunks[i-1]["start_word"] + 1

# start beat for each chunk = beat tag at its start_word (walk forward to a tagged token)
def beat_at_word(idx):
    for j in range(idx, len(tokens)):
        if tokens[j][1]: return tokens[j][1]
    return beat_order[-1]
for c in chunks: c["start_beat"] = beat_at_word(c["start_word"])

# partition beats to chunks by start_beat boundaries (beat_order sequence)
bpos = {b: i for i, b in enumerate(beat_order)}
for i, c in enumerate(chunks):
    lo = bpos[c["start_beat"]]
    hi = bpos[chunks[i+1]["start_beat"]] if i+1 < len(chunks) else len(beat_order)
    c["beats"] = beat_order[lo:hi]

# --- concat narration in order ---
listf = os.path.join(CH, "_concat.txt")
open(listf, "w").write("".join(f"file '{os.path.join(CH,c['name'])}'\n" for c in chunks))
narr = os.path.join(OUTDIR, "narration.mp3")
subprocess.run([FF, "-loglevel","error","-y","-f","concat","-safe","0","-i",listf,"-c","copy",narr], check=True)

# --- per-beat global timing: proportional-by-wordcount within each chunk's real duration ---
timing = {}; t0 = 0.0
for c in chunks:
    tot_wc = sum(beat_wc.get(b, 1) for b in c["beats"]) or 1
    local = 0.0
    for b in c["beats"]:
        share = beat_wc.get(b, 1) / tot_wc * c["dur"]
        timing[b] = {"start": round(t0 + local, 3), "dur": round(share, 3)}
        local += share
    t0 += c["dur"]

json.dump({"chunks":[{k:c[k] for k in ("name","start_beat","dur","beats")} for c in chunks],
           "beats": timing}, open(os.path.join(OUTDIR,"beat_timing.json"),"w"), indent=1)
print("chunks (chrono) -> start_beat / #beats / dur:")
for c in chunks:
    print(f"  {c['name'][-13:-4]}  start={c['start_beat']:>4}  beats={len(c['beats']):>2}  {c['dur']:.1f}s  [{c['beats'][0]}..{c['beats'][-1]}]")
print(f"\ntotal beats timed: {len(timing)} / {len(beat_order)} | narration: {sum(c['dur'] for c in chunks)/60:.1f} min")
print("wrote narration.mp3 + beat_timing.json")
