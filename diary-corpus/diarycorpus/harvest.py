"""Harvest orchestrator: search a source, fetch full text, cache raw to disk.

Resumable: a work whose raw cache file already exists is skipped, so re-running
picks up where a previous run stopped. Writes a manifest of what was harvested.
"""
from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Optional

from .config import Config
from .sources import get_source
from .sources.base import RawWork, WorkRef


def _cache_path(raw_dir: Path, ref: WorkRef) -> Path:
    safe_id = ref.source_id.replace("/", "_")
    return raw_dir / f"{ref.source}__{safe_id}.txt"


def _meta_path(raw_dir: Path, ref: WorkRef) -> Path:
    safe_id = ref.source_id.replace("/", "_")
    return raw_dir / f"{ref.source}__{safe_id}.json"


def harvest(config: Config, limit: Optional[int] = None, refetch: bool = False) -> dict:
    """Search + fetch + cache. Returns a summary dict (also written to manifest)."""
    config.ensure_dirs()
    source = get_source(config.source, config.http, config.source_options)

    fetched, skipped_cached, skipped_rejected = 0, 0, 0
    records = []

    print(f"[harvest] source={config.source} limit={limit}")
    # Search yields more candidates than `limit` accepted works, because some
    # are rejected (not PD / no OCR). We keep pulling until we accept `limit`.
    for ref in source.search(max_works=None):
        if limit is not None and fetched >= limit:
            break

        cache_file = _cache_path(config.raw_dir, ref)
        if cache_file.exists() and not refetch:
            skipped_cached += 1
            records.append(_manifest_row(ref, cache_file, cached=True))
            fetched += 1  # counts toward the limit; already have it
            print(f"  [cached]   {ref.source_id}  {ref.title[:60]}")
            continue

        raw: Optional[RawWork] = source.fetch(ref)
        if raw is None:
            skipped_rejected += 1
            print(f"  [skip]     {ref.source_id}  (not PD / no OCR)")
            continue

        cache_file.write_text(raw.text, encoding="utf-8")
        _meta_path(config.raw_dir, ref).write_text(
            json.dumps(
                {**asdict(raw.ref), "copyright_status": raw.copyright_status},
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        fetched += 1
        records.append(_manifest_row(ref, cache_file, cached=False,
                                      copyright_status=raw.copyright_status,
                                      chars=len(raw.text)))
        print(f"  [fetched]  {ref.source_id}  ({len(raw.text):,} chars)  {ref.title[:50]}")

    summary = {
        "source": config.source,
        "accepted": fetched,
        "skipped_cached": skipped_cached,
        "skipped_rejected": skipped_rejected,
        "works": records,
    }
    config.manifest_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(
        f"[harvest] done: {fetched} accepted "
        f"({skipped_cached} from cache), {skipped_rejected} rejected"
    )
    return summary


def _manifest_row(ref: WorkRef, cache_file: Path, cached: bool,
                  copyright_status: Optional[str] = None,
                  chars: Optional[int] = None) -> dict:
    return {
        "source": ref.source,
        "source_id": ref.source_id,
        "title": ref.title,
        "creator": ref.creator,
        "year": ref.year,
        "language": ref.language,
        "url": ref.url,
        "copyright_status": copyright_status,
        "cache_file": str(cache_file),
        "chars": chars,
        "from_cache": cached,
    }
