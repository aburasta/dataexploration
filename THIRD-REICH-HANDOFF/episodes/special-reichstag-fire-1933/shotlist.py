# Shot list for special-reichstag-fire-1933 — silent visual cut.
# Each beat: (id, text_span, primary_query, [alt_queries], motion, transition)
# duration = words / WPS (documentary pace). Media sourced from Wikimedia Commons.
WPS = 2.42  # ~145 wpm

BEATS = [
 # ---- P1 cold open: Göring's 1942 boast ----
 ("01","Picture the Nuremberg rallies. Hundreds of thousands of raised arms, one word thundering across the stadium.","Reichsparteitag Nürnberg 1933 Menge",["Nuremberg rally 1934 crowd","Reichsparteitag 1935"],"slow-push","cut"),
 ("02","And Hermann Goering, Reich Marshal, second most powerful man in Germany, cuts in.","Hermann Göring 1932 portrait",["Hermann Goering 1933","Hermann Göring Reichstag"],"slow-pull","xfade"),
 ("03","General Franz Halder was sitting close enough to hear it. Goering said it out loud: the only one who really knows about the Reichstag is I, because I set it on fire.","Franz Halder general",["Franz Halder 1938","Halder Wehrmacht"],"slow-push","xfade"),
 ("04","Nine years earlier, that fire had handed Adolf Hitler the legal machinery for a dictatorship that was never once repealed.","Reichstagsbrand 1933",["Reichstag fire 1933","Reichstagsgebäude Brand 1933"],"slow-push","dip-to-black"),

 # ---- P2 late Feb 1933, Chancellor 4 weeks ----
 ("05","By late February 1933, Hitler had been Chancellor for exactly four weeks, and he still did not have what he needed.","Adolf Hitler Reichskanzler 1933",["Hitler chancellor January 1933","Hitler 1933 portrait"],"slow-push","cut"),
 ("06","He led a coalition cabinet with only three Nazi ministers out of eleven.","Hitler Kabinett 1933",["Reich cabinet 1933","Hitler cabinet Papen"],"pan-right","xfade"),
 ("07","An election was set for March 5th, and Hitler needed a real majority, not a borrowed one.","NSDAP Wahlplakat 1933",["Reichstagswahl März 1933 Plakat","Nazi election poster 1933"],"slow-push","xfade"),
 ("08","His own party's raid on Communist headquarters weeks earlier had turned up nothing but old pamphlets in a cellar.","Karl-Liebknecht-Haus Berlin",["KPD headquarters Berlin 1933","Karl Liebknecht Haus"],"slow-pull","dip-to-black"),

 # ---- P3 Göring, the tunnel ----
 ("09","Here is a detail most retellings skip: Hermann Goering was President of the Reichstag.","Hermann Göring 1933",["Göring Reichstagspräsident","Hermann Goering uniform 1933"],"slow-push","cut"),
 ("10","His official residence was connected to the Reichstag building itself by an underground passage, built to carry the central heating.","Reichstagspräsidentenpalais",["Reichstag president palace Berlin","Reichstagsgebäude 1930"],"pan-left","xfade"),
 ("11","Shirer is blunt: it was where a plan was connived to burn the Reichstag down. The tunnel was the delivery route.","Reichstag Berlin 1932",["Reichstag building 1930s","Reichstagsgebäude Berlin historisch"],"slow-push","dip-to-black"),

 # ---- P4 Feb 27 evening, two dinners ----
 ("12","On the evening of February 27th, two dinners were underway a few streets apart in Berlin.","Berlin 1933 street night",["Berlin Wilhelmstrasse 1933","Berlin 1930s street"],"pan-right","cut"),
 ("13","At the exclusive Herrenklub, Vice-Chancellor Franz von Papen was entertaining President Paul von Hindenburg.","Franz von Papen",["Franz von Papen 1933","Papen Vizekanzler"],"slow-push","xfade"),
 ("14","Across town at Joseph Goebbels' home, Hitler had come to dine with friends, relaxed. Then the phone rang.","Joseph Goebbels 1933",["Joseph Goebbels portrait","Goebbels 1932"],"slow-pull","dip-to-black"),

 # ---- P5 Goebbels diary, Hanfstaengl call ----
 ("15","Goebbels wrote it down himself, that same night, in his diary.","Joseph Goebbels desk writing",["Goebbels schreibtisch","Goebbels diary"],"slow-push","cut"),
 ("16","A call came in from Ernst Hanfstaengl: the Reichstag is on fire. Goebbels declined even to mention it to the Fuehrer.","Ernst Hanfstaengl",["Putzi Hanfstaengl","Ernst Hanfstaengl 1933"],"slow-push","xfade"),
 ("17","A few minutes later he believed it. Then he and Hitler were in a car racing at sixty miles an hour toward the scene of the crime.","Mercedes 1930s car Berlin",["1930s German car night","Berlin automobile 1933"],"pan-left","dip-to-black"),

 # ---- P6 Papen & Hindenburg see the glow ----
 ("18","Papen was closer. From the Herrenklub, he and Hindenburg saw it directly: a red glow through the windows.","Reichstagsbrand Feuer 1933",["Reichstag fire flames","Reichstag burning 1933"],"slow-push","cut"),
 ("19","The dome of the Reichstag looking as though it were illuminated by searchlights, a burst of flame and a swirl of smoke.","Reichstag fire dome smoke",["Reichstagsbrand Kuppel","Reichstag fire 1933 exterior"],"slow-push","xfade"),
 ("20","Papen bundled the elderly President into his car and drove straight for the fire.","Paul von Hindenburg 1933",["Hindenburg Reichspräsident","Paul von Hindenburg car"],"slow-pull","dip-to-black"),

 # ---- P7 Göring at scene, orders ----
 ("21","Goering was already there when Hitler and Goebbels arrived, quite beside himself with excitement.","Hermann Göring speaking 1933",["Goering rede","Hermann Goering gesture"],"slow-push","cut"),
 ("22","This is the beginning of the Communist revolution, he declared. Every Communist official must be shot where he is found.","Rudolf Diels Gestapo",["Rudolf Diels","Diels Gestapo chief"],"slow-push","xfade"),
 ("23","That order came before a single fact about the fire had been established.","Reichstag fire interior ruins",["Reichstag burned interior 1933","Reichstagsbrand Innenraum"],"slow-pull","dip-to-black"),

 # ---- P8 van der Lubbe ----
 ("24","Inside the burning building, police found one man: Marinus van der Lubbe, a young Dutch council-communist.","Marinus van der Lubbe",["Marinus van der Lubbe 1933","van der Lubbe mugshot"],"slow-push","cut"),
 ("25","A half-witted, feeble-minded pyromaniac, in Shirer's phrase, though he had a real communist background and had tried arson before.","Marinus van der Lubbe portrait",["van der Lubbe trial","Marinus van der Lubbe Leipzig"],"slow-push","xfade"),
 ("26","Days earlier the SA had picked him up after he boasted he meant to try the Reichstag next. To the Nazis he was a godsend.","Sturmabteilung SA 1933",["SA Sturmabteilung 1933 Berlin","SA men 1933"],"pan-right","dip-to-black"),

 # ---- P9 physical evidence / trial ----
 ("27","But the physical evidence, established later at trial in Leipzig, did not fit a lone arsonist.","Reichstagsbrandprozess Leipzig",["Reichstag fire trial Leipzig 1933","Reichsgericht Leipzig"],"slow-push","cut"),
 ("28","Two and a half minutes after he entered, the great central hall was already fiercely burning, with nothing but his own shirt for tinder.","Reichstag plenarsaal Brand",["Reichstag plenary hall burned","Reichstag Sitzungssaal 1933"],"slow-push","xfade"),
 ("29","Trial experts testified the main fires had been set with substantial chemicals and gasoline, more than one man could carry.","Reichstag fire damage 1933",["Reichstagsbrand Schaden","Reichstag ruins interior"],"slow-pull","dip-to-black"),

 # ---- P10 Karl Ernst & the tunnel ----
 ("30","That was Karl Ernst's job, a former hotel bellhop turned Berlin SA leader.","Karl Ernst SA Führer",["Karl Ernst SA 1933","Karl Ernst Sturmabteilung"],"slow-push","cut"),
 ("31","Through Goering's underground tunnel, Ernst led a detachment of storm troopers who scattered gasoline and self-igniting chemicals.","SA Sturmtrupp 1933",["storm troopers 1933","SA marching Berlin 1933"],"pan-left","xfade"),
 ("32","Van der Lubbe, wandering the same darkened building with his own small fires, had no idea he was not alone.","Reichstag building night 1933",["Reichstag exterior night","Reichstagsgebäude 1933"],"slow-pull","dip-to-black"),

 # ---- P11 Nuremberg testimony, Shirer verdict ----
 ("33","This is not speculation. It came out under oath, years later, at Nuremberg.","Nuremberg trials courtroom 1946",["Nürnberger Prozesse","Nuremberg trial defendants"],"slow-push","cut"),
 ("34","Hans Gisevius testified plainly: it was Goebbels who first thought of setting the Reichstag on fire.","Hans Bernd Gisevius",["Hans Gisevius Nuremberg","Gisevius witness"],"slow-push","xfade"),
 ("35","Rudolf Diels swore that Goering knew exactly how the fire was to be started.","Rudolf Diels portrait",["Rudolf Diels 1933","Diels affidavit"],"slow-pull","xfade"),
 ("36","And Goering's own birthday boast was recalled at Nuremberg by General Franz Halder, who heard it firsthand.","Franz Halder Nuremberg",["Franz Halder witness","Halder general portrait"],"slow-push","xfade"),
 ("37","Shirer's verdict: there is enough evidence to establish beyond a reasonable doubt that it was the Nazis who planned the arson.","William Shirer author",["William L Shirer","Rise and Fall of the Third Reich book"],"slow-push","dip-to-black"),

 # ---- P12 the decree ----
 ("38","The morning after, February 28th, Hitler brought President Hindenburg a decree for the Protection of the People and the State.","Reichstagsbrandverordnung 1933",["Reichstag Fire Decree document","Verordnung 28 Februar 1933"],"slow-push","cut"),
 ("39","It suspended seven sections of the constitution outright: freedom of expression, the press, assembly, privacy of mail, protection from searches.","Weimar Verfassung document",["Weimar constitution 1919","Reichsgesetzblatt 1933"],"pan-right","xfade"),
 ("40","This decree was never repealed. It remained the legal foundation of the Third Reich for the entirety of its twelve years.","Paul von Hindenburg signature",["Hindenburg signing decree","Hindenburg 1933 portrait"],"slow-pull","dip-to-black"),

 # ---- P13 arrests ----
 ("41","The arrests began within hours. Roughly four thousand Communist officials were rounded up, including sitting Reichstag deputies.","SA arrests 1933 Berlin",["Verhaftung 1933","SA Razzia 1933"],"slow-push","cut"),
 ("42","Storm troopers in trucks broke into homes, dragging people to SA barracks to be beaten and tortured.","SA Lastwagen 1933",["SA truck Berlin 1933","Sturmabteilung truck"],"pan-left","xfade"),
 ("43","Communist and Social Democrat papers were shut down. Only the Nazis and their Nationalist allies were left free to campaign.","Die Rote Fahne Zeitung",["KPD newspaper 1933","Nazi newspaper Völkischer Beobachter"],"slow-pull","dip-to-black"),

 # ---- P14 Prussian statement, Göring Frankfurt ----
 ("44","The Prussian government backed the story with an official statement claiming proof of a Communist plot.","Nazi propaganda newspaper 1933",["Völkischer Beobachter 1933","German newspaper 1933 headline"],"slow-push","cut"),
 ("45","On March 3rd, in Frankfurt, Goering told a crowd: my mission is only to destroy and exterminate, nothing more.","Hermann Göring Rede Menge",["Goering speech crowd","Hermann Goering speaking rally"],"slow-push","dip-to-black"),

 # ---- P15 March 5 election ----
 ("46","Even after all of it, Germans still did not hand Hitler a majority. On March 5th, the Nazis took 44 percent of the vote.","Reichstagswahl 5 März 1933",["German election March 1933","Wahllokal 1933"],"slow-push","cut"),
 ("47","Hitler needed his Nationalist partners' seats just to scrape a majority, nowhere near the two-thirds for the Enabling Act.","Reichstag Kroll Oper 1933",["Enabling Act 1933","Reichstag session 1933 Kroll"],"pan-right","dip-to-black"),

 # ---- P16 four communists to trial, Dimitrov ----
 ("48","Four Communists were headed to trial: Ernst Torgler, the party's parliamentary leader, who turned himself in.","Ernst Torgler",["Ernst Torgler KPD","Torgler Reichstag"],"slow-push","cut"),
 ("49","And three Bulgarian Communists: Georgi Dimitroff, Blagoi Popov, and Vasil Tanev.","Georgi Dimitrov 1933",["Georgi Dimitrov Leipzig trial","Dimitrov 1933"],"slow-push","xfade"),
 ("50","Dimitroff, acting as his own lawyer, turned the Leipzig trial into a public humiliation for Goering.","Reichstagsbrandprozess Gericht",["Leipzig trial courtroom 1933","Reichstag fire trial court"],"pan-left","xfade"),
 ("51","Goering snapped: out with you, you scoundrel. Dimitroff got the last word: are you afraid of my questions?","Hermann Göring Zeuge Gericht",["Goering witness stand 1933","Hermann Goering trial"],"slow-pull","dip-to-black"),

 # ---- P17 verdict ----
 ("52","The verdict, in December 1933, was its own kind of scandal: Torgler and all three Bulgarians were acquitted outright.","Reichstag fire trial verdict",["Leipzig Reichsgericht 1933","Reichstagsbrandprozess Urteil"],"slow-push","cut"),
 ("53","Only van der Lubbe, who had confessed, was convicted and executed by guillotine.","Marinus van der Lubbe court",["van der Lubbe trial 1933","Marinus van der Lubbe verurteilt"],"slow-pull","dip-to-black"),

 # ---- P18 People's Court ----
 ("54","That acquittal enraged Hitler and Goering. Within a month the right to try treason was stripped from the Supreme Court.","Reichsgericht Leipzig Gebäude",["Reichsgericht building Leipzig","German Supreme Court Leipzig"],"slow-push","cut"),
 ("55","It was handed to a brand-new tribunal, the Volksgerichtshof, the People's Court. There was no appeal. It became the most feared court in the Reich.","Volksgerichtshof",["Volksgerichtshof Berlin","People's Court Nazi Freisler"],"slow-push","dip-to-black"),

 # ---- P19 Karl Ernst killed ----
 ("56","Karl Ernst did not get to enjoy the outcome. In the Night of the Long Knives, June 1934, Ernst was murdered.","Röhm Putsch 1934",["Night of the Long Knives","Ernst Röhm SA purge"],"slow-push","cut"),
 ("57","Killed along with three other SA men believed to have been his accomplices in setting the Reichstag on fire. They knew too much.","Sturmabteilung SA parade",["SA Sturmabteilung parade 1933","storm troopers formation"],"slow-pull","dip-to-black"),

 # ---- P20 1939 beer hall, Shirer diary, close ----
 ("58","Six years later, in November 1939, a bomb went off in a Munich beer hall minutes after Hitler left.","Bürgerbräukeller 1939 Attentat",["Bürgerbräukeller bombing 1939","Munich beer hall 1939 explosion"],"slow-push","cut"),
 ("59","Shirer, in Berlin at the time, wrote in his diary: most of us think it smells of another Reichstag fire.","William Shirer Berlin Diary",["William Shirer journalist","Berlin Diary Shirer"],"slow-push","xfade"),
 ("60","The decree Hindenburg signed the morning after never was repealed. One fire. One signature. Twelve years.","Reichstagsbrand ruins 1933",["Reichstag fire aftermath","Reichstagsgebäude ausgebrannt 1933"],"slow-push","dip-to-black"),
]

REAL_WORDS = 2046  # full script narration word count
if __name__ == "__main__":
    import json
    rows=[]
    raw_total=0
    for b in BEATS:
        bid,text,q,alts,motion,trans=b
        w=len(text.split())
        raw=w/WPS
        raw_total+=raw
        rows.append(dict(id=bid,text=text,query=q,alts=alts,motion=motion,transition=trans,words=w,_raw=raw))
    target = REAL_WORDS/WPS            # true narration seconds
    scale = target/raw_total          # stretch paraphrase timing up to real narration
    total=0
    for r in rows:
        r["durationSec"]=round(max(3.4, r.pop("_raw")*scale),2)
        total+=r["durationSec"]
    json.dump(rows, open("THIRD-REICH-HANDOFF/episodes/special-reichstag-fire-1933/plan.json","w"), indent=1, ensure_ascii=False)
    print(f"beats={len(rows)} scale={scale:.2f} total_video_sec={round(total,1)} (~{round(total/60,1)} min, excl. end card)")
