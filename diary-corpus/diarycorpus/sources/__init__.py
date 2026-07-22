"""Pluggable diary sources.

Each source implements the DiarySource interface (see base.py). Register new
sources in the SOURCES map so the CLI can select them by name via config.
"""
from __future__ import annotations

from typing import Any

from .base import DiarySource, RawWork, WorkRef
from .internet_archive import InternetArchiveSource


def get_source(name: str, http_config: Any, options: dict[str, Any]) -> DiarySource:
    """Instantiate a source by config name."""
    if name in ("internet_archive", "ia", "archive.org"):
        return InternetArchiveSource(http_config, options)
    raise ValueError(f"Unknown source: {name!r}")


__all__ = ["DiarySource", "RawWork", "WorkRef", "InternetArchiveSource", "get_source"]
