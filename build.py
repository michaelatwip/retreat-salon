#!/usr/bin/env python3
"""Builds the static site into _site/ from content/*.json. Standard library only.

    python3 build.py            # build
    python3 build.py --serve    # build, then serve on http://localhost:8000
"""
import html, json, os, shutil, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, '_site')


def load(name):
    with open(os.path.join(ROOT, 'content', name + '.json'), encoding='utf-8') as f:
        return json.load(f)


SITE = load('site')
TEAM = [s for s in load('team')['stylists'] if s.get('show', True)]
SERVICES = load('services')['services']
GALLERY = load('gallery')['photos']

e = html.escape


def paras(text):
    return ''.join(f'<p>{e(p.strip())}</p>' for p in (text or '').split('\n\n') if p.strip())


def book_url(stylist=None):
    return (stylist or {}).get('bookingUrl') or SITE['bookingUrl']


def first(name):
    return name.split()[0]


DIRECTIONS = 'https://www.google.com/maps/search/?api=1&query=' + '+'.join(
    (SITE['address1'] + ' ' + SITE['address2']).replace(',', '').split())
MAP_EMBED = 'https://maps.google.com/maps?q=' + '%20'.join(
    (SITE['address1'] + ' ' + SITE['address2']).split()) + '&z=15&output=embed'

