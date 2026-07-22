"""SQLite storage for works and entries, with an FTS5 full-text index.

Schema:
  works    - one row per diary work (source + metadata)
  entries  - one row per segmented entry, linked to a work
  entries_fts - FTS5 index over entry text (external-content, linked to entries)

Upserts are idempotent on (source, source_id) so re-runs update in place.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterable, Optional

SCHEMA = """
CREATE TABLE IF NOT EXISTS works (
    id               INTEGER PRIMARY KEY,
    source           TEXT NOT NULL,
    source_id        TEXT NOT NULL,
    title            TEXT,
    creator          TEXT,
    year             INTEGER,
    language         TEXT,
    copyright_status TEXT,
    url              TEXT,
    n_entries        INTEGER DEFAULT 0,
    -- NLP curation fields (populated by `curate`)
    n_words           INTEGER,
    english_ratio     REAL,
    firstperson       REAL,
    everyday_score    REAL,
    drama_score       REAL,
    naturalist_score  REAL,
    narrative_score   REAL,
    selected          INTEGER DEFAULT 0,
    UNIQUE (source, source_id)
);

CREATE TABLE IF NOT EXISTS entries (
    id               INTEGER PRIMARY KEY,
    work_id          INTEGER NOT NULL REFERENCES works(id) ON DELETE CASCADE,
    seq              INTEGER NOT NULL,
    entry_date       TEXT,          -- normalized ISO date when parseable, else NULL
    raw_date_heading TEXT,          -- the heading text as found in the OCR
    text             TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_entries_work ON entries(work_id);

CREATE VIRTUAL TABLE IF NOT EXISTS entries_fts USING fts5(
    text,
    content='entries',
    content_rowid='id'
);
"""


class Store:
    def __init__(self, db_path: str | Path):
        self.db_path = str(db_path)
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.conn.executescript(SCHEMA)
        self._migrate()
        self.conn.commit()

    def _migrate(self) -> None:
        """Add NLP columns to a `works` table created before curation existed."""
        existing = {r["name"] for r in self.conn.execute("PRAGMA table_info(works)")}
        additions = {
            "n_words": "INTEGER", "english_ratio": "REAL", "firstperson": "REAL",
            "everyday_score": "REAL", "drama_score": "REAL",
            "naturalist_score": "REAL", "narrative_score": "REAL",
            "selected": "INTEGER DEFAULT 0",
        }
        for col, decl in additions.items():
            if col not in existing:
                self.conn.execute(f"ALTER TABLE works ADD COLUMN {col} {decl}")

    def close(self) -> None:
        self.conn.close()

    def __enter__(self) -> "Store":
        return self

    def __exit__(self, *exc) -> None:
        self.close()

    # -- works -------------------------------------------------------------
    def upsert_work(
        self,
        *,
        source: str,
        source_id: str,
        title: Optional[str],
        creator: Optional[str],
        year: Optional[int],
        language: Optional[str],
        copyright_status: Optional[str],
        url: Optional[str],
    ) -> int:
        cur = self.conn.execute(
            """
            INSERT INTO works (source, source_id, title, creator, year, language, copyright_status, url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(source, source_id) DO UPDATE SET
                title=excluded.title,
                creator=excluded.creator,
                year=excluded.year,
                language=excluded.language,
                copyright_status=excluded.copyright_status,
                url=excluded.url
            """,
            (source, source_id, title, creator, year, language, copyright_status, url),
        )
        self.conn.commit()
        if cur.lastrowid:
            row = self.conn.execute(
                "SELECT id FROM works WHERE source=? AND source_id=?",
                (source, source_id),
            ).fetchone()
            return row["id"]
        row = self.conn.execute(
            "SELECT id FROM works WHERE source=? AND source_id=?", (source, source_id)
        ).fetchone()
        return row["id"]

    def work_id(self, source: str, source_id: str) -> Optional[int]:
        row = self.conn.execute(
            "SELECT id FROM works WHERE source=? AND source_id=?", (source, source_id)
        ).fetchone()
        return row["id"] if row else None

    # -- entries -----------------------------------------------------------
    def replace_entries(self, work_id: int, entries: Iterable[dict]) -> int:
        """Delete existing entries for a work and insert the given ones.

        Keeps the FTS index in sync via delete/insert on the shadow table.
        Returns the number of entries inserted.
        """
        # Remove old entries + their FTS rows.
        old_ids = [
            r["id"]
            for r in self.conn.execute(
                "SELECT id FROM entries WHERE work_id=?", (work_id,)
            )
        ]
        for oid in old_ids:
            self.conn.execute(
                "INSERT INTO entries_fts(entries_fts, rowid, text) VALUES('delete', ?, "
                "(SELECT text FROM entries WHERE id=?))",
                (oid, oid),
            )
        self.conn.execute("DELETE FROM entries WHERE work_id=?", (work_id,))

        count = 0
        for entry in entries:
            cur = self.conn.execute(
                """
                INSERT INTO entries (work_id, seq, entry_date, raw_date_heading, text)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    work_id,
                    entry["seq"],
                    entry.get("entry_date"),
                    entry.get("raw_date_heading"),
                    entry["text"],
                ),
            )
            rowid = cur.lastrowid
            self.conn.execute(
                "INSERT INTO entries_fts(rowid, text) VALUES (?, ?)",
                (rowid, entry["text"]),
            )
            count += 1

        self.conn.execute("UPDATE works SET n_entries=? WHERE id=?", (count, work_id))
        self.conn.commit()
        return count

    # -- curation ----------------------------------------------------------
    def all_works(self):
        """Every work (used by the curator to score, regardless of selection)."""
        return self.conn.execute("SELECT * FROM works ORDER BY id").fetchall()

    def set_work_scores(self, work_id: int, scores: dict, selected: bool) -> None:
        self.conn.execute(
            """
            UPDATE works SET
                n_words=?, english_ratio=?, firstperson=?, everyday_score=?,
                drama_score=?, naturalist_score=?, narrative_score=?, selected=?
            WHERE id=?
            """,
            (
                scores.get("n_words"), scores.get("english_ratio"),
                scores.get("firstperson"), scores.get("everyday"),
                scores.get("drama"), scores.get("naturalist"),
                scores.get("narrative_score"), 1 if selected else 0, work_id,
            ),
        )
        self.conn.commit()

    def delete_entries_below(self, work_id: int, min_words: int) -> int:
        """Drop micro-entries (fewer than `min_words` words) from a work.

        Keeps the FTS index in sync. Never deletes the sole remaining entry, so a
        short-but-whole journal still shows something.
        """
        rows = self.conn.execute(
            "SELECT id, text FROM entries WHERE work_id=? ORDER BY seq", (work_id,)
        ).fetchall()
        if len(rows) <= 1:
            return 0
        removed = 0
        for r in rows:
            if len(rows) - removed <= 1:
                break
            if len(r["text"].split()) < min_words:
                self.conn.execute(
                    "INSERT INTO entries_fts(entries_fts, rowid, text) VALUES('delete', ?, ?)",
                    (r["id"], r["text"]),
                )
                self.conn.execute("DELETE FROM entries WHERE id=?", (r["id"],))
                removed += 1
        if removed:
            n = self.conn.execute(
                "SELECT COUNT(*) AS n FROM entries WHERE work_id=?", (work_id,)
            ).fetchone()["n"]
            self.conn.execute("UPDATE works SET n_entries=? WHERE id=?", (n, work_id))
            self.conn.commit()
        return removed

    # -- queries used by reader / stats / export ---------------------------
    def _where_selected(self, selected_only: bool, alias: str = "w") -> str:
        return f" WHERE {alias}.selected=1 " if selected_only else " "

    def stats(self, selected_only: bool = False) -> dict:
        c = self.conn
        wcond = "WHERE selected=1" if selected_only else ""
        n_works = c.execute(f"SELECT COUNT(*) AS n FROM works {wcond}").fetchone()["n"]
        econd = ("WHERE work_id IN (SELECT id FROM works WHERE selected=1)"
                 if selected_only else "")
        n_entries = c.execute(f"SELECT COUNT(*) AS n FROM entries {econd}").fetchone()["n"]
        yr = c.execute(
            f"SELECT MIN(year) AS lo, MAX(year) AS hi FROM works "
            f"{'WHERE selected=1 AND' if selected_only else 'WHERE'} year IS NOT NULL"
        ).fetchone()
        langs = [
            (r["language"], r["n"])
            for r in c.execute(
                f"SELECT language, COUNT(*) AS n FROM works {wcond} "
                "GROUP BY language ORDER BY n DESC"
            )
        ]
        total = c.execute("SELECT COUNT(*) AS n FROM works").fetchone()["n"]
        return {
            "works": n_works,
            "total_works": total,
            "entries": n_entries,
            "year_min": yr["lo"],
            "year_max": yr["hi"],
            "languages": langs,
        }

    def list_works(self, selected_only: bool = False):
        cond = "WHERE selected=1" if selected_only else ""
        return self.conn.execute(
            "SELECT id, title, creator, year, language, n_entries, url, "
            "n_words, narrative_score, everyday_score, drama_score "
            f"FROM works {cond} ORDER BY year, title"
        ).fetchall()

    def get_work(self, work_id: int):
        return self.conn.execute("SELECT * FROM works WHERE id=?", (work_id,)).fetchone()

    def get_entries(self, work_id: int):
        return self.conn.execute(
            "SELECT * FROM entries WHERE work_id=? ORDER BY seq", (work_id,)
        ).fetchall()

    def search_entries(self, query: str, limit: int = 50, selected_only: bool = False):
        cond = "AND w.selected=1" if selected_only else ""
        return self.conn.execute(
            f"""
            SELECT e.id, e.work_id, e.entry_date, e.raw_date_heading,
                   w.title, w.creator, w.year,
                   snippet(entries_fts, 0, '[', ']', ' … ', 12) AS snippet
            FROM entries_fts
            JOIN entries e ON e.id = entries_fts.rowid
            JOIN works w ON w.id = e.work_id
            WHERE entries_fts MATCH ? {cond}
            ORDER BY rank
            LIMIT ?
            """,
            (query, limit),
        ).fetchall()

    def iter_entries_with_work(self, selected_only: bool = False):
        cond = "WHERE w.selected=1" if selected_only else ""
        return self.conn.execute(
            f"""
            SELECT e.id AS entry_id, e.seq, e.entry_date, e.raw_date_heading, e.text,
                   w.source, w.source_id, w.title, w.creator, w.year, w.language,
                   w.copyright_status, w.url, w.narrative_score, w.everyday_score,
                   w.drama_score, w.n_words
            FROM entries e JOIN works w ON w.id = e.work_id
            {cond}
            ORDER BY w.id, e.seq
            """
        )
