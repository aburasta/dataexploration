import json, os
from PIL import Image

MEDIA="/home/user/dataexploration/THIRD-REICH-HANDOFF/Media/hitler-mussolini"
AUDIO_LEN=620.90
OUTRO=6.0

# (src, motion, narration-span-for-timing) — in narrative order, best-fit real image per span
scenes=[
 ("s01.jpg","slow-push","April 29th, 1945. In a bunker under Berlin, Adolf Hitler receives a piece of news from Italy."),
 ("s03.jpg","settle","His oldest political friend, Benito Mussolini, is dead. Shot two days earlier by his own countrymen, then strung up by the heels from a lamppost in a Milan piazza, where a crowd spent a day spitting on the body."),
 ("s04.jpg","pan-right","In 1922, when Benito Mussolini marched his black shirts into Rome and simply took the government, it seemed unimaginable that this would be a reality within 30 years."),
 ("s05.jpg","pan-left","Hitler at that time was still building a fringe party in Bavaria and instantly takes inspiration and plans his own march on Berlin."),
 ("s06.jpg","slow-push","A year later, Hitler attempts it, but the plan does not even survive beyond the Munich Beer Hall, and by the time he marches his men to the centre of Munich, the police is waiting for them and his coup is already over."),
 ("s11.jpg","settle","By 1933, Hitler is Chancellor, and his days of petty street fighting is over, although his party has never stopped street fighting."),
 ("s14.jpg","pan-right","Hitler's brown shirts are a mirror reflection of Mussolini's black shirts."),
 ("s15.jpg","pan-left","At this point, Mussolini has been ruling Italy for over a decade already, contrary to popular perception, is unimpressed and unenthused about Hitler being in power."),
 ("s86.jpg","slow-push","A Germany that's strong right next door, threatened to put the Duce in the shade, and worse, a pan-German Reich would include Austria and the Balkans, which is territory Mussolini had already staked his own claims to."),
 ("s38.jpg","settle","From the very start, it was a relationship of convenience where Mussolini was the established dictator and Hitler was the imitator."),
 ("s19.jpg","slow-push","June 14th, 1934, their first face-to-face meeting, in Venice. It does not go well for Hitler. Privately, he feels Mussolini was condescending to him."),
 ("s02.jpg","settle","Hitler flies home irritated, feeling humiliated in front of the man he'd modelled himself on. It's a small moment, but it will not stay small."),
 ("s23.jpg","slow-push","Six weeks later, on July 25th, 1934, Austrian Nazis storm the Chancellery in Vienna and murder Chancellor Dollfuss."),
 ("s58.jpg","pan-right","Hitler, at the Wagner Festival in Bayreuth, can barely hide his delight when the news reaches him. But the coup collapses within hours and Mussolini, whom Hitler had personally promised in Venice he would leave Austria alone, responds by mobilising four full divisions to the Brenner Pass, right on Austria's border. Hitler backs down instantly."),
 ("s15b_UNUSED","settle",""),  # placeholder removed below
 ("s31.jpg","slow-push","A year and a half later, in October 1935, Mussolini invades Abyssinia, now Ethiopia, in open defiance of the League of Nations. Britain and France respond with sanctions. These sanctions are half-hearted and doomed to fail, but they are enough to permanently poison Mussolini's relationship with the West."),
 ("s35.jpg","settle","Within the Nazi party, this is welcome news. Now isolated by the West and drawn toward Berlin, Mussolini sends his son-in-law and foreign minister, Galeazzo Ciano, to meet with Hitler at Berchtesgaden in October 1936."),
 ("s38b","pan-left",""),  # remove
 ("s45.jpg","slow-push","Days later, in a speech in Milan, Mussolini publicly names the new arrangement between the two powers, an axis. May 1939. On a sudden impulse during a phone call, Mussolini proposes turning the loose Axis into a full military alliance. Hitler agrees on the spot. The Pact of Steel is signed."),
 ("s50.jpg","settle","March 11th, 1938. Hitler is about to annex Austria, terrified Mussolini will do again what he did in 1934. Mussolini says Austria is immaterial to him, and Hitler is overcome. Then please tell Mussolini I will never forget him for this. Never, never, never, no matter what happens, even if the whole world gangs up on him."),
 ("s51.jpg","pan-right","Mussolini sits out the first nine months of the war because he knows Italy isn't ready. Then, in June 1940, with France already beaten, he jumps in anyway. 32 Italian divisions attack six French ones on the Alpine front but cannot move them an inch. When the two dictators meet at Munich to set armistice terms, the German memo is blunt: this war has been won by Hitler."),
 ("s54.jpg","slow-push","The senior partner of 1934 is now the junior one. Emboldened, Mussolini invades Greece that October without warning Hitler. It collapses within a week. In North Africa, it's worse: a British desert force one-third the size of the Italian army routs it completely, taking 130,000 prisoners."),
 ("s56.jpg","settle","Hitler now has to divert German troops, the Afrika Korps,"),
 ("s57.jpg","pan-left","and eventually an invasion of the Balkans just to keep Italy standing, delaying his own invasion of the Soviet Union to do it. The alliance that was supposed to multiply Hitler's strength became a drain on it."),
 ("s61.jpg","slow-push","By the summer of 1943, with Sicily invaded and Rome bombed for the first time, even Mussolini's own inner circle has had enough. On the night of July 24th, his Fascist Grand Council votes 19 to 8 to strip him of military command and restore power to the king. That evening, the King summons him, dismisses him on the spot, and has him carted off under arrest in an ambulance. The news reaches Hitler's headquarters that night. His first instinct is rage, and he even openly discusses an invasion of Italy and the Vatican in order to restore Mussolini and the alliance."),
 ("s66.jpg","settle","For weeks, German intelligence hunts for Mussolini's location while his captors move him from island to island. In headquarters transcripts, he's referred to only as the valuable object, and most of Hitler's own generals, even Goebbels, privately doubt he's worth the trouble anymore, but Hitler disagrees."),
 ("s67.jpg","slow-push","He finally learns Mussolini is being held at a hotel on the Gran Sasso, the highest peak in the Apennines."),
 ("s65.jpg","pan-right","reachable only by funicular."),
 ("s69.jpg","settle","On September 12th, 1943, an Austrian SS officer named Otto Skorzeny"),
 ("s70.jpg","slow-push","leads a glider assault onto the mountaintop meadow."),
 ("s71.jpg","slow-push","Not a shot is fired,"),
 ("s72.jpg","pan-left","and within minutes he's airborne in a tiny two-seat plane, flown first to Rome, then to Vienna."),
 ("s73.jpg","settle","Hitler wants his old friend to immediately purge and punish the men who betrayed him, but Mussolini seems uninterested. Goebbels records Hitler's disappointment: he is not a revolutionary like the Fuehrer or Stalin."),
 ("s75.jpg","pan-right","At Hitler's insistence, Mussolini proclaims a new Italian Social Republic. For the next year and a half, the puppet government, the Salo Republic, governs a sliver of northern Italy at German gunpoint, at the behest of Hitler."),
 ("s78.jpg","settle","On April 27th, 1945, Mussolini and his mistress, Clara Petacci, are caught by Italian partisans near Lake Como, trying to slip into Switzerland. They are shot two days later. That night their bodies are trucked into Milan and the next day strung up by the heels, where a crowd spends the day reviling them. On May Day, he's buried in a pauper's plot."),
 ("s84.jpg","slow-push","The news reaches Hitler's bunker that same afternoon. Within hours he hands his own secretaries and his newly wedded wife Eva Braun capsules of cyanide."),
 ("s68.jpg","settle","He'd written, in his political testament, that he refused to become a spectacle for his enemies, not their live selves or their bodies. One can only speculate how much of Mussolini's degradation reached him. But the timing speaks for itself, and no one sees Hitler alive ever again."),
 ("s05b","slow-push",""),  # remove
]
# drop placeholders (empty text or missing files)
scenes=[s for s in scenes if s[2] and os.path.exists(os.path.join(MEDIA,s[0]))]