CSS = r"""
:root{--bg:#F6F1E9;--ink:#3A3A30;--accent:#7F8C6E;--onaccent:#fff;--card:#FFFDF8;--line:#DDD3C2;--oak:#C9A97E;
--serif:'Cormorant Garamond',serif;--sans:Jost,sans-serif;--radius:22px}
*{box-sizing:border-box;margin:0;padding:0}html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--ink);font-family:var(--sans);font-weight:300;line-height:1.6;-webkit-font-smoothing:antialiased}
a{color:inherit}button{font:inherit;color:inherit;background:none;border:0;cursor:pointer}img{max-width:100%;display:block}
.cover{width:100%;height:100%;object-fit:cover}
.ann{background:var(--ink);color:#EDE6D8;text-align:center;font-size:12px;letter-spacing:.16em;text-transform:uppercase;padding:10px}
.ann a{text-decoration:underline;text-underline-offset:3px}
nav{position:sticky;top:0;z-index:20;background:rgba(246,241,233,.92);backdrop-filter:blur(10px);display:grid;grid-template-columns:1fr auto 1fr;align-items:center;padding:16px 5vw;font-size:12px;letter-spacing:.16em;text-transform:uppercase;border-bottom:1px solid rgba(0,0,0,.05)}
nav .links{display:flex;gap:30px}nav .links a{text-decoration:none}nav .links a.cur{border-bottom:1px solid var(--accent)}
nav .logo{width:200px;filter:brightness(.28) sepia(.3)}
nav .right{justify-self:end;display:flex;gap:22px;align-items:center}nav .right a.loc{text-decoration:none}
nav .bbtn{padding:12px 24px}
.menu-btn{display:none;font-size:22px}
.mnav{display:none;position:fixed;inset:0;z-index:40;background:var(--bg);flex-direction:column;justify-content:center;align-items:center;gap:22px;font-family:var(--serif);font-size:36px}
.mnav a{text-decoration:none}.mnav .x{position:absolute;top:14px;right:22px;font-size:38px;font-family:var(--sans)}
body.menu-open .mnav{display:flex}
.bbtn{display:inline-block;background:var(--accent);color:var(--onaccent);padding:15px 32px;border-radius:40px;font-size:12px;letter-spacing:.18em;text-transform:uppercase;font-weight:500;text-decoration:none;transition:.2s;font-family:var(--sans)}
.bbtn:hover{filter:brightness(1.08)}.bbtn.light{background:#F6F1E9;color:var(--ink)}
.ghost{display:inline-block;padding:15px 30px;border:1px solid currentColor;border-radius:40px;font-size:12px;letter-spacing:.18em;text-transform:uppercase;text-decoration:none}
.eyebrow{font-size:12px;letter-spacing:.24em;text-transform:uppercase;margin-bottom:18px;display:block}
.eyebrow.a{color:var(--accent)}
.h2{font-family:var(--serif);font-weight:300;font-size:clamp(40px,4.6vw,68px);line-height:1.05}
.h2 em,.h1 em{font-style:italic;color:var(--accent)}
section{padding:130px 6vw}
.hero{position:relative;height:calc(100vh - 110px);min-height:600px;margin:0 2vw;border-radius:0 0 28px 28px;overflow:hidden}
.hero>img{position:absolute;inset:0}
.hero:after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(40,36,28,.62) 0%,rgba(40,36,28,.25) 45%,transparent 70%)}
.hero .copy{position:absolute;z-index:2;left:6vw;bottom:14vh;color:#FBF7EF;max-width:560px}
.hero h1{font-family:var(--serif);font-weight:300;font-size:clamp(54px,7.5vw,108px);line-height:.95;margin-bottom:22px}
.hero h1 em{font-style:italic}
.hero p{font-size:18px;max-width:440px;margin-bottom:32px;opacity:.92}
.hero .ghost{margin-left:10px;border-color:rgba(255,255,255,.7)}
.hcard{position:absolute;z-index:2;right:4vw;bottom:6vh;background:rgba(255,253,248,.94);border-radius:18px;padding:20px 24px;display:flex;gap:18px;align-items:center;max-width:380px;text-decoration:none}
.hcard .dot{width:9px;height:9px;flex:none;border-radius:50%;background:var(--accent);box-shadow:0 0 0 5px rgba(127,140,110,.2)}
.hcard small{display:block;font-size:11px;letter-spacing:.14em;text-transform:uppercase;opacity:.6}.hcard b{font-weight:500}
.hcard span.go{font-size:12px;letter-spacing:.14em;text-transform:uppercase;white-space:nowrap}
.pagehead{padding:110px 6vw 60px;text-align:center;max-width:860px;margin:0 auto}
.pagehead .h2{font-size:clamp(46px,6vw,84px)}.pagehead p{margin-top:20px;font-size:18px;opacity:.8}
.intro{display:grid;grid-template-columns:1.1fr 1fr;gap:8vw;align-items:end}
.intro p.lead{font-size:18px;margin-bottom:34px}
.stats{display:grid;grid-template-columns:repeat(3,1fr);border-top:1px solid var(--line);padding-top:24px;gap:20px}
.stats b{font-family:var(--serif);font-size:40px;font-weight:400;display:block;line-height:1}.stats span{font-size:13px;opacity:.7}
.services{display:grid;grid-template-columns:.9fr 1.3fr;gap:6vw;background:var(--card);border-radius:28px;margin:0 2vw;padding:120px 5vw}
.services .stick{position:sticky;top:110px;align-self:start}
.services .stick img{height:440px;border-radius:200px 200px 18px 18px;margin-top:36px}
.services .stick p{margin-top:20px;max-width:380px;font-size:15px;opacity:.75}
.svc{display:grid;grid-template-columns:60px 1fr 160px;gap:20px;padding:30px 0;border-bottom:1px solid var(--line)}
.svc .num{font-family:var(--serif);font-size:22px;color:var(--oak)}
.svc h3{font-family:var(--serif);font-weight:400;font-size:32px;line-height:1.1;margin-bottom:6px}
.svc .inc{font-size:13.5px;opacity:.6;margin-top:6px}
.svc-r{text-align:right;font-size:13px;letter-spacing:.08em}.svc-r span{display:block;margin-bottom:10px;opacity:.7}
.tl{font-size:12px;letter-spacing:.18em;text-transform:uppercase;text-underline-offset:5px;color:var(--accent)}
.more{margin-top:34px}
.space-head{display:flex;justify-content:space-between;align-items:end;margin-bottom:46px;gap:40px}.space-head p{max-width:420px;opacity:.8}
.gal{display:grid;grid-template-columns:1.4fr 1fr 1fr;grid-template-rows:300px 300px;gap:14px}
.gal figure{border-radius:18px;position:relative;overflow:hidden}.gal figure:first-child{grid-row:span 2}
.gal figcaption{position:absolute;left:16px;bottom:14px;color:#fff;font-size:12px;letter-spacing:.16em;text-transform:uppercase;text-shadow:0 1px 8px rgba(0,0,0,.4)}
.gal.full{grid-template-rows:none;grid-auto-rows:320px}.gal.full figure:first-child{grid-row:span 2}
.team-head{text-align:center;max-width:640px;margin:0 auto 60px}.team-head p{margin-top:16px;opacity:.8}
.team{display:grid;grid-template-columns:repeat(5,1fr);gap:34px 22px}
.tm{text-align:left;text-decoration:none;display:block}
.tm-img{aspect-ratio:3/4;border-radius:14px;position:relative;overflow:hidden;filter:grayscale(1) contrast(1.02);transition:.4s}
.tm-img span{position:absolute;inset:auto 12px 12px 12px;background:rgba(255,253,248,.92);border-radius:30px;padding:9px;text-align:center;font-size:11px;letter-spacing:.16em;text-transform:uppercase;opacity:0;transform:translateY(8px);transition:.3s}
.tm-img img{object-position:center 20%}
.tm:hover .tm-img{filter:grayscale(.2) sepia(.15)}.tm:hover .tm-img span{opacity:1;transform:none}
.tm-n{font-family:var(--serif);font-size:23px;margin-top:14px;line-height:1.1}.tm-r{font-size:13px;opacity:.65}
.booking{background:var(--accent);color:#F6F1E9;border-radius:28px;margin:0 2vw;display:grid;grid-template-columns:1fr 1fr;gap:5vw;align-items:center;padding:110px 5vw}
.booking .h2 em{color:#EDE3CF}.booking p{margin:22px 0 30px;opacity:.92;max-width:440px}
.booking img{height:420px;border-radius:200px 200px 18px 18px}
.booking .row{display:flex;gap:14px;flex-wrap:wrap;align-items:center}
.booking .ghost{color:#F6F1E9}
.ritual{display:grid;grid-template-columns:1fr 1fr;gap:6vw;align-items:center}
.ritual img{height:620px;border-radius:300px 300px 22px 22px}
.step{display:grid;grid-template-columns:70px 1fr;padding:28px 0;border-bottom:1px solid var(--line)}
.step b{font-family:var(--serif);font-weight:300;font-size:40px;color:var(--oak);line-height:1}
.step h3{font-family:var(--serif);font-weight:400;font-size:28px}.step p{opacity:.75}
.visit{display:grid;grid-template-columns:1fr 1fr;gap:5vw}
.visit iframe{width:100%;height:100%;min-height:460px;border:0;border-radius:22px;filter:grayscale(.6) sepia(.25) contrast(.95)}
.mapcard{display:flex;align-items:flex-end;min-height:460px;border-radius:22px;text-decoration:none;position:relative;overflow:hidden}
.mapcard img{position:absolute;inset:0}
.mapcard span.lbl{position:relative;z-index:1;margin:20px;background:var(--bg);padding:18px 22px;border-radius:12px;font-size:14px;line-height:1.5}
.info{display:grid;grid-template-columns:1fr 1fr;gap:26px;margin:30px 0}.info h4{font-size:11px;letter-spacing:.2em;text-transform:uppercase;opacity:.6;font-weight:400;margin-bottom:6px}
.faqwrap{margin-top:50px}
.faq-i{border-bottom:1px solid var(--line)}
.faq-q{width:100%;display:flex;justify-content:space-between;gap:20px;padding:20px 0;font-size:17px;text-align:left}
.faq-q span{font-size:22px;transition:.3s}.faq-a{max-height:0;overflow:hidden;transition:.35s;opacity:.8}
.faq-i.open .faq-a{max-height:300px;padding-bottom:20px}.faq-i.open .faq-q span{transform:rotate(45deg)}
.ig-h{text-align:center;padding:90px 0 30px}.ig-h a{font-family:var(--serif);font-size:30px;text-decoration:none}
.ig{display:grid;grid-template-columns:repeat(6,1fr);gap:6px;padding:0 2vw}.ig a{aspect-ratio:1;border-radius:6px;overflow:hidden}
.ig img{transition:.4s}.ig a:hover img{transform:scale(1.04)}
.profile{display:grid;grid-template-columns:.9fr 1.1fr;gap:6vw;padding:70px 6vw 110px;align-items:start}
.profile .pimg{border-radius:240px 240px 22px 22px;overflow:hidden;aspect-ratio:3/4.4;position:sticky;top:100px}
.profile .pimg img{object-position:center 20%}
.profile .h2{font-size:clamp(46px,5.4vw,80px);margin-bottom:6px}
.profile .spec{font-size:15px;letter-spacing:.06em;opacity:.7;margin-bottom:34px}
.profile .bio p{margin-bottom:18px;font-size:17px;max-width:560px}
.profile .acts{display:flex;gap:14px;flex-wrap:wrap;align-items:center;margin:34px 0 0}
.crumb{font-size:12px;letter-spacing:.16em;text-transform:uppercase;text-decoration:none;opacity:.65;display:inline-block;margin-bottom:30px}
.bookpage{display:grid;grid-template-columns:1fr 1fr;gap:5vw;padding:40px 6vw 110px;align-items:start}
.bookcard{background:var(--card);border-radius:28px;padding:50px;box-shadow:0 30px 80px -40px rgba(0,0,0,.25)}
.bookcard h3{font-family:var(--serif);font-weight:400;font-size:34px;line-height:1.1;margin-bottom:14px}
.bookcard ol{margin:24px 0 30px 20px}.bookcard li{margin-bottom:8px}
.widget{margin-top:10px}
.bylist{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.by{display:flex;gap:14px;align-items:center;border:1px solid var(--line);border-radius:16px;padding:12px;text-decoration:none;transition:.2s;background:var(--card)}
.by:hover{border-color:var(--accent)}.by img{width:52px;height:52px;border-radius:50%;object-fit:cover;object-position:center 20%;filter:grayscale(1)}
.by b{font-weight:500;display:block;font-size:15px}.by small{font-size:12.5px;opacity:.65}
footer{background:var(--ink);color:#E6DECF;margin-top:6px;padding:80px 6vw 40px;display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:40px;font-size:14px}
footer .logo{width:240px;margin-bottom:20px}footer h4{font-size:11px;letter-spacing:.2em;text-transform:uppercase;opacity:.6;font-weight:400;margin-bottom:12px}
footer a{display:block;text-decoration:none;margin-bottom:6px;opacity:.85}.fine{grid-column:1/-1;border-top:1px solid rgba(255,255,255,.12);padding-top:22px;font-size:12px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px}.fine span.c{opacity:.5}footer .fine a.wip{display:inline;margin:0;opacity:.5;letter-spacing:.2em;text-transform:uppercase;font-size:11px}footer .fine a.wip:hover{opacity:1}
.mbook{display:none}
@media(max-width:1100px){.team{grid-template-columns:repeat(4,1fr)}}
@media(max-width:820px){
 nav{grid-template-columns:auto 1fr auto;padding:14px 5vw}nav .links{display:none}nav .logo{width:150px}nav .right a.loc{display:none}nav .bbtn{padding:10px 16px}
 .menu-btn{display:block;margin-right:10px}nav .right{gap:8px}
 .hero{height:86vh;min-height:560px;margin:0;border-radius:0}.hero:after{background:linear-gradient(0deg,rgba(40,36,28,.75) 0%,rgba(40,36,28,.2) 60%,transparent)}
 .hero .copy{left:6vw;right:6vw;bottom:150px}.hero .ghost{margin:12px 0 0}.hcard{left:5vw;right:5vw;bottom:24px;max-width:none}
 section{padding:80px 6vw}.pagehead{padding:70px 6vw 30px}
 .intro,.services,.booking,.ritual,.visit,.profile,.bookpage{grid-template-columns:1fr}.services{margin:0;border-radius:0;padding:80px 6vw}
 .services .stick{position:static}.services .stick img{height:300px}.svc{grid-template-columns:40px 1fr}.svc-r{grid-column:2;text-align:left;display:flex;gap:18px}
 .space-head{display:block}.space-head p{margin-top:14px}
 .gal,.gal.full{grid-template-columns:1fr 1fr;grid-template-rows:none;grid-auto-rows:200px}.gal figure:first-child,.gal.full figure:first-child{grid-column:span 2;grid-row:auto}
 .team{grid-template-columns:1fr 1fr;gap:26px 14px}.booking{margin:0;border-radius:0;padding:80px 6vw}.booking img{height:300px}
 .ritual img{height:380px}.info{grid-template-columns:1fr}.ig{grid-template-columns:repeat(3,1fr)}footer{grid-template-columns:1fr 1fr}
 .profile{padding:30px 6vw 80px}.profile .pimg{position:static}
 .bookpage{padding:20px 5vw 80px}.bookcard{padding:30px 22px}.bylist{grid-template-columns:1fr}
 .mbook{display:block;position:fixed;left:5vw;right:5vw;bottom:16px;z-index:30;text-align:center;box-shadow:0 10px 30px -10px rgba(0,0,0,.4)}
 body{padding-bottom:70px}
}
"""

