# Alien MCP Cross-Validation (17 August 2026)

Alien AI MCP connector access was granted on 17 August 2026 (after the public-API measurements in
`atlas-veri.json` were already complete). To validate that the public OpenAIRE Graph API results
used throughout this project match what the Alien MCP connector (`openaire-graph-api-v3`, tool
`search_5`) returns, 8 works spanning the density range (zero / low / high) were re-queried live
through the MCP connector using the exact same `graf_sorgusu` string stored in `atlas-veri.json`.

| Work | Query | Public API (`atlas-veri.json`) | Alien MCP (live, 17 Aug) | Match |
|---|---|---:|---:|---|
| Manetho, Apotelesmatika | `Manetho Apotelesmatica astrology` | 0 | 0 | exact |
| Lucio Bellanti, Defence of Astrology | `Lucio Bellanti defence of astrology against Pico` | 0 | 0 | exact |
| Sahl ibn Bishr, Introduction to Astrology | `Sahl ibn Bishr Introduction to Astrology` | 0 | 0 | exact |
| Al-Qabisi, Introduction to Astrology | `Al-Qabisi Introduction to Astrology` | 3 | 3 | exact |
| Kepler, Harmonices Mundi (astrology) | `Kepler astrology Harmonices` | 3 | 3 | exact |
| Pico della Mirandola, Disputationes | `Pico della Mirandola Disputationes adversus astrologiam` | 13 | 13 | exact |
| Plotinus, Enneads | `Plotinus Enneads` | 600 | 637 | close (+6%, graph snapshot drift) |
| Blavatsky (2 works, shared query) | `Blavatsky` | 446 | 475 | close (+6.5%, graph snapshot drift) |

**Result:** 6 of 8 exact matches, 2 close (small positive drift, consistent with the OpenAIRE
Graph being re-indexed continuously between the original measurement date and 17 August 2026 —
not a methodology discrepancy). This confirms the public-API-based `atlas_betigi.py` pipeline and
the Alien MCP connector query the same underlying Graph and agree on results.

## Reproducing this check

Any of the 844 `graf_sorgusu` values in `atlas-veri.json` can be re-run live through the Alien MCP
connector's `openaire-graph-api-v3` `search_5`/`search` tool (publications search by keyword) —
the same string that `atlas_betigi.py` sends to the public REST API is passed as the `search`
parameter. MCP server used: `https://mcp.alien.club/mcp?config=cfg_9GbZGRTo6PV_` (Alien
Intelligence marketplace, OpenAIRE Graph API V3 connector, 12 tools).
