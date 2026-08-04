#!/usr/bin/env python3
"""Source one Commons image per beat into reich-engine media dir. PD/CC tier."""
import json, time, urllib.parse, subprocess, os, sys

MEDIA = "THIRD-REICH-HANDOFF/reich-engine/public/media/special-reichstag-fire-1933"
os.makedirs(MEDIA, exist_ok=True)
API = "https://commons.wikimedia.org/w/api.php"
UA = "ThumbnailFetch/1.0 (research; contact tafohousemafia@gmail.com)"
plan = json.load(open("THIRD-REICH-HANDOFF/episodes/special-reichstag-fire-1933/plan.json"))

BAD = ("coat of arms","wappen","flag of","location map","locator","stamp","briefmarke",
       "logo","map of","medal","orden ","banknote","chart")

def api_search(q, limit=8):
    params = {"action":"query","format":"json","generator":"search","gsrsearch":q,
              "gsrnamespace":"6","gsrlimit":str(limit),"prop":"imageinfo",
              "iiprop":"url|size|mime|extmetadata","iiurlwidth":"1500"}
    url = API+"?"+urllib.parse.urlencode(params)
    out = subprocess.run(["curl","-s","-A",UA,url],capture_output=True,text=True).stdout
    try: d=json.loads(out)
    except: return []
    pages=d.get("query",{}).get("pages",{})
    res=sorted(pages.values(), key=lambda x:x.get("index",99))
    cands=[]
    for v in res:
        ii=v.get("imageinfo",[{}])[0]
        title=v.get("title","")
        mime=ii.get("mime","")
        if not mime.startswith("image/"): continue
        if ii.get("mime")=="image/svg+xml": continue
        low=title.lower()
        if any(b in low for b in BAD): continue
        w=ii.get("width",0); h=ii.get("height",0)
        if w<300 or h<300: continue
        thumb=ii.get("thumburl") or ii.get("url")
        cands.append((title,thumb,w,h))
    return cands

results={}
used=set()
for r in plan:
    bid=r["id"]; queries=[r["query"]]+r.get("alts",[])
    got=None
    for q in queries:
        cands=api_search(q)
        for title,thumb,w,h in cands:
            if title in used: continue
            got=(title,thumb,w,h,q); used.add(title); break
        if got: break
        time.sleep(0.5)
    if not got:
        print(f"[{bid}] NO RESULT for {queries}"); results[bid]=None; continue
    title,thumb,w,h,q=got
    dest=f"{MEDIA}/{bid}.jpg"
    subprocess.run(["curl","-sL","-A",UA,"-o",dest,thumb])
    sz=os.path.getsize(dest) if os.path.exists(dest) else 0
    results[bid]={"title":title,"query":q,"w":w,"h":h,"bytes":sz,"src":thumb}
    print(f"[{bid}] {sz//1024}KB  {title[:70]}  <= '{q}'")
    time.sleep(0.4)

json.dump(results, open("THIRD-REICH-HANDOFF/episodes/special-reichstag-fire-1933/media-sources.json","w"),indent=1,ensure_ascii=False)
miss=[k for k,v in results.items() if not v]
print(f"\nDONE. got={sum(1 for v in results.values() if v)}/{len(plan)}  missing={miss}")
