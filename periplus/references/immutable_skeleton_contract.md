# Immutable Master Skeleton and publication integrity contract — v2.7.0

## Source precedence

1. Explicit current traveler instructions are controlling. Ask for consent before changing any locked historical heading. The traveler has explicitly approved only the typo correction `Around Aera` -> `Around Area` and the new display ordering for bilingual titles.
2. The authoritative heading inventory is `assets/Seven_Ninths_Master_Skeleton.md`, derived from the three historic user brochures and adjusted only for approved corrections.
3. The Kobe reference is a binding **presentation and coverage exemplar**, not a source for destination facts. A new destination needs independent research. The skill may add more detailed sub-entries, but cannot delete or rename any locked heading.

## Heading and coverage invariant

- The seven published H1 chapters and ALL fixed topical H2/H3 labels must appear **in the master order and at the master heading level**, with their original English text, including historical variants that may cover related material. Never collapse `Literature` into `Literature & Art`, `Delicacy` into `Diet & Cuisine`, `Events` into `Events & Festivals`, `Railways` into `Railways & Metro`, or `Highway` into `Roads`.
- For a category with no local counterpart (e.g., no metro), retain its exact heading and give a short visitor-useful factual description. Do not substitute internal explanations about the skeleton. Do not create fake attractions or services for the sake of a category.
- Transport-leg-specific fields (Flight, Railway, Airport Bus, Ferry, etc.) are populated only when the actual trip or a viable alternate involves that mode; never invent nonexistent schedules. Arrival and Departure remain mandatory and identify the supplied origin and final endpoint. Preserve their labels, with actual dates substituted.
- The master Skeleton's working appendices (booking checklist, media checklist, audit) are mandatory **internal records** stored under `research/` and `TASKS.md`; they MUST NEVER appear as content pages, appendices, captions, introduction or editorial narration in the traveler-facing guide.
- At least Maps A–J are prepared as geographic areas or separate functional geographic panels when relevant. Each published Map needs a high-resolution Google Maps browser screenshot with accurate venue identifiers and visible Google/data-provider attribution. Do not create blank or synthetic pseudo-maps. If geographically meaningful areas cannot be mapped from real sources, mark FINAL blocked and request a scope decision; do not quietly remove the headings.
- Fixed section labels remain English. Titles of named places, monuments, stations, museums, accommodation, restaurants, shops and markets are English first followed by Chinese (when available). Do not rename established formal English names or pretend a descriptive translation is official. Japanese locations additionally receive original script, verified kana and Hepburn romanization in the body record. All traveler-facing prose defaults to Simplified Chinese, allowing quotations, other languages and local text.
- `Around Area` is the sole permitted normalized spelling. It must always denote a genuine same-day out-and-back excursion from the primary base.

## Image invariant

- EVERY *individually described or recommended* place / attraction / nested attraction / gallery / museum / hotel / restaurant / cafe / bar / shopping mall / shop / market / shopping street needs AT LEAST ONE actual corresponding, identifiable photograph physically embedded directly within its own entry, including food and interior subjects. No image sharing by omission, map substitutions, generic stock photographs, logos, blank frames, source links or illustrative wallpaper.
- The entry ledger `research/ENTRY_CATALOGUE.json` and the photo ledger `research/MEDIA_MANIFEST.json` must maintain reciprocal links by entry ID. Run both machine coverage checks and manual page-by-page subject/branch verification; the source must permit the actual intended reuse, and the credit must be retained. One photo cannot prove that a different business or branch is depicted.
- A geographically accurate source-grounded access/location map must be embedded for each map panel; include hotel and transfer maps separately where required.
- A missing image, wrong license, broken embedding, absent source, or unverified venue-photo relationship is a **FAIL** preventing final publication. Do not cut venue chapters or hide missing pictures to pass.

## Typography and historical layout

- Reproduce the original restrained JAPAN / destination / dates cover: top hairline rule and small red disc. Do not insert editorial slogans, marketing badges or decorative page titles.
- In the Kobe/Nagoya/Tokyo reference, the front cover has no running textual header/footer. Content and body pages have centered `Seven Ninths Travel Brochure`, thin rule, and current/total page numbers excluding the cover.
- Start the principal H1 chapters on new pages; keep H2/H3 in normal flow with `keep-with-next`. Forcing every H2 onto a new page violates the Kobe layout. Use actual A4 document typography, not full-screen slides or cards.
- Oswald is mandatory for Latin/western glyphs in the title, text, headings, TOC, running furniture and page numbers; CJK fonts must support Chinese and Japanese text and be visually inspected. Never distribute Oswald font binaries in the package.
- The TOC is a genuine updateable, page-numbered, clickable three-level Word field and corresponding PDF navigation, with page numbers verified against the final PDF pagination; no manually typed text-only TOC.
- Format final names as `YYYY.EnglishCountry.EnglishCity.MMDD-MMDD[.MMDD-MMDD...].docx` and `.pdf`, preserving ALL disconnected date periods.

## Reader-facing prose isolation

- The published guide contains *only* destination facts, practical travel logistics, cultural/architectural descriptions, photography/child-friendly notes, and truly meaningful uncertainty warnings.
- Forbidden: model reasoning, self-talk, agent execution summaries, internal QA/report status, “this skill requires”, “to satisfy the template”, heading rationale, technical implementation, research collection steps, source-protocol discussions, empty editorial remarks, and checklist artifacts. Store such material only in internal `research/` files.
- A factually important limitation may be explained in travel language without naming internal policy; historical travel dates must not be misrepresented as live availability.

## Independent completion gates

A document cannot be marked FINAL before these checks pass:

1. Immutable heading spelling, nesting, section order and English-first bilingual titles: `python scripts/skeleton_audit.py --project PATH`.
2. Every actual venue associated with at least one correctly identified licensed photo embedded beside its own content: `ENTRY_CATALOGUE`, `MEDIA_MANIFEST`, and visual manual review.
3. All real area maps and hotel/transfer maps physically embedded and correctly located.
4. Verified date-specific route recommendation and reasonable connections, transfers, luggage handling, children/pace and venue closures.
5. Full-size DOCX and matching PDF, correct historical cover/TOC/body layout, real Oswald rendering and verified page numbering and clickable headings.
6. No internal reasoning or QA commentary in the reader-facing guide; maintain reports separately.

Stop and explicitly state unmet requirements rather than call a partial guide final.
