"""Split a diary's OCR text into per-entry records by detecting date headings.

OCR'd diaries are messy and inconsistent, so this is best-effort:
  * We scan line-by-line for lines that look like a date heading.
  * Each such heading starts a new entry; text accumulates until the next one.
  * If no headings are found, the whole work becomes a single fallback entry,
    so no text is ever lost.

`entry_date` is a normalized ISO string (YYYY-MM-DD, or YYYY-MM / YYYY when the
day/month are missing) when we can parse it; otherwise None while the original
`raw_date_heading` is always preserved.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Optional

MONTHS = {
    "january": 1, "jan": 1, "february": 2, "feb": 2, "march": 3, "mar": 3,
    "april": 4, "apr": 4, "may": 5, "june": 6, "jun": 6, "july": 7, "jul": 7,
    "august": 8, "aug": 8, "september": 9, "sept": 9, "sep": 9, "october": 10,
    "oct": 10, "november": 11, "nov": 11, "december": 12, "dec": 12,
}

_MONTH_ALT = "|".join(sorted(MONTHS.keys(), key=len, reverse=True))
_WEEKDAY = r"(?:mon|tues?|wed(?:nes)?|thurs?|fri|satur?|sun)(?:day)?"

# Date-heading patterns. Each must match a full-ish line to reduce false hits.
_PATTERNS = [
    # 1917-01-03  /  1917/1/3
    re.compile(r"^\s*(?P<y>\d{4})[-/](?P<m>\d{1,2})[-/](?P<d>\d{1,2})\s*[.,:]?\s*$", re.I),
    # January 3, 1917  /  January 3 1917  /  Jan. 3rd, 1917
    re.compile(
        rf"^\s*(?:{_WEEKDAY}[,\.\s]+)?(?P<mon>{_MONTH_ALT})\.?\s+"
        rf"(?P<d>\d{{1,2}})(?:st|nd|rd|th)?[,\.\s]+(?P<y>\d{{4}})\s*[.,:]?\s*$",
        re.I,
    ),
    # 3 January 1917  /  3rd Jan. 1917  /  Tuesday, 3 January 1917
    re.compile(
        rf"^\s*(?:{_WEEKDAY}[,\.\s]+)?(?P<d>\d{{1,2}})(?:st|nd|rd|th)?\s+"
        rf"(?P<mon>{_MONTH_ALT})\.?[,\.\s]+(?P<y>\d{{4}})\s*[.,:]?\s*$",
        re.I,
    ),
    # January 1917  (month + year only)
    re.compile(
        rf"^\s*(?P<mon>{_MONTH_ALT})\.?\s+(?P<y>\d{{4}})\s*[.,:]?\s*$", re.I
    ),
]


@dataclass
class Entry:
    seq: int
    entry_date: Optional[str]
    raw_date_heading: Optional[str]
    text: str


def _parse_heading(line: str) -> Optional[tuple[str, Optional[str]]]:
    """Return (raw_heading, iso_date_or_None) if the line is a date heading."""
    stripped = line.strip()
    if not stripped or len(stripped) > 60:
        return None
    for pat in _PATTERNS:
        m = pat.match(stripped)
        if not m:
            continue
        gd = m.groupdict()
        year = int(gd["y"])
        if not (1400 <= year <= 2100):
            return None
        month = None
        if gd.get("mon"):
            month = MONTHS.get(gd["mon"].lower())
        elif gd.get("m"):
            month = int(gd["m"])
        day = int(gd["d"]) if gd.get("d") else None

        iso = _to_iso(year, month, day)
        return stripped, iso
    return None


def _to_iso(year: int, month: Optional[int], day: Optional[int]) -> Optional[str]:
    if month and not (1 <= month <= 12):
        month = None
    if day and not (1 <= day <= 31):
        day = None
    if month and day:
        return f"{year:04d}-{month:02d}-{day:02d}"
    if month:
        return f"{year:04d}-{month:02d}"
    return f"{year:04d}"


def segment_text(text: str, min_entry_chars: int = 20) -> List[Entry]:
    """Split raw diary text into dated entries (best-effort)."""
    lines = text.splitlines()
    entries: List[Entry] = []
    cur_heading: Optional[str] = None
    cur_iso: Optional[str] = None
    cur_lines: List[str] = []

    def flush() -> None:
        body = "\n".join(cur_lines).strip()
        if cur_heading is None and not body:
            return
        if cur_heading is None and len(body) < min_entry_chars:
            return
        entries.append(
            Entry(
                seq=len(entries),
                entry_date=cur_iso,
                raw_date_heading=cur_heading,
                text=body,
            )
        )

    for line in lines:
        parsed = _parse_heading(line)
        if parsed is not None:
            # New entry starts here; flush the previous one.
            if cur_heading is not None or "".join(cur_lines).strip():
                flush()
            cur_heading, cur_iso = parsed
            cur_lines = []
        else:
            cur_lines.append(line)
    flush()

    # Fallback: no date headings found -> whole work as a single entry.
    if not entries:
        body = text.strip()
        if body:
            entries = [Entry(seq=0, entry_date=None, raw_date_heading=None, text=body)]

    # Renumber sequentially (flush may have skipped short leading fragments).
    for i, e in enumerate(entries):
        e.seq = i
    return entries
