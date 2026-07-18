#!/usr/bin/env python3
"""Rough-transcribe each audio chunk with pocketsphinx (offline, bundled model),
capturing word-level timestamps, so chunks can be ordered/aligned against the script."""
import os, glob, json, subprocess, imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
AUD = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "public", "audio", "special-legal-coup-1919-1933", "_chunks"))
OUT = os.path.join(AUD, "_transcripts.json")
from pocketsphinx import AudioFile

def transcribe(mp3):
    wav = "/tmp/claude-0/-home-user-dataexploration/909fba24-5d12-5c16-aeb7-92d6d8575e4f/scratchpad/_asr.wav"
    subprocess.run([FF,"-loglevel","error","-y","-i",mp3,"-ar","16000","-ac","1",wav], check=True)
    words=[]
    for phrase in AudioFile(audio_file=wav, frate=100):
        for w, prob, start, end in phrase.segments(detailed=True):
            if w in ("<s>","</s>","<sil>","(NULL)") or w.startswith("["): continue
            words.append({"w":w, "s":round(start/100,2), "e":round(end/100,2)})
    return words

res={}
for mp3 in sorted(glob.glob(os.path.join(AUD,"*.mp3"))):
    name=os.path.basename(mp3)
    dur=float(subprocess.run([FF,"-i",mp3],capture_output=True,text=True).stderr.split("Duration:")[1].split(",")[0].strip().replace(":"," ").split().__str__()) if False else None
    words=transcribe(mp3)
    res[name]={"nwords":len(words), "words":words}
    print(f"{name}: {len(words)} words, first: {' '.join(w['w'] for w in words[:12])}")
json.dump(res, open(OUT,"w"))
print("wrote", OUT)
