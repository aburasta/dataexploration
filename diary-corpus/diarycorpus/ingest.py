"""Ingest cached raw texts into the SQLite store, segmenting into entries.

Reads the raw/*.txt cache produced by harvest (plus its sidecar *.json metadata),
segments each work into entries, and upserts works + entries into the store.
"""
from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .config import Config
from .segment import segment_text
from .store import Store


def ingest(config: Config) -> dict:
    config.ensure_dirs()
    raw_files = sorted(config.raw_dir.glob("*.txt"))
    if not raw_files:
        print(f"[segment] no raw texts found in {config.raw_dir} — run harvest first")
        return {"works": 0, "entries": 0}

    total_works, total_entries = 0, 0
    with Store(config.db_path) as store:
        for txt_path in raw_files:
            meta_path = txt_path.with_suffix(".json")
            meta = _load_meta(meta_path)
            if meta is None:
                print(f"  [warn] missing metadata for {txt_path.name}, skipping")
                continue

            text = txt_path.read_text(encoding="utf-8", errors="replace")
            work_id = store.upsert_work(
                source=meta["source"],
                source_id=meta["source_id"],
                title=meta.get("title"),
                creator=meta.get("creator"),
                year=meta.get("year"),
                language=meta.get("language"),
                copyright_status=meta.get("copyright_status"),
                url=meta.get("url"),
            )
            entries = segment_text(text)
            n = store.replace_entries(work_id, [asdict(e) for e in entries])
            total_works += 1
            total_entries += n
            print(f"  [ingest] {meta['source_id']}: {n} entries")

    print(f"[segment] done: {total_works} works, {total_entries} entries")
    return {"works": total_works, "entries": total_entries}


def _load_meta(meta_path: Path):
    if not meta_path.exists():
        return None
    try:
        return json.loads(meta_path.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return None
