# English filenames and arbitrary date periods

Use the same basename for DOCX and PDF. Match the user's convention:

`2026.Japan.Tokyo.0711-0712.0717-0719.docx`
`2026.Japan.Tokyo.0711-0712.0717-0719.pdf`

Single-year rule: `YYYY.Country.City.MMDD-MMDD[.MMDD-MMDD…]`. Include EVERY inclusive date period chronologically; there is no fixed number of periods. Keep user-separated adjacent periods separate. A one-day period is `MMDD-MMDD` with identical endpoints. Never replace disjoint periods with earliest–latest, insert gap days, or silently truncate the period list. Month crossings use the same rule, e.g. `0730-0802`.

All filenames are ASCII English. Independently research canonical English country/city names and store `country_en` and `destination_en` in request.json when the source input is Chinese/Japanese/another script. Do not demand these labels from the user or mechanically strip non-English names into an empty/generic filename. Use the verified English label’s case. Replace spaces/unsafe punctuation with hyphens (e.g. `United-Kingdom`, `New-York`); dots separate filename fields only. Do not include Chinese/local-script characters in any deliverable filename. Do not add FINAL/version/Travel_Brochure suffixes unless the traveler explicitly requests them.

If periods involve more than one calendar year, use an unambiguous extension: `YYYY-YYYY.Country.City.YYYYMMDD-YYYYMMDD[.YYYYMMDD-YYYYMMDD…]`, e.g. `2026-2027.Japan.Tokyo.20261230-20270102.20270310-20270312.docx`. Same basename for PDF. Keep all years in each date endpoint in this case.

## Date input and normalization

Accept natural-language lists of any length or structured `date_ranges: [{start_date, end_date}, …]`. Both endpoints use `YYYY-MM-DD`; all ranges are inclusive. Existing `start_date` + `end_date` remains accepted and normalizes to a one-element date_ranges list. Sort chronologically and reject inverted/overlapping/repeated ranges instead of inventing intent. If envelope dates are also provided, they must agree with the first/last range; derived `start_date/end_date` are bookkeeping bounds only, never a continuous stay assertion.

Example:
```json
{"destination":"Tokyo","country":"Japan","destination_en":"Tokyo","country_en":"Japan",
 "date_ranges":[{"start_date":"2026-07-11","end_date":"2026-07-12"},
                {"start_date":"2026-07-17","end_date":"2026-07-19"}]}
```
Journey endpoints and other existing required inputs still apply. Per-period hotel or journey records may be provided inside date_ranges; preserve and use them without implying a single continuous hotel reservation. Global departure/return describes the first start and final endpoint; research intermediate arrivals/departures when relevant. Do not invent intervening stays/activities. Ask only for a truly indispensable unresolved endpoint if supplied facts cannot resolve it.

## Publication and checks

Keep `exports/Seven_Ninths_Travel_Brochure.md` as the internal reproducible manuscript; only final DOCX/PDF receive the date-based basename. Use `scripts/trip_dates.py` for normalized periods, active travel days, cover dates and `publication_stem(request)`. The exporter writes those final names directly, and the CLI verifies those same paths. Never merely change download-link labels while files still have generic names.

Schedule each active day of every period exactly once, with a clear period grouping; no schedule day for excluded gaps. Cover/date labels display the actual separated periods, not the envelope. Recheck bookings, opening dates, transport and per-period hotel access independently. Media quotas and trip duration count active travel days only. If the user explicitly requests extra file formats, their user-facing filenames also follow the same English convention; the internal manuscript remains stable for tooling.
