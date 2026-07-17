import json,os
MEDIA=os.path.join(os.path.dirname(__file__),"..","public","media","special-legal-coup-1919-1933")
mf=json.load(open(os.path.join(MEDIA,"_manifest_sourcing.json")))
def key(t): t=t["tag"]; return (0,int(t)) if t.isdigit() else (1,t)
mf.sort(key=key)
ok=[r for r in mf if r.get("status")=="ok"]; miss=[r for r in mf if r.get("status")=="miss"]
img=[r for r in ok if r.get("type")!="video"]; vid=[r for r in ok if r.get("type")=="video"]
L=["# Legal Coup - Media Sourcing Manifest",
   f"\n**{len(ok)} beats sourced** ({len(img)} images, {len(vid)} video) - **{len(miss)} pending**\n",
   "## Video clips","| Beat | File | Source | Clip | Shows |","|---|---|---|---|---|"]
for r in vid: L.append(f"| {r['tag']} | {r['file']} | {r.get('source','')} | {r.get('clip','')} | {r.get('note','')} |")
L+=["\n## Images","| Beat | File | License | Source page | Title |","|---|---|---|---|---|"]
for r in img: L.append(f"| {r['tag']} | {r.get('file','')} | {r.get('license','')} | {r.get('page','')} | {r.get('title','')[:55]} |")
if miss: L.append("\n## Pending: "+", ".join(sorted(m['tag'] for m in miss)))
open(os.path.join(os.path.dirname(__file__),"MANIFEST_readable.md"),"w").write("\n".join(L))
print("manifest:",len(ok),"ok",len(miss),"miss")
