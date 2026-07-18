#!/usr/bin/env python3
"""Write the full per-section music cue timeline into active-episode.json.
Cues are placed for dramatic effect (not wall-to-wall); silences are deliberate."""
import json, os, subprocess, imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
BASE = os.path.abspath("..")
MUS = os.path.join(BASE, "public", "audio", "special-legal-coup-1919-1933", "music")
SPEC = os.path.join(BASE, "src", "active-episode.json")
FPS = 30

TRACK_VOL = {"A": 0.166, "B": 0.129, "C": 0.084, "D": 0.107}
def tlen(t):
    s = subprocess.run([FF,"-i",os.path.join(MUS,f"music-{t}.mp3")],capture_output=True,text=True).stderr
    d=s.split("Duration:")[1].split(",")[0].strip(); h,m,se=d.split(":"); return int(h)*3600+int(m)*60+float(se)
TLEN = {t: tlen(t) for t in TRACK_VOL}

# (start_s, dur_s, track, startFrom_s, vol_override)  — silences are the gaps
plan = [
 (0,    32,  "A", 0,   None),  # cold open — ominous hook
 (32,   150, "B", 0,   None),  # the founding lie / stab-in-the-back — somber
 (210,  65,  "D", 0,   None),  # seizing the party — cold menace
 # — SILENCE 4:39 Weimar's rigged justice (assassinations) —
 (322,  93,  "C", 0,   None),  # the Beer Hall Putsch — building tension
 # — SILENCE ~6:57 the 16 dead —
 (448,  72,  "B", 10,  None),  # trial & Landsberg — reflective
 (523,  32,  "A", 0,   None),  # the pivot: the "legal way" (Q6)
 (565,  58,  "D", 20,  None),  # building the shadow state
 (632,  85,  "D", 70,  0.09),  # Strasser/Goebbels fight — softer
 # — SILENCE 11:57 the diary entries —
 (800,  95,  "C", 5,   None),  # 1928 flop -> the Crash hits
 (900,  100, "C", 0,   None),  # Article 48 + the 1930 breakthrough
 (1025, 100, "D", 0,   None),  # Harzburg / 1932 race
 (1170, 65,  "D", 90,  None),  # Schleicher's intrigues
 # — SILENCE 20:37 Prussia deposed —
 (1280, 55,  "B", 90,  None),  # the peak — and the decline
 (1340, 150, "D", 0,   None),  # Strasser crisis / secret deals — claustrophobic
 (1495, 68,  "C", 10,  None),  # Ribbentrop stitch-up -> chancellorship
 # — SILENCE 26:06 the hollow chancellorship (builds to the fire) —
 (1658, 54,  "C", 0,   0.095), # THE REICHSTAG FIRE — dramatic
 (1713, 148, "D", 0,   None),  # legal architecture locks in / Enabling Act — grim finale
 (1863, 48,  "B", 0,   0.10),  # closing thought — thin to near-silence
]

cues=[]
for start_s, dur_s, tr, sf, volo in plan:
    maxdur = TLEN[tr] - sf - 0.2
    d = min(dur_s, maxdur)
    if d <= 1: continue
    cues.append({
        "src": f"music/music-{tr}.mp3",
        "from": round(start_s*FPS),
        "durationInFrames": round(d*FPS),
        "startFrom": sf,
        "volume": volo if volo is not None else TRACK_VOL[tr],
        "fadeIn": 45, "fadeOut": 75,
    })

s=json.load(open(SPEC))
s["music"]=False
s["musicCues"]=cues
json.dump(s,open(SPEC,"w"),indent=1)
print(f"wrote {len(cues)} music cues; tracks A={TLEN['A']:.0f}s B={TLEN['B']:.0f}s C={TLEN['C']:.0f}s D={TLEN['D']:.0f}s")
tot_music=sum(c['durationInFrames'] for c in cues)/FPS
print(f"music covers ~{tot_music/60:.1f} min of the {1908/60:.1f} min film (rest is deliberate silence)")
