#!/usr/bin/env python3
"""
Source public-domain / freely-licensed stills from Wikimedia Commons for the
Legal Coup episode, one file per script beat.

Usage:  python3 source_commons.py queries_batchN.json
  queries file = JSON list of {"tag": "1", "query": "Adolf Hitler Hindenburg", "type": "img"}

Downloads chosen file (server-capped to <=1920px long edge) into the episode media
dir as <tag>.<ext> and appends a row to _manifest_sourcing.json in that dir.
Only licenses in ALLOWED are accepted; anything else -> logged as a MISS for manual review.
"""
import json, sys, os, re, time, urllib.parse, urllib.request, html

MEDIA_DIR = os.path.join(os.path.dirname(__file__), "..", "public", "media", "special-legal-coup-1919-1933")
MEDIA_DIR = os.path.abspath(MEDIA_DIR)
MANIFEST = os.path.join(MEDIA_DIR, "_manifest_sourcing.json")
API = "https://commons.wikimedia.org/w/api.php"
UA = "LegalCoupDocBot/1.0 (educational WW2 history documentary; non-commercial research)"

# license ranking: lower = preferred. Accept PD / CC0 / CC-BY / CC-BY-SA.
def license_rank(short):
    s = (short or "").lower()
    if "public domain" in s or s in ("pd", "cc0") or "cc0" in s:
        return 0
    if re.search(r"cc[\s-]?by(?![\s-]?sa)", s):
        return 1
    if re.search(r"cc[\s-]?by[\s-]?sa", s):
        return 2
    return 99  # non-free / unknown -> reject

BAD_EXT = (".svg", ".gif", ".tif", ".tiff", ".ogv", ".webm", ".pdf", ".djvu", ".ogg", ".oga", ".wav", ".flac", ".mp3", ".mid")

def fetch(url, timeout=60, tries=6):
    """GET with exponential backoff, honoring Retry-After on 429/503."""
    delay = 2.0
    for attempt in range(tries):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code in (429, 503) and attempt < tries - 1:
                ra = e.headers.get("Retry-After")
                wait = float(ra) if (ra and ra.isdigit()) else delay
                time.sleep(min(wait, 60)); delay *= 2; continue
            raise
        except Exception:
            if attempt < tries - 1:
                time.sleep(delay); delay *= 2; continue
            raise

def api_get(params):
    params = dict(params); params["format"] = "json"; params["maxlag"] = 5
    url = API + "?" + urllib.parse.urlencode(params)
    return json.loads(fetch(url, timeout=40))

def clean(txt):
    if not txt: return ""
    txt = re.sub(r"<[^>]+>", "", txt)
    return html.unescape(txt).strip()

def search(query, limit=25):
    d = api_get({
        "action": "query", "generator": "search", "gsrnamespace": 6,
        "gsrsearch": query, "gsrlimit": limit,
        "prop": "imageinfo", "iiprop": "url|extmetadata|size|mime",
        "iiurlwidth": 1920,
    })
    pages = d.get("query", {}).get("pages", {})
    out = []
    for p in pages.values():
        ii = (p.get("imageinfo") or [{}])[0]
        title = p.get("title", "")
        if any(title.lower().endswith(e) for e in BAD_EXT):
            continue
        em = ii.get("extmetadata", {})
        lic = clean(em.get("LicenseShortName", {}).get("value", ""))
        rank = license_rank(lic)
        if rank == 99:
            continue
        w = ii.get("width", 0) or 0
        if w and w < 450:  # too small to be useful
            continue
        out.append({
            "title": title,
            "page": ii.get("descriptionurl", ""),
            "thumb": ii.get("thumburl") or ii.get("url"),
            "full": ii.get("url"),
            "w": ii.get("thumbwidth") or w, "h": ii.get("thumbheight") or ii.get("height", 0),
            "license": lic,
            "artist": clean(em.get("Artist", {}).get("value", "")),
            "credit": clean(em.get("Credit", {}).get("value", "")),
            "rank": rank,
            "index": p.get("index", 999),
        })
    # prefer better license, then original search relevance (index)
    out.sort(key=lambda c: (c["rank"], c.get("index", 999)))
    return out

def download(url, dest):
    data = fetch(url, timeout=90)
    with open(dest, "wb") as f:
        f.write(data)
    return os.path.getsize(dest)

def load_manifest():
    if os.path.exists(MANIFEST):
        return json.load(open(MANIFEST))
    return []

def main():
    queries = json.load(open(sys.argv[1]))
    manifest = load_manifest()
    have = {row["tag"] for row in manifest if row.get("status") == "ok"}
    # global de-dup: title -> tag that already uses it (across images AND video sources)
    used = {row["title"]: row["tag"] for row in manifest
            if row.get("status") == "ok" and row.get("title")}
    for q in queries:
        tag, query = q["tag"], q["query"]
        if tag in have and "--force" not in sys.argv:
            print(f"[{tag}] skip (already sourced)"); continue
        cands = search(query)
        # drop any candidate already used by a DIFFERENT tag (enforce variety)
        cands = [c for c in cands if used.get(c["title"], tag) == tag]
        if not cands:
            print(f"[{tag}] MISS  q='{query}'")
            manifest = [r for r in manifest if r["tag"] != tag]
            manifest.append({"tag": tag, "status": "miss", "query": query})
            time.sleep(1.5); continue
        c = cands[0]
        used[c["title"]] = tag
        ext = os.path.splitext(c["full"] or c["thumb"])[1].lower() or ".jpg"
        if ext not in (".jpg", ".jpeg", ".png", ".webp"): ext = ".jpg"
        fname = f"{tag}{ext}"
        try:
            size = download(c["thumb"], os.path.join(MEDIA_DIR, fname))
        except Exception as e:
            print(f"[{tag}] DL-FAIL {e}"); time.sleep(0.5); continue
        # validate
        try:
            from PIL import Image
            im = Image.open(os.path.join(MEDIA_DIR, fname)); im.verify()
            dims = f"{c['w']}x{c['h']}"
        except Exception as e:
            dims = f"UNVERIFIED({e})"
        manifest = [r for r in manifest if r["tag"] != tag]
        manifest.append({
            "tag": tag, "status": "ok", "file": fname, "query": query,
            "title": c["title"], "page": c["page"], "license": c["license"],
            "attribution": c["artist"] or c["credit"], "dims": dims,
            "alts": [x["title"] for x in cands[1:4]],
        })
        print(f"[{tag}] OK  {fname}  {c['license']:<16} {size//1024}KB  {c['title'][:60]}")
        json.dump(manifest, open(MANIFEST, "w"), indent=1, ensure_ascii=False)
        time.sleep(1.5)
    json.dump(manifest, open(MANIFEST, "w"), indent=1, ensure_ascii=False)
    ok = sum(1 for r in manifest if r["status"] == "ok")
    miss = sum(1 for r in manifest if r["status"] == "miss")
    print(f"\n== manifest: {ok} ok, {miss} miss, total {len(manifest)} ==")

if __name__ == "__main__":
    main()
