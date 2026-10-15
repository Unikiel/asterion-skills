# Real Photographs & Maps — Non-negotiable Media Contract

The reader explicitly requires **genuine visual material physically present in both DOCX and PDF**. A hyperlink to an online picture, map URL, mocked map, placeholder box, or generated fantasy depiction DOES NOT meet this contract. Never substitute text-only output and mark FINAL. No need for the user to attach pictures: research, source and download suitable assets during the ordinary automatic phases.

## Per-entry obligation

Every attraction, nested facility, dining venue, shopping venue and hotel must have at least one correctly identified real photo inside its own illustrated entry. Maintain `ENTRY_CATALOGUE.json` and adjacent hidden markers per `reader_contract.md`; each venue photo manifest record includes reciprocal `entry_ids`. Supplementary photos may have no venue association; genuine ticket/product/floor-plan graphics use `kind: illustration` with source/rights in `photos/`, but cannot substitute for venue photos. Hotel/access maps do not replace hotel photos. Ordinary catalogue cross-references need not duplicate entries, but all new independent recommendations need cards and photos. Audit manuscript tables/run-in mentions manually for unregistered venue cards. Minimum total counts below are supplementary, never a substitute for 100% entry coverage.

## Photos — acquisition

1. Discover genuine destination / attraction / hotel / architecture photos from official tourism/venue sites or reusable repositories (e.g. Wikimedia Commons) and verify that the actual photo depicts the named subject. Prefer original, high resolution >= 700×450. Avoid watermark/stock preview, vague results or mismatched objects. Use genuine photo, not AI-generated imagery.
2. Confirm permitted publication/reuse terms. **A publicly accessible image is not automatically licensed for redistribution**. If attribution or license terms cannot be established, use another image. For user-provided images, mark `license: user-provided` and retain privacy considerations. Do not bypass website restrictions.
3. Download image bytes to `photos/` as `.jpg` or `.png` (not just a URL). Maintain correct orientation, aspect ratio, copyright/creator attribution, link to originating item and retrieval record; avoid duplicate photos or spurious geotags.
4. In the manuscript, place `![English + Chinese attraction name, photographer/source](../photos/attraction.jpg)` near the relevant entry and an immediately adjacent print caption credit and linked source.

## Maps — real cartographic assets

1. At least one genuine sourced area/map image PER displayed `Map A`, `Map B`, ... section. This must reflect **actual geography** with recognizable street/transit network, orientation/scale when available, and labeled relevant points/stations. Also include actual accommodation access / airport-station interchange maps if operationally necessary.
2. Preferred: official city/railway/venue maps with reuse permission. Otherwise render cartography from verified OSM or another legally usable geographic data layer. Cite source/provider and required attribution (e.g. `© OpenStreetMap contributors` and ODbL details where relevant). Check tile use policies; do not bulk download, scrape, remove attribution, or imply a coordinate plotting grid is a real street map. A pure text list, Google Maps hyperlink, or decorative graphic is not a map image.
3. Save geographically accurate maps to `maps/map_a.png` etc (>=850×500). Map with pins must match source-verified coordinates and geography. Use larger maps or multiple panels when labels would not print legibly.
4. Each `Map A` chapter embeds its map immediately: `![Map A - Chinese area name / Central Area, base map and annotation sources](../maps/map_a.png)`; add a source/attribution caption and map legend. Repeat for every displayed regional map. Also keep online map URLs as OPTIONAL supplements to embedded real map.

## Manifest — actual provenance

For every real asset, append a record to `research/MEDIA_MANIFEST.json`:

```json
{
  "assets": [
    {
      "id": "photo_kiyomizu_01",
      "kind": "photo",
      "entry_ids": ["kiyomizu"],
      "file": "photos/kiyomizu_01.jpg",
      "source_url": "https://example.org/actual-item-page",
      "creator": "Photographer name or credited institution",
      "license": "Verified CC BY-SA 4.0 / official explicit license / user-provided",
      "attribution": "Required credit text",
      "subject": "Kiyomizu-dera",
      "checked_on": "2026-10-13"
    },
    {
      "id": "map_a",
      "kind": "map",
      "map_id": "Map A",
      "file": "maps/map_a.png",
      "source_url": "https://example.org/real-map-source",
      "map_data_source": "OSM / municipal / railway verified cartography",
      "creator": "Map creator / cartographic provider",
      "license": "Verified permitted reuse terms",
      "attribution": "Required cartography and map data credits",
      "subject": "Map A – Kyoto central area",
      "checked_on": "2026-10-13"
    }
  ]
}
```

These `example.org` URLs are SCHEMA ILLUSTRATIONS ONLY: replace with real URLs retrieved during execution. Never publish sample media or imaginary image credits.

## Print layout

Place a specific heading, photo, concise caption/credit, substantive description and operational facts together, following the Kobe reference. Preserve aspect ratio; do not stretch, arbitrarily crop or use oversized portrait images. Default single-column photos have height at most 9 cm; map panels can be larger while labels stay readable. Keep photo and caption together, and heading with the first image/text. Use a fresh page for a venue when required to prevent isolated headings or tiny continuation fragments; H3 pagination is discretionary. Repeat table headers, keep rows intact and verify no figure/caption clipping or excessive whitespace. Visual inspection of every final page remains mandatory; machine image counts cannot certify layout.

## Publication gate

- `scripts/validate.py --mode final` checks manifest, local image existence/decoding/resolution, attribution/license/source fields, manuscript embedding refs, minimum asset counts, every registered entry’s own photo/reciprocal associations and Map A/B/... coverage. Manually reconcile all named venue cards against the inventory before release.
- `scripts/export_brochure.py` embeds JPEG/PNG bytes in DOCX; remotely linked / nonexistent media raises an error. It then verifies actual image files inside DOCX, image instances in PDF and H1/H2 page breaks.
- No FINAL badge/release if actual photos/maps are missing. If site licensing or web tools block all real image acquisition, report an explicit blocker rather than quietly substituting map links.
- Machine checks can verify physical embedded media and recorded provenance, not authenticate subject/license by themselves. An agent must inspect images and validate rights against original sources.

## Built-in deterministic media helpers

- `python scripts/fetch_media.py --project <TRIP_DIR>` downloads explicitly researched, licensed image URLs recorded as `download_url` in the manifest. This is not web image discovery; the agent must first verify actual source and rights. No bulk scraping.
- For maps when an official licensed raster image is unavailable: download accurately georeferenced and legally usable **real** GeoJSON features (roads, railway, park and river geometry), gather verified point coordinates, then call:

```bash
python scripts/map_from_geojson.py \
  --geojson maps/source/area_a.geojson \
  --pins maps/source/area_a_pins.json \
  --output maps/map_a.png \
  --title 'Map A — Downtown' \
  --attribution '© OpenStreetMap contributors, ODbL (or appropriate provider)'
```

Pins JSON is a list of objects like `{"lat": 35.0, "lon": 135.0, "label": "Central Station"}` using **source-verified coordinates**. The map is an authentic rendering of actual geographic geometry; not an illustration substituting for missing spatial data. Record underlying GeoJSON source URL, map creator and data license in the media manifest. If the data are not verified, do not generate a fictional map.
