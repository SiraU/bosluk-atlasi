# Boşluk Atlası / Translation-Gap Atlas

**OpenAIRE AI Hackathon 2026 — Theme B (Build)**

A small, reproducible tool that measures where a Turkish-language open-access primary-source
library ([Kadim Kütüphane](https://kadimkutuphane.com), 844 translated texts of the Western
esoteric tradition — Hermetica, Picatrix, alchemical and Kabbalistic sources, Templar
material, etc.) sits inside the international OpenAIRE Graph, and how visible Turkish-language
scholarship is around each of those texts.

**Live result:** https://kadimkutuphane.com/gap-atlas (English) · https://kadimkutuphane.com/bosluk-atlasi (Turkish)

## The idea

```
gap_score(work, language) = graph_density(work) × (1 − accessibility(work, language))
```

For each of the 844 works, we build a disambiguated OpenAIRE `keywords` query identifying the
work/author unambiguously (e.g. *"Agrippa Fourth Book Occult Philosophy"*, not the raw Turkish
slug fragments the query would otherwise be built from), measure how many publications the
OpenAIRE Graph returns for it, and combine that with a topic-level heat map of Turkish-language
representation across nine esotericism-adjacent research clusters (alchemy, gnosticism,
hermeticism, Knights Templar, etc.).

**The loop:** graph measures the gap → library translates the text → the openly licensed
translation (CC BY 4.0, some CC BY-SA 4.0) is deposited on Zenodo with a DOI → the graph
re-measures and the gap (in principle) narrows.
144 translations are already live on Zenodo (as of 18 August 2026) as a first proof of this loop.

## Repository contents

| File | Purpose |
|---|---|
| `kaynak_katalog.csv` | Catalogue of the 844 translated works (slug, title, collection) |
| `atlas_betigi.py` | Core script: builds a query for each work, queries the OpenAIRE Graph, computes the gap score → `atlas-veri.json` |
| `graf_olcum.py` | Topic-level heat map: language distribution across 9 esotericism research clusters → `graf_olcum_sonuc.json` |
| `kapsanmayan_eserler.csv` | The ~687 works whose auto-generated query needed manual/LLM-assisted disambiguation |
| `uygula_yeni_sorgular.py` | Applies the corrected queries to `atlas-veri.json` and re-measures |
| `bosluk_atlasi_uret.py` | Generates the Turkish static page (`/bosluk-atlasi`) from `atlas-veri.json` + `graf_olcum_sonuc.json` |
| `gap_atlas_en_uret.py` | Generates the English static page (`/gap-atlas`) from the same data |
| `atlas-veri.json` | Final measured data: per-work OpenAIRE query, density, gap score |
| `graf_olcum_sonuc.json` | Heat-map data: per-cluster totals and language counts |
| `basvuru-taslagi.md` | Submission draft (story, checklist) |
| `mcp_dogrulama.md` | Cross-validation of the public-API results against the Alien AI MCP connector (OpenAIRE Graph API V3) |

## Reproducing

```bash
# 1. Topic-level heat map (9 clusters)
python3 graf_olcum.py

# 2. Full per-work measurement (844 works, ~30–40 min, polite 0.4s delay between calls)
python3 atlas_betigi.py

# 3. Generate the static pages (Turkish + English)
python3 bosluk_atlasi_uret.py
python3 gap_atlas_en_uret.py
```

No API key is required — all measurements use the public OpenAIRE Graph API
(`api.openaire.eu/search/publications`). The generated site is a single static HTML file with
no server-side component and no live API calls at view time, so it works for any evaluator
without setup.

## Data & methodology notes

- OpenAIRE's public search API does not expose a `lang` filter parameter; language distribution
  is counted record-by-record from the returned `language` field (see `graf_olcum.py`).
- ~45% of scanned records have undetermined language metadata; the reported Turkish-language
  gap holds even accounting for that uncertainty (see `basvuru-taslagi.md` §5 for the full
  discussion).
- Query disambiguation for the long tail (687 of 844 works) was done with LLM assistance,
  following explicit rules: never invent an author, prefer internationally recognized titles,
  qualify ambiguous common names (e.g. *"Henry More Cambridge Platonist"*, not just *"Henry
  More"*). `kapsanmayan_eserler.csv` records the original (poor) auto-generated query for
  comparison.

## Alien AI MCP connector

Access to the Alien AI MCP connector was granted on 17 August 2026. The `atlas_betigi.py`
measurements above were built entirely on the public OpenAIRE Graph API before that; after
gaining MCP access, 8 works spanning the density range were re-queried live through the Alien
MCP connector (`openaire-graph-api-v3`, tool `search_5`) using the same query strings, to confirm
the two sources agree. 6 of 8 matched exactly, 2 were close (small positive drift consistent with
continuous re-indexing of the Graph between measurement dates). See `mcp_dogrulama.md` for the
full comparison table and reproduction notes.

## License

All code and data in this repository are released under **CC BY 4.0**. See `LICENSE`.

## Author

Şira Nur Uysal — [Kadim Kütüphane](https://kadimkutuphane.com) · [Kutsala Dönüş](https://kutsaladonus.com)