JS = r"""<script>
document.querySelectorAll('.faq-q').forEach(q=>q.onclick=()=>q.parentElement.classList.toggle('open'));
document.querySelectorAll('[data-menu]').forEach(b=>b.onclick=()=>document.body.classList.toggle('menu-open'));
</script>"""

NAV = [('services/', 'Services'), ('stylists/', 'Stylists'), ('space/', 'The Space'), ('visit/', 'Visit')]


def page(path, title, body, desc=None, cur=None, sticky=True):
    """Writes one page. path is like '' (home) or 'stylists/maddy/'; links are made relative."""
    up = '../' * path.count('/')
    def u(p):
        return up + p if not p.startswith('http') else p
    links = ''.join(f'<a href="{u(p)}"{" class=cur" if cur == p else ""}>{n}</a>' for p, n in NAV)
    mlinks = ''.join(f'<a href="{u(p)}">{n}</a>' for p, n in NAV)
    desc = desc or SITE['intro']
    full_title = f'{title} · {SITE["name"]}' if title else f'{SITE["name"]} · Hair Salon in San Juan Capistrano'
    mbook = f'<a class="bbtn mbook" href="{u("book/")}">Book an appointment</a>' if sticky else ''
    ld = json.dumps({"@context": "https://schema.org", "@type": "HairSalon", "name": SITE['name'],
                     "address": {"@type": "PostalAddress", "streetAddress": SITE['address1'],
                                 "addressLocality": "San Juan Capistrano", "addressRegion": "CA", "postalCode": "92675"},
                     "url": "https://www.theretreatsalon.co/", "sameAs": [f"https://www.instagram.com/{SITE['instagram']}/"]})
    doc = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(full_title)}</title><meta name="description" content="{e(desc[:300])}">
