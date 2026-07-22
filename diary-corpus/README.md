# diary-corpus

A small, extensible system for retrieving **public-domain diary texts of real people**
and turning them into a corpus that is both **NLP-ready** (structured JSONL + SQLite)
and **browsable** (a tiny local web reader with full-text search).

The first (and currently only) source is the **Internet Archive** — open API, no key,
thousands of diary texts, downloadable OCR, and machine-readable copyright status.
The design is pluggable so institutional archives like **Europeana** can be added next
behind the same interface.

## How it works

```
search (advancedsearch.php)  ->  fetch (metadata + OCR download)  ->  raw/*.txt cache
        │                                                                   │
        └── public-domain + OCR filters                     segment (date headings)
                                                                            │
                                                              SQLite (works + entries + FTS5)
                                                              ├── export -> entries.jsonl (NLP)
                                                              └── serve  -> web reader (browse/search)
```

Only works whose Internet Archive metadata reports `possible-copyright-status`
starting with **"Public domain"** are accepted, and lending-restricted / access-restricted
items are excluded at both the search and fetch stages. Harvested text is cached to disk
and **not committed** (see `.gitignore`) — we version the code, not scraped content.

## Setup

```bash
cd diary-corpus
pip install -r requirements.txt
```

## Usage

```bash
# 1. Fetch N public-domain diary works (resumable; re-running skips cached items)
python cli.py harvest --limit 20

# 2. Segment cached texts into dated entries and load into SQLite
python cli.py segment

# 3. See what you have
python cli.py stats

# 4. Export the NLP-ready corpus (one JSON object per entry)
python cli.py export          # -> corpus/export/entries.jsonl

# 5. Browse + full-text search in a local web reader
python cli.py serve           # -> http://127.0.0.1:5000
```

`harvest --limit N` accepts N works; because many candidates are rejected (not public
domain, or no OCR text), the tool keeps paging through search results until it has N
accepted works. Run it again later to fetch more — already-cached works are skipped.

## Output shape

Each line of `entries.jsonl`:

```json
{
  "entry_id": 42,
  "seq": 3,
  "entry_date": "1912-01-15",
  "raw_date_heading": "Jan. 15, 1912",
  "text": "Woke early. Cold morning …",
  "work": {
    "source": "internet_archive",
    "source_id": "diarieswilliamb1912brew",
    "title": "Diaries of William Brewster, 1865-1919",
    "creator": "Brewster, William",
    "year": 1912,
    "language": "eng",
    "copyright_status": "Public domain. …",
    "url": "https://archive.org/details/diarieswilliamb1912brew"
  }
}
```

## Configuration

Edit `config.yaml` to change the search window, languages, rate limits, and paths:

- `internet_archive.year_from` / `year_to` — public-domain window (default 1500–1928).
- `internet_archive.languages` — e.g. `["eng"]` to restrict; empty = any.
- `internet_archive.subject` — the Internet Archive subject to search (`"diaries"`).
- `http.request_delay_seconds`, `max_retries`, `backoff_base_seconds` — politeness.

## A note on segmentation quality

Diaries are handwritten and OCR is imperfect, so per-entry splitting is **best-effort**:
`segment.py` detects common date-heading formats (`January 3, 1917`, `3 Jan. 1917`,
`1917-01-03`, weekday-prefixed, month+year). When a work has no detectable headings it
becomes a single fallback entry, so no text is ever dropped. Expect entry granularity to
vary a lot with scan quality.

## Adding another source (e.g. Europeana)

1. Create `diarycorpus/sources/europeana.py` with a class subclassing
   `DiarySource` (see `sources/base.py`) and implement:
   - `search(max_works)` → yields `WorkRef` objects.
   - `fetch(ref)` → returns a `RawWork` (or `None` to skip).
2. Register it in `diarycorpus/sources/__init__.py::get_source`.
3. Add a config block and set `source:` in `config.yaml`.

The harvest / segment / store / export / reader layers are source-agnostic and need no
changes. Institutional sources may require an API key and have their own terms of use —
honor those in the new source class.

## Legal / ethical scope

This tool is limited to **public-domain** works and is intended for research and reading.
It does not fetch in-copyright or access-restricted material. When extending to other
providers, respect each provider's licensing and terms.
```
