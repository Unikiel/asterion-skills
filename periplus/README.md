# Periplus v2.5.0

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

- Generate DOCX and a matching PDF by default. Keep the complete historical section taxonomy, substantive destination background and detailed venue catalogues.
- Preserve A4 cover, genuine clickable three-level page-numbered Content, `Seven Ninths Travel Brochure` header on every page and current/total footer. Start H1 and H2 on new pages.
- Use Oswald for Western text and readable CJK fonts for Chinese/Japanese. Verify real PDF fonts; font files are not bundled.
- Every attraction, nested facility, shopping venue, dining venue and hotel needs a corresponding licensed real photo in its own card. Hotels also need a separate access map. Register and reconcile ENTRY_CATALOGUE and MEDIA_MANIFEST.
- Embed actual geographic maps for every Map A/B/etc. URLs alone do not count. Keep credits and reuse permissions.
- Keep internal reasoning out of the guide. Around Area titles use destination names. Tours emphasize distinctive experiences. Tickets & Prices covers passes, combinations and discounts, not a default trip budget.
- Display Chinese + English place names; in Japan also show Japanese script, verified kana and Hepburn readings. This generated-content requirement does not change the English-only skill source policy.
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

Independent source/rights verification and every-page rendered visual review remain required; test fixtures and structural validation do not establish real travel facts.
