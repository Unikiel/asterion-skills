# QA and Release Gates

Do not label output **FINAL** unless it passes all relevant gates. The scripts enforce structural/procedural checks only; editorial and factual accuracy still require human/agent review and source validation.

## Date/naming gate

- [ ] Actual final DOCX/PDF basenames follow YYYY.Country.City and every date period, using ASCII English names. Same basename for both; cross-year endpoints remain unambiguous.
- [ ] Any number of date_ranges accepted; no merged gaps, no artificial segment-count limit, no gap-day schedules. Cover and day list reflect actual separated periods.
- [ ] English labels researched when input names are non-English; no generic filename fallback.

## Structural gate

- [ ] `SKILL.md` frontmatter valid; all referenced resources exist.
- [ ] Cover identity, dates/place, real TOC, chapter order.
- [ ] Original main categories covered, including Tokyo-only and Kobe/Nagoya-only categories (or explicitly merged/NA in coverage log).
- [ ] `Sightseeing & Adventure` splits: Main Destination / Around Area / Tours.
- [ ] Canonical Around Area means **same-day out-and-back**; not a main-city alias.
- [ ] Regional maps A… correctly reference corresponding destinations and schedules.
- [ ] Arrival + departure, hotel + transport, food and shopping, passes and tourist offices, important numbers and links accounted for.

## Updated reader contract gate

- [ ] Attached reference inspected for uncertain presentation choices; latest explicit comments override older reference details.
- [ ] Every attraction/nested facility, shop, restaurant/café/bar and hotel has a specific real photo in its own card; catalogue, markers and photo IDs reconcile against all venues in tables/prose. Hotel access map is additional.
- [ ] Missing service numbers result in actual researched dated primary and backup services, after predecessor/immigration/baggage/terminal/boarding margins. No broad timetable window substitutes for a published actual service.
- [ ] All sensible transport modes considered; show three or more useful alternatives where available, no invented mode padding. TRANSPORT_PLAN arithmetic and source applicability checked.
- [ ] No internal reasoning/compliance monologues; Around Area titles are only destinations/themes.
- [ ] Tours explain distinctive activities/experience/participation. Tickets & Prices lists transport/attraction passes, combinations and discounts, no budgets.
- [ ] Accommodation is a factual, illustrated hotel card with contact/access, no default daily-routine filler.
- [ ] Each photo/caption/heading placement checked after rendering; no orphan captions, distorted images, split rows or unreadable maps.

## Operational gate

- [ ] Incoming/return transit modes, terminals, station exits, real travel duration, realistic interchange and luggage allowances.
- [ ] `journey.outbound.origin` identifies the journey starting point and `journey.return.destination` identifies the final return endpoint; these may differ and must not automatically be set to the same value.
- [ ] Each Around Area entry independently has outbound and return route and enough visiting time, with same-day return verified if claimed.
- [ ] Venue hours/closure days and ticket prices are relevant to chosen dates and cited.
- [ ] Weather, disruption and alternative plans.
- [ ] No invented departure times, local maps, reservation links or live availability.

## Evidence gate

- [ ] User plans differentiated from real bookings.
- [ ] Historical sources not treated as up-to-date logistics.
- [ ] Provenance / checked dates stored in evidence ledger.
- [ ] Photographs/maps licensed or user-provided with appropriate attribution.
- [ ] Nothing sensitive copied from ticket/booking paperwork to publicly distributable example.

## Editorial gate

- [ ] No template markers (`[Attraction 1]`, TODO, TBD etc.) remaining in final publication.
- [ ] Proper local-language place names and unambiguous region/station identity.
- [ ] Descriptions informative, not repeated stock boilerplate.
- [ ] Source references functional; clear map/ticket/restaurant data.
- [ ] Date, time, currency symbols and units consistent.
- [ ] Default DOCX + PDF deliverables generated and independently checked. PDF actually uses Oswald for English letters, numerals, cover, TOC and header; corresponding DOCX Latin styles declare Oswald. CJK characters are legible and uncorrupted.
- [ ] `PROJECT.md`/`TASKS.md` accurately reflect outstanding tasks and verified status.

## Release classification

- `SCAFFOLD`: an initialized file and task structure, NOT a finished guide.
- `DRAFT`: substantive content underway; unverified operational details explicitly labeled.
- `RESEARCH-COMPLETE`: content and ledger populated; must still pass review.
- `FINAL`: editorial and operational gates passed and deliverables verified.

Never turn scaffold/draft validator success into a claim that train times or tickets are factually confirmed.


## Multilingual labels and three-level contents (mandatory)

Requests may use any language, including Chinese; guide narrative defaults to Simplified Chinese. Every important place, attraction, transport station and route needs Chinese + English. Japanese destinations also need original Japanese names, verified kana pronunciation and romanization; never invent unverified readings. See `multilingual_names_and_pronunciation.md`. Final DOCX/PDF contents require Heading 1-3, actual page numbers and clickable links; see `legacy_layout_contract.md`. The English language of skill documentation and examples does not change generated-guide defaults.


## Four permanent operational gates

- [ ] Arrival & Departure reflect ACTUAL outbound + return modes; flight is optional. Rail/coach/ferry/driving/mixed segments must be properly planned.
- [ ] If `hotel` is supplied, brochure contains the exact provided name/address and hotel-to-terminal directions; if missing, recommendations are UNBOOKED.
- [ ] Actual licensed/source-backed photographs and actual geographic map images in both DOCX/PDF, not just hyperlinks. `MEDIA_MANIFEST.json` complete and physical DOCX/PDF image audit passed.
- [ ] Each Heading 1 starts a new chapter page. Headings 2 and 3 flow naturally as in the Kobe reference; verify no orphaned headings or forced blank space.

## Mandatory map and final-link audit

Verify every map is an authentic Google Maps browser screenshot at native high resolution, with readable final-size labels and unaltered visible attribution. Confirm capture metadata against actual image dimensions; downloaded low-resolution maps and artificial upscaling fail. Check final References/Bibliography links for destination and Around Area travel relevance. Remove image-only sources, direct media, repositories, license pages and production tools from the final link list; retain required image credits nearby and complete media provenance internally.
