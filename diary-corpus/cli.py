#!/usr/bin/env python3
"""diary-corpus command-line interface.

Commands:
  harvest   search a source, fetch public-domain diary texts, cache raw to disk
  segment   split cached texts into dated entries and load them into SQLite
  stats     print corpus statistics
  export    write the corpus to JSONL (NLP-ready)
  serve     launch the Flask reader (browse + full-text search)

Run `python cli.py <command> --help` for options.
"""
from __future__ import annotations

import argparse
import sys

from diarycorpus.config import Config


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="cli.py", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--config", help="path to config.yaml (default: project config.yaml)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_harvest = sub.add_parser("harvest", help="fetch public-domain diary texts")
    p_harvest.add_argument("--limit", type=int, default=20,
                           help="number of works to accept (default: 20)")
    p_harvest.add_argument("--refetch", action="store_true",
                           help="re-download even if a cached copy exists")

    sub.add_parser("segment", help="segment cached texts into entries and load into SQLite")
    sub.add_parser("curate", help="NLP-score works and select English narrative journals")

    p_stats = sub.add_parser("stats", help="print corpus statistics")
    p_stats.add_argument("--all", action="store_true",
                         help="include unselected works (default: curated only)")

    p_export = sub.add_parser("export", help="export curated corpus to JSONL")
    p_export.add_argument("--filename", default="entries.jsonl")
    p_export.add_argument("--all", action="store_true",
                          help="export every work, not just curated ones")

    p_serve = sub.add_parser("serve", help="launch the Flask reader")
    p_serve.add_argument("--host", default="127.0.0.1")
    p_serve.add_argument("--port", type=int, default=5000)

    p_page = sub.add_parser("page", help="build a self-contained static reading-room HTML")
    p_page.add_argument("--out", default=None, help="output path (default: corpus/export/reading-room.html)")

    p_journals = sub.add_parser(
        "journals", help="write one text file per curated journal (+ index + zip)")
    p_journals.add_argument("--all", action="store_true",
                            help="include every work, not just curated ones")

    args = parser.parse_args(argv)
    config = Config.load(args.config)

    if args.command == "harvest":
        from diarycorpus.harvest import harvest
        harvest(config, limit=args.limit, refetch=args.refetch)
    elif args.command == "segment":
        from diarycorpus.ingest import ingest
        ingest(config)
    elif args.command == "curate":
        from diarycorpus.curate import curate
        curate(config)
    elif args.command == "stats":
        _print_stats(config, selected_only=not args.all)
    elif args.command == "export":
        from diarycorpus.export import export_jsonl
        export_jsonl(config, filename=args.filename, selected_only=not args.all)
    elif args.command == "serve":
        from diarycorpus.reader.app import serve
        serve(config, host=args.host, port=args.port)
    elif args.command == "page":
        from diarycorpus.staticpage import build_page
        build_page(config, out_path=args.out)
    elif args.command == "journals":
        from diarycorpus.journals import export_journals
        export_journals(config, selected_only=not args.all)
    else:  # pragma: no cover
        parser.print_help()
        return 1
    return 0


def _print_stats(config: Config, selected_only: bool = True) -> None:
    from pathlib import Path
    from diarycorpus.store import Store

    if not Path(config.db_path).exists():
        print(f"[stats] no database at {config.db_path} — run harvest + segment first")
        return
    with Store(config.db_path) as s:
        st = s.stats(selected_only=selected_only)
    label = "curated" if selected_only else "all"
    print(f"Works ({label}):  {st['works']}" +
          (f"  (of {st['total_works']} harvested)" if selected_only else ""))
    print(f"Entries:  {st['entries']}")
    if st["year_min"]:
        print(f"Years:    {st['year_min']}–{st['year_max']}")
    if st["languages"]:
        langs = ", ".join(f"{lang or '?'} ({n})" for lang, n in st["languages"][:8])
        print(f"Languages: {langs}")
    if selected_only and st["works"] == 0:
        print("(nothing curated yet — run `python cli.py curate`)")


if __name__ == "__main__":
    sys.exit(main())
