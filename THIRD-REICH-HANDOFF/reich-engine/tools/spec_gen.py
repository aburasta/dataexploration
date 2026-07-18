#!/usr/bin/env python3
"""Assemble active-episode.json: 175 scenes in beat order, using the sourced media
(manifest), per-beat timing (beat_timing.json), a global narration track, hemicycle
charts for H beats, and varied motion/transitions."""
import json, os, subprocess, imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
BASE = os.path.abspath("..")
MEDIA = os.path.join(BASE, "public", "media", "special-legal-coup-1919-1933")
AUDIO = os.path.join(BASE, "public", "audio", "special-legal-coup-1919-1933")
manifest = json.load(open(os.path.join(MEDIA, "_manifest_sourcing.json")))
timing = json.load(open(os.path.join(AUDIO, "beat_timing.json")))

by_tag = {r["tag"]: r for r in manifest if r.get("status") == "ok"}
beat_order = [b for c in timing["chunks"] for b in c["beats"]]

RED = "#b03028"; GREY = "#4a4a4a"; GREY2 = "#6f6f6f"
HEMI = {
 "H1": {"segments":[{"count":12,"color":RED,"label":"NSDAP 12"},{"count":479,"color":GREY}], "total":491, "caption":"May 1928 — 12 / 491"},
 "H2": {"segments":[{"count":107,"color":RED,"label":"NSDAP 107"},{"count":384,"color":GREY}], "total":491, "caption":"Sept 1930 — 107 / 491"},
 "H3": {"segments":[{"count":53,"color":GREY,"label":"Hindenburg 53%"},{"count":37,"color":RED,"label":"Hitler 37%"},{"count":10,"color":GREY2,"label":"other 10%"}], "total":100, "caption":"1932 runoff"},
 "H4": {"segments":[{"count":230,"color":RED,"label":"NSDAP 230"},{"count":378,"color":GREY}], "total":608, "caption":"July 1932 — 230 / 608"},
 "H5": {"segments":[{"count":196,"color":RED,"label":"NSDAP 196"},{"count":388,"color":GREY}], "total":584, "caption":"Nov 1932 — 196 / 584"},
 "H6": {"segments":[{"count":288,"color":RED,"label":"NSDAP 288"},{"count":359,"color":GREY}], "total":647, "caption":"March 1933 — 288 / 647"},
 "H7": {"segments":[{"count":84,"color":RED,"label":"Nein 84"},{"count":441,"color":GREY,"label":"Ja 441"}], "total":525, "caption":"Enabling Act — 441 to 84"},
}
MOTIONS = ["slow-push","pan-left","slow-pull","pan-right","settle"]
# act boundaries (dip-to-black) at major narrative turns
DIP = {"1","41","48","50","56","68","77","86","92","95","99","105","108","113","121","125","132","137","140","143","146","151","156"}

def clip_len(path):
    s = subprocess.run([FF,"-i",path],capture_output=True,text=True).stderr
    try:
        d=s.split("Duration:")[1].split(",")[0].strip(); h,m,se=d.split(":")
        return int(h)*3600+int(m)*60+float(se)
    except: return None

scenes=[]; mi=0
for tag in beat_order:
    t=timing["beats"][tag]; dsec=round(t["dur"],3)
    if dsec<=0: dsec=2.0
    trans = "dip-to-black" if tag in DIP else ("cut" if (tag.isdigit() and int(tag)%7==0) else "xfade")
    if tag.startswith("H"):
        h=HEMI.get(tag,{})
        scenes.append({"n":tag,"type":"hemicycle","durationSec":dsec,"transition":trans,
                       "segments":h.get("segments"),"total":h.get("total"),"showLabels":True,"caption":h.get("caption","")})
        continue
    r=by_tag.get(tag)
    if not r:
        scenes.append({"n":tag,"type":"hemicycle","durationSec":dsec,"transition":trans,
                       "segments":[{"count":1,"color":GREY}],"total":1}); continue
    if r.get("type")=="video":
        src=r["file"]; L=clip_len(os.path.join(MEDIA,src)) or dsec
        pr=round(max(0.25,min(2.0, L/dsec)),3)  # stretch/compress clip to fill the beat
        scenes.append({"n":tag,"type":"clip","src":src,"durationSec":dsec,"startTrim":0,
                       "playbackRate":pr,"transition":trans})
    else:
        motion=MOTIONS[mi%len(MOTIONS)]; mi+=1
        scenes.append({"n":tag,"type":"image","src":r["file"],"durationSec":dsec,
                       "motion":motion,"transition":trans})

# closing outro card (standard Like/Subscribe) — brief, after narration
scenes.append({"n":"outro","type":"outro","durationSec":6,"transition":"dip-to-black"})

spec={"title":"The Legal Coup (1919-1933)","slug":"special-legal-coup-1919-1933",
      "mediaDir":"special-legal-coup-1919-1933","narration":"narration.mp3",
      "music":False,"scenes":scenes}
out=os.path.join(BASE,"src","active-episode.json")
json.dump(spec,open(out,"w"),indent=1)
tot=sum(s["durationSec"] for s in scenes)
print(f"scenes: {len(scenes)} ({sum(1 for s in scenes if s['type']=='image')} img, "
      f"{sum(1 for s in scenes if s['type']=='clip')} clip, "
      f"{sum(1 for s in scenes if s['type']=='hemicycle')} hemicycle, 1 outro)")
print(f"total timeline: {tot/60:.1f} min | narration track: narration.mp3")
print("wrote", out)
