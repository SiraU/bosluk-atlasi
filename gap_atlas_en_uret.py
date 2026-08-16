# -*- coding: utf-8 -*-
"""Generates the English Gap Atlas page (/gap-atlas) — mirror of /bosluk-atlasi.
Input: graf_olcum_sonuc.json (cluster level), atlas-veri.json (work level)
Output: /tmp/gap-atlas.html"""
import json, html as htmlmod
from pathlib import Path
from datetime import date

WD = Path(__file__).parent

def esc(s): return htmlmod.escape(str(s), quote=True)

with open(WD / "graf_olcum_sonuc.json", encoding="utf-8") as f:
    kume = json.load(f)
with open(WD / "atlas-veri.json", encoding="utf-8") as f:
    atlas = json.load(f)
eserler = atlas["eserler"]

KUME_EN = {
    "alchemy": "Alchemy", "gnosticism": "Gnosticism", "western esotericism": "Western Esotericism",
    "hermeticism": "Hermeticism", "knights templar": "Knights Templar", "hermetica": "Hermetica",
    "corpus hermeticum": "Corpus Hermeticum", "cornelius agrippa": "Cornelius Agrippa",
    "picatrix": "Picatrix",
}
satirlar = []
for kw, d in kume.items():
    tr = d["turkish"]; scanned = d["scanned"]; total = d["total"]
    pct = (tr / scanned * 100) if scanned else 0
    satirlar.append((kw, KUME_EN.get(kw, kw), total, scanned, tr, pct))
satirlar.sort(key=lambda x: -x[2])

toplam_yayin = sum(x[2] for x in satirlar)
toplam_taranan = sum(x[3] for x in satirlar)
toplam_tr = sum(x[4] for x in satirlar)
ort_tr_pct = (toplam_tr / toplam_taranan * 100) if toplam_taranan else 0

MAX_TOTAL = satirlar[0][2] if satirlar and satirlar[0][2] > 0 else 1

def bar_row(kw, ad, total, scanned, tr, pct):
    genislik = min(100, (total / MAX_TOTAL) * 100)
    tr_str = f"{pct:.2f}%" if pct > 0 else "0"
    return (
        '<div style="margin:0 0 1.1rem">'
        '<div style="display:flex;justify-content:space-between;align-items:baseline;'
        'font-family:\'Raleway\',sans-serif;font-size:.88rem;margin-bottom:.3rem">'
        f'<span style="color:var(--ink);font-weight:600">{esc(ad)}</span>'
        f'<span style="color:var(--muted)">{total:,} publications &middot; TR {tr_str}</span></div>'
        '<div style="background:var(--cream-dark,#ece3d1);border-radius:6px;height:10px;overflow:hidden">'
        f'<div style="width:{genislik:.1f}%;height:100%;background:var(--navy)"></div></div>'
        '</div>'
    )

isi_haritasi = "".join(bar_row(*s) for s in satirlar)

gecerli = [e for e in eserler if e["graf_yogunlugu"] > 0]
en_yogun = sorted(gecerli, key=lambda x: -x["graf_yogunlugu"])[:20]
yogun_satirlar = "".join(
    f'<a href="/{esc(e["slug"])}" style="display:flex;align-items:center;gap:1rem;padding:.7rem .9rem;'
    'background:var(--cream);border:1px solid var(--line);border-radius:10px;text-decoration:none;'
    'margin-bottom:.5rem;transition:border-color .15s">'
    f'<span style="flex-shrink:0;width:8px;height:8px;border-radius:50%;background:var(--gold)"></span>'
    '<span style="flex:1;line-height:1.3">'
    f'<span style="display:block;font-family:\'Raleway\',sans-serif;font-size:.94rem;font-weight:600;'
    f'color:var(--ink)">{esc(e["graf_sorgusu"])}</span>'
    f'<span style="display:block;font-family:\'Cormorant Garamond\',serif;font-size:.95rem;'
    f'color:var(--muted)">{esc(e["baslik"])}</span></span>'
    f'<span style="font-family:\'Raleway\',sans-serif;font-size:.7rem;color:var(--muted);white-space:nowrap">'
    f'{e["graf_yogunlugu"]:,} publications</span></a>'
    for e in en_yogun
)

sifir_sayisi = sum(1 for e in eserler if e["graf_yogunlugu"] == 0)
iz_birakan = len(eserler) - sifir_sayisi

today = date.today()
tarih_str = today.strftime("%d %B %Y")

