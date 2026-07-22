"""Export each curated journal as its own text file, plus an index and a zip.

Unlike `export.py` (one JSONL row per entry, for NLP), this writes one human-
readable file per journal into `corpus/export/journals/`, then bundles the folder
into `corpus/export/journals.zip` for a single direct download.
"""
from __future__ import annotations

import csv
import re
import zipfile
from pathlib import Path

from .config import Config
from .store import Store


def _slug(text: str, maxlen: int = 60) -> str:
    text = re.sub(r"[^\w\s-]", "", (text or "").lower()).strip()
    text = re.sub(r"[\s_-]+", "-", text)
    return text[:maxlen].strip("-") or "untitled"


def export_journals(config: Config, selected_only: bool = True) -> Path:
    out_dir = config.export_dir / "journals"
    out_dir.mkdir(parents=True, exist_ok=True)
    # Clear any previous run so removed works don't linger.
    for old in out_dir.glob("*.txt"):
        old.unlink()

    index_rows = []
    used_names: set[str] = set()

    with Store(config.db_path) as s:
        works = s.list_works(selected_only=selected_only)
        for w in works:
            full = s.get_work(w["id"])
            entries = s.get_entries(w["id"])

            year = full["year"] or "0000"
            base = f"{year}_{_slug(full['title'])}"
            name = base
            n = 2
            while name in used_names:            # de-dupe (e.g. two Robbins volumes)
                name = f"{base}-{n}"; n += 1
            used_names.add(name)
            filename = f"{name}.txt"

            text = _render(full, entries)
            (out_dir / filename).write_text(text, encoding="utf-8")

            index_rows.append({
                "file": filename,
                "title": full["title"],
                "author": full["creator"],
                "year": full["year"],
                "words": full["n_words"],
                "entries": full["n_entries"],
                "narrative_score": round(full["narrative_score"], 1) if full["narrative_score"] is not None else "",
                "source_url": full["url"],
            })

    # index.csv
    index_path = out_dir / "index.csv"
    with open(index_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(index_rows[0].keys()) if index_rows
                                else ["file", "title", "author", "year", "words",
                                      "entries", "narrative_score", "source_url"])
        writer.writeheader()
        writer.writerows(index_rows)

    # README
    (out_dir / "README.txt").write_text(_readme(len(index_rows)), encoding="utf-8")

    # Zip the whole folder for a single download.
    zip_path = config.export_dir / "journals.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in sorted(out_dir.iterdir()):
            zf.write(f, arcname=f"journals/{f.name}")

    print(f"[journals] wrote {len(index_rows)} journal files -> {out_dir}")
    print(f"[journals] index -> {index_path}")
    print(f"[journals] zip   -> {zip_path}")
    return zip_path


def _render(work, entries) -> str:
    lines = []
    lines.append("=" * 70)
    lines.append(work["title"] or "Untitled")
    if work["creator"]:
        lines.append(f"Author:      {work['creator']}")
    if work["year"]:
        lines.append(f"Year:        {work['year']}")
    if work["language"]:
        lines.append(f"Language:    {work['language']}")
    if work["copyright_status"]:
        lines.append(f"Rights:      {work['copyright_status']}")
    if work["url"]:
        lines.append(f"Source:      {work['url']}")
    lines.append(f"Words:       {work['n_words']}   Entries: {work['n_entries']}")
    if work["narrative_score"] is not None:
        lines.append(f"NLP scores:  narrative={work['narrative_score']:.1f}  "
                     f"everyday={work['everyday_score']:.1f}  drama={work['drama_score']:.1f}")
    lines.append("Public-domain text retrieved from the Internet Archive via diary-corpus.")
    lines.append("Text is OCR from the original scan; expect occasional errors.")
    lines.append("=" * 70)
    lines.append("")

    for e in entries:
        heading = e["raw_date_heading"] or (e["entry_date"] or "")
        if heading:
            lines.append("")
            lines.append(f"--- {heading} ---")
        lines.append(e["text"])
        lines.append("")
    return "\n".join(lines)


def _readme(n: int) -> str:
    return (
        "Diaries of Everyday Life — curated journals\n"
        "==========================================\n\n"
        f"This folder contains {n} public-domain English diaries/journals, one plain-text\n"
        "file each, selected by NLP curation for everyday-life and dramatic narrative.\n\n"
        "  * Each .txt file: a metadata header followed by the full journal text\n"
        "    (entries separated by their date headings where detected).\n"
        "  * index.csv: a table of all files with author, year, word count and source URL.\n\n"
        "Text is OCR from handwritten/printed scans on the Internet Archive, so it contains\n"
        "recognition errors. The 'Source' URL in each file links to the original scan.\n"
    )