<meta property="og:title" content="{e(full_title)}"><meta property="og:description" content="{e(desc[:300])}"><meta property="og:image" content="{u(SITE['heroImage'])}">
<link rel="icon" href="{u('images/logo.png')}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400&family=Jost:wght@300;400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{u('style.css')}"><script type="application/ld+json">{ld}</script></head><body>
<div class="ann">{e(SITE['announcement'])} · <a href="{e(SITE['bookingUrl'])}" target="_blank" rel="noopener">Book online</a></div>
<nav><div class="links">{links}</div><button class="menu-btn" data-menu aria-label="Menu">☰</button>
<a href="{u('') or './'}"><img class="logo" src="{u('images/logo.png')}" alt="the retreat salon"></a>
<div class="right"><a class="loc" href="{u('visit/')}">San Juan Capistrano</a><a href="{u('book/')}" class="bbtn">Book</a></div></nav>
<div class="mnav"><button class="x" data-menu aria-label="Close">×</button>{mlinks}<a href="{u('book/')}" class="bbtn">Book now</a></div>
<main>{body(u)}</main>
<footer><div><img class="logo" src="{u('images/logo.png')}" alt="the retreat salon"><p style="max-width:300px;opacity:.7">{e(SITE['tagline'])} A beach-inspired salon in San Juan Capistrano.</p></div>
<div><h4>Visit</h4>{e(SITE['address1'])}<br>{e(SITE['address2'])}<br><span style="opacity:.7">{e(SITE['hours'])}</span></div>
<div><h4>Explore</h4>{mlinks}<a href="{u('book/')}">Book</a></div>
<div><h4>Follow</h4><a href="https://www.instagram.com/{e(SITE['instagram'])}/" target="_blank" rel="noopener">Instagram</a><a href="{e(SITE['bookingUrl'])}" target="_blank" rel="noopener">Book on Vagaro</a></div>
<p class="fine"><span class="c">© <span data-year>2026</span> {e(SITE['name'])} · San Juan Capistrano, California</span><a class="wip" href="https://workinprogress.agency/" target="_blank" rel="noopener">Site by WIP</a></p></footer>
{mbook}
{JS}<script>document.querySelector('[data-year]').textContent=new Date().getFullYear()</script>
</body></html>'''
    out = os.path.join(OUT, path, 'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w', encoding='utf-8') as f:
        f.write(doc)


def img(u, src, alt='', cls='cover', lazy=True):
    return f'<img class="{cls}" src="{u(src)}" alt="{e(alt)}"{" loading=lazy" if lazy else ""}>'


def svc_rows(u, limit=None):
    rows = ''
    for i, s in enumerate(SERVICES[:limit] if limit else SERVICES):
        price = f'<span>{e(s["price"])}</span>' if s.get('price') else ''
        rows += f'''<div class="svc"><span class="num">{i + 1:02d}</span><div><h3>{e(s["name"])}</h3><p>{e(s["description"])}</p><p class="inc">{e(s["includes"])}</p></div>
