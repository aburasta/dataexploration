#!/usr/bin/env python3
"""Trim varied clips from a downloaded PD source film into the episode media dir.
Usage: python3 trim_clips.py clips_<name>.json
Each clip -> <tag>.mp4 (h264, muted, <=1280w) in public/media/<slug>/ + manifest row.
"""
import json, sys, os, subprocess, imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
MEDIA = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "public", "media", "special-legal-coup-1919-1933"))
MANIFEST = os.path.join(MEDIA, "_manifest_sourcing.json")
REVIEW = os.path.join(MEDIA, "_review"); os.makedirs(REVIEW, exist_ok=True)

def load(p):
    return json.load(open(p)) if os.path.exists(p) else []

def main():
    spec = json.load(open(sys.argv[1]))
    src = os.path.join(os.path.dirname(__file__), spec["source_file"])
    manifest = load(MANIFEST)
    for c in spec["clips"]:
        tag = c["tag"]; out = os.path.join(MEDIA, f"{tag}.mp4")
        cmd = [FF, "-loglevel","error","-y","-ss",str(c["start"]),"-i",src,
               "-t",str(c["dur"]),"-an","-c:v","libx264","-preset","veryfast",
               "-pix_fmt","yuv420p","-vf","scale='min(1280,iw)':-2","-movflags","+faststart", out]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            print(f"[{tag}] TRIM-FAIL {r.stderr[:120]}"); continue
        # grab a mid-clip verification frame
        subprocess.run([FF,"-loglevel","error","-y","-ss",str(c["start"]+c["dur"]/2),
                        "-i",src,"-frames:v","1","-vf","scale=320:-1",
                        os.path.join(REVIEW, f"{tag}_frame.jpg")], capture_output=True)
        size = os.path.getsize(out)//1024
        manifest = [r for r in manifest if r["tag"] != tag]
        manifest.append({"tag":tag,"status":"ok","type":"video","file":f"{tag}.mp4",
                         "source":spec["source_id"],"page":spec["page"],
                         "license":spec["license"],"attribution":spec.get("attribution",spec["source_id"]),
                         "clip":f"{c['start']}s+{c['dur']}s","note":c["note"]})
        print(f"[{tag}] OK  {tag}.mp4  {size}KB  ({c['start']}s+{c['dur']}s)  {c['note'][:48]}")
        json.dump(manifest, open(MANIFEST,"w"), indent=1, ensure_ascii=False)
    json.dump(manifest, open(MANIFEST,"w"), indent=1, ensure_ascii=False)
    v=sum(1 for r in manifest if r.get("type")=="video"); print(f"\n== {v} video clips in manifest ==")

if __name__=="__main__": main()
