# Phase 1 — Research actual outbound/return transportation, lodging and arrival/departure logistics

Read `request.json`, `PROJECT.md`, installed Periplus SKILL and source rules. Automatically search fresh, primary sources, do not merely restate request.

1. Preserve `journey.outbound.origin` as the true journey START and `journey.return.destination` as the true journey END. They need not match, and may be different countries; never replace the final return endpoint with the outbound origin. Resolve the user’s actual `journey.outbound` and `journey.return` mode(s) FOR THE APPLICABLE DATE: flight numbers/airport terminals when flying; railway/train/platforms when by rail; bus stops, ferry ports, road routing or multimodal transfer details as appropriate. Validate service/route numbers where given and respect user-supplied reservation status; never assume flying. Handle arrival-date shifts and local timezones.
2. Research actual arrival terminal/station/port/parking → main-destination hotel/base (and reverse), with actual operators, fare bands, boarding stations, likely transfer, earliest/last service, walking/exits, and weather/luggage contingencies. Do not assert live timetables based solely on general route articles.
3. If `request.hotel` is supplied, research and honor its actual location, check-in/check-out, local spelling and access. Only if there is no supplied hotel, compare 2–3 logical neighborhoods and 2–3 accommodation choices without invented prices or availability; choose tentative best base for day-trip planning. Do not claim any reservation.
4. Research relevant travel restrictions, holiday and seasonal factors for the date window, and record operational sources and access dates.
5. Save detailed evidence-backed prose to `research/01_operations.md` (minimum 1200 meaningful Chinese characters or equivalent, unless actual destination is extremely constrained). Write timestamped URL entries into `research/EVIDENCE_LEDGER.md`. Keep source links near claims in notes.
6. If online research capability is unavailable, write `research/RESEARCH_BLOCKER.md` specifying which capability must be enabled and DO NOT invent facts. Do not mark phase complete when blocked.

Required deliverable this phase: `research/01_operations.md` containing actual outbound/return mode and service facts, reservation status, door-to-door options, supplied hotel details or clearly unbooked alternatives, and citations.


## Mandatory language-independent input, multilingual names and legacy layout

Accept traveler input in any language, including Chinese; never demand an English prompt. Generate narration in `request.json` customization.language, defaulting to Simplified Chinese (`zh-CN`). Give every important place, attraction, station, line, hotel and restaurant Chinese and English names. In Japan, also provide original Japanese script, verified kana and Hepburn romanization, with usable show-to-staff name cards. Apply `references/multilingual_names_and_pronunciation.md`. Use the three historical brochures for cover, header, footer and genuine three-level paginated TOC format only; research all current facts and fares independently. Apply `references/legacy_layout_contract.md`. Include names in the main body and route directions, not only an appendix. Keep this skill and every bundled example in English; this documentation policy does not change input/output language support.


### Permanent travel and visuals requirements

Read `request.journey.outbound/return` (modes may be flight, rail, bus, ferry, drive, mixed, other) and `request.hotel` when supplied. Do not assume flights or airports. Identify arrival/departure terminals/vehicles/road nodes appropriate to the actual modes; include accurate hotel transfer instructions. Open `references/media_acquisition_and_maps.md`; research legally reusable real photographic sources and real map assets, with provenance and image rights. Start `research/MEDIA_MANIFEST.json`, downloads into `photos/` / `maps/` during normal execution.

## Current reader and validation contract

Read `references/reader_contract.md`, `references/service_selection.md` and `references/kobe_reference_contract.md`. Apply attached-reference presentation choices and latest explicit instructions. Keep process reasoning in research, use destination-only Around Area titles, make Tours experiential, and put passes/combined discounts rather than budgets in Tickets & Prices. Every venue card (attraction, shopping, dining, hotel, including nested venues) needs its own real photo and catalogue/marker association; never satisfy this with aggregate counts. Hotel photo and access map are separate requirements. Maintain ENTRY_CATALOGUE and TRANSPORT_PLAN; validate all entries, preceding-activity buffers and concrete service recommendations.


## Date periods and final filenames

Read `references/filename_and_date_periods.md`. Preserve all `date_ranges` (any count); arrange only their inclusive active days, never gap days. Enrich verified `country_en`/`destination_en` without extra traveler input. Write actual DOCX/PDF basenames as `YYYY.Country.City.MMDD-MMDD[.MMDD-MMDD…]`, every period retained and ASCII English only; use the documented full-year variant across years. Keep internal manuscript filename stable.
