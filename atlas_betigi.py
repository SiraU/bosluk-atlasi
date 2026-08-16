#!/usr/bin/env python3
"""
Boşluk Atlası — çekirdek betik
Kadim Kütüphane kataloğundaki her eser için OpenAIRE Graph yoğunluğunu ölçer,
boşluk skoru hesaplar ve atlas-veri.json üretir.

Kullanım:
  python3 atlas_betigi.py --demo        # 8 eserlik örnek koşu (hızlı)
  python3 atlas_betigi.py --top 100     # en bilinen 100 eser (tam koşu öncesi)
  python3 atlas_betigi.py               # tam katalog (844 eser, ~30-40 dk)
"""
import csv, json, time, sys, urllib.request, urllib.parse
from pathlib import Path

BASE = "https://api.openaire.eu/search/publications"
GECIKME = 0.4  # API'ye nazik bekleme (sn)

# ------------------------------------------------------------------
# 1. ADIM: katalog satırından graf sorgusu üret
#    Slug'larda latinize yazar adı var (örn. 'agrippa', 'ficino').
#    Bilinen kanonik adlar için düzeltme tablosu; gerisi slug'dan türetilir.
# ------------------------------------------------------------------
KANONIK = {
    "agrippa": "Heinrich Cornelius Agrippa",
    "ficino": "Marsilio Ficino",
    "picatrix": "Picatrix Ghayat al-Hakim",
    "corpus-hermeticum": "Corpus Hermeticum",
    "hermes": "Hermes Trismegistus",
    "paracelsus": "Paracelsus",
    "pico": "Pico della Mirandola",
    "batlamyus": "Ptolemy Tetrabiblos",
    "ptolemaios": "Ptolemy",
    "zohar": "Zohar Kabbalah",
    "sefer-yetzirah": "Sefer Yetzirah",
    "fludd": "Robert Fludd",
    "boehme": "Jacob Boehme",
    "dee": "John Dee Monas",
    "kircher": "Athanasius Kircher",
    "bruno": "Giordano Bruno",
    "reuchlin": "Johannes Reuchlin Kabbalah",
    "trithemius": "Trithemius",
    "lilly": "William Lilly astrology",
    "bonatti": "Guido Bonatti",
    "abu-maser": "Albumasar Abu Ma'shar",
    "kepler": "Kepler astrology Harmonices",
    "steiner": "Rudolf Steiner",
    "levi": "Eliphas Levi",
    "crowley": "Aleister Crowley",
    "blavatsky": "Blavatsky",
    "nag-hammadi": "Nag Hammadi",
    "arbatel": "Arbatel de magia",
    "goetia": "Lesser Key of Solomon Goetia",
    "kyranides": "Kyranides",
    # 11 Ağu düzeltmesi: genel/belirsiz isimler yanlış-pozitif ürettiği için
    # (örn. "john smith" 76.656 yayınla en tepedeydi) veya slug parçalama
    # kişiyi yanlış tanımladığı için (örn. "hugo victor" Victor Hugo sanılmıştı,
    # aslında ortaçağ teologu Hugh of Saint Victor) eklendi.
    "john-smith": "John Smith Cambridge Platonist Select Discourses",
    "fourth-book-occult-philosophy": "Agrippa Fourth Book Occult Philosophy",
    "hugo-victor": "Hugh of Saint Victor",
    "richard-saint-victor": "Richard of Saint Victor Benjamin",
    "richard-of-st-victor": "Richard of Saint Victor Benjamin Minor",
    "saint-martin": "Louis-Claude de Saint-Martin",
    "henry-more": "Henry More Cambridge Platonist",
    "thomas-taylor": "Thomas Taylor Platonist translator",
    "della-porta": "Giambattista della Porta Magia Naturalis",
}

def sorgu_uret(slug: str, baslik: str, koleksiyon: str) -> str:
    """Eser için OpenAIRE keywords sorgusu üret."""
    for anahtar, kanonik in KANONIK.items():
        if anahtar in slug:
            return kanonik
    # geri dönüş: slug'ın ilk iki anlamlı parçası + koleksiyonun İngilizce karşılığı
    parcalar = [p for p in slug.split("-") if len(p) > 3][:2]
    return " ".join(parcalar)

# ------------------------------------------------------------------
# 2. ADIM: OpenAIRE Graph sorgusu
# ------------------------------------------------------------------
def graf_yogunlugu(sorgu: str) -> int:
    """OpenAIRE Graph'te sorguya düşen yayın sayısı."""
    url = f"{BASE}?format=json&size=0&keywords={urllib.parse.quote(sorgu)}"
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return int(json.load(r)["response"]["header"]["total"]["$"])
    except Exception as e:
        print(f"  ! sorgu hatası ({sorgu}): {e}", file=sys.stderr)
        return -1

# ------------------------------------------------------------------
# 3. ADIM: boşluk skoru
#    erişilebilirlik: metin Kadim Kütüphane'de varsa Türkçe erişilebilir = 1
#    skor: graf yoğunluğu — Türkçesi olmayan ama talebi yüksek eserler
#    (katalog dışı adaylar için); katalog içi eserler 'çevrildi' işaretlenir
# ------------------------------------------------------------------
def skorla(yogunluk: int, katalogda: bool) -> float:
    if yogunluk <= 0:
        return 0.0
    erisilebilirlik = 1.0 if katalogda else 0.0
    return round(yogunluk * (1 - erisilebilirlik), 1)

# ------------------------------------------------------------------
def main():
    demo = "--demo" in sys.argv
    top = None
    for a in sys.argv:
        if a.startswith("--top"):
            top = int(sys.argv[sys.argv.index(a) + 1])

    katalog_yolu = Path(__file__).parent / "kaynak_katalog.csv"
    with open(katalog_yolu, encoding="utf-8") as f:
        katalog = list(csv.DictReader(f))

    if demo:
        bilinen = [x for x in katalog if any(k in x["slug"] for k in KANONIK)]
        katalog = bilinen[:8]
    elif top:
        katalog = katalog[:top]

    sonuclar = []
    for i, eser in enumerate(katalog, 1):
        sorgu = sorgu_uret(eser["slug"], eser["baslik"], eser["koleksiyon"])
        y = graf_yogunlugu(sorgu)
        sonuc = {
            "slug": eser["slug"], "baslik": eser["baslik"],
            "koleksiyon": eser["koleksiyon"], "graf_sorgusu": sorgu,
            "graf_yogunlugu": y, "katalogda": True,
            "bosluk_skoru": skorla(y, katalogda=True),
        }
        sonuclar.append(sonuc)
        print(f"[{i}/{len(katalog)}] {eser['baslik'][:45]:<47} → {sorgu[:30]:<32} {y:>6} yayın")
        time.sleep(GECIKME)

    cikti = Path(__file__).parent / "atlas-veri.json"
    with open(cikti, "w", encoding="utf-8") as f:
        json.dump({"olcum_tarihi": time.strftime("%Y-%m-%d"),
                   "eser_sayisi": len(sonuclar), "eserler": sonuclar},
                  f, ensure_ascii=False, indent=1)
    print(f"\n✓ {cikti.name} yazıldı ({len(sonuclar)} eser)")

if __name__ == "__main__":
    main()
