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
            + retargeted away from naturalist material                      │
                                                              SQLite (works + entries + FTS5)
                                                                            │
                                                              curate (NLP scoring + select)
                                                              ├── export -> entries.jsonl (NLP, curated)
                                                              ├── serve  -> web reader (curated)
                                                              └── page   -> self-contained HTML (curated)
```

**Public-domain filtering.** A work is accepted when its Internet Archive metadata
reports a public-domain `possible-copyright-status`, or — when that field is missing —
when its publication year falls inside the pre-1929 window the search already enforces
(date-based public domain). Anything explicitly marked in-copyright, or
lending/access-restricted, is rejected. Harvested text is cached to disk and **not
committed** (see `.gitignore`) — we version the code, not scraped content.

**Retargeting + NLP curation.** The search is steered *away* from naturalists' field
notebooks (which dominate public-domain diaries via the Biodiversity Heritage Library) by
excluding that collection and its subjects, and toward personal narratives, English only.
Then `curate` runs a transparent, dependency-light NLP pass (`diarycorpus/nlp.py`) that
scores each journal and keeps only the substantial, English, story-like ones — see below.

## Setup

```bash
cd diary-corpus
pip install -r requirements.txt
```

## Usage

```bash
# 1. Fetch a pool of public-domain personal diaries (resumable; re-run skips cached)
python cli.py harvest --limit 150

# 2. Segment cached texts into dated entries and load into SQLite
python cli.py segment

# 3. NLP curation: score journals, keep the long English narrative ones
python cli.py curate

# 4. See what survived (curated by default; --all for everything harvested)
python cli.py stats

# 5. Export the NLP-ready corpus (curated only; one JSON object per entry)
python cli.py export          # -> corpus/export/entries.jsonl

# 6a. Browse + full-text search in a local web reader (curated)
python cli.py serve           # -> http://127.0.0.1:5000
# 6b. …or build one self-contained HTML file you can open offline / share
python cli.py page            # -> corpus/export/reading-room.html

# 7. Export each journal as its own text file (+ index.csv) and a single zip
python cli.py journals        # -> corpus/export/journals/ + corpus/export/journals.zip
```

`harvest --limit N` accepts N works; because many candidates are rejected (not public
domain, or no OCR text), the tool keeps paging through search results until it has N
accepted works. Run it again later to fetch more — already-cached works are skipped.

### Curation: what gets kept

`curate` concatenates each journal's text and computes lexical features (per 1,000 words):
first-person density, an **everyday-life** lexicon (home, family, church, letters, work…),
a **drama** lexicon (death, illness, love, war, fear…), and a **naturalist penalty**
(field-note vocabulary, Latin binomials, measurements). A work is **selected** when it
clears every gate in `config.yaml → curate`:

| gate | default | purpose |
|------|---------|---------|
| `min_words` | 2000 | drop stray fragments; keep whole journals that tell a story |
| `english_min` | 0.16 | stopword-density language check (English only) |
| `naturalist_max` | 12.0 | reject field notebooks |
| `min_entry_words` | 40 | prune micro-entries inside a kept journal |

No top-N cap — **every** journal passing the gates is kept, ranked by a combined
`narrative_score` (balanced everyday + drama). Re-tune the numbers and re-run
`python cli.py curate` **without re-harvesting**. `stats`, `export`, `serve` and `page`
all show the curated set by default.

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
    "url": "https://archive.org/details/...",
    "n_words": 48213,
    "narrative_score": 74.6,
    "everyday_score": 41.2,
    "drama_score": 28.9
  }
}
```

## Configuration

Edit `config.yaml` to change targeting, curation, rate limits, and paths:

- `internet_archive.subject` / `extra_subjects` — subjects to search (`"Diaries"`,
  broadened with `"Personal narratives"`).
- `internet_archive.exclude_collections` / `exclude_subjects` — steer away from
  naturalist material (default drops `biodiversity` + `Natural history`, `Birds`, …).
- `internet_archive.year_from` / `year_to` — public-domain window (default 1500–1928).
- `internet_archive.languages` — `["eng"]` for English only.
- `curate.*` — the NLP gates and scoring weights (see the table above).
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
