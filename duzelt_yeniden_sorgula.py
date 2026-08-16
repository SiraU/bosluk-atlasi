#!/usr/bin/env python3
"""KANONIK duzeltmesinden sonra SADECE etkilenen eserleri yeniden sorgulayip
atlas-veri.json icindeki karsiliklarini gunceller (tam 844'luk kosuyu tekrarlamadan)."""
import json, time, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import atlas_betigi as ab

ETKILENEN_SLUGLER = {
    "della-porta-dogal-buyu", "della-porta-yildizlar-ve-mizac-goksel-fizyonomi",
    "fourth-book-occult-philosophy-magus-ilahi-yorumcu",
    "richard-saint-victor-benjamin-gormeyen-goz",
    "john-smith-select-discourses-mutlulugun-tanri-hazzi",
    "richard-of-st-victor-benjamin-minor-preparation-of-the-soul-for-contemplation",
    "hugo-victor-ruhun-yaraticiyi-temasa-bilgisi",
    "saint-martin-insandan-bagimsiz-hakikatler",
    "henry-more-ruhun-olumsuzlugu-ebedi-hayata-yukselis",
    "john-smith-secme-soylevler-ilahi-bilgi",
    "thomas-taylor-eleusis-gizemleri-inisiyasyon-toreni",
}

veri_yolu = Path(__file__).parent / "atlas-veri.json"
d = json.load(open(veri_yolu, encoding="utf-8"))

n = 0
for e in d["eserler"]:
    if e["slug"] not in ETKILENEN_SLUGLER:
        continue
    eski_sorgu, eski_y = e["graf_sorgusu"], e["graf_yogunlugu"]
    yeni_sorgu = ab.sorgu_uret(e["slug"], e["baslik"], e["koleksiyon"])
    yeni_y = ab.graf_yogunlugu(yeni_sorgu)
    e["graf_sorgusu"] = yeni_sorgu
    e["graf_yogunlugu"] = yeni_y
    e["bosluk_skoru"] = ab.skorla(yeni_y, katalogda=True)
    print(f"{e['slug'][:55]:<57} {eski_sorgu!r} ({eski_y}) -> {yeni_sorgu!r} ({yeni_y})")
    n += 1
    time.sleep(ab.GECIKME)

d["olcum_tarihi"] = time.strftime("%Y-%m-%d")
json.dump(d, open(veri_yolu, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"\n✓ {n} eser guncellendi, atlas-veri.json yeniden yazildi")
