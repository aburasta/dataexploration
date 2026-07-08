#!/usr/bin/env python3
"""Generate dashboard.html from data/moment_bank.csv."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FAMILY_LABELS = {
    "pursuits": "Pursuits & Chases",
    "interrogation": "Interrogation Room",
    "forensics_reveals": "Forensics & Reveals",
    "bodycam_encounters": "Bodycam Encounters",
    "dark_discoveries": "Dark Discoveries",
    "justice_courtroom": "Courtroom & Justice",
    "force_danger": "Use of Force & Danger",
    "perpetrator_profiles": "Perpetrator Profiles",
    "calls_dispatch": "911 & Dispatch",
    "hero_moments": "Hero Moments",
}

rows = list(csv.DictReader(open(ROOT / "data" / "moment_bank.csv")))
for r in rows:
    r["family_label"] = FAMILY_LABELS.get(r["family"], r["family"])

fam_counts = {}
for r in rows:
    fam_counts[r["family_label"]] = fam_counts.get(r["family_label"], 0) + 1
fam_counts = dict(sorted(fam_counts.items(), key=lambda kv: -kv[1]))

channels = [
    ("Dr Insanity", 161.2), ("EWU Bodycam", 94.6), ("EXPLORE WITH US", 52.1),
    ("EWU Crime Storytime", 38.3), ("Police Insider", 24.0),
    ("Law&Crime BodyCam", 14.2), ("The Hidden Files", 7.7),
    ("Stranger Stories", 7.3), ("JustThoughtLounge", 7.3),
    ("Vigilant Detective", 7.1),
]

template = (ROOT / "scripts" / "dashboard_template.html").read_text()
html = (template
        .replace("__ROWS__", json.dumps(rows))
        .replace("__FAMS__", json.dumps(fam_counts))
        .replace("__CHANNELS__", json.dumps(channels)))
(ROOT / "dashboard.html").write_text(html)
print(f"dashboard.html written: {len(rows)} rows, {len(fam_counts)} families")