def stat_card(num_str, label, accent=False):
    col = "var(--gold)" if accent else "var(--ink)"
    return ('<div style="flex:1;min-width:140px;background:var(--cream);border:1px solid var(--line);'
            'border-radius:12px;padding:1.6rem 1.4rem;text-align:center">'
            f'<div style="font-family:\'Cormorant Garamond\',serif;font-size:2.4rem;font-weight:700;'
            f'line-height:1;color:{col}">{num_str}</div>'
            '<div style="font-family:\'Raleway\',sans-serif;font-size:.72rem;letter-spacing:.08em;'
            f'text-transform:none;color:var(--muted);margin-top:.6rem">{label}</div></div>')

HTML = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="icon" type="image/svg+xml" href="/favicon.svg?v=2">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png?v=2">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16.png?v=2">
<link rel="icon" href="/favicon.ico?v=2" sizes="any">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v=2">
<title>Gap Atlas: How Lonely Does a Field Live? — Kadim Kütüphane</title>
<meta name="description" content="An open-data tool crossing international research density in the OpenAIRE Graph with the Turkish-language accessibility of the 844 primary sources translated by Kadim Kütüphane.">
<link rel="canonical" href="https://kadimkutuphane.com/gap-atlas">
<link rel="alternate" hreflang="tr" href="https://kadimkutuphane.com/bosluk-atlasi">
<link rel="alternate" hreflang="en" href="https://kadimkutuphane.com/gap-atlas">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Kadim Kütüphane">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="Gap Atlas — Kadim Kütüphane × OpenAIRE">
<meta property="og:description" content="The Western esoteric tradition is internationally active research — and nearly silent in Turkish. Measured with the OpenAIRE Graph.">
<meta property="og:url" content="https://kadimkutuphane.com/gap-atlas">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="Gap Atlas — Kadim Kütüphane × OpenAIRE">
<meta name="twitter:description" content="How internationally alive is a research field, and how lonely is it in Turkish? Measured with the OpenAIRE Graph.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600&family=Raleway:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/style.css">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Dataset","name":"Gap Atlas: Translation-Gap Atlas",
"description":"Open dataset and methodology crossing OpenAIRE Graph research density with Kadim Kütüphane's Turkish translation catalogue.",
"creator":{{"@type":"Person","name":"Şira Nur Uysal"}},
"license":"https://creativecommons.org/licenses/by/4.0/",
"isPartOf":{{"@type":"CreativeWork","name":"OpenAIRE AI Hackathon 2026"}}}}
</script>
</head><body>
<nav class="kd-nav"><a class="kd-nav-brand" href="/">Kadim Kütüphane</a><div class="kd-nav-links">
<a href="/">Library</a><a href="/ara">Search</a><a href="/sanat">Art</a><a href="/rehberler">Guides</a>
<a href="/hakkinda">About</a><a href="/lisans">License</a>
<a href="https://kutsaladonus.com" target="_blank" rel="noopener">Kutsala Dönüş</a></div>
<button class="kd-burger" id="kdBurger" aria-label="Toggle menu" aria-expanded="false"><span></span><span></span><span></span></button></nav>
<script>(function(){{var b=document.getElementById('kdBurger');var m=document.querySelector('.kd-nav-links');if(!b||!m)return;
b.addEventListener('click',function(){{var open=m.classList.toggle('open');b.classList.toggle('open',open);
b.setAttribute('aria-expanded',open?'true':'false');}});
m.querySelectorAll('a').forEach(function(a){{a.addEventListener('click',function(){{m.classList.remove('open');
b.classList.remove('open');b.setAttribute('aria-expanded','false');}});}});}})();</script>

<div class="wrap" style="max-width:860px">

<div class="section-label" style="text-transform:none;display:flex;justify-content:space-between;align-items:baseline;gap:1rem;flex-wrap:wrap">
<span>GAP ATLAS &middot; OpenAIRE AI Hackathon 2026 &middot; {tarih_str}</span>
<a href="/bosluk-atlasi" style="font-family:'Raleway',sans-serif;font-size:.78rem;letter-spacing:.06em;color:var(--gold);text-decoration:none;white-space:nowrap">Türkçe sürüm &rarr;</a></div>
<h1 style="font-family:'Cormorant Garamond',serif;color:var(--ink);font-size:2.6rem;font-weight:700;
margin:0 0 .8rem;line-height:1.12">How lonely does a field live?</h1>
<p style="font-family:'Raleway',sans-serif;font-size:1.04rem;line-height:1.75;color:var(--ink);
max-width:700px;margin:0 0 2rem">
The Western esoteric tradition (alchemy, Hermeticism, gnosticism, the Knights Templar&hellip;) is a
lively field of international scholarship. But how accessible are its primary sources in Turkish,
and how much Turkish-language research exists around them? The <b>Gap Atlas</b> makes this
measurable by scanning publication density in the OpenAIRE Graph &mdash; and shows where
Kadim Kütüphane's 844-source translation catalogue stands inside that gap.
</p>

