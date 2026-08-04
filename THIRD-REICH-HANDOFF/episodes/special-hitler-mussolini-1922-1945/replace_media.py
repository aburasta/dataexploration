import json, time, urllib.parse, subprocess, os, shutil
SLUG="special-hitler-mussolini-1922-1945"
MEDIA=f"THIRD-REICH-HANDOFF/reich-engine/public/media/{SLUG}"
API="https://commons.wikimedia.org/w/api.php"
UA="ThumbnailFetch/1.0 (research; contact tafohousemafia@gmail.com)"
BAD=("coat of arms","wappen","flag of","locator","location map","openstreetmap","stamp","logo","djvu",
     "google","medal","banknote",".pdf","map of","chart","kinderbild","quote","careless talk","diaries",
     "grave of","cemetery","voetbal","football","title","band (","saint mary","christ child")
REQUERY={
 "04":["Adolf Hitler 1921 portrait","Hitler early 1920s Munich portrait"],
 "09":["Mussolini Palazzo Venezia speech","Benito Mussolini 1934 balcony"],
 "11":["Benito Mussolini profile 1935","Mussolini military uniform 1930s"],
 "15":["Engelbert Dollfuss 1933","Dollfuss Bundeskanzler portrait"],
 "16":["Festspielhaus Bayreuth building","Bayreuth Wagner opera house"],
 "17":["Regio Esercito 1934 soldiers","Italian army alpini 1930s"],
 "26":["Adolf Hitler 1938 portrait","Hitler telephone Berghof"],
 "27":["Hitler Heldenplatz 1938","Hitler Linz Austria 1938 crowd"],
 "46":["Italian soldiers 1943","Regio Esercito 1943"],
 "47":["Joseph Goebbels 1942 portrait","Goebbels Bundesarchiv portrait"],
 "58":["Adolf Hitler 1944 portrait","Hitler 1945 last photograph"],
 "59":["Reichskanzlei 1945 zerstört","Reich Chancellery Berlin 1945 ruins"],
}
REUSE={"12":"14","23":"31","52":"60","53":"21","57":"03"}
def api_search(q,limit=10):
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
        cands.append((title, ii.get("thumburl") or ii.get("url")))
    return cands
src=json.load(open(f"THIRD-REICH-HANDOFF/episodes/{SLUG}/media-sources.json"))
for bid,queries in REQUERY.items():
    got=None
    for q in queries:
        for title,thumb in api_search(q): got=(title,thumb,q);break
        if got: break
        time.sleep(0.4)
    if not got: print(f"[{bid}] STILL NONE {queries}");continue
    title,thumb,q=got
    subprocess.run(["curl","-sL","-A",UA,"-o",f"{MEDIA}/{bid}.jpg",thumb])
    src[bid]={"title":title,"query":q,"bytes":os.path.getsize(f"{MEDIA}/{bid}.jpg")}
    print(f"[{bid}] {title[:60]} <= '{q}'");time.sleep(0.35)
for bid,ref in REUSE.items():
    shutil.copyfile(f"{MEDIA}/{ref}.jpg",f"{MEDIA}/{bid}.jpg")
    src[bid]={"title":f"[reuse beat {ref}] "+src.get(ref,{}).get('title',''),"reuse":ref}
    print(f"[{bid}] reuse <= {ref}")
json.dump(src,open(f"THIRD-REICH-HANDOFF/episodes/{SLUG}/media-sources.json","w"),indent=1,ensure_ascii=False)
print("done")
