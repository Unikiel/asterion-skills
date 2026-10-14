# Phase 3 — Full individual attraction catalogue + qualified Around Area excursions

Read all prior phases and the Around Area contract and itinerary engine. Use official/local source research and nearby maps. Write a detailed `research/03_attractions_and_around_area.md`.

A. **Primary destination**: research a broad catalogue spanning central areas and outer districts, not just planned day's stops. For each actual named place include localized official name, relevant historical/architectural/cultural reason, location, typical visit duration, opening windows/closed dates where sourceable, fare when sourceable, access via rail/bus + nearby station, reservation notes, seasonal/weather notes and photography. Include sites suitable for user's explicit interests. Mark missing live facts precisely (do not fill placeholders). Do not duplicate major landmarks under multiple categories.
B. **Area maps**: create an annotated geographic grouping Map A / Map B / ... with named neighborhoods, ground locators (station/address), and links to verified map or directions sources; MUST obtain REAL map assets and download/save them in `maps/`, at least one geographically accurate map image for every Map A/B/... chapter, with verifiable provenance and license/OSM attribution in `research/MEDIA_MANIFEST.json`. Map links alone do not fulfill the output. If map acquisition is blocked, report blocker rather than claim completion.
C. **Around Area** is *a different locality visited on a one-day round trip from the principal city/base, returning same calendar day*. Each candidate must include outbound route and realistic departure, on-site visits/time, return service/window, total travel burden and contingency. Classify recommended / possible with constraints / rejected (overnight). Do not use the principal city as Around Area subheading; never imply nearby simply means one-direction journey time is short. Inspect last trains and seasonality.
D. Special Tours (themes, events, festivals, seasonal strolls, accessible photo routes) separately from Around Area city excursions.

Scale catalogue to destination complexity: major Japanese metro often dozens of detailed sites, multiple districts and multiple vetted day trips. Source all practical data with URL+access date in evidence ledger.


## Mandatory language-independent input, multilingual names and legacy layout

Accept traveler input in any language, including Chinese; never demand an English prompt. Generate narration in `request.json` customization.language, defaulting to Simplified Chinese (`zh-CN`). Give every important place, attraction, station, line, hotel and restaurant Chinese and English names. In Japan, also provide original Japanese script, verified kana and Hepburn romanization, with usable show-to-staff name cards. Apply `references/multilingual_names_and_pronunciation.md`. Use the three historical brochures for cover, header, footer and genuine three-level paginated TOC format only; research all current facts and fares independently. Apply `references/legacy_layout_contract.md`. Include names in the main body and route directions, not only an appendix. Keep this skill and every bundled example in English; this documentation policy does not change input/output language support.


**Additional mandatory index:** write `research/NAME_INDEX.md` as a structured all-major-places index, one row for each venue/destination/station/interchange/route (including the main city and each Around Area). Columns: category; Chinese name; English name (official or explanatory); local native name; Japanese kana/other verified phonetic reading; romaji/transliteration; location/short address; source URL; verification status. Every name included in the brochure must be consistently represented, no guessed reading.


**Photographs mandatory:** obtain genuine site photos with verified attribution/usage rights into `photos/`, not just hyperlinks. Caption every figure in Chinese/English and Japanese/local where necessary. Add real local-file Markdown image tags such as `![...](../photos/...)`; every Map A/B/... section must display an actual `![...](../maps/...)`. Minimum photos: 3 (up to 3 days), otherwise 6. Minimum maps: 1 (up to 3 days), otherwise 2. Every referenced file must be in `MEDIA_MANIFEST.json` with creator, license, source_url, attribution and subject.

## Current reader and validation contract

Read `references/reader_contract.md`, `references/service_selection.md` and `references/kobe_reference_contract.md`. Apply attached-reference presentation choices and latest explicit instructions. Keep process reasoning in research, use destination-only Around Area titles, make Tours experiential, and put passes/combined discounts rather than budgets in Tickets & Prices. Every venue card (attraction, shopping, dining, hotel, including nested venues) needs its own real photo and catalogue/marker association; never satisfy this with aggregate counts. Hotel photo and access map are separate requirements. Maintain ENTRY_CATALOGUE and TRANSPORT_PLAN; validate all entries, preceding-activity buffers and concrete service recommendations.


## Date periods and final filenames

Read `references/filename_and_date_periods.md`. Preserve all `date_ranges` (any count); arrange only their inclusive active days, never gap days. Enrich verified `country_en`/`destination_en` without extra traveler input. Write actual DOCX/PDF basenames as `YYYY.Country.City.MMDD-MMDD[.MMDD-MMDD…]`, every period retained and ASCII English only; use the documented full-year variant across years. Keep internal manuscript filename stable.
