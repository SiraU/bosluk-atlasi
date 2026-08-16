# -*- coding: utf-8 -*-
"""Bosluk Atlasi (Translation-Gap Atlas) sayfasini uretir.
OpenAIRE AI Hackathon (Tema B) teslimi icin.
Girdi: graf_olcum_sonuc.json (koleksiyon-seviyesi), atlas-veri.json (eser-seviyesi)
Cikti: /tmp/bosluk-atlasi.html"""
import json, html as htmlmod
from pathlib import Path
from datetime import date

WD = Path(__file__).parent

def esc(s): return htmlmod.escape(str(s), quote=True)

kume = json.load(open(WD / "graf_olcum_sonuc.json", encoding="utf-8"))
atlas = json.load(open(WD / "atlas-veri.json", encoding="utf-8"))
eserler = atlas["eserler"]

# ---- Koleksiyon/kume tablosu, toplam yayina gore sirali ----
KUME_TR = {
    "alchemy": "Simya", "gnosticism": "Gnostisizm", "western esotericism": "Batı Ezoterizmi",
    "hermeticism": "Hermetisizm", "knights templar": "Tapınakçılar", "hermetica": "Hermetica",
    "corpus hermeticum": "Corpus Hermeticum", "cornelius agrippa": "Cornelius Agrippa",
    "picatrix": "Picatrix",
}
satirlar = []
for kw, d in kume.items():
    tr = d["turkish"]; scanned = d["scanned"]; total = d["total"]
    pct = (tr / scanned * 100) if scanned else 0
    satirlar.append((kw, KUME_TR.get(kw, kw), total, scanned, tr, pct))
satirlar.sort(key=lambda x: -x[2])

toplam_yayin = sum(x[2] for x in satirlar)
toplam_taranan = sum(x[3] for x in satirlar)
toplam_tr = sum(x[4] for x in satirlar)
ort_tr_pct = (toplam_tr / toplam_taranan * 100) if toplam_taranan else 0

def bin_ayrac(n):
    """1234 -> '1.234' (Turkce binlik ayiraci). SADECE sayiya uygulanir,
    cevredeki metne (baslik ictindeki gercek virguller vb.) dokunmaz."""
    return f"{n:,}".replace(",", ".")

def bar_row(kw, ad, total, scanned, tr, pct):
    genislik = min(100, (total / satirlar[0][2]) * 100)
    tr_str = f"%{pct:.2f}".replace(".", ",") if pct > 0 else "0"
    renk = "var(--gold)" if pct > 0 else "var(--muted)"
    return (
        '<div style="margin:0 0 1.1rem">'
        '<div style="display:flex;justify-content:space-between;align-items:baseline;'
        'font-family:\'Raleway\',sans-serif;font-size:.88rem;margin-bottom:.3rem">'
        f'<span style="color:var(--ink);font-weight:600">{esc(ad)}</span>'
        f'<span style="color:var(--muted)">{bin_ayrac(total)} yayın · TR {tr_str}</span></div>'
        '<div style="background:var(--cream-dark,#ece3d1);border-radius:6px;height:10px;overflow:hidden">'
        f'<div style="width:{genislik:.1f}%;height:100%;background:var(--navy)"></div></div>'
        '</div>'
    )

isi_haritasi = "".join(bar_row(*s) for s in satirlar)

# ---- En yogun 20 (zaten cevrilmis eserler, alani en canli olanlar) ----
gecerli = [e for e in eserler if e["graf_yogunlugu"] > 0]
en_yogun = sorted(gecerli, key=lambda x: -x["graf_yogunlugu"])[:20]
yogun_satirlar = "".join(
    f'<a href="/{esc(e["slug"])}" style="display:flex;align-items:center;gap:1rem;padding:.7rem .9rem;'
    'background:var(--cream);border:1px solid var(--line);border-radius:10px;text-decoration:none;'
    'margin-bottom:.5rem;transition:border-color .15s">'
    f'<span style="flex-shrink:0;width:8px;height:8px;border-radius:50%;background:var(--gold)"></span>'
    f'<span style="flex:1;font-family:\'Cormorant Garamond\',serif;font-size:1.08rem;font-weight:600;'
    f'color:var(--ink);line-height:1.25">{esc(e["baslik"])}</span>'
    f'<span style="font-family:\'Raleway\',sans-serif;font-size:.7rem;color:var(--muted);white-space:nowrap">'
    f'{bin_ayrac(e["graf_yogunlugu"])} yayın</span></a>'
    for e in en_yogun
)

