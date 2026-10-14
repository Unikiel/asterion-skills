# Source-to-Skill Coverage Matrix

The schema is the **union** of three user-authored Seven Ninths brochures. Do not convert this into a short sightseeing-only guide. Each row denotes a preserved information *capability*, not a claim that every destination has relevant content for every row.

| Canonical section | 2024 Nagoya | 2025 Kobe | 2026 Tokyo | Periplus rule |
|---|:---:|:---:|:---:|---|
| Cover + Contents | ✓ | ✓ | ✓ | Cover metadata, navigable TOC, numbered regional maps |
| Arrival & Departure / Flight | ✓ | ✓ | ✓ | Historic brochures used flights; NEW skill accepts all travel modes, flight optional |
| Airport railway / airport bus | Railway | Airport Bus | Railway | Transport modality is configurable, preserve both |
| Accommodation | ✓ | ✓ | ✓ | Hotel contacts, station access, hotel-to-platform logistics |
| Brief Sketch + History | ✓ | ✓ | ✓ | Research city history, region-specific period subdivisions |
| Geography + Climate | ✓ | ✓ | ✓ | Terrain, climate, practical seasonality |
| Administrative Region | implicit | implicit | ✓ | Administrative and functional geographical divisions |
| Population | ✓ | ✓ | ✓ | Dated counts, distribution, demographic developments |
| Religion | contextual | contextual | ✓ | Religion and ritual when culturally relevant |
| Politics | ✓ | ✓ | ✓ | Explain institutions; avoid treating old officials as current |
| Economy / sectors | ✓ | ✓ | ✓ | Primary, secondary, tertiary as relevant |
| Education | ✓ | ✓ | ✓ | Universities, research and educational heritage |
| Culture / Travel | ✓ | ✓ | ✓ | Destination's distinctive attractions and landscape |
| Literature | ✓ | ✓ | ✓ | Literary background and local connections |
| Literature & Art | separate | separate | ✓ | Alias of merged topic, do not double-count |
| Language & Dialect | Localism | Localism | ✓ | Language, localism and regional identity |
| Art & Craft | ✓ | art | contextual | Heritage crafts, contemporary art and workshops |
| Events & Festivals | ✓ | ✓ | Events | Date-dependent festivals & annual activities |
| Delicacy / Diet & Cuisine | ✓ | ✓ | ✓ | Regional food traditions; distinct from restaurant directory |
| Media | ✓ | ✓ | ✓ | Media, film and print where relevant |
| Sports | ✓ | ✓ | ✓ | Clubs, sporting culture and facilities |
| Architecture | ✓ | ✓ | contextual | Distinct architecture sections where useful |
| Museum | ✓ | ✓ | ✓ | Museum index and detailed entries |
| Subculture | contextual | contextual | ✓ | Gaming, music, anime and related culture |
| Transportation | ✓ | ✓ | ✓ | Rail, metro, roads, bus, ports, airport as applicable |
| Highway / Roads | contextual | ✓ | ✓ | Different labels; preserve subject |
| Public Transportation | contextual | contextual | ✓ | Overview, tickets, rail and bus network |
| International Exchange | contextual | ✓ | contextual | Diplomatic/city relationships and international heritage |
| Attractions & Schedule | ✓ | ✓ | ✓ | Maps organized geographically plus day-by-day schedule |
| Maps | A–J | A–J | A–P | Unlimited regions as justified, no invented maps |
| Sightseeing & Adventure | ✓ | ✓ | ✓ | Destination's main detailed attraction catalogue |
| **Around Area / one-day round trips** | Toyota, Tokoname | Okayama, Kurashiki, Himeji | Kamakura, Fujisawa, Hanno, Lake Kawaguchi | **NEARBY day-trip destinations only, home-base return the same day. NEVER an alias for primary destination.** |
| Tours | Sakura, LEGOLAND, sightseeing bus | Kobe Hanabi, Arima Onsen | Tokyo Disneyland | Themed routes, seasonal events, tour experiences |
| Delicacy & Shopping | ✓ | ✓ | ✓ | Restaurant/Café/Bar + Store/Supermarket/Market |
| Tourist Travel Pass & Ticket | ✓ | ✓ | ✓ | Tourist Centers, pass coverage, tickets, fare rules |
| Practical Information | ✓ | ✓ | ✓ | Currency, embassy/consulate, emergency, relevant practical notes |
| Important Numbers | ✓ | ✓ | ✓ | Verify emergency numbers by jurisdiction |
| Useful links | Official / Transport | Official / Transport | Official / Transport | Official and transportation sources with checked access |

## The Around Area distinction (critical)

- `Sightseeing & Adventure > [Main Destination]` lists **sites in the primary destination**; it does not contain day-trip cities merely because they can be visited from the hotel.
- `Sightseeing & Adventure > Around Area > [Nearby Place]` lists **neighboring destinations for one-day round trips** from the traveler's main base. Each has a separate city/area overview, outbound route, realistic on-site window, return route, alternative if disrupted and confidence/status.
- `Tours` contains **themes, activities, itineraries and events**; a tour may be inside the main destination or inside an Around Area day trip. Do not classify a neighboring town as a `Tour` purely because it is a day trip.
- Canonical spelling: **Around Area**. The legacy source brochures use **Around Aera**; preserve it as a documented source spelling, not as an alias for the destination. A user's existing brochure may retain that spelling without losing its semantics.
- Day-trip feasibility must be evaluated rather than assumed; a far-flung suggestion not reasonably returnable on the same day is a `possible extension`/`overnight candidate`, not a qualified Around Area entry.

## Legacy editorial label normalization

- `Railways`, `Railways & Metro`, `Metro`, `Bus & Auto`, `Bus`, `Roads`, `Highway`: preserve the underlying transportation categories; use destination-specific grouping without eliminating one.
- `Literature` / `Literature & Art`, `Delicacy` / `Diet & Cuisine`, `Events` / `Events & Festivals` may be unified if there is no content loss. The audit must acknowledge merged headings.
- `Religion`, `International Exchange`, `Subculture`, `Art & Craft`, `Architecture`, `Museum` are NOT optional to silently skip. Mark **not applicable**, **not researched**, or **covered in a named section** explicitly.

## Editorial and source relationship

- A brochure is a knowledge reference and actionable travel guide, not a transport booking system.
- Historical brochures are useful **structure exemplars**, not trusted sources for current ticket prices, transport timetables, institutional officeholders or opening schedules.
- Store source coverage in the working coverage log. Do not place the raw private DOCX files in a distributable Skill.


**v2.4 adaptation:** `Arrival & Departure` is a mode-agnostic wrapper (flight/train/bus/ferry/drive/mixed); legacy Flight heading is included only if an actual flight segment exists. `Accommodation` honors supplied hotel details as travel anchor, else recommends unbooked hotels. Photographs and maps are embedded physical deliverables, not links. H1/H2 require new pages.