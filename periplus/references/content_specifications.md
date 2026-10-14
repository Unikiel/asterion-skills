# Content Contracts and Section Coverage

Full taxonomic skeleton: `../assets/Seven_Ninths_Master_Skeleton.md`.

## Mandatory publication spine (order)

1. Cover, date scope, Contents
2. Arrival & Departure (arrival transfer, return transfer, flights where relevant)
3. Accommodation (contact, exact access, hotel arrival instructions)
4. Brief Sketch (history, geography, climate, demography, religion, politics, economy, education, culture, transportation)
5. Attractions & Schedule (area maps + day/visit plan)
6. Sightseeing & Adventure (main city, **Around Area qualified day trips**, Tours)
7. Delicacy & Shopping (Restaurants & Cafés & Bars; Supermarkets & Stores & Markets)
8. Recommends & Tips (Tourist passes/tickets and tourist centers; practical information; emergency contacts; authoritative links)

## Topic completeness within Brief Sketch

- History: meaningful local historical periods and influences; explain why today’s city looks as it does.
- Geography: landscape, region divisions, weather/climate, seasonal implications and geography-based routing.
- Administrative Region: municipality/prefecture/wards/neighborhoods as appropriate.
- Population: anchored to a year and source (no undated demographic claims).
- Religion: historic shrine/temple/institution and practices where relevant.
- Politics: institutional explanation and dated current officeholders if included.
- Economy: primary/secondary/tertiary industries, identifying local specializations.
- Education: universities, research institutions and connections to city history.
- Culture: language/dialect, localism, travel, literature, art & craft, architecture, museums, events & festivals, food, media, sports and subculture.
- Transportation: public transport, railway/subway, bus, roads/highway, port/ferry and airport as relevant, international exchange where sourced/pertinent.

When a topic has little local relevance, mark `Not applicable — [specific reason]` in the internal coverage audit; do not delete the category from the inherited reference taxonomy. In published prose, avoid pointless empty headings and collapse aliases only when coverage is retained.

## Entry specifications

### Attractions, architecture, museums, scenic spots

Local (e.g., Japanese) name, English/Chinese name where available; type; reason to visit; historical/architectural/artistic significance; practical visit details (address, hours, last entry, closures, ticket, booking, website, station and exit); seasonal factors; photography notes and image with provenance. If no validated value, `Verification pending` in draft; never guess.

### Hotels / arrival

Support each actual entry/exit mode (flight, rail, bus, ferry, driving, mixed) and each segment; show terminal/platform/bus stop, station exit, travel times, fares, time-zone, changes, payment and baggage. If `request.hotel` exists, treat its supplied name/address and check-in/out as core anchors; hotel desk/floor, entrance quirks and genuine embedded access map. If no hotel exists, offer clearly unbooked recommendations.

### Dining and shopping

Restaurant/café/bar category, specialty, service hours, closure days, reservation status, local-language name, exact branch, address and nearest station. Retail stores, markets and shopping streets also need hours, branch and tax-free rules when relevant.

### Tourist passes and tickets

Operator, covered lines, exclusions, duration, price and refund rules with validity period, purchase channels, adult/child prices when applicable, surcharge, whether worthwhile for **the actual itinerary**, and date checked. Prefer arithmetic rather than marketing claims.

### Around Area

**Refer to `around_area.md`.** Required: named nearby destination **distinct from the main base**, round-trip outbound/return itineraries in a single day, arrival/departure feasibility, a genuine on-site visit window, contingencies and verified source status. A one-way route is insufficient.

### Tours

Design experiences: what to do, see, learn or participate in, distinctive theme, season/event date, duration, provider or self-guided status, booking, participation/mobility rules and weather alternative. Follow `reader_contract.md`. Do not reuse the geographical catalogue as generic thematic stop lists.

## Depth and editorial quality

- Depth should resemble a researched handbook; not one-line site blurbs or generic AI listicles.
- Retain structured station maps, floor-plan notes, timetables and route diagrams when justified and suitably licensed.
- Separate factual description from personal preference and practical recommendation.
- A research note is not a finished brochure. In final status, no unresolved template markers and all claims tied to sources.


## Multilingual labels and three-level contents (mandatory)

Requests may use any language, including Chinese; guide narrative defaults to Simplified Chinese. Every important place, attraction, transport station and route needs Chinese + English. Japanese destinations also need original Japanese names, verified kana pronunciation and romanization; never invent unverified readings. See `multilingual_names_and_pronunciation.md`. Final DOCX/PDF contents require Heading 1-3, actual page numbers and clickable links; see `legacy_layout_contract.md`. The English language of skill documentation and examples does not change generated-guide defaults.


## Visual obligations

Real, source-verified licensed photos and actual sourced geographic maps must be downloaded to `photos/` and `maps/` and embedded inline in the manuscript, DOCX, and PDF. Multiple regional map illustrations are mandatory; every individual attraction, shopping/dining venue and hotel requires at least one corresponding photo beside its entry, including nested facilities and Around Area/Tours venues. Use the entry catalogue and markers from `reader_contract.md`; aggregate counts cannot satisfy missing entries (see `media_acquisition_and_maps.md`). A citation hyperlink is not an image.

## Pagination obligations

Heading 1 and Heading 2 MUST start on fresh pages. Write narrative directly below Heading 1 before the next Heading 2 to avoid title-only pages.