cut_idx={1,30}     # "is dead"; "Not a shot is fired"
slide_l={2,12,24}  # act opens
slide_r={6,17,27}
xcyc=[13,18,24,16,21]
def trans_for(i,src):
    if i==0: return ("crossfade",0)
    if i in cut_idx: return ("cut",0)
    if i in slide_l: return ("slide-left",22)
    if i in slide_r: return ("slide-right",22)
    return ("crossfade",xcyc[i%len(xcyc)])

tot=sum(len(t) for _,_,t in scenes)
out=[]; acc=0.0
for i,(src,motion,text) in enumerate(scenes):
    dur=max(AUDIO_LEN*len(text)/tot,3.0); acc+=dur
    w,h=Image.open(os.path.join(MEDIA,src)).size
    k,tin=trans_for(i,src)
    out.append({"n":i+1,"src":src,"motion":motion,"transition":k,"tin":tin,
                "durationSec":round(dur,3),"aspectRatio":round(w/h,4)})
sc=AUDIO_LEN/acc
for s in out: s["durationSec"]=round(s["durationSec"]*sc,3)
out.append({"n":len(out)+1,"type":"outro","durationSec":OUTRO,"transition":"crossfade","tin":20})

spec={"title":"The Imitator and the Duce — Hitler & Mussolini","slug":"hitler-mussolini",
      "mediaDir":"hitler-mussolini","narration":"ES_Voice_Benjamin-hitler-mussolini.mp3","scenes":out}
json.dump(spec,open("/home/user/dataexploration/THIRD-REICH-HANDOFF/reich-engine/src/active-episode.json","w"),indent=1,ensure_ascii=False)
print("scenes:",len(out),"sum:",round(sum(s['durationSec'] for s in out),1),"s")