<div class="svc-r"><span>{e(s["duration"] or "Time varies")}</span>{price}<a href="{u('book/')}" class="tl">Book</a></div></div>'''
    return rows


def team_grid(u):
    return ''.join(f'''<a class="tm" href="{u('stylists/' + s['slug'] + '/')}"><div class="tm-img">{img(u, s['photo'], s['name'])}<span>View profile</span></div>
<p class="tm-n">{e(s["name"])}</p><p class="tm-r">{e(s["role"] if s["role"] != "Stylist" else s["specialty"])}</p></a>''' for s in TEAM)


def gallery(u, items, cls='gal'):
    return f'<div class="{cls}">' + ''.join(
        f'<figure>{img(u, g["image"], g["caption"])}<figcaption>{e(g["caption"])}</figcaption></figure>' for g in items) + '</div>'


def faq():
    return ''.join(f'<div class="faq-i"><button class="faq-q">{e(f["question"])}<span>+</span></button><div class="faq-a">{e(f["answer"])}</div></div>'
                   for f in SITE['faq'])


def booking_band(u):
    return f'''<div class="booking" id="book"><div><span class="eyebrow">Book online</span><h2 class="h2">Reserve <em>your hour.</em></h2>
<p>See real availability and book your service and stylist online. New to The Retreat? Tell us your hair goals and we’ll match you with the right stylist.</p>
<div class="row"><a href="{u('book/')}" class="bbtn light">Book an appointment</a><a href="{u('stylists/')}" class="ghost">Choose a stylist</a></div></div>
{img(u, 'images/space/entry.jpg', 'The entry at The Retreat Salon')}</div>'''


def visit_block(u, live_map=True):
    right = (f'<iframe src="{MAP_EMBED}" loading="lazy" title="Map to The Retreat Salon"></iframe>' if live_map else '')
    return f'''<section class="visit" id="visit"><div><span class="eyebrow a">Visit</span><h2 class="h2">Spend a day of <em>self care.</em></h2>
