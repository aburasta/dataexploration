"""Generate a single self-contained HTML reading-room page from the curated corpus.

Reads selected works + their entries from the store and embeds them (with the NLP
scores) into one static, offline-openable HTML file with client-side search,
diarist filters and per-entry links back to the original scan.
"""
from __future__ import annotations

import html
import json
from collections import OrderedDict
from pathlib import Path

from .config import Config
from .store import Store


def build_page(config: Config, out_path: str | Path | None = None,
               selected_only: bool = True, max_entry_chars: int = 6000) -> Path:
    """Build the self-contained reading-room HTML.

    Entry text is capped at `max_entry_chars` so the page stays a reasonable size
    even when a journal segments into one enormous whole-work blob; the complete
    text always lives in the JSONL export, and every entry links to its scan.
    """
    out = Path(out_path) if out_path else config.export_dir / "reading-room.html"
    out.parent.mkdir(parents=True, exist_ok=True)

    with Store(config.db_path) as s:
        works = s.list_works(selected_only=selected_only)
        entries = []
        for w in works:
            creator = (w["creator"] or "Unknown")
            short = creator.split(",")[0].strip() if creator else "Unknown"
            for e in s.get_entries(w["id"]):
                text = e["text"]
                truncated = len(text) > max_entry_chars
                if truncated:
                    cut = text.rfind(" ", 0, max_entry_chars)
                    text = text[: cut if cut > 0 else max_entry_chars]
                entries.append({
                    "diarist": short,
                    "creator_full": creator,
                    "title": w["title"],
                    "year": w["year"],
                    "url": w["url"],
                    "score": round(w["narrative_score"], 1) if w["narrative_score"] is not None else None,
                    "heading": e["raw_date_heading"],
                    "date": e["entry_date"],
                    "text": text,
                    "truncated": truncated,
                })

    by_diarist: "OrderedDict[str, int]" = OrderedDict()
    for e in entries:
        by_diarist[e["diarist"]] = by_diarist.get(e["diarist"], 0) + 1
    years = [w["year"] for w in works if w["year"]]
    stats = {
        "works": len(works), "entries": len(entries),
        "diarists": len(by_diarist),
        "year_min": min(years) if years else None,
        "year_max": max(years) if years else None,
    }
    payload = json.dumps({
        "entries": entries, "stats": stats,
        "diarists": [{"name": k, "count": v} for k, v in
                     sorted(by_diarist.items(), key=lambda kv: -kv[1])],
    }, ensure_ascii=False)

    html_doc = _TEMPLATE.replace("__PAYLOAD__", payload) \
                        .replace("__STATS_WORKS__", str(stats["works"])) \
                        .replace("__STATS_ENTRIES__", str(stats["entries"])) \
                        .replace("__STATS_DIARISTS__", str(stats["diarists"])) \
                        .replace("__YEAR_MIN__", str(stats["year_min"] or "")) \
                        .replace("__YEAR_MAX__", str(stats["year_max"] or ""))
    out.write_text(html_doc, encoding="utf-8")
    print(f"[page] wrote {stats['works']} works / {stats['entries']} entries -> {out}")
    return out


