# Phase 2 — Build encyclopedic Brief Sketch

Read request, research/01_operations.md, all coverage and content specifications in the installed skill. Search authoritative sources; no filler or skeletal bullet-only text.

Write `research/02_destination_compendium.md` as a real substantial chapter of the finished guide. Keep meaningful hierarchy:
- Brief Sketch with city orientation and destination boundaries;
- History (organized by meaningful eras and dated inflection points);
- Geography / Administrative Region / Climate / Population / Religion / Politics;
- Economy (primary/secondary/tertiary industries) / Education;
- Culture, Language & Dialect, Localism, Travel, Literature & Art, Art & Craft, Architecture, Museum, Events & Festivals, Delicacy & Diet & Cuisine, Media, Sports, Subculture;
- Transportation: national and local rail, metro, buses, roads/highway, ports/ferries, airports and international exchange when pertinent.

Use actual names, substantive history/background, meaningful context, contemporary corrections, relevant photo/architecture/museum knowledge. Organize on the template taxonomy and make cross references. Look beyond the user's chosen short itinerary—the brochure doubles as a reference encyclopedia. Avoid stale political incumbents and unsupported rankings. Every time-sensitive statistic is dated and sourced. Append source URLs + retrieval dates to `research/EVIDENCE_LEDGER.md`. Target high detail (several thousand Chinese characters). Preserve all relevant categories; for nonexistent facilities say why.

Required output: `research/02_destination_compendium.md`; not a table of contents.


## Mandatory language-independent input, multilingual names and legacy layout

Accept traveler input in any language, including Chinese; never demand an English prompt. Generate narration in `request.json` customization.language, defaulting to Simplified Chinese (`zh-CN`). Give every important place, attraction, station, line, hotel and restaurant English-first, then Chinese (where available) titles; use Simplified Chinese for main narrative. In Japan, also provide original Japanese script, verified kana and Hepburn romanization, with usable show-to-staff name cards. Apply `references/multilingual_names_and_pronunciation.md`. Use the three historical brochures for cover, header, footer and genuine three-level paginated TOC format only; research all current facts and fares independently. Apply `references/legacy_layout_contract.md`. Include names in the main body and route directions, not only an appendix. Keep this skill and every bundled example in English; this documentation policy does not change input/output language support.


Source and acquire representative real photos (city, museums, architecture) with verified publication rights. Save actual JPEG/PNG images, register every asset in `MEDIA_MANIFEST.json`, and embed/credit photos in researched notes. Images must not be links only.

## Current reader and validation contract

Read `references/reader_contract.md`, `references/service_selection.md` and `references/kobe_reference_contract.md`. Apply attached-reference presentation choices and latest explicit instructions. Keep process reasoning in research, use destination-only Around Area titles, make Tours experiential, and put passes/combined discounts rather than budgets in Tickets & Prices. Every venue card (attraction, shopping, dining, hotel, including nested venues) needs its own real photo and catalogue/marker association; never satisfy this with aggregate counts. Hotel photo and access map are separate requirements. Maintain ENTRY_CATALOGUE and TRANSPORT_PLAN; validate all entries, preceding-activity buffers and concrete service recommendations.


## Date periods and final filenames

Read `references/filename_and_date_periods.md`. Preserve all `date_ranges` (any count); arrange only their inclusive active days, never gap days. Enrich verified `country_en`/`destination_en` without extra traveler input. Write actual DOCX/PDF basenames as `YYYY.Country.City.MMDD-MMDD[.MMDD-MMDD…]`, every period retained and ASCII English only; use the documented full-year variant across years. Keep internal manuscript filename stable.

**Immutable v2.7.0 publication contract:** Follow `references/immutable_skeleton_contract.md`. Preserve every fixed Master Skeleton section name and depth without rewriting, combining or dropping topics. `Around Area` is the approved correction. Bilingual titles must be English first, Chinese second when present; narrative remains Simplified Chinese by default. Keep ALL internal reasoning, compliance, QA and author commentary out of the traveler-facing manuscript; write them in research notes only. Entry-by-entry genuine embedded photographs are mandatory for each attraction, nested venue, restaurant, cafe, bar, shop, market and hotel. Run `scripts/skeleton_audit.py` and the full media gate before marking FINAL.