<p style="margin-top:20px">{e(SITE["location"])}</p><div class="info"><div><h4>Address</h4>{e(SITE["address1"])}<br>{e(SITE["address2"])}<br>
<a href="{DIRECTIONS}" target="_blank" rel="noopener" class="tl">Get directions</a></div><div><h4>Hours</h4>{e(SITE["hours"])}</div></div>
<a href="{u('book/')}" class="bbtn">Book an appointment</a><div class="faqwrap">{faq()}</div></div>
{right}</section>'''


def home(u):
    t1, t2 = (SITE['heroTitle'].split('|') + [''])[:2]
    ig = ['images/space/styling-floor.jpg', TEAM[1]['photo'], 'images/space/wash.jpg', TEAM[0]['photo'],
          'images/space/entry.jpg', 'images/space/wash-lounge.jpg']
    return f'''<header class="hero">{img(u, SITE['heroImage'], 'The styling floor at The Retreat Salon', lazy=False)}<div class="copy"><span class="eyebrow">{e(SITE['name'])} · San Juan Capistrano</span>
<h1>{e(t1)}<br><em>{e(t2)}</em></h1><p>{e(SITE['heroText'])}</p>
<a href="{u('book/')}" class="bbtn">Book an appointment</a><a href="{u('stylists/')}" class="ghost">Meet the stylists</a></div>
<a class="hcard" href="{e(SITE['bookingUrl'])}" target="_blank" rel="noopener"><span class="dot"></span><div><small>Book online, any time</small><b>See live availability</b> for all {len(TEAM)} stylists</div><span class="go">Book →</span></a></header>

<section class="intro"><div><span class="eyebrow a">Welcome to The Retreat</span>
<h2 class="h2">Your personal escape, <em>just off the coast.</em></h2></div>
<div><p class="lead">{e(SITE['intro'])}</p><div class="stats"><div><b>{len(TEAM)}</b><span>stylists</span></div><div><b>Lived-in</b><span>color specialists</span></div><div><b>Minutes</b><span>from Dana Point</span></div></div></div></section>

<div class="services" id="services"><div class="stick"><span class="eyebrow a">Services</span><h2 class="h2">Color, cuts &amp; <em>care.</em></h2>
{img(u, 'images/space/wash.jpg', 'The wash lounge')}<p>{e(SITE['servicesNote'])}</p></div>
<div>{svc_rows(u)}<div class="more"><a class="tl" href="{u('services/')}">All services and details →</a></div></div></div>

<section id="space"><div class="space-head"><h2 class="h2">Designed to <em>slow you down.</em></h2><p>Soft light through the arches, warm oak, deep wash chairs and nowhere you need to be. Come early, stay a little longer.</p></div>
{gallery(u, GALLERY[:5])}<div class="more"><a class="tl" href="{u('space/')}">See the space →</a></div></section>

