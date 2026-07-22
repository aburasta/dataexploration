"""Source interface: how the harvester talks to any diary provider.

Add a new provider (e.g. Europeana) by subclassing DiarySource and implementing
`search()` and `fetch()`. The rest of the pipeline (harvest/segment/store) is
source-agnostic and only depends on these two dataclasses.
"""
from __future__ import annotations

import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Iterator, Optional

import requests


@dataclass
class WorkRef:
    """A lightweight reference to a diary work, returned by search()."""
    source: str            # e.g. "internet_archive"
    source_id: str         # provider-native identifier
    title: str
    creator: Optional[str] = None
    year: Optional[int] = None
    language: Optional[str] = None
    url: Optional[str] = None


@dataclass
class RawWork:
    """A fully-fetched work: its reference plus copyright status and full text."""
    ref: WorkRef
    copyright_status: Optional[str]
    text: str


class DiarySource(ABC):
    """Abstract base for a diary provider.

    Subclasses share a polite HTTP session with rate limiting and retry/backoff
    via `_get()`. This keeps provider code focused on query/parse logic.
    """

    name: str = "base"

    def __init__(self, http_config: Any, options: dict[str, Any]):
        self.http = http_config
        self.options = options or {}
        self._session = requests.Session()
        self._session.headers.update({"User-Agent": getattr(http_config, "user_agent", "diary-corpus")})
        self._last_request_ts = 0.0

    # -- shared polite HTTP ------------------------------------------------
    def _throttle(self) -> None:
        delay = getattr(self.http, "request_delay_seconds", 1.0)
        elapsed = time.monotonic() - self._last_request_ts
        if elapsed < delay:
            time.sleep(delay - elapsed)
        self._last_request_ts = time.monotonic()

    def _get(self, url: str, **kwargs) -> requests.Response:
        """GET with rate limiting, redirect-follow, and exponential backoff."""
        max_retries = getattr(self.http, "max_retries", 4)
        backoff_base = getattr(self.http, "backoff_base_seconds", 2.0)
        timeout = getattr(self.http, "timeout_seconds", 60)
        kwargs.setdefault("timeout", timeout)
        kwargs.setdefault("allow_redirects", True)  # essential for archive.org downloads

        last_exc: Optional[Exception] = None
        for attempt in range(max_retries + 1):
            self._throttle()
            try:
                resp = self._session.get(url, **kwargs)
                # Retry on transient server / rate-limit statuses.
                if resp.status_code in (429, 500, 502, 503, 504):
                    raise requests.HTTPError(f"HTTP {resp.status_code}", response=resp)
                return resp
            except (requests.RequestException,) as exc:
                last_exc = exc
                if attempt >= max_retries:
                    break
                time.sleep(backoff_base * (2 ** attempt))
        raise RuntimeError(f"GET failed after {max_retries + 1} attempts: {url}") from last_exc

    # -- provider API ------------------------------------------------------
    @abstractmethod
    def search(self, max_works: Optional[int] = None) -> Iterator[WorkRef]:
        """Yield WorkRefs matching this source's diary filters (paginated)."""
        raise NotImplementedError

    @abstractmethod
    def fetch(self, ref: WorkRef) -> Optional[RawWork]:
        """Fetch full text + copyright status for a WorkRef.

        Return None if the work should be skipped (e.g. not public domain,
        access-restricted, or no OCR text available).
        """
        raise NotImplementedError
