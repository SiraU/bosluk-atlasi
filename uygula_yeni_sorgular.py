#!/usr/bin/env python3
"""Kapsanmayan 687 eser icin uretilen yeni sorgulari uygular, OpenAIRE'i yeniden sorgular,
atlas-veri.json'daki karsiliklarini gunceller."""
import json, time, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import atlas_betigi as ab

yeni_sorgular = json.load(open('/tmp/sorgu_birlesik.json', encoding='utf-8'))

veri_yolu = Path(__file__).parent / "atlas-veri.json"
d = json.load(open(veri_yolu, encoding="utf-8"))

n = 0
hata = 0
for e in d["eserler"]:
    slug = e["slug"]
    if slug not in yeni_sorgular:
        continue
    yeni_sorgu = yeni_sorgular[slug]
    eski_y = e["graf_yogunlugu"]
    y = ab.graf_yogunlugu(yeni_sorgu)
    if y == -1:
        hata += 1
        time.sleep(1)
        y = ab.graf_yogunlugu(yeni_sorgu)  # bir kez daha dene
    e["graf_sorgusu"] = yeni_sorgu
    e["graf_yogunlugu"] = y
    e["bosluk_skoru"] = ab.skorla(y, katalogda=True)
    n += 1
    if n % 25 == 0:
        print(f"[{n}/687] {slug[:40]:<42} {eski_y:>6} -> {y:>6}  ({yeni_sorgu})", flush=True)
        json.dump(d, open(veri_yolu, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    time.sleep(ab.GECIKME)

d["olcum_tarihi"] = time.strftime("%Y-%m-%d")
json.dump(d, open(veri_yolu, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"\n✓ TAMAM: {n} eser guncellendi, {hata} gecici hata, atlas-veri.json yeniden yazildi")
