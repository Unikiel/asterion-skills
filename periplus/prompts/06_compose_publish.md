# Phase 6 — Write the ACTUAL finished Seven Ninths Travel Brochure

This is a full-writing phase, not a scaffold phase. Read all existing research files and the full Seven Ninths master structure. Compose `exports/Seven_Ninths_Travel_Brochure.md` as a polished, publication-ready, continuous, comprehensive travel guide in the requested language.

Preserve all top-level sections, in order:
1. Do NOT manually author a cover or Content/TOC in the Markdown manuscript: the DOCX/PDF exporter creates the legacy cover and a real three-level page-numbered clickable Content section;
2. Arrival & Departure (actual outbound and return mode(s), flight only when applicable, station/port/terminal transfer and hotel access);
3. Accommodation (booked or clearly recommended);
4. Brief Sketch (full researched country/city history, geography, population, politics, economy, education, language, culture, transport, etc);
5. Attractions & Schedule (Area Maps and every travel date schedule);
6. Sightseeing & Adventure (detailed primary destination catalogue, qualified Around Area day trips, Tours);
7. Delicacy & Shopping (restaurants/cafés and markets/stores);
8. Recommends & Tips (Tourist Travel Pass & Ticket, Tourist Center, Tickets & Prices, Practical Information, Currency, Embassy, Important Numbers, Useful links);
9. Source bibliography and any discreet dated verification caveats.

DO NOT just copy the master skeleton into the published output! Remove all bracket placeholders, TODOs, instructional metadata and dummy lists. Write actual factual paragraphs for every applicable chapter, tables only for genuinely tabular material, and complete substantive entries for each recommended attraction, dining/retail venue and excursion. Retain Japanese/local names. Provide source links with time-sensitive claims; NEVER substitute bare hyperlinks for real photographs or maps. Embed downloaded, legally reusable genuine JPEG/PNG photographs from `photos/` and actual geographic map images from `maps/` using local-file Markdown image syntax and captions/credits; require complete research/MEDIA_MANIFEST.json. If missing, report blockers and do not mark FINAL.

This should read like the user's substantial Nagoya/Kobe/Tokyo compendia, not a thin one-page itinerary. For large destinations, draft over multiple writing passes to avoid truncation—preserve and extend existing prose rather than leaving sections empty. Never mark brochure complete simply because the file exists.

After writing, create `research/QUALITY_REPORT.md` with completeness-by-section, source/freshness audit, explicit limitations and outstanding booking checks. Set project status to `DRAFT_REVIEW` until Phase 7 succeeds. DOCX and PDF are mandatory default publication outputs. Finish the substantive Markdown manuscript first; after Phase 7 the runner calls export_brochure.py and checks the brand header on every page. Never treat Markdown as the default deliverable or claim output without rendering.


## Mandatory language-independent input, multilingual names and legacy layout

Accept traveler input in any language, including Chinese; never demand an English prompt. Generate narration in `request.json` customization.language, defaulting to Simplified Chinese (`zh-CN`). Give every important place, attraction, station, line, hotel and restaurant Chinese and English names. In Japan, also provide original Japanese script, verified kana and Hepburn romanization, with usable show-to-staff name cards. Apply `references/multilingual_names_and_pronunciation.md`. Use the three historical brochures for cover, header, footer and genuine three-level paginated TOC format only; research all current facts and fares independently. Apply `references/legacy_layout_contract.md`. Include names in the main body and route directions, not only an appendix. Keep this skill and every bundled example in English; this documentation policy does not change input/output language support.


**Before publication:** read `research/NAME_INDEX.md`, expand the names within the body itself (not only in an appendix); provide usable local-language show-to-staff names and verified pronunciations.

### Publication handoff contract

Write only the substantive body and chapter headings in Markdown. Do not author `# COVER`, `# Content`, manual contents, dotted leaders or page numbers, and do not copy asset template placeholders. `scripts/export_brochure.py` creates the cover and three-level paginated TOC from request.json. Preserve verified multilingual names and pronunciations in the body for the publisher.


### Final-format mandatory layout tests

- `Heading 1` AND `Heading 2` each starts a new printed page, even if adjacent to previous heading; include meaningful section introduction to avoid title-only pages.
- Use **Oswald** for ALL western/English text in headings, paragraphs, the running header, cover and the three-level TOC, with readable CJK font for Chinese/Japanese and real-PDF font verification (not substituted).
- `Content` is the three-level clickable table of contents with actual verified page numbers; running header exact `Seven Ninths Travel Brochure`.
- Photos and maps **MUST physically appear** in both DOCX/PDF. Real media must be documented with source, photographer/creator, license and caption. External-only links, generated decorative images, blank maps are blockers.
- Hotel in request is treated as confirmed only when status=booked; hotel recommendation only if not specified. Outbound and return modes need not be flights.

## Current reader and validation contract

Read `references/reader_contract.md`, `references/service_selection.md` and `references/kobe_reference_contract.md`. Apply attached-reference presentation choices and latest explicit instructions. Keep process reasoning in research, use destination-only Around Area titles, make Tours experiential, and put passes/combined discounts rather than budgets in Tickets & Prices. Every venue card (attraction, shopping, dining, hotel, including nested venues) needs its own real photo and catalogue/marker association; never satisfy this with aggregate counts. Hotel photo and access map are separate requirements. Maintain ENTRY_CATALOGUE and TRANSPORT_PLAN; validate all entries, preceding-activity buffers and concrete service recommendations.


## Date periods and final filenames

Read `references/filename_and_date_periods.md`. Preserve all `date_ranges` (any count); arrange only their inclusive active days, never gap days. Enrich verified `country_en`/`destination_en` without extra traveler input. Write actual DOCX/PDF basenames as `YYYY.Country.City.MMDD-MMDD[.MMDD-MMDD…]`, every period retained and ASCII English only; use the documented full-year variant across years. Keep internal manuscript filename stable.
