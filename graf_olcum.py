#!/usr/bin/env python3
"""OpenAIRE Graph: ezoterizm alanlarinda dil dagilimi olcumu."""
import json, time, urllib.request, urllib.parse
from collections import Counter

BASE = "https://api.openaire.eu/search/publications"

def fetch_total(kw):
    url = f"{BASE}?format=json&size=0&keywords={urllib.parse.quote(kw)}"
    with urllib.request.urlopen(url, timeout=30) as r:
        return int(json.load(r)["response"]["header"]["total"]["$"])

def lang_of(md):
    l = md.get("language")
    if isinstance(l, dict):
        return l.get("@classname") or "Undetermined"
    if isinstance(l, list):
        return l[0].get("@classname", "Undetermined") if l and isinstance(l[0], dict) else "Undetermined"
    return l or "Undetermined"

def fetch_langs(kw, cap=1000):
    """Dil dagilimini say; cap kadar kayit tara."""
    total = fetch_total(kw)
    n = min(total, cap)
    counts, got = Counter(), 0
    page = 1
    while got < n:
        size = min(100, n - got)
        url = f"{BASE}?format=json&size={size}&page={page}&keywords={urllib.parse.quote(kw)}"
        with urllib.request.urlopen(url, timeout=30) as r:
            d = json.load(r)
        res = d["response"].get("results", {}).get("result")
        if not res:
            break
        items = res if isinstance(res, list) else [res]
        for it in items:
            md = it.get("metadata", {}).get("oaf:entity", {}).get("oaf:result", {})
            counts[lang_of(md)] += 1
        got += len(items)
        page += 1
        time.sleep(0.4)
    return total, got, counts

SETS = ["western esotericism", "hermetica", "hermeticism", "picatrix",
        "corpus hermeticum", "knights templar", "cornelius agrippa",
        "gnosticism", "alchemy"]

print(f"{'konu':<22}{'toplam':>8}{'taranan':>9}{'TR':>5}{'TR%':>7}  ilk-3 dil")
out = {}
for kw in SETS:
    total, got, counts = fetch_langs(kw)
    tr = counts.get("Turkish", 0)
    pct = (tr / got * 100) if got else 0
    top3 = ", ".join(f"{l}:{c}" for l, c in counts.most_common(3))
    print(f"{kw:<22}{total:>8}{got:>9}{tr:>5}{pct:>6.2f}%  {top3}")
    out[kw] = {"total": total, "scanned": got, "turkish": tr,
               "langs": dict(counts.most_common(10))}

with open("graf_olcum_sonuc.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print("\nkaydedildi: graf_olcum_sonuc.json")
