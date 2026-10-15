# Seven Ninths Travel Brochure — Historical Layout Contract

The layout is based on three Word guides personally supplied by the user; their old itineraries, fares and destination facts are not reused:
- `2024.Japan.Nagoya.0323-0328.docx`
- `2025.Japan.Kobe.1002-1007.docx`
- `2026.Japan.Tokyo.0501-0504.docx`

## Required inherited publication format

1. **A4 portrait long-form handbook**, not a presentation-style travel poster, single-page attraction list or blog layout.
2. **Separate cover**: country name such as `JAPAN` above/centrally, large destination title and `YYYY.MM.DD - YYYY.MM.DD` date periods (retain every separate period without merging gaps). Use restrained black/white design with a Japanese-style red accent. Do not reuse old-guide images or content in the body.
3. **Content/table of contents directly after the cover**: **three heading levels** (Heading 1-3), hierarchical left indentation, dot leaders and right-aligned **actual page numbers**. Allow automatic continuation over multiple pages.
4. All three historical DOCX files contain a `TOC \\o "1-3" \\h \\z \\u` field with page numbers in TOC1/2/3. Periplus must generate a genuine Word-updatable TOC field and prepopulate verified TOC page numbers in the exported DOCX and PDF, without requiring the reader to open Word and manually update fields.
5. **Recurring header**: `Seven Ninths Travel Brochure` centered above a thin separator on all pages AFTER the cover. The historical cover has its top horizontal line, but no running text header or page-number footer. Centre content/body footers with current / total counts excluding the cover.
6. **Body structure and heading hierarchy**: inherit only the sections and hierarchy of the three historical guides. Independently research destination facts, flights, timetables and sources; do not reuse old content.
7. Every attraction, nested facility, shopping venue, restaurant/cafe/bar and hotel needs at least one corresponding genuine photograph. Transport includes genuine photographs, geographic/platform maps and tables where useful. **Acquire and physically embed images/maps in DOCX and PDF**, not merely external links, with copyright/source attribution. If legally usable genuine media cannot be acquired, block FINAL and report the obstacle.
8. Narrative defaults to Simplified Chinese; entity names are Chinese/English plus local official names and pronunciation. See `multilingual_names_and_pronunciation.md`.
9. **Oswald is the default Latin/English font** for cover, headings, Latin body text, header, TOC, captions and numerals. Use suitable CJK fonts for Chinese/Japanese. DOCX must declare Oswald and PDF must actually use it. If unavailable on the conversion host, report the block and advise installation from official sources; do not silently substitute or bundle font files with the skill. Font fallback must not create missing-glyph boxes.
10. **Inspect every page after DOCX-to-PDF conversion**, including headers, TOC page numbers, navigation and footers. TOC numbers must match actual PDF pages; the Word TOC remains updateable.

## Chapter architecture

- Arrival & Departure
- Accommodation
- Brief Sketch (History / Geography / Climate / Population / Religion / Politics / Economy / Education / Culture / Transportation / ...)
- Attractions & Schedule (Maps A-P ... / Schedule)
- Sightseeing & Adventure (Primary City / Around Area [nearby destinations with same-day return] / Tours)
- Delicacy & Shopping (Restaurant & Cafe & Bar / Supermarket & Store & Market)
- Recommends & Tips (Tourist Travel Pass & Ticket / Tourist Center / Tickets & Prices / Practical Information / Currency / Embassy / Important Numbers / Useful links)

Structural section headings MUST retain their inherited English labels, spelling, order and depth; venue headings are English-first, with Chinese second where available, while the narrative is primarily Chinese. English chapter labels do not remove Chinese/English/Japanese place-name requirements.

## DOCX output constraints

- Encode the body with genuine `Heading 1/2/3` styles, enabling the Word Navigation Pane and PDF bookmarks.
- The built-in `TOC` field supports subsequent Word updates and **must also contain static cached page numbers checked after pagination stabilizes**, allowing immediate DOCX/PDF reading.
- Reject manual contents without numeric pages, `000` caches, empty pages containing only `Contents`, and TOC numbers misaligned with the body.
- Exclude large cover titles from the TOC. The `Content` heading must not list itself.

### Reference-faithful pagination

Set `page_break_before=True` for main `Heading 1` chapters. Do not automatically break before `Heading 2` or `Heading 3`: in the original Kobe guide multiple lower-level headings share pages and flow naturally. Keep headings attached to their following content and check for orphans. Confirm by rendering every page.

### Publication media

Acquire genuine photographs and regional geographic maps, with captions/credits, following `references/media_acquisition_and_maps.md`. Follow historical layout examples, but **do not copy old-file photographs as evidence about a new destination**.

Final filenames follow `filename_and_date_periods.md`: year.English-country.English-city.all-date-periods.docx / .pdf, with no fixed period count.