sifir_sayisi = sum(1 for e in eserler if e["graf_yogunlugu"] == 0)

AY = ["", "Ocak","Şubat","Mart","Nisan","Mayıs","Haziran","Temmuz",
      "Ağustos","Eylül","Ekim","Kasım","Aralık"]
today = date.today()
tarih_str = f"{today.day} {AY[today.month]} {today.year}"

def stat_card(num_str, label, accent=False):
    col = "var(--gold)" if accent else "var(--ink)"
    return ('<div style="flex:1;min-width:140px;background:var(--cream);border:1px solid var(--line);'
            'border-radius:12px;padding:1.6rem 1.4rem;text-align:center">'
            f'<div style="font-family:\'Cormorant Garamond\',serif;font-size:2.4rem;font-weight:700;'
            f'line-height:1;color:{col}">{num_str}</div>'
            '<div style="font-family:\'Raleway\',sans-serif;font-size:.72rem;letter-spacing:.08em;'
            f'text-transform:none;color:var(--muted);margin-top:.6rem">{label}</div></div>')

HTML = f"""<!doctype html><html lang="tr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="icon" type="image/svg+xml" href="/favicon.svg?v=2">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png?v=2">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16.png?v=2">
<link rel="icon" href="/favicon.ico?v=2" sizes="any">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v=2">
<title>Boşluk Atlası: Bir Alan Ne Kadar Yalnız Yaşıyor — Kadim Kütüphane</title>
<meta name="description" content="OpenAIRE Graph'teki uluslararası araştırma yoğunluğunu, Kadim Kütüphane'nin çevirdiği kaynakların Türkçe erişilebilirliğiyle karşılaştıran açık veri aracı. Batı ezoterizmi alanı uluslararası canlı ama Türkçe bilimsel çıktı neredeyse sıfır.">
<link rel="canonical" href="https://kadimkutuphane.com/bosluk-atlasi">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Kadim Kütüphane">
<meta property="og:locale" content="tr_TR">
<meta property="og:title" content="Boşluk Atlası — Kadim Kütüphane × OpenAIRE">
<meta property="og:description" content="Batı ezoterizmi alanında uluslararası literatür yoğun, Türkçe bilimsel çıktı ise neredeyse sıfır. OpenAIRE Graph verisiyle ölçüldü.">
<meta property="og:url" content="https://kadimkutuphane.com/bosluk-atlasi">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="Boşluk Atlası — Kadim Kütüphane × OpenAIRE">
<meta name="twitter:description" content="Bir araştırma alanı uluslararası ne kadar canlı, Türkçede ne kadar yalnız? OpenAIRE Graph ile ölçüldü.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600&family=Raleway:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/style.css">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Dataset","name":"Boşluk Atlası: Translation-Gap Atlas",
"description":"OpenAIRE Graph araştırma yoğunluğu ile Kadim Kütüphane'nin Türkçe çeviri kataloğunu karşılaştıran açık veri seti ve metodoloji.",
"creator":{{"@type":"Person","name":"Şira Nur Uysal"}},
"license":"https://creativecommons.org/licenses/by/4.0/",
"isPartOf":{{"@type":"CreativeWork","name":"OpenAIRE AI Hackathon 2026"}}}}
</script>
</head><body>
<nav class="kd-nav"><a class="kd-nav-brand" href="/">Kadim Kütüphane</a><div class="kd-nav-links">
<a href="/">Kütüphane</a><a href="/ara">Ara</a><a href="/sanat">Sanat</a><a href="/rehberler">Rehberler</a>
<a href="/hakkinda">Hakkında</a><a href="/lisans">Lisans</a>
<a href="https://kutsaladonus.com" target="_blank" rel="noopener">Kutsala Dönüş</a></div>
<button class="kd-burger" id="kdBurger" aria-label="Menüyü aç/kapa" aria-expanded="false"><span></span><span></span><span></span></button></nav>
<script>(function(){{var b=document.getElementById('kdBurger');var m=document.querySelector('.kd-nav-links');if(!b||!m)return;
b.addEventListener('click',function(){{var open=m.classList.toggle('open');b.classList.toggle('open',open);
b.setAttribute('aria-expanded',open?'true':'false');}});
m.querySelectorAll('a').forEach(function(a){{a.addEventListener('click',function(){{m.classList.remove('open');
b.classList.remove('open');b.setAttribute('aria-expanded','false');}});}});}})();</script>

<div class="wrap" style="max-width:860px">

<div class="section-label" style="text-transform:none">BOŞLUK ATLASI · OpenAIRE AI Hackathon 2026 · {tarih_str}</div>
<h1 style="font-family:'Cormorant Garamond',serif;color:var(--ink);font-size:2.6rem;font-weight:700;
margin:0 0 .8rem;line-height:1.12">Bir alan ne kadar yalnız yaşıyor?</h1>
<p style="font-family:'Raleway',sans-serif;font-size:1.04rem;line-height:1.75;color:var(--ink);
max-width:700px;margin:0 0 2rem">
Batı ezoterik geleneği (simya, Hermetisizm, gnostisizm, Tapınakçılar…) uluslararası akademide
canlı bir araştırma alanı. Ama bu alanın birincil kaynakları Türkçede ne kadar erişilebilir, ve
bilimsel yazın Türkçede ne kadar var? <b>Boşluk Atlası</b>, OpenAIRE Graph'teki yayın yoğunluğunu
tarayarak bu soruyu ölçülebilir hale getiriyor — ve Kadim Kütüphane'nin 844 kaynaklık çeviri
kataloğunun bu boşluğun neresinde durduğunu gösteriyor.
</p>

<div style="display:flex;gap:1rem;flex-wrap:wrap;margin:0 0 2.6rem">
{stat_card(f"{toplam_yayin:,}".replace(",", "."), "taranan konu kümesinde toplam yayın", True)}
{stat_card(f"%{ort_tr_pct:.2f}".replace(".", ","), "ortalama Türkçe pay")}
{stat_card("844", "Kadim Kütüphane'nin çevirdiği kaynak")}
{stat_card(str(sifir_sayisi), "OpenAIRE'de iz bırakmamış çeviri")}
</div>

<h2 style="font-family:'Cormorant Garamond',serif;color:var(--ink);font-size:1.7rem;font-weight:700;
margin:0 0 .3rem">Isı Haritası: 9 konu kümesi, uluslararası yoğunluk ve Türkçe pay</h2>
<p style="font-family:'Raleway',sans-serif;font-size:.92rem;color:var(--muted);margin:0 0 1.6rem">
OpenAIRE'in genel API'sinden ({today.strftime('%Y-%m-%d')} itibarıyla) anahtar kelime taramasıyla ölçüldü.
Çubuk uzunluğu toplam yayın sayısını, altın rozet Türkçe payı gösterir.
</p>
<div style="background:var(--cream);border:1px solid var(--line);border-radius:14px;padding:1.6rem 1.6rem 1rem;margin:0 0 2.6rem">
{isi_haritasi}
</div>

<h2 style="font-family:'Cormorant Garamond',serif;color:var(--ink);font-size:1.7rem;font-weight:700;
margin:0 0 .3rem">Zaten Çevrilenler: En Yoğun Araştırılan 20 Kaynak</h2>
<p style="font-family:'Raleway',sans-serif;font-size:.92rem;color:var(--muted);margin:0 0 1.4rem">
Kadim Kütüphane'nin 844 çevirisinden, OpenAIRE Graph'te en yoğun araştırma izine sahip 20'si —
yani uluslararası akademinin en çok ilgilendiği ama Türkçe okurun artık doğrudan erişebildiği eserler.
</p>
<div style="margin:0 0 2.6rem">
{yogun_satirlar}
</div>

<h2 style="font-family:'Cormorant Garamond',serif;color:var(--ink);font-size:1.7rem;font-weight:700;
margin:0 0 .8rem">Döngü: Grafı Okumakla Kalmıyoruz, Grafı Besliyoruz</h2>
<p style="font-family:'Raleway',sans-serif;font-size:1rem;line-height:1.75;color:var(--ink);margin:0 0 1.2rem">
Kadim Kütüphane'nin çevirileri Zenodo'ya DOI'li kayıtlar olarak yükleniyor (CC BY-SA 4.0) —
bu kayıtlar zamanla OpenAIRE Graph'e düşüyor. Yani bu araç sadece boşluğu <i>ölçmüyor</i>;
kütüphanenin kendi çevirileri, ölçtüğü grafın bir parçası haline geliyor. Şu an canlıda
<a href="https://zenodo.org/search?q=%22kadim%20k%C3%BCt%C3%BCphane%22" target="_blank" rel="noopener">7 DOI'li kayıt</a> var, devamı geliyor.
</p>

<div style="background:var(--navy);color:#fff;border-radius:14px;padding:1.8rem 2rem;margin:0 0 2.6rem">
<div style="font-family:'Raleway',sans-serif;font-size:.72rem;letter-spacing:.12em;color:var(--gold);
margin-bottom:.6rem">FOR EVALUATORS — ENGLISH SUMMARY</div>
<p style="font-family:'Raleway',sans-serif;font-size:.95rem;line-height:1.7;color:#eee;margin:0 0 1rem">
Kadim Kütüphane publishes Turkish translations of 844 primary sources of the Western esoteric
tradition under CC BY-SA 4.0. This tool connects that catalogue to the OpenAIRE Graph: for nine
core topic clusters (alchemy, gnosticism, western esotericism, hermeticism, Knights Templar,
hermetica, Corpus Hermeticum, Cornelius Agrippa, Picatrix) we measured total publication volume
and language distribution record-by-record via OpenAIRE's public API.
</p>
<p style="font-family:'Raleway',sans-serif;font-size:.95rem;line-height:1.7;color:#eee;margin:0">
<b>Finding:</b> the field is internationally active ({toplam_yayin:,} publications scanned across
the nine clusters) but linguistically one-sided &mdash; average Turkish-language share is
<b>{ort_tr_pct:.2f}%</b>, with zero Turkish records for Picatrix, Hermetica and Cornelius Agrippa.
This is the structural gap Kadim Kütüphane's translation work addresses. Methodology, scripts and
the full dataset are published under CC-BY for reuse with any other language or source library.
</p>
</div>

<div style="font-family:'Raleway',sans-serif;font-size:.85rem;color:var(--muted);line-height:1.7;
border-top:1px solid var(--line);padding-top:1.4rem">
<b>Metodoloji ve tekrar üretilebilirlik:</b> Veri OpenAIRE'in genel API'sinden
(<code>api.openaire.eu/search/publications</code>) çevrimdışı olarak üretildi, bu sayfa canlı bir
API'ye bağlı değil. Ölçüm betikleri ve tam veri seti CC-BY lisansıyla açık — metodoloji notu ve
kaynak kod için <a href="/hakkinda">Hakkında</a> sayfasına bakın. Boşluk skoru formülü:
<code>boşluk_skoru(eser,dil) = graf_yoğunluğu(eser) × (1 − dilde_erişilebilirlik(eser,dil))</code>.
</div>

</div>
</body></html>"""

out = Path("/tmp/bosluk-atlasi.html")
out.write_text(HTML, encoding="utf-8")
print(f"✓ {out} yazıldı ({len(HTML):,} bayt)".replace(",", "."))
