#!/usr/bin/env python3
import json, time, urllib.parse, subprocess, os
SLUG="special-hitler-mussolini-1922-1945"
MEDIA=f"THIRD-REICH-HANDOFF/reich-engine/public/media/{SLUG}"
os.makedirs(MEDIA, exist_ok=True)
API="https://commons.wikimedia.org/w/api.php"
UA="ThumbnailFetch/1.0 (research; contact tafohousemafia@gmail.com)"
plan=json.load(open(f"THIRD-REICH-HANDOFF/episodes/{SLUG}/plan.json"))
BAD=("coat of arms","wappen","flag of","locator","location map","stamp","briefmarke","logo",
     "djvu","film daily","journalism review","library annual","ibis -","diary of the times",
     "google","medal","banknote",".pdf","volume","annual","review volume","organisationsbuc",
     "map of","chart","poster stamp")
def api_search(q,limit=8):
    params={"action":"query","format":"json","generator":"search","gsrsearch":q,
            "gsrnamespace":"6","gsrlimit":str(limit),"prop":"imageinfo",
            "iiprop":"url|size|mime","iiurlwidth":"1500"}
    out=subprocess.run(["curl","-s","-A",UA,API+"?"+urllib.parse.urlencode(params)],capture_output=True,text=True).stdout
    try: d=json.loads(out)
    except: return []
    cands=[]
    for v in sorted(d.get("query",{}).get("pages",{}).values(),key=lambda x:x.get("index",99)):
        ii=v.get("imageinfo",[{}])[0];title=v.get("title","");low=title.lower();mime=ii.get("mime","")
        if not mime.startswith("image/") or mime=="image/svg+xml": continue
        if any(b in low for b in BAD): continue
        w,h=ii.get("width",0),ii.get("height",0)
        if w<350 or h<350: continue
        cands.append((title, ii.get("thumburl") or ii.get("url"),w,h))
    return cands
results={};used=set()
for r in plan:
    bid=r["id"];queries=[r["query"]]+r.get("alts",[]);got=None
    for q in queries:
        for title,thumb,w,h in api_search(q):
            if title in used: continue
            got=(title,thumb,w,h,q);used.add(title);break
        if got: break
        time.sleep(0.4)
    if not got:
        print(f"[{bid}] NO RESULT {queries}");results[bid]=None;continue
    title,thumb,w,h,q=got
    subprocess.run(["curl","-sL","-A",UA,"-o",f"{MEDIA}/{bid}.jpg",thumb])
    sz=os.path.getsize(f"{MEDIA}/{bid}.jpg") if os.path.exists(f"{MEDIA}/{bid}.jpg") else 0
    results[bid]={"title":title,"query":q,"w":w,"h":h,"bytes":sz,"src":thumb}
    print(f"[{bid}] {sz//1024}KB {title[:66]} <= '{q}'")
    time.sleep(0.35)
json.dump(results,open(f"THIRD-REICH-HANDOFF/episodes/{SLUG}/media-sources.json","w"),indent=1,ensure_ascii=False)
miss=[k for k,v in results.items() if not v]
print(f"\nDONE got={sum(1 for v in results.values() if v)}/{len(plan)} missing={miss}")
