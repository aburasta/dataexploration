#!/usr/bin/env python3
"""Second pass: replace wrong/modern/illustration images with tuned queries + reuses."""
import json, time, urllib.parse, subprocess, os, shutil

MEDIA = "THIRD-REICH-HANDOFF/reich-engine/public/media/special-reichstag-fire-1933"
API = "https://commons.wikimedia.org/w/api.php"
UA = "ThumbnailFetch/1.0 (research; contact tafohousemafia@gmail.com)"

BAD = ("coat of arms","wappen","flag of","locator","location map","stamp","briefmarke","logo",
       "djvu","film daily","journalism review","library annual","ibis -","diary of the times",
       "google","checkpoint","bundesverwaltungsgericht","medal","banknote",".pdf","volume",
       "annual","review volume","organisationsbuc")

# beat -> list of queries to try
REQUERY = {
 "08":["Karl-Liebknecht-Haus 1932","Berlin Karl Liebknecht Haus KPD 1931"],
 "10":["Reichstag Berlin 1926","Reichstagsgebäude 1928 Postkarte"],
 "12":["Berlin Wilhelmstrasse 1932","Berlin Leipziger Strasse 1931 nacht"],
 "15":["Bundesarchiv Goebbels Rede 1932","Joseph Goebbels 1932 speaking"],
 "17":["Bundesarchiv Auto 1933 Berlin","Mercedes-Benz 1933 Bundesarchiv"],
 "19":["Reichstagsbrand Feuerwehr","Reichstag fire firemen 1933"],
 "21":["Bundesarchiv Göring Rede 1933","Hermann Göring speech 1933"],
 "23":["Bundesarchiv Reichstag ausgebrannt","Reichstag Plenarsaal Brand 1933"],
 "26":["Bundesarchiv Sturmabteilung 1933 Berlin","SA Aufmarsch 1933"],
 "30":["Karl Ernst SA Gruppenführer","Karl Ernst Obergruppenführer"],
 "31":["Bundesarchiv SA Marsch 1933","Sturmabteilung Umzug 1933"],
 "34":["Hans Bernd Gisevius","Gisevius Widerstand"],
 "42":["Bundesarchiv SA Lastwagen 1933","SA Razzia Berlin 1933"],
 "45":["Hermann Göring Ansprache 1933","Göring Rede Menge 1933"],
 "50":["Reichstagsbrandprozess Gerichtssaal","Leipzig Reichsgericht Prozess 1933"],
 "56":["Ernst Röhm 1933","Ernst Röhm SA Stabschef"],
 "57":["Bundesarchiv SA Formation 1933","Sturmabteilung Berlin Parade 1933"],
}
# beat -> reuse existing beat file (same subject already sourced well)
REUSE = {"35":"22","36":"03","52":"27","54":"27","59":"37"}

def api_search(q, limit=10):
    params={"action":"query","format":"json","generator":"search","gsrsearch":q,
            "gsrnamespace":"6","gsrlimit":str(limit),"prop":"imageinfo",
            "iiprop":"url|size|mime","iiurlwidth":"1500"}
    out=subprocess.run(["curl","-s","-A",UA,API+"?"+urllib.parse.urlencode(params)],
                       capture_output=True,text=True).stdout
    try: d=json.loads(out)
    except: return []
    pages=d.get("query",{}).get("pages",{})
    cands=[]
    for v in sorted(pages.values(),key=lambda x:x.get("index",99)):
        ii=v.get("imageinfo",[{}])[0]; title=v.get("title",""); low=title.lower()
        mime=ii.get("mime","")
        if not mime.startswith("image/") or mime=="image/svg+xml": continue
        if any(b in low for b in BAD): continue
        w,h=ii.get("width",0),ii.get("height",0)
        if w<350 or h<350: continue
        cands.append((title, ii.get("thumburl") or ii.get("url")))
    return cands

src=json.load(open(f"THIRD-REICH-HANDOFF/episodes/special-reichstag-fire-1933/media-sources.json"))
for bid,queries in REQUERY.items():
    got=None
    for q in queries:
        for title,thumb in api_search(q):
            got=(title,thumb,q); break
        if got: break
        time.sleep(0.5)
    if not got:
        print(f"[{bid}] STILL NO RESULT {queries}"); continue
    title,thumb,q=got
    subprocess.run(["curl","-sL","-A",UA,"-o",f"{MEDIA}/{bid}.jpg",thumb])
    sz=os.path.getsize(f"{MEDIA}/{bid}.jpg")
    src[bid]={"title":title,"query":q,"bytes":sz,"src":thumb}
    print(f"[{bid}] {sz//1024}KB {title[:66]} <= '{q}'")
    time.sleep(0.4)

for bid,ref in REUSE.items():
    shutil.copyfile(f"{MEDIA}/{ref}.jpg", f"{MEDIA}/{bid}.jpg")
    src[bid]={"title":f"[reuse of beat {ref}] "+src.get(ref,{}).get('title',''),"reuse":ref}
    print(f"[{bid}] reuse <= beat {ref}")

json.dump(src, open(f"THIRD-REICH-HANDOFF/episodes/special-reichstag-fire-1933/media-sources.json","w"),indent=1,ensure_ascii=False)
print("done")