<section id="stylists" style="padding-top:40px"><div class="team-head"><span class="eyebrow a">Meet your stylists</span><h2 class="h2">{len(TEAM)} artists, <em>one calm room.</em></h2>
<p>Every stylist here specializes in custom, lived-in hair that grows out beautifully. Tap a stylist to read their story and book with them.</p></div>
<div class="team">{team_grid(u)}</div></section>

{booking_band(u)}

<section class="ritual">{img(u, 'images/space/lobby.jpg', 'The lobby')}<div><span class="eyebrow a">The Retreat ritual</span><h2 class="h2" style="margin-bottom:24px">More than an <em>appointment.</em></h2>
<div class="step"><b>i.</b><div><h3>Arrive</h3><p>A warm welcome, a drink in hand and a quiet seat in the lobby.</p></div></div>
<div class="step"><b>ii.</b><div><h3>Consult</h3><p>Your stylist listens first: your hair, your routine, how you want it to grow out.</p></div></div>
<div class="step"><b>iii.</b><div><h3>Unwind</h3><p>A slow wash in the lounge, then color and cut with care for every detail.</p></div></div>
<div class="step"><b>iv.</b><div><h3>Leave effortless</h3><p>Finished with a blow dry &amp; style, and a plan for your next visit.</p></div></div></div></section>

{visit_block(u)}

<div class="ig-h"><span class="eyebrow a">Follow along</span><a href="https://www.instagram.com/{e(SITE['instagram'])}/" target="_blank" rel="noopener">@{e(SITE['instagram'])}</a></div>
<div class="ig">{''.join(f'<a href="https://www.instagram.com/{e(SITE["instagram"])}/" target="_blank" rel="noopener">{img(u, p)}</a>' for p in ig)}</div>'''


def services_page(u):
    return f'''<div class="pagehead"><span class="eyebrow a">Services</span><h1 class="h2">Color, cuts &amp; <em>care.</em></h1><p>{e(SITE['servicesNote'])}</p></div>
<div class="services"><div class="stick"><span class="eyebrow a">The menu</span><h2 class="h2" style="font-size:44px">Every service ends with a <em>blow dry &amp; style.</em></h2>
{img(u, 'images/space/wash-lounge.jpg', 'The wash lounge')}<p>Not sure what to book? Choose a consultation or tell your stylist your goals when you book, and they’ll plan it with you.</p></div>
<div>{svc_rows(u)}</div></div>{booking_band(u)}'''


def stylists_page(u):
    return f'''<div class="pagehead"><span class="eyebrow a">Meet your stylists</span><h1 class="h2">{len(TEAM)} artists, <em>one calm room.</em></h1>
<p>Every stylist here specializes in custom, lived-in hair that grows out beautifully. Pricing is set by each stylist.</p></div>
<section style="padding-top:20px"><div class="team">{team_grid(u)}</div></section>{booking_band(u)}'''


def stylist_page(s):
    def body(u):
        bio = paras(s['bio']) or f'<p>{e(s["summary"])}</p>'
        others = [o for o in TEAM if o['slug'] != s['slug']][:5]
        more = ''.join(f'''<a class="tm" href="{u('stylists/' + o['slug'] + '/')}"><div class="tm-img">{img(u, o['photo'], o['name'])}<span>View profile</span></div>
<p class="tm-n">{e(o["name"])}</p><p class="tm-r">{e(o["specialty"])}</p></a>''' for o in others)
        return f'''<div class="profile"><div class="pimg">{img(u, s['photo'], s['name'], lazy=False)}</div><div>
<a class="crumb" href="{u('stylists/')}">← All stylists</a><span class="eyebrow a">{e(s['role'])}</span>
<h1 class="h2">{e(s['name'])}</h1><p class="spec">{e(s['specialty'])}</p><div class="bio">{bio}</div>
<div class="acts"><a class="bbtn" href="{e(book_url(s))}" target="_blank" rel="noopener">Book with {e(first(s['name']))}</a>
<a class="ghost" href="https://www.instagram.com/{e(s['instagram'])}/" target="_blank" rel="noopener">@{e(s['instagram'])}</a></div></div></div>
<section style="padding-top:20px"><div class="team-head" style="margin-bottom:40px"><h2 class="h2" style="font-size:46px">More of <em>the team</em></h2></div><div class="team">{more}</div></section>'''
    page(f'stylists/{s["slug"]}/', s['name'], body, desc=f'{s["name"]}, {s["role"]} at {SITE["name"]}: {s["summary"]}', cur='stylists/')


def space_page(u):
    return f'''<div class="pagehead"><span class="eyebrow a">The Space</span><h1 class="h2">Designed to <em>slow you down.</em></h1>
