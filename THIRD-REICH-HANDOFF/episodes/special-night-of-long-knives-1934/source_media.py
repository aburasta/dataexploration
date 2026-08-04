#!/usr/bin/env python3
import json, time, urllib.parse, subprocess, os
SLUG="special-night-of-long-knives-1934"
MEDIA=f"THIRD-REICH-HANDOFF/reich-engine/public/media/{SLUG}"
os.makedirs(MEDIA, exist_ok=True)
API="https://commons.wikimedia.org/w/api.php"
UA="ThumbnailFetch/1.0 (research; contact tafohousemafia@gmail.com)"
plan=json.load(open(f"THIRD-REICH-HANDOFF/episodes/{SLUG}/plan.json"))
BAD=("coat of arms","wappen","flag of","locator","location map","openstreetmap","stamp","logo","djvu",
     "google","medal","banknote",".pdf","volume","annual","organisationsbuc","map of","chart","insignia",
     "monument","memorial","denkmal","gedenktafel","museum","reenact","bundeswehr","2015","2016","2017",
     "2018","2019","2020","2021","2022","2023","2024","modern")
def api_search(q,limit=9):
    params={"action":"query","format":"json","generator":"search","gsrsearch":q,"gsrnamespace":"6",
            "gsrlimit":str(limit),"prop":"imageinfo","iiprop":"url|size|mime","iiurlwidth":"1500"}
    out=subprocess.run(["curl","-s","-A",UA,API+"?"+urllib.parse.urlencode(params)],capture_output=True,text=True).stdout
    try: d=json.loads(out)
    except: return []
    cands=[]
    for v in sorted(d.get("query",{}).get("pages",{}).values(),key=lambda x:x.get("index",99)):
        ii=v.get("imageinfo",[{}])[0];title=v.get("title","");low=title.lower();mime=ii.get("mime","")
        if not mime.startswith("image/") or mime=="image/svg+xml": continue
        if any(b in low for b in BAD): continue
        if ii.get("width",0)<350 or ii.get("height",0)<350: continue
        cands.append((title, ii.get("thumburl") or ii.get("url"),ii.get("width"),ii.get("height")))
    return cands
results={};used=set()
for r in plan:
    if r["kind"]!="IMG":
        results[r["id"]]={"clip":r["ref"]}; continue
    bid=r["id"];queries=r["ref"] if isinstance(r["ref"],list) else [r["ref"]];got=None
    for q in queries:
        for title,thumb,w,h in api_search(q):
            if title in used: continue
            got=(title,thumb,q);used.add(title);break
        if got: break
        time.sleep(0.35)
    if not got:
        print(f"[{bid}] NO RESULT {queries}");results[bid]=None;continue
    title,thumb,q=got
    subprocess.run(["curl","-sL","-A",UA,"-o",f"{MEDIA}/{bid}.jpg",thumb])
    sz=os.path.getsize(f"{MEDIA}/{bid}.jpg") if os.path.exists(f"{MEDIA}/{bid}.jpg") else 0
    results[bid]={"title":title,"query":q,"bytes":sz,"src":thumb}
    print(f"[{bid}] {sz//1024}KB {title[:60]} <= '{q}'")
    time.sleep(0.3)
json.dump(results,open(f"THIRD-REICH-HANDOFF/episodes/{SLUG}/media-sources.json","w"),indent=1,ensure_ascii=False)
miss=[k for k,v in results.items() if v is None]
print(f"\nDONE images_got={sum(1 for v in results.values() if v and 'title' in v)} missing={miss}")
