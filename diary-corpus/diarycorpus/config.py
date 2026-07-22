"""Configuration loading and path resolution.

All paths in config.yaml are resolved relative to the diary-corpus/ project root
(the directory that contains config.yaml), so the CLI works from anywhere.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

# Project root = diary-corpus/ (parent of the diarycorpus package dir).
PROJECT_ROOT = Path(__file__).resolve().parent.parent


@dataclass
class HttpConfig:
    user_agent: str = "diary-corpus/0.1"
    request_delay_seconds: float = 1.0
    max_retries: int = 4
    backoff_base_seconds: float = 2.0
    timeout_seconds: int = 60


@dataclass
class Config:
    raw_dir: Path
    db_path: Path
    export_dir: Path
    manifest_path: Path
    source: str
    http: HttpConfig
    source_options: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def load(cls, path: str | os.PathLike | None = None) -> "Config":
        cfg_path = Path(path) if path else PROJECT_ROOT / "config.yaml"
        with open(cfg_path, "r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}

        paths = data.get("paths", {})

        def resolve(p: str) -> Path:
            pp = Path(p)
            return pp if pp.is_absolute() else PROJECT_ROOT / pp

        http_data = data.get("http", {})
        http = HttpConfig(
            user_agent=http_data.get("user_agent", HttpConfig.user_agent),
            request_delay_seconds=float(http_data.get("request_delay_seconds", 1.0)),
            max_retries=int(http_data.get("max_retries", 4)),
            backoff_base_seconds=float(http_data.get("backoff_base_seconds", 2.0)),
            timeout_seconds=int(http_data.get("timeout_seconds", 60)),
        )

        source = data.get("source", "internet_archive")

        return cls(
            raw_dir=resolve(paths.get("raw_dir", "corpus/raw")),
            db_path=resolve(paths.get("db_path", "corpus/diary.db")),
            export_dir=resolve(paths.get("export_dir", "corpus/export")),
            manifest_path=resolve(paths.get("manifest_path", "corpus/harvest_manifest.json")),
            source=source,
            http=http,
            source_options=data.get(source, {}) or {},
        )

    def ensure_dirs(self) -> None:
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.export_dir.mkdir(parents=True, exist_ok=True)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
