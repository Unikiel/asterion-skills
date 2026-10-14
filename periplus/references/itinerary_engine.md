# Itinerary, Transport, Maps and Logistics

## Planning order

1. Fix **outbound origin (where the traveler starts)**, **return final destination (where traveler ends)**, main stay **base**, stay date(s), arrivals/departures, immovable reservations and user walking/energy preferences. Outbound origin and return destination can differ; never force a round-trip symmetry.
2. Group primary city attractions by geography and public transport network: the inherited `Map A`, `Map B` naming system.
3. Classify nearby destinations using **[Around Area](around_area.md)** with outbound AND return feasibility. No day trip should be promoted solely because a destination is famous.
4. Build a feasible daily route, integrating opening days, queues, last-entry, meal/rest breaks, photography light, transfers, station exits, baggage, and route contingency.
5. Put chosen dates/time windows in Schedule. The detailed Catalogue then expands the stops in the same geographical order, preserving map references.
6. Re-evaluate when rain, closures or transit changes invalidate assumptions.

## Time model

For each leg, estimate conservatively, using sourced transit times where available:

```
Real door-to-door ≈ walk to station + ticket/security margin
                  + expected wait + in-vehicle time + interchange
                  + exit/walk to destination + contingency buffer
```

- Do not conflate station-to-station times with hotel-to-entrance time.
- User-requested light walking: cap walking and transfer stairs wherever possible; display accessible routes when confirmed.
- Mixed operator passes: check validity **per segment** and surcharge (limited express, reserved seats, luggage fees).
- Respect station operating hours, last train, and contingency for delayed arrival.
- Each time has a date and local timezone if cross-border/cross-timezone.

## Route record

```markdown
| Seq | Place | Arrival window | Visit duration | Next transport | Walk / transfer | Ticket | Evidence status |
|---:|---|---|---|---|---|---|---|
| 1 | Hotel | ... | ... | ... | ... | ... | ... |
```

## Map contract

- Show true spatial relationships, regional groupings and major stations, not a decorative illustration.
- Each map has: ID (Map A/B/...), region name, all labeled attraction IDs, transit hub(s), optional food/shopping and source note.
- Geographic locations must be grounded in validated geocodable names/addresses or coordinates from evidence. Do not guess street addresses/latitudes/travel minutes.
- The agent MUST acquire/render and embed genuine geographic map images in `maps/` for Map A/B/... and include source/license details in `research/MEDIA_MANIFEST.json`. Map URL links are supplementary only; missing embedded maps block publication. See `media_acquisition_and_maps.md`.
- Keep maps and day schedule consistent; the table of maps should reference the detailed attraction IDs.

## Separate indexes

- `Main destination attractions` = destination interior; chronological route / geographic catalogue.
- `Around Area` = same-day independent destination visits; each has round-trip operations.
- `Tours` = thematic and seasonal ways to combine experiences, within the main city or a qualified nearby excursion.


## 多语言标注与三级目录（固定要求）

用户请求语言不限，攻略默认简体中文。每个重要地点、景点、交通站和路线必须中文＋英文；日本还须含日文原名、假名发音及罗马字；不能核实的读音不得编造。参照 `multilingual_names_and_pronunciation.md`。最终 DOCX/PDF 的目录需 Heading 1–3、真实页码与可点击链接；参照 `legacy_layout_contract.md`。


**Entry and exit modes:** outbound/return travel may be flight, rail, bus, ferry, driving or multimodal; connect chosen hotel (when given) or proposed accommodation base to both termini. Never require airport transfers when the user takes the train.

**Hotel:** accept `request.hotel` as a first-class input; preserve it and compute every relevant transfer from its actual address, if provided. An unbooked recommended hotel is never represented as confirmed.