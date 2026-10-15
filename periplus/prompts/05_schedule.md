# Phase 5 — Concrete date-aware itinerary with validated logistics

Read request.json, every research/*.md completed so far and all source guidance. Write `research/05_day_by_day_itinerary.md` using actual outward/return travel legs in `journey`, regardless of mode, as first/last-day anchors.

Build:
1. An overview with primary base/hotel proposal vs booked hotel status, map-area legend, daily timeline and ranked must-sees from user customization.
2. Detailed daily plan for **every inclusive travel date**, with times or transparent estimates, travel mode and transfers, stops with meaningful onsite durations, meal and coffee anchors, rest/walking buffers, and return to lodging. Distinguish optional stops. Avoid stacking physically remote areas or excessive walking if user limits it.
3. Respect real closed weekdays, seasonal operating windows and reservation lead times. Do not make a hard-time claim unsupported by source. For attractions requiring entry reservations, provide booking site and mark unbooked.
4. Include bad-weather alternative per day, avoiding long walks when user requests short walking. Recommend qualified Around Area excursions if feasible but keep them optional unless user specified.
5. For arrival and departure, explicitly budget the ACTUAL journey: immigration/security and airport lead time only for relevant international flight segments; railway interchange/platform time for trains, boarding deadlines for ferries/buses, driving or road delays where relevant, plus luggage and hotel check-in. If terminal details are unclear, say exactly what requires reconfirmation.
6. Provide a transit cost comparison where sourced; list useful route/official timetable URLs. Check that no service/route or date conflict exists.

Append any new sources to ledger. End with a practical prioritized reservation/verification checklist—not blank planning questions.


## Mandatory language-independent input, multilingual names and legacy layout

Accept traveler input in any language, including Chinese; never demand an English prompt. Generate narration in `request.json` customization.language, defaulting to Simplified Chinese (`zh-CN`). Give every important place, attraction, station, line, hotel and restaurant English-first, then Chinese (where available) titles; use Simplified Chinese for main narrative. In Japan, also provide original Japanese script, verified kana and Hepburn romanization, with usable show-to-staff name cards. Apply `references/multilingual_names_and_pronunciation.md`. Use the three historical brochures for cover, header, footer and genuine three-level paginated TOC format only; research all current facts and fares independently. Apply `references/legacy_layout_contract.md`. Include names in the main body and route directions, not only an appendix. Keep this skill and every bundled example in English; this documentation policy does not change input/output language support.


Honor the explicitly supplied hotel address/name if present. Do not invent a new hotel base. Include cross-checked real area map images; photo-ready timetables, transit diagrams and physical documents are not replaceable with URLs.

## Current reader and validation contract

Read `references/reader_contract.md`, `references/service_selection.md` and `references/kobe_reference_contract.md`. Apply attached-reference presentation choices and latest explicit instructions. Keep process reasoning in research, use destination-only Around Area titles, make Tours experiential, and put passes/combined discounts rather than budgets in Tickets & Prices. Every venue card (attraction, shopping, dining, hotel, including nested venues) needs its own real photo and catalogue/marker association; never satisfy this with aggregate counts. Hotel photo and access map are separate requirements. Maintain ENTRY_CATALOGUE and TRANSPORT_PLAN; validate all entries, preceding-activity buffers and concrete service recommendations.


## Date periods and final filenames

Read `references/filename_and_date_periods.md`. Preserve all `date_ranges` (any count); arrange only their inclusive active days, never gap days. Enrich verified `country_en`/`destination_en` without extra traveler input. Write actual DOCX/PDF basenames as `YYYY.Country.City.MMDD-MMDD[.MMDD-MMDD…]`, every period retained and ASCII English only; use the documented full-year variant across years. Keep internal manuscript filename stable.

**Immutable v2.6.0 publication contract:** Follow `references/immutable_skeleton_contract.md`. Preserve every fixed Master Skeleton section name and depth without rewriting, combining or dropping topics. `Around Area` is the approved correction. Bilingual titles must be English first, Chinese second when present; narrative remains Simplified Chinese by default. Keep ALL internal reasoning, compliance, QA and author commentary out of the traveler-facing manuscript; write them in research notes only. Entry-by-entry genuine embedded photographs are mandatory for each attraction, nested venue, restaurant, cafe, bar, shop, market and hotel. Run `scripts/skeleton_audit.py` and the full media gate before marking FINAL.
