"""Export the corpus to JSONL — the NLP-ready artifact.

One line per entry, with its parent work's metadata joined in.
"""
from __future__ import annotations

import json
from pathlib import Path

from .config import Config
from .store import Store


def export_jsonl(config: Config, filename: str = "entries.jsonl") -> Path:
    config.ensure_dirs()
    out_path = config.export_dir / filename
    n = 0
    with Store(config.db_path) as store, open(out_path, "w", encoding="utf-8") as fh:
        for row in store.iter_entries_with_work():
            record = {
                "entry_id": row["entry_id"],
                "seq": row["seq"],
                "entry_date": row["entry_date"],
                "raw_date_heading": row["raw_date_heading"],
                "text": row["text"],
                "work": {
                    "source": row["source"],
                    "source_id": row["source_id"],
                    "title": row["title"],
                    "creator": row["creator"],
                    "year": row["year"],
                    "language": row["language"],
                    "copyright_status": row["copyright_status"],
                    "url": row["url"],
                },
            }
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
            n += 1
    print(f"[export] wrote {n} entries -> {out_path}")
    return out_path
