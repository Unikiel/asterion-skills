# Periplus v2.6.0

Automatically research and publish a complete Seven Ninths Travel Brochure. All skill documentation and bundled examples are English. Traveler requests may be written in Chinese, English, Japanese or any other language. Generated narration defaults to Simplified Chinese (`zh-CN`) and follows an explicitly requested alternative language.

## Request example

```text
$periplus
Destination: Kyoto, Japan
Dates: 2026-11-05 through 2026-11-11
Outbound: Shinkansen, Tokyo Station -> Kyoto Station
Return: Shinkansen, Kyoto Station -> Osaka Station
Accommodation: supplied hotel name and address, if known
Preferences: modern architecture, railways, museums, photography, minimal walking
```

Do not require service numbers. Research specific date-applicable services, allow preceding arrival/activity and immigration/baggage/terminal/boarding buffers, and compare sensible transport modes. Treat supplied bookings as anchors without inventing availability. Outbound origin and final return destination are mandatory and may differ. Hotel information is optional.

## Publication contract

- Generate DOCX and a matching PDF by default. Keep ALL original Master Skeleton topics and heading levels; do not rename, merge, delete, reorder, or abbreviate them. Only the approved typo correction `Around Aera` -> `Around Area` is allowed. Record non-applicable transport-specific headings factually without deleting the skeleton.
- Preserve the exact historical A4 cover geometry (no creative redesign), genuine clickable three-level page-numbered Content, centered `Seven Ninths Travel Brochure` header and current/total footer on non-cover pages. Start H1 on new pages; allow H2 to flow like the Kobe original.
- Use Oswald for Western text and readable CJK fonts for Chinese/Japanese. Verify real PDF fonts; font files are not bundled.
- Every attraction, nested facility, shopping venue, dining venue and hotel needs a corresponding licensed real photo in its own card. Hotels also need a separate access map. Register and reconcile ENTRY_CATALOGUE and MEDIA_MANIFEST.
- Embed actual geographic maps for every Map A/B/etc. URLs alone do not count. Keep credits and reuse permissions.
- Keep ALL execution explanations, internal reasoning, rule discussions, QA reports and editorial selection monologues out of the guide. Internal working checklists stay in research files, not in the published manuscript. Around Area titles use destination names. Tours emphasize distinctive experiences. Tickets & Prices covers passes, combinations and discounts, not a default trip budget.
- For finished-guide venue/location headings use **English first, then Chinese when available** (e.g., `English Name — Chinese Name`); keep the inherited structural section titles exactly in English. Main narrative defaults to Simplified Chinese and can include other languages. For Japan also show Japanese script, verified kana and Hepburn readings. This generated-content requirement does not change the English-only skill source policy.
- Accept any number of date periods. Schedule active days only and preserve every period in the final English filename.

For Tokyo stays on July 11-12 and July 17-19, the actual outputs are:

```text
2026.Japan.Tokyo.0711-0712.0717-0719.docx
2026.Japan.Tokyo.0711-0712.0717-0719.pdf
```

Read `references/filename_and_date_periods.md` for cross-year rules. The stable internal manuscript is `exports/Seven_Ninths_Travel_Brochure.md`; explicitly requested public Markdown uses the same date-based filename as other outputs.

## Install and run

See `INSTALL.md`. The ZIP contains a `periplus/` folder. Install that folder into the local Codex skills directory or use the bundled platform installer. Local installation does not install runtime dependencies or register a skill in a different account.

From the installed skill directory:

```bash
python scripts/generate.py --version
python scripts/generate.py --request examples/trip_request.json --out ./trips
```

The generator runs the research and writing phases through a configured Codex CLI. It needs working web-research access. Publication requires Python `python-docx`, `markdown-it-py`, `Pillow`, `pymupdf` and LibreOffice. `--dry-run` initializes diagnostics only and never produces a completed guide. Resume using `--resume --project PATH`.

## Release checks

`VERSION` is the canonical skill release number. Project records include the skill and schema versions. The release tests cover multilingual acceptance, default Chinese output, per-entry media, connection margins, English filenames, arbitrary date periods and orchestration. Run:

```bash
python -m unittest discover -s scripts -p 'test_*.py'
```

Before FINAL, verify compulsory Skeleton coverage and per-entry photo coverage with `python scripts/skeleton_audit.py --project PATH` plus the publication QA. Independent source/rights verification and every-page rendered visual review remain required; test fixtures and structural validation do not establish real travel facts.

## v2.6.0 — Release changes (2026-10-15)

- Lock all historical Master Skeleton headings, their spelling and hierarchy; preserve all topical categories and move process-only appendices to private QA files.
- Adopt the user-approved spelling `Around Area`; older `Around Aera` is invalid in newly published material.
- Mandate English-first, Chinese-second venue titles; default Simplified Chinese narrative with optional multilingual passages and Japanese name/pronunciation records.
- Keep H1 chapter page breaks but let H2 flow like the Kobe reference; restore the reference cover and exclude it from running header/footer numbering.
- Strengthen embedded-photo per-entry, geographic map, and no-internal-reasoning gates; unfulfilled items block FINAL.
- Synchronize `SKILL.md`, README/INSTALL/version metadata, reference contracts, prompts, publication code, and release tests.
