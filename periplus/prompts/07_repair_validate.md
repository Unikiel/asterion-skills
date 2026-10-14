# Phase 7 — Publication quality gate

Read `research/QUALITY_REPORT.md`, `request.json`, `exports/Seven_Ninths_Travel_Brochure.md`, and original source coverage matrix. Execute `python ABSOLUTE_SKILL_PATH/scripts/validate.py --project . --mode final` (resolve absolute Skill path from invocation). If failing, FIX the actual brochure/research immediately, then rerun. Do not evade validation by weakening requirements or deleting needed categories.

Check full itinerary date coverage, actual outbound/return mode-specific itineraries (not necessarily flights), lodging status, all main headings, real Around Area day-trip status, historical source vs current verified sources, enough genuine and unique named attractions, captions/maps source references, local names and no prompts/placeholders left. Check all departure and same-day-return time windows against verified dates where possible. When legitimate limitations remain (e.g. schedule not yet published), label them precisely and update `research/QUALITY_REPORT.md`.

Finish only after publication quality review. `project.json` may be set to `"release_status":"FINAL"` only if final audit passes. Maintain `TASKS.md` with real completion marks. The wrapper also runs local structural validation and must not print false success.


Release gate: default requested formats are DOCX and PDF, with running header `Seven Ninths Travel Brochure`. The execution wrapper performs the actual conversion after agent phases. Ensure text is complete before conversion.


## Mandatory language-independent input, multilingual names and legacy layout

Accept traveler input in any language, including Chinese; never demand an English prompt. Generate narration in `request.json` customization.language, defaulting to Simplified Chinese (`zh-CN`). Give every important place, attraction, station, line, hotel and restaurant Chinese and English names. In Japan, also provide original Japanese script, verified kana and Hepburn romanization, with usable show-to-staff name cards. Apply `references/multilingual_names_and_pronunciation.md`. Use the three historical brochures for cover, header, footer and genuine three-level paginated TOC format only; research all current facts and fares independently. Apply `references/legacy_layout_contract.md`. Include names in the main body and route directions, not only an appendix. Keep this skill and every bundled example in English; this documentation policy does not change input/output language support.


**Check localized names:** use `research/NAME_INDEX.md` to verify Chinese+English each major place, with Japanese original+verified kana+romaji in Japan, along with proofread pages and functioning 3-level TOC. Do not pass review if columns are incomplete or main guide does not show the same labels.


### Hard media/pagination gates

Verify all real photo/map files exist in `photos/` / `maps/`, match provenance/rights in `research/MEDIA_MANIFEST.json`, and are actually referenced inline (not URLs) in output. Each `Map A/B/...` has corresponding real map illustration. Verify docx and pdf contain embedded raster media, not only links. Every printed H1 and H2 must start fresh page. Validate supplied hotel and mode-agnostic outbound/return routes. No FINAL unless these pass.

## Current reader and validation contract

Read `references/reader_contract.md`, `references/service_selection.md` and `references/kobe_reference_contract.md`. Apply attached-reference presentation choices and latest explicit instructions. Keep process reasoning in research, use destination-only Around Area titles, make Tours experiential, and put passes/combined discounts rather than budgets in Tickets & Prices. Every venue card (attraction, shopping, dining, hotel, including nested venues) needs its own real photo and catalogue/marker association; never satisfy this with aggregate counts. Hotel photo and access map are separate requirements. Maintain ENTRY_CATALOGUE and TRANSPORT_PLAN; validate all entries, preceding-activity buffers and concrete service recommendations.


## Date periods and final filenames

Read `references/filename_and_date_periods.md`. Preserve all `date_ranges` (any count); arrange only their inclusive active days, never gap days. Enrich verified `country_en`/`destination_en` without extra traveler input. Write actual DOCX/PDF basenames as `YYYY.Country.City.MMDD-MMDD[.MMDD-MMDD…]`, every period retained and ASCII English only; use the documented full-year variant across years. Keep internal manuscript filename stable.
