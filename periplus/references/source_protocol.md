# Evidence, Source Quality and Freshness

## Evidence categories

Assign every externally sourced operational assertion an evidence record:

- **CONFIRMED_USER_BOOKING**: supported by supplied ticket/reservation; redact identifiers in public artifacts.
- **USER_PLAN**: user's proposed intention, not yet booked/verified.
- **VERIFIED_CURRENT**: supported by credible, date-appropriate information (official operator/venue ideal).
- **HISTORICAL_CONTEXT**: source-identified contextual material where current applicability is not implied.
- **ESTIMATE**: explicitly labeled assumption or reasonable planning envelope, *never* a train departure/confirmed ticket.
- **UNVERIFIED**: open issue; no silently invented values.

## Source priority

1. User-provided booking confirmations for what was booked; compare with carrier/venue for current disruptions.
2. Current official museum, rail operator, bus provider, airline, accommodation, city tourism or transport authority documentation for schedules, tariffs, rules.
3. Primary research and scholarly sources for history and heritage claims.
4. High-quality independent travel/cultural journalism, clearly dated.
5. Community reviews for flavor, not authoritative timetables.

Do not confuse **live availability** with a static page listing a schedule. When tools cannot verify information, label as provisional.

## Freshness and currency

- **Short-lived**: fares, timetable, tickets, platform, operating hours, closures, events, booking availability, transport disruptions, weather. Verify for the trip date, record `checked_at` and source.
- **Medium-lived**: hotels, shops, restaurants, station exits, tourist office locations. Check recently.
- **Long-lived**: historical era, architecture, major artworks, geography. Source properly, date numerical claims, don't use decades-old demographics as current.
- Prevent chronology bugs: a photograph or outdated brochure may show an earlier timetable, old political official, changed venue/brand, or former transit tariff.
- Whenever operational data are unavailable, keep the factual statement absent/provisional and include a research task rather than inventing.

## Minimal evidence record

```markdown
| ID | Section / claim | Status | Source title | URL / file locator | Published / effective | Checked at | Trip date applicable? | Notes |
|---|---|---|---|---|---|---|---|---|
| EV-001 | ... | UNVERIFIED | ... | ... | ... | ... | ... | ... |
```

Use stable citation links near facts in published markdown; internal evidence IDs should link to source ledger. Distinguish user-provided input from sources so private document names are not inadvertently made public.

## Copyright and privacy

- Paraphrase the source documents; do not copy entire earlier brochures into the published output.
- Images: only use correctly licensed/user-provided material; credit creator/source/license if required. A link to a photo is not itself a reuse license.
- Never package flight booking references, passport numbers, private contact details or payment information in a reusable public Skill.
