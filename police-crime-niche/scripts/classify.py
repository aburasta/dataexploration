#!/usr/bin/env python3
"""Multi-label classification of niche video titles against taxonomy.json.

Reads data/catalog.csv, applies every subcategory's regex patterns to each
title (case-insensitive), and writes back catalog.csv/catalog.json with a
`labels` column (semicolon-separated subcategory ids) plus a coverage summary
to stdout.
"""
import json
import re
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent


def load_rules():
    taxonomy = json.loads((ROOT / "taxonomy.json").read_text())
    rules = []  # (family_id, subcat_id, compiled_regex)
    for fam_id, family in taxonomy["families"].items():
        for sub_id, sub in family["subcategories"].items():
            combined = "|".join(f"(?:{p})" for p in sub["patterns"])
            rules.append((fam_id, sub_id, re.compile(combined, re.IGNORECASE)))
    return rules


def classify_title(title, rules):
    labels, families = [], []
    for fam_id, sub_id, rx in rules:
        if rx.search(title):
            labels.append(sub_id)
            families.append(fam_id)
    return labels, sorted(set(families))


def main():
    catalog_path = ROOT / "data" / "catalog.csv"
    df = pd.read_csv(catalog_path)
    rules = load_rules()

    all_labels, all_families = [], []
    for title in df["title"].fillna(""):
        labels, families = classify_title(str(title), rules)
        all_labels.append(";".join(labels))
        all_families.append(";".join(families))

    df["labels"] = all_labels
    df["families"] = all_families
    df.to_csv(catalog_path, index=False)
    df.to_json(ROOT / "data" / "catalog.json", orient="records", indent=1)

    classified = (df["labels"] != "").sum()
    print(f"videos: {len(df)}  classified: {classified}  "
          f"coverage: {classified / len(df):.1%}")

    counts = {}
    for row in df["labels"]:
        for label in filter(None, row.split(";")):
            counts[label] = counts.get(label, 0) + 1
    for label, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"{n:5d}  {label}")

    unclassified = df[df["labels"] == ""]
    if len(unclassified):
        print("\n--- sample unclassified titles ---")
        for t in unclassified["title"].head(30):
            print(" ", t)


if __name__ == "__main__":
    sys.exit(main())