<p>Soft light through the arches, warm oak, deep wash chairs and nowhere you need to be. Come early, stay a little longer.</p></div>
<section style="padding-top:20px">{gallery(u, GALLERY, 'gal full')}</section>{booking_band(u)}'''


def visit_page(u):
    return f'''<div class="pagehead"><span class="eyebrow a">Visit</span><h1 class="h2">Find <em>your retreat.</em></h1></div>
{visit_block(u)}'''


def book_page(u):
    widget = SITE.get('vagaroWidget', '').strip()
    if widget:
        main = f'<div class="bookcard"><h3>Book your appointment</h3><div class="widget">{widget}</div></div>'
    else:
        main = f'''<div class="bookcard"><span class="eyebrow a">Book online</span><h3>Choose your service, stylist and time.</h3>
<p>We book through Vagaro, so you’ll see each stylist’s real availability and get a confirmation and reminders by text and email.</p>
<ol><li>Pick your service</li><li>Choose a stylist, or anyone available</li><li>Pick a time and confirm</li></ol>
<a class="bbtn" href="{e(SITE['bookingUrl'])}" target="_blank" rel="noopener">Book on Vagaro</a></div>'''
    by = ''.join(f'''<a class="by" href="{e(book_url(s))}" target="_blank" rel="noopener">{img(u, s['photo'], s['name'], cls='')}<span><b>{e(s['name'])}</b><small>{e(s['specialty'])}</small></span></a>''' for s in TEAM)
    return f'''<div class="pagehead"><span class="eyebrow a">Book</span><h1 class="h2">Reserve <em>your hour.</em></h1>
<p>New to The Retreat? Book a consultation or your service with any stylist, and tell us your hair goals in the notes.</p></div>
<div class="bookpage">{main}<div><span class="eyebrow a">Book with a stylist</span><div class="bylist">{by}</div>
<p style="margin-top:24px;font-size:14px;opacity:.7">{e(SITE['servicesNote'])}</p></div></div>'''


def not_found(u):
    return f'''<div class="pagehead" style="padding-bottom:140px"><span class="eyebrow a">Page not found</span><h1 class="h2">Let’s get you <em>back.</em></h1>
<p>That page has moved. <a href="{u('') or './'}">Go to the home page</a> or <a href="{u('book/')}">book an appointment</a>.</p></div>'''


def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    shutil.copytree(os.path.join(ROOT, 'images'), os.path.join(OUT, 'images'))
    with open(os.path.join(OUT, 'style.css'), 'w', encoding='utf-8') as f:
        f.write(CSS)
    page('', '', home)
    page('services/', 'Services', services_page, cur='services/')
    page('stylists/', 'Stylists', stylists_page, cur='stylists/')
    for s in TEAM:
        stylist_page(s)
    page('space/', 'The Space', space_page, cur='space/')
    page('visit/', 'Visit', visit_page, cur='visit/')
    page('book/', 'Book', book_page, sticky=False)
    # 404 lives at the root, so its links must be absolute
    page('404/', 'Page not found', not_found)
    with open(os.path.join(OUT, '404', 'index.html'), encoding='utf-8') as f:
        doc = f.read().replace('href="../', 'href="/').replace('src="../', 'src="/')
    with open(os.path.join(OUT, '404.html'), 'w', encoding='utf-8') as f:
        f.write(doc)
    shutil.rmtree(os.path.join(OUT, '404'))
    pages = ['', 'services/', 'stylists/', 'space/', 'visit/', 'book/'] + [f'stylists/{s["slug"]}/' for s in TEAM]
    with open(os.path.join(OUT, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                + ''.join(f'<url><loc>https://www.theretreatsalon.co/{p}</loc></url>' for p in pages) + '</urlset>')
    with open(os.path.join(OUT, 'robots.txt'), 'w') as f:
        f.write('User-agent: *\nAllow: /\nSitemap: https://www.theretreatsalon.co/sitemap.xml\n')
    print(f'Built {len(pages)} pages into _site/')


if __name__ == '__main__':
    main()
    if '--serve' in sys.argv:
        import http.server, functools
        http.server.ThreadingHTTPServer(('', 8000), functools.partial(http.server.SimpleHTTPRequestHandler, directory=OUT)).serve_forever()
