import re, json, os, shutil, html, sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from data import *
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"site")
shutil.rmtree(OUT,ignore_errors=True)
for d in ("tips","pros","img"): os.makedirs(f"{OUT}/{d}")
esc=html.escape
def slug(s): return re.sub(r"-+","-",re.sub(r"[^a-z0-9]+","-",s.lower())).strip("-")[:70]
tips=[dict(n=i+1,cat=c,q=q,causes=ca.split("|"),fix=f,slug=slug(q)) for i,(c,q,ca,f) in enumerate(TIPS)]
pros=[dict(slug=p[0],name=p[1],role=p[2],loc=p[3],tel=p[4],mail=p[5],hours=p[6],cats=p[7],color=p[8],bio=p[9]) for p in PROS]
NAV=lambda r:f'<header class="top"><a class="logo" href="{r}index.html">Affordaboat</a><nav><a href="{r}tips.html">Boat tips</a><a href="{r}pros.html">Professionals</a></nav></header>'
def page(title,desc,body,r="",extra=""):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@600;800&family=Source+Sans+3:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}style.css">{extra}</head><body>{NAV(r)}<main>{body}</main>
<footer><p>Affordaboat.com. Tips are general guidance, not a substitute for a qualified marine technician. Professionals shown are fictional placeholders.</p></footer>
<script src="{r}script.js"></script></body></html>'''
def tipcard(t,r):
    return f'<a class="card tip" href="{r}tips/{t["slug"]}.html" data-cat="{t["cat"]}"><span class="cat">{t["cat"]}</span><h3>{esc(t["q"])}</h3><p>{esc(t["causes"][0].split(" (")[0][:110])}</p></a>'
def procard(p,r):
    return f'<a class="card pro" href="{r}pros/{p["slug"]}.html"><img src="{r}img/{p["slug"]}.svg" alt="Photo of {p["name"]}" width="96" height="96"><h3>{p["name"]}</h3><p class="role">{p["role"]}</p><p>{p["loc"]}</p></a>'
def write(path,s): open(f"{OUT}/{path}","w",encoding="utf-8").write(s)

# avatars
for p in pros:
    ini="".join(w[0] for w in p["name"].split())
    write(f'img/{p["slug"]}.svg',f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200"><rect width="200" height="200" fill="{p["color"]}"/><circle cx="100" cy="78" r="38" fill="#fff" opacity=".9"/><path d="M28 200c4-52 38-76 72-76s68 24 72 76z" fill="#fff" opacity=".9"/></svg>')

# tip pages
for t in tips:
    same=[x for x in tips if x["cat"]==t["cat"] and x is not t]
    i=same.index(min(same,key=lambda x:abs(x["n"]-t["n"])))
    rel=same[max(0,min(i-1,len(same)-3)):][:3]
    mp=[p for p in pros if t["cat"] in p["cats"]][:3]
    faq={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":t["q"],"acceptedAnswer":{"@type":"Answer","text":"Likely causes: "+"; ".join(t["causes"])+". Fix: "+t["fix"]}}]}
    body=f'''<article class="wrap narrow"><p class="crumb"><a href="../tips.html">Boat tips</a> / {t["cat"]}</p><h1>{esc(t["q"])}</h1>
<h2>Most likely causes</h2><ul class="causes">{"".join(f"<li>{esc(c)}</li>" for c in t["causes"])}</ul>
<h2>The fix</h2><p>{esc(t["fix"])}</p>
<h2>When to call a mechanic</h2><p>Call a professional if {CALL[t["cat"]]}</p></article>
<section class="band"><div class="wrap"><h2>Professionals who can fix this</h2><div class="grid3">{"".join(procard(p,"../") for p in mp)}</div></div></section>
<section class="wrap"><h2>Related tips</h2><div class="grid3">{"".join(tipcard(x,"../") for x in rel)}</div></section>'''
    write(f'tips/{t["slug"]}.html',page(f'{t["q"]} | Affordaboat',t["fix"][:155],body,"../",f'<script type="application/ld+json">{json.dumps(faq)}</script>'))

# pro pages
for p in pros:
    tl=[t for t in tips if t["cat"] in p["cats"]][:6]
    body=f'''<section class="wrap narrow prof"><img src="../img/{p["slug"]}.svg" alt="Photo of {p["name"]}" width="220" height="220"><div><h1>{p["name"]}</h1><p class="role">{p["role"]} in {p["loc"]}</p><p>{esc(p["bio"])}</p>
