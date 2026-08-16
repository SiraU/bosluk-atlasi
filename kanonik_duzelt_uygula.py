#!/usr/bin/env python3
import json, time, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import atlas_betigi as ab

yeni = json.load(open('/tmp/kanonik_duzelt.json', encoding='utf-8'))
veri_yolu = Path(__file__).parent / "atlas-veri.json"
d = json.load(open(veri_yolu, encoding="utf-8"))

n = 0
for e in d["eserler"]:
    if e["slug"] not in yeni:
        continue
    yeni_sorgu = yeni[e["slug"]]
    eski_y = e["graf_yogunlugu"]
    y = ab.graf_yogunlugu(yeni_sorgu)
    e["graf_sorgusu"] = yeni_sorgu
    e["graf_yogunlugu"] = y
    e["bosluk_skoru"] = ab.skorla(y, katalogda=True)
    print(f"{e['slug'][:45]:<47} {eski_y:>6} -> {y:>6}  ({yeni_sorgu})")
    n += 1
    time.sleep(ab.GECIKME)

d["olcum_tarihi"] = time.strftime("%Y-%m-%d")
json.dump(d, open(veri_yolu, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"\n✓ {n} eser guncellendi")