# The page is intentionally one self-contained file (system fonts, inline CSS/JS)
# so it opens offline. Data is injected at __PAYLOAD__.
_TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Diaries of Everyday Life</title>
<style>
:root{
  --paper:#f0ede4; --raised:#f8f6ef; --edge:#d8d2c2;
  --ink:#241f1a; --soft:#5a5248; --faint:#8a8072;
  --accent:#8a5a2b; --accent-soft:#ece0cf; --mark-bg:#f3d9a8;
  --serif:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,"Times New Roman",serif;
  --mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace;
  --shadow:0 1px 0 #ffffff99,0 2px 12px -7px #2a221940;
}
@media (prefers-color-scheme:dark){:root{
  --paper:#191613; --raised:#221d18; --edge:#39312a;
  --ink:#eae3d7; --soft:#b7ac9c; --faint:#847a6c;
  --accent:#d99a5b; --accent-soft:#2e2519; --mark-bg:#3d2f18;
  --shadow:0 1px 0 #ffffff08,0 6px 20px -12px #000000aa;
}}
:root[data-theme="dark"]{--paper:#191613;--raised:#221d18;--edge:#39312a;--ink:#eae3d7;--soft:#b7ac9c;--faint:#847a6c;--accent:#d99a5b;--accent-soft:#2e2519;--mark-bg:#3d2f18;--shadow:0 1px 0 #ffffff08,0 6px 20px -12px #000000aa;}
:root[data-theme="light"]{--paper:#f0ede4;--raised:#f8f6ef;--edge:#d8d2c2;--ink:#241f1a;--soft:#5a5248;--faint:#8a8072;--accent:#8a5a2b;--accent-soft:#ece0cf;--mark-bg:#f3d9a8;--shadow:0 1px 0 #ffffff99,0 2px 12px -7px #2a221940;}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--serif);line-height:1.62}
.wrap{max-width:1060px;margin:0 auto;padding:0 clamp(1rem,4vw,2.4rem)}
a{color:var(--accent);text-underline-offset:2px}
header.mast{padding:clamp(2.2rem,6vw,4rem) 0 1.5rem;border-bottom:1px solid var(--edge)}
.eyebrow{font-family:var(--mono);font-size:.72rem;letter-spacing:.22em;text-transform:uppercase;color:var(--accent);margin:0 0 .9rem}
h1{font-size:clamp(2.1rem,6vw,3.5rem);line-height:1.02;margin:0;font-weight:600;letter-spacing:-.01em;text-wrap:balance}
.lede{max-width:60ch;color:var(--soft);font-size:1.08rem;margin:1rem 0 0}
.stats{display:flex;flex-wrap:wrap;gap:0 2.2rem;margin:1.6rem 0 0;font-family:var(--mono);font-size:.8rem;color:var(--faint);font-variant-numeric:tabular-nums}
.stats b{color:var(--ink);font-weight:600}
.controls{position:sticky;top:0;z-index:5;background:color-mix(in srgb,var(--paper) 88%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--edge);padding:.85rem 0}
.controls .row{display:flex;gap:.7rem;align-items:center;flex-wrap:wrap}
.search{flex:1 1 240px;display:flex;align-items:center;gap:.55rem;background:var(--raised);border:1px solid var(--edge);border-radius:2px;padding:.55rem .8rem;box-shadow:var(--shadow)}
.search input{border:0;background:transparent;font:inherit;color:var(--ink);width:100%;outline:none}
.search svg{flex:none;opacity:.5}
.count{font-family:var(--mono);font-size:.74rem;color:var(--faint);white-space:nowrap}
button.theme{border:1px solid var(--edge);background:var(--raised);color:var(--soft);font-family:var(--mono);font-size:.72rem;padding:.5rem .7rem;border-radius:2px;cursor:pointer}
button.theme:hover{color:var(--ink)}
.chips{display:flex;gap:.4rem;flex-wrap:wrap;padding:1rem 0 .2rem}
.chip{font-family:var(--mono);font-size:.71rem;padding:.34rem .6rem;border:1px solid var(--edge);border-radius:100px;background:transparent;color:var(--soft);cursor:pointer;transition:.12s}
.chip:hover{border-color:var(--accent);color:var(--ink)}
.chip[aria-pressed="true"]{background:var(--accent);border-color:var(--accent);color:var(--paper)}
.chip .n{opacity:.65}
main{padding:1.4rem 0 5rem}
.entry{border:1px solid var(--edge);background:var(--raised);border-radius:3px;box-shadow:var(--shadow);padding:1.3rem 1.5rem;margin:0 0 1.1rem}
.entry .meta{display:flex;flex-wrap:wrap;gap:.4rem 1rem;align-items:baseline;font-family:var(--mono);font-size:.73rem;color:var(--faint);margin:0 0 .7rem;padding:0 0 .7rem;border-bottom:1px dotted var(--edge)}
.entry .date{color:var(--accent);font-weight:600}
.entry .who b{color:var(--ink);font-weight:600}
.entry .body{font-size:1.03rem;white-space:pre-wrap;word-break:break-word;max-height:16em;overflow:hidden;position:relative;transition:max-height .2s}
.entry .body.expanded{max-height:none}
.entry .body:not(.expanded)::after{content:"";position:absolute;left:0;right:0;bottom:0;height:4em;background:linear-gradient(transparent,var(--raised))}
.entry .foot{display:flex;gap:1rem;align-items:center;margin-top:.7rem}
.entry .more{font-family:var(--mono);font-size:.72rem;background:none;border:0;color:var(--accent);cursor:pointer;padding:0}
.entry .trunc{font-family:var(--mono);font-size:.68rem;color:var(--faint);font-style:italic}
.entry .src{font-family:var(--mono);font-size:.72rem;margin-left:auto}
mark{background:var(--mark-bg);color:var(--ink);padding:0 .1em;border-radius:1px}
.empty{text-align:center;color:var(--faint);padding:3rem 0;font-family:var(--mono);font-size:.82rem}
.note{background:var(--accent-soft);border:1px solid var(--edge);border-radius:3px;padding:.85rem 1.1rem;margin:1.4rem 0 0;font-size:.92rem;color:var(--soft)}
.note b{color:var(--ink)}
footer{border-top:1px solid var(--edge);padding:2rem 0 3rem;color:var(--faint);font-family:var(--mono);font-size:.74rem;line-height:1.7}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
</style>
</head>
<body>
<header class="mast"><div class="wrap">
  <p class="eyebrow">Public domain &middot; English &middot; NLP-curated</p>
  <h1>Diaries of Everyday Life</h1>
  <p class="lede">Personal journals of real people &mdash; ministers, soldiers,
  travellers and householders &mdash; kept over months and years. Each was scored
  for narrative richness and everyday or dramatic content, and only substantial,
  story-like journals made the cut. Every entry links back to its original scan.</p>
  <div class="stats">
    <span><b>__STATS_WORKS__</b> journals</span>
    <span><b>__STATS_ENTRIES__</b> entries</span>
    <span><b>__STATS_DIARISTS__</b> diarists</span>
    <span><b>__YEAR_MIN__&ndash;__YEAR_MAX__</b></span>
  </div>
</div></header>
<div class="controls"><div class="wrap"><div class="row">
  <label class="search">
    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg>
    <input id="q" type="search" placeholder="Search every entry&hellip;" autocomplete="off">
  </label>
  <span id="count" class="count"></span>
  <button id="theme" class="theme">&#9728; Theme</button>
</div><div id="chips" class="chips"></div></div></div>
<div class="wrap"><div class="note"><b>How this was made:</b> harvested from the
Internet Archive, filtered to public-domain English diaries, then an NLP pass
scored each journal for first-person narrative, everyday-life and dramatic
vocabulary (and penalized naturalist field-notes). Text is OCR from handwriting,
so expect rough patches &mdash; the <b>&ldquo;View original scan&rdquo;</b> link shows the real page.</div></div>
<main><div class="wrap"><div id="list"></div></div></main>
<footer><div class="wrap">Built with the diary-corpus retriever &mdash; search &rarr;
public-domain filter &rarr; OCR download &rarr; segmentation &rarr; NLP curation. Source: archive.org.</div></footer>
<script id="data" type="application/json">__PAYLOAD__</script>
<script>
const DATA=JSON.parse(document.getElementById('data').textContent);
const listEl=document.getElementById('list'),countEl=document.getElementById('count'),chipsEl=document.getElementById('chips'),searchEl=document.getElementById('q');
let activeDiarist=null,query='';
DATA.diarists.forEach(d=>{const b=document.createElement('button');b.className='chip';b.setAttribute('aria-pressed','false');b.innerHTML=`${esc(d.name)} <span class="n">${d.count}</span>`;b.onclick=()=>{activeDiarist=activeDiarist===d.name?null:d.name;[...chipsEl.children].forEach(c=>c.setAttribute('aria-pressed',c===b&&activeDiarist?'true':'false'));render();};chipsEl.appendChild(b);});
function esc(s){return (s||'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));}
function hi(t,q){const e=esc(t);if(!q)return e;try{const re=new RegExp('('+q.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+')','ig');return e.replace(re,'<mark>$1</mark>');}catch(_){return e;}}
function render(){const q=query.trim().toLowerCase();let rows=DATA.entries;if(activeDiarist)rows=rows.filter(e=>e.diarist===activeDiarist);if(q)rows=rows.filter(e=>(e.text||'').toLowerCase().includes(q)||(e.heading||'').toLowerCase().includes(q)||(e.creator_full||'').toLowerCase().includes(q)||(e.title||'').toLowerCase().includes(q));countEl.textContent=rows.length+(rows.length===1?' entry':' entries');listEl.innerHTML='';if(!rows.length){listEl.innerHTML='<div class="empty">No entries match &mdash; try another word or clear the filter.</div>';return;}const frag=document.createDocumentFragment();rows.forEach(e=>frag.appendChild(card(e,query.trim())));listEl.appendChild(frag);}
function card(e,q){const el=document.createElement('article');el.className='entry';const head=e.heading||e.date||'Undated entry';const yr=e.year?' &middot; '+e.year:'';const tnote=e.truncated?'<span class="trunc">preview &middot; full text in original scan</span>':'';el.innerHTML=`<div class="meta"><span class="date">${esc(head)}</span><span class="who"><b>${esc(e.diarist)}</b>${yr}</span>${e.title?`<span>${esc(e.title).slice(0,60)}</span>`:''}</div><div class="body">${hi(e.text,q)}</div><div class="foot"><button class="more">Read full entry</button>${tnote}${e.url?`<a class="src" href="${esc(e.url)}" target="_blank" rel="noopener">View original scan &#8599;</a>`:''}</div>`;const body=el.querySelector('.body'),more=el.querySelector('.more');requestAnimationFrame(()=>{if(body.scrollHeight<=body.clientHeight+4)more.style.display='none';});more.onclick=()=>{const x=body.classList.toggle('expanded');more.textContent=x?'Collapse':'Read full entry';};return el;}
searchEl.addEventListener('input',e=>{query=e.target.value;render();});
const root=document.documentElement,tbtn=document.getElementById('theme');
tbtn.onclick=()=>{const cur=root.getAttribute('data-theme')||(matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light');const next=cur==='dark'?'light':'dark';root.setAttribute('data-theme',next);tbtn.textContent=next==='dark'?'☾ Dark':'☀ Light';};
render();
</script>
</body>
</html>
"""
