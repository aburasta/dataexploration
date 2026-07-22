"""Minimal Flask reader: browse works, read entries, full-text search.

Backed by the SQLite store's FTS5 index. Read-only.
"""
from __future__ import annotations

from pathlib import Path

from flask import Flask, abort, render_template, request

from ..config import Config
from ..store import Store


def create_app(config: Config | None = None) -> Flask:
    config = config or Config.load()
    app = Flask(__name__)
    app.config["DIARY_CONFIG"] = config

    def store() -> Store:
        return Store(config.db_path)

    @app.route("/")
    def index():
        with store() as s:
            works = s.list_works(selected_only=True)
            stats = s.stats(selected_only=True)
        return render_template("index.html", works=works, stats=stats)

    @app.route("/work/<int:work_id>")
    def work(work_id: int):
        with store() as s:
            w = s.get_work(work_id)
            if w is None:
                abort(404)
            entries = s.get_entries(work_id)
        return render_template("work.html", work=w, entries=entries)

    @app.route("/search")
    def search():
        query = (request.args.get("q") or "").strip()
        results = []
        error = None
        if query:
            with store() as s:
                try:
                    results = s.search_entries(query, limit=100, selected_only=True)
                except Exception as exc:  # FTS syntax errors -> friendly message
                    error = f"Search error: {exc}"
        return render_template("search.html", query=query, results=results, error=error)

    return app


def serve(config: Config, host: str = "127.0.0.1", port: int = 5000) -> None:
    if not Path(config.db_path).exists():
        print(f"[serve] database not found at {config.db_path} — run harvest + segment first")
        return
    app = create_app(config)
    print(f"[serve] reader at http://{host}:{port}  (Ctrl-C to stop)")
    app.run(host=host, port=port, debug=False)