<div style="display:flex;gap:1rem;flex-wrap:wrap;margin:0 0 2.6rem">
{stat_card(f"{toplam_yayin:,}", "total publications in scanned clusters", True)}
{stat_card(f"{ort_tr_pct:.2f}%", "average Turkish-language share")}
{stat_card("844", "sources translated by Kadim Kütüphane")}
{stat_card(f"{sifir_sayisi:,}", "translations with zero trace in OpenAIRE")}
</div>

<h2 style="font-family:'Cormorant Garamond',serif;color:var(--ink);font-size:1.7rem;font-weight:700;
margin:0 0 .3rem">Heat Map: 9 topic clusters, international density and Turkish share</h2>
<p style="font-family:'Raleway',sans-serif;font-size:.92rem;color:var(--muted);margin:0 0 1.6rem">
Measured via keyword scans of OpenAIRE's public API (as of {today.strftime('%Y-%m-%d')}).
Bar length shows total publication count; the badge shows the Turkish-language share.
</p>
<div style="background:var(--cream);border:1px solid var(--line);border-radius:14px;padding:1.6rem 1.6rem 1rem;margin:0 0 2.6rem">
{isi_haritasi}
</div>

<h2 style="font-family:'Cormorant Garamond',serif;color:var(--ink);font-size:1.7rem;font-weight:700;
margin:0 0 .3rem">Already Translated: The 20 Most-Researched Sources</h2>
<p style="font-family:'Raleway',sans-serif;font-size:.92rem;color:var(--muted);margin:0 0 1.4rem">
Of Kadim Kütüphane's 844 translations, the 20 with the densest research trace in the OpenAIRE Graph
&mdash; the works international academia studies most, now directly readable in Turkish.
Overall, {iz_birakan} of the 844 works (63%) leave at least one trace in the Graph; {sifir_sayisi} (37%) leave none.
</p>
<div style="margin:0 0 2.6rem">
{yogun_satirlar}
</div>

<h2 style="font-family:'Cormorant Garamond',serif;color:var(--ink);font-size:1.7rem;font-weight:700;
margin:0 0 .8rem">The Loop: We Don't Just Read the Graph, We Feed It</h2>
<p style="font-family:'Raleway',sans-serif;font-size:1rem;line-height:1.75;color:var(--ink);margin:0 0 1.2rem">
Kadim Kütüphane's translations are deposited on Zenodo as DOI-bearing records (CC BY-SA 4.0) &mdash;
and those records flow into the OpenAIRE Graph over time. So this tool does not merely <i>measure</i>
the gap; the library's own translations become part of the very graph being measured. There are
currently <a href="https://zenodo.org/search?q=%22kadim%20k%C3%BCt%C3%BCphane%22" target="_blank" rel="noopener">7 DOI-bearing records</a> live, with more on the way.
</p>

<div style="background:var(--navy);color:#fff;border-radius:14px;padding:1.8rem 2rem;margin:0 0 2.6rem">
<div style="font-family:'Raleway',sans-serif;font-size:.72rem;letter-spacing:.12em;color:var(--gold);
margin-bottom:.6rem">METHOD IN ONE PARAGRAPH</div>
<p style="font-family:'Raleway',sans-serif;font-size:.95rem;line-height:1.7;color:#eee;margin:0">
For each of the 844 works we built a disambiguated OpenAIRE <code>keywords</code> query identifying
the work or author unambiguously (never the raw Turkish page slug &mdash; naive queries either go
silent or collide with unrelated namesakes), measured how many publications the public Graph API
returns, and combined that with the cluster-level heat map above. Gap score formula:
<code>gap_score(work, language) = graph_density(work) &times; (1 &minus; accessibility(work, language))</code>.
All scripts and the full dataset are CC-BY.
</p>
</div>

<div style="font-family:'Raleway',sans-serif;font-size:.85rem;color:var(--muted);line-height:1.7;
border-top:1px solid var(--line);padding-top:1.4rem">
<b>Methodology &amp; reproducibility:</b> Data was produced offline from OpenAIRE's public API
(<code>api.openaire.eu/search/publications</code>); this page makes no live API calls.
Measurement scripts and the full dataset are open under CC-BY:
<a href="https://github.com/SiraU/bosluk-atlasi" target="_blank" rel="noopener">github.com/SiraU/bosluk-atlasi</a>.
Turkish version of this page: <a href="/bosluk-atlasi">/bosluk-atlasi</a>.
</div>

</div>
</body></html>"""

out = Path("/tmp/gap-atlas.html")
out.write_text(HTML, encoding="utf-8")
print(f"OK {out} written ({len(HTML):,} bytes)")