<p>Handles: {", ".join(p["cats"])}.</p></div></section>
<section class="band"><div class="wrap narrow"><h2>Contact {p["name"].split()[0]}</h2><ul class="contact"><li>Phone: <a href="tel:{re.sub(r"[^0-9]","",p["tel"])}">{p["tel"]}</a></li><li>Email: <a href="mailto:{p["mail"]}">{p["mail"]}</a></li><li>Location: {p["loc"]}</li><li>Hours: {p["hours"]}</li></ul></div></section>
<section class="wrap"><h2>Problems {p["name"].split()[0]} can help with</h2><div class="grid3">{"".join(tipcard(t,"../") for t in tl[:3])}</div></section>'''
    write(f'pros/{p["slug"]}.html',page(f'{p["name"]}, {p["role"]} | Affordaboat',p["bio"][:155],body,"../"))

# home
feat=[tips[0],tips[13],tips[21]]
home=f'''<section class="hero"><div class="wrap"><h1>Don't call a mechanic yet.</h1><p>Plain answers to the boat problems people search most, plus a local professional when it's time to call one.</p>
<form action="tips.html" method="get" class="search"><input type="search" name="q" placeholder="Search: won't start, overheating, bottom paint" aria-label="Search boat tips"><button>Search</button></form></div></section>
<section class="wrap"><h2>Popular tips</h2><div class="grid3">{"".join(tipcard(t,"") for t in feat)}</div><p class="more"><a href="tips.html">See all {len(tips)} tips</a></p></section>
<section class="band"><div class="wrap"><h2>Professionals near you</h2><div class="grid3">{"".join(procard(p,"") for p in pros[:3])}</div><p class="more"><a href="pros.html">See all professionals</a></p></div></section>'''
write("index.html",page("Affordaboat | Boat engine, electrical and paint problems solved","Answers to common outboard and inboard problems, with local marine professionals.",home))

# all tips
cats=[E,L,M,C]
tp=f'''<section class="wrap"><h1>Boat tips</h1><div class="filters"><input id="q" type="search" placeholder="Search tips" aria-label="Search tips"><div id="chips"><button data-c="" class="on">All</button>{"".join(f'<button data-c="{c}">{c}</button>' for c in cats)}</div></div>
<div class="grid3" id="list">{"".join(tipcard(t,"") for t in tips)}</div><p id="none" hidden>No tips match. Try a shorter search.</p></section>'''
write("tips.html",page("All boat tips | Affordaboat","Searchable boat engine, electrical, paint and maintenance tips.",tp))
write("pros.html",page("Marine professionals | Affordaboat","Marine mechanics, electricians and hull specialists.",f'<section class="wrap"><h1>Professionals</h1><div class="grid3">{"".join(procard(p,"") for p in pros)}</div></section>'))
write(".nojekyll","")

write("style.css",'''
:root{--ink:#10293B;--paper:#F6F9F8;--sea:#DCEEE7;--sig:#F2B91F;--slate:#4F6677;--line:#C9D9D3;color-scheme:light}
*{box-sizing:border-box}html{scroll-padding-top:70px}
body{margin:0;background:var(--paper);color:var(--ink);font:18px/1.6 "Source Sans 3",system-ui,sans-serif}
h1,h2,h3,.logo{font-family:"Bricolage Grotesque",system-ui,sans-serif;line-height:1.15;margin:0 0 .5em}
h1{font-size:clamp(2rem,5vw,3.4rem);font-weight:800}h2{font-size:1.5rem;margin-top:1.6em}h3{font-size:1.15rem}
a{color:inherit}a:focus-visible,button:focus-visible,input:focus-visible{outline:3px solid var(--sig);outline-offset:2px}
.top{display:flex;justify-content:space-between;align-items:center;padding:14px 24px;background:var(--ink);color:#fff;position:sticky;top:0;z-index:5}
.top a{text-decoration:none}.logo{font-size:1.3rem;font-weight:800;margin:0;color:var(--sig)}.top nav a{margin-left:20px}.top nav a:hover{text-decoration:underline}
.wrap{max-width:1040px;margin:0 auto;padding:36px 24px}.narrow{max-width:740px}
.hero{background:var(--ink);color:#fff;border-bottom:8px solid var(--sig)}.hero .wrap{padding:72px 24px}.hero p{font-size:1.2rem;max-width:34em;color:#CFE0E8}
.search{display:flex;gap:8px;max-width:560px;margin-top:24px}.search input,.filters input{flex:1;padding:12px 14px;font:inherit;border:2px solid var(--line);border-radius:6px;width:100%}
button{font:inherit;cursor:pointer}.search button{padding:12px 20px;background:var(--sig);color:var(--ink);border:0;border-radius:6px;font-weight:600}
.band{background:var(--sea)}.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.card{display:block;background:#fff;border:1px solid var(--line);border-radius:8px;padding:20px;text-decoration:none}
.card:hover{border-color:var(--ink)}.card p{margin:.3em 0 0;color:var(--slate);font-size:.95rem}
.tip{border-top:5px solid var(--sig)}.cat{font-size:.85rem;color:var(--slate);font-weight:600}
.pro{text-align:center}.pro img,.prof img{border-radius:50%;display:block;margin:0 auto 12px}.pro .role{color:var(--ink);font-weight:600}
.prof{display:flex;gap:32px;align-items:center}.prof img{flex:none;margin:0}.role{color:var(--slate)}
.causes li{margin-bottom:.4em}.crumb{font-size:.95rem;color:var(--slate)}.more{margin-top:20px}
.contact{list-style:none;padding:0;font-size:1.1rem}.contact li{padding:8px 0;border-bottom:1px solid var(--line)}
.filters{margin:12px 0 24px}#chips{margin-top:12px;display:flex;flex-wrap:wrap;gap:8px}
#chips button{padding:6px 14px;border:2px solid var(--ink);background:#fff;border-radius:99px}#chips button.on{background:var(--ink);color:#fff}
footer{padding:28px 24px;text-align:center;color:var(--slate);font-size:.9rem}
@media(max-width:800px){.grid3{grid-template-columns:1fr}.prof{flex-direction:column;text-align:center}.top nav a{margin-left:12px}}
''')
write("script.js",'''
(function(){var q=document.getElementById("q");if(!q)return;
var cards=[].slice.call(document.querySelectorAll("#list .card")),chips=document.querySelectorAll("#chips button"),none=document.getElementById("none"),cat="";
function run(){var t=q.value.toLowerCase().trim(),n=0;cards.forEach(function(c){var ok=(!cat||c.dataset.cat===cat)&&(!t||c.textContent.toLowerCase().indexOf(t)>-1);c.hidden=!ok;if(ok)n++});none.hidden=n>0}
q.addEventListener("input",run);
chips.forEach(function(b){b.addEventListener("click",function(){cat=b.dataset.c;chips.forEach(function(x){x.classList.toggle("on",x===b)});run()})});
var p=new URLSearchParams(location.search).get("q");if(p){q.value=p;run()}})();
''')
write("README.md","# Affordaboat\n\nStatic site for GitHub Pages. Edit `data.py` and run `python3 generate.py` to rebuild, or edit the HTML directly.\n\nProfessionals are fictional placeholders. To use a real photo, replace `img/<name>.svg` or change the `src` in `pros/<name>.html`.\n")
print(len(tips),"tips",len(pros),"pros")
