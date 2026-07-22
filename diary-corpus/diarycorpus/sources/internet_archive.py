"""Internet Archive (archive.org) diary source.

Validated 3-step flow:
  1. advancedsearch.php  -> paginated JSON of candidate works (public-domain filters)
  2. metadata/<id>       -> copyright status + exact OCR text filename
  3. download/<id>/<f>   -> full OCR text (requires following redirects)

Only non-lending-restricted, public-domain works with OCR text are accepted.
"""
from __future__ import annotations

from typing import Any, Iterator, Optional
from urllib.parse import quote

from .base import DiarySource, RawWork, WorkRef

SEARCH_URL = "https://archive.org/advancedsearch.php"
METADATA_URL = "https://archive.org/metadata/{identifier}"
DOWNLOAD_URL = "https://archive.org/download/{identifier}/{filename}"


class InternetArchiveSource(DiarySource):
    name = "internet_archive"

    def __init__(self, http_config: Any, options: dict[str, Any]):
        super().__init__(http_config, options)
        self.subject = self.options.get("subject", "diaries")
        self.year_from = int(self.options.get("year_from", 1500))
        self.year_to = int(self.options.get("year_to", 1928))
        self.languages = self.options.get("languages") or []
        self.copyright_prefix = self.options.get(
            "require_copyright_status_prefix", "Public domain"
        )
        self.batch_size = int(self.options.get("batch_size", 50))

    # -- query construction ------------------------------------------------
    def _query(self) -> str:
        parts = [
            f'subject:"{self.subject}"',
            "mediatype:texts",
            'format:"DjVuTXT"',  # guarantees an OCR text file exists
            f"year:[{self.year_from} TO {self.year_to}]",
            "-collection:inlibrary",          # exclude borrow-only scans
            "-access-restricted-item:true",   # exclude restricted items
        ]
        if self.languages:
            langs = " OR ".join(f"language:{lang}" for lang in self.languages)
            parts.append(f"({langs})")
        return " AND ".join(parts)

    # -- step 1: search ----------------------------------------------------
    def search(self, max_works: Optional[int] = None) -> Iterator[WorkRef]:
        query = self._query()
        page = 1
        yielded = 0
        while True:
            params = {
                "q": query,
                "fl[]": ["identifier", "title", "creator", "year", "language"],
                "rows": self.batch_size,
                "page": page,
                "output": "json",
            }
            resp = self._get(SEARCH_URL, params=params)
            data = resp.json()
            docs = data.get("response", {}).get("docs", [])
            if not docs:
                return
            for doc in docs:
                ref = WorkRef(
                    source=self.name,
                    source_id=doc["identifier"],
                    title=_as_str(doc.get("title")) or doc["identifier"],
                    creator=_as_str(doc.get("creator")),
                    year=_as_int(doc.get("year")),
                    language=_as_str(doc.get("language")),
                    url=f"https://archive.org/details/{doc['identifier']}",
                )
                yield ref
                yielded += 1
                if max_works is not None and yielded >= max_works:
                    return
            page += 1

    # -- steps 2 + 3: fetch ------------------------------------------------
    def fetch(self, ref: WorkRef) -> Optional[RawWork]:
        # Step 2: metadata -> copyright status + text filename.
        meta_resp = self._get(METADATA_URL.format(identifier=ref.source_id))
        try:
            meta = meta_resp.json()
        except ValueError:
            return None
        md = meta.get("metadata", {})

        copyright_status = _as_str(md.get("possible-copyright-status"))
        if not self._is_public_domain(copyright_status):
            return None
        if str(md.get("access-restricted-item", "")).lower() == "true":
            return None

        text_filename = self._pick_text_file(meta.get("files", []), ref.source_id)
        if not text_filename:
            return None

        # Step 3: download OCR text (redirects followed by _get).
        dl_url = DOWNLOAD_URL.format(
            identifier=ref.source_id, filename=quote(text_filename)
        )
        text_resp = self._get(dl_url)
        text = text_resp.text if text_resp.status_code == 200 else ""
        if not text.strip():
            return None  # restricted or empty OCR

        return RawWork(ref=ref, copyright_status=copyright_status, text=text)

    # -- helpers -----------------------------------------------------------
    def _is_public_domain(self, status: Optional[str]) -> bool:
        if not self.copyright_prefix:
            return True
        if not status:
            return False
        return status.strip().lower().startswith(self.copyright_prefix.strip().lower())

    @staticmethod
    def _pick_text_file(files: list[dict], identifier: str) -> Optional[str]:
        txts = [f["name"] for f in files if f.get("name", "").endswith(".txt")]
        if not txts:
            return None
        preferred = f"{identifier}_djvu.txt"
        if preferred in txts:
            return preferred
        # Otherwise take the first djvu text, else any .txt.
        for name in txts:
            if name.endswith("_djvu.txt"):
                return name
        return txts[0]


def _as_str(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, list):
        return ", ".join(str(v) for v in value) if value else None
    return str(value)


def _as_int(value: Any) -> Optional[int]:
    if isinstance(value, list):
        value = value[0] if value else None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
