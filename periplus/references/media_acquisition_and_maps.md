# Real Photographs & Maps — Non-negotiable Media Contract

The reader explicitly requires **genuine visual material physically present in both DOCX and PDF**. A hyperlink to an online picture, map URL, mocked map, placeholder box, or generated fantasy depiction DOES NOT meet this contract. Never substitute text-only output and mark FINAL. No need for the user to attach pictures: research, source and download suitable assets during the ordinary automatic phases.

## Per-entry obligation

Every attraction, nested facility, dining venue, shopping venue and hotel must have at least one correctly identified real photo inside its own illustrated entry. Maintain `ENTRY_CATALOGUE.json` and adjacent hidden markers per `reader_contract.md`; each venue photo manifest record includes reciprocal `entry_ids`. Supplementary photos may have no venue association; genuine ticket/product/floor-plan graphics use `kind: illustration` with source/rights in `photos/`, but cannot substitute for venue photos. Hotel/access maps do not replace hotel photos. Ordinary catalogue cross-references need not duplicate entries, but all new independent recommendations need cards and photos. Audit manuscript tables/run-in mentions manually for unregistered venue cards. Minimum total counts below are supplementary, never a substitute for 100% entry coverage.

## Photos — acquisition

1. Discover genuine destination / attraction / hotel / architecture photos from official tourism/venue sites or reusable repositories (e.g. Wikimedia Commons) and verify that the actual photo depicts the named subject. Prefer original, high resolution >= 700×450. Avoid watermark/stock preview, vague results or mismatched objects. Use genuine photo, not AI-generated imagery.

   A correctly licensed native original below 700x450 may be used as a genuinely small inset only when it is at least 300x200, prints at >=240 ppi without enlarging pixel data, and is visually clear at the actual print size. Record native_resolution, print_width_cm and small_print_reviewed: true. The exporter must enforce that width and final QA must verify the actual DOCX and PDF placement; an artificially enlarged file cannot qualify. This reconciles the preference for large originals with sharp small photographs, while maintaining complete venue coverage.
2. Confirm permitted publication/reuse terms. **A publicly accessible image is not automatically licensed for redistribution**. If attribution or license terms cannot be established, use another image. For user-provided images, mark `license: user-provided` and retain privacy considerations. Do not bypass website restrictions.
3. Download image bytes to `photos/` as `.jpg` or `.png` (not just a URL). Maintain correct orientation, aspect ratio, copyright/creator attribution, link to originating item and retrieval record; avoid duplicate photos or spurious geotags.
4. In the manuscript, place `![English + Chinese attraction name, photographer/source](../photos/attraction.jpg)` near the relevant entry and an immediately adjacent print caption with the required creator/copyright/license credit. Store the image-source link in the internal manifest, not in the final bibliography. Include a caption link only where its license expressly requires one.

## Maps - mandatory high-resolution Google Maps screenshots

1. Every displayed Map A/B/... area, hotel access map and other necessary geographic panel MUST embed an actual screenshot captured from Google Maps. A Google Maps hyperlink alone is insufficient. Do not download low-resolution map pictures, enlarge thumbnails, reconstruct the map from tiles, or silently substitute OSM, GSI, a coordinate grid or a schematic. If Google Maps cannot be loaded or its intended use is not permitted, record the specific blocker; do not mislabel another provider as Google.
2. Use a fresh browser context, frame the relevant area, wait for roads, labels and points to finish loading, and capture at native device scale >=2. Target at least 2000x1200 physical pixels per panel. Higher pixel counts do not excuse tiny labels: inspect at the actual DOCX/PDF display size, and change viewport/zoom or split panels until station names, road names and relevant venues can be read. Never upscale an existing low-resolution capture to pass validation.
3. Keep the Google logo, map/data-provider copyright and attribution visible and unobscured. Do not use Street View photographs as printable venue images. Check Google's current Geo Guidelines for the actual personal/public/commercial distribution scope; screenshots do not grant a blanket publication license. Never imply Google endorsement.
4. Verify hotel, station entrance, venue and map extent against primary sources. Add helpful legends outside the screenshot or in permitted unobscuring annotations. Save lossless PNGs to maps/map_a.png etc. Every area embeds its own map immediately beneath the area introduction. Keep an optional live Google Maps directions link for travelers.
5. Each map manifest record includes provider: Google Maps, capture_method: browser_screenshot, capture_url, captured_on, viewport_css, device_scale_factor, screenshot_pixels, attribution_visible: true, the exact attribution text and a print_readability_checked flag. Retain the screenshot provenance in research, rather than adding map-production/source links to the end-of-guide bibliography.

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
      "map_data_source": "Google Maps browser-rendered map",
      "provider": "Google Maps",
      "capture_method": "browser_screenshot",
      "capture_url": "https://www.google.com/maps/",
      "viewport_css": [1000, 700],
      "device_scale_factor": 2,
      "screenshot_pixels": [2000, 1400],
      "captured_on": "2026-10-15",
      "attribution_visible": true,
      "print_readability_checked": true,
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

Preserve native screenshot pixel dimensions in BOTH DOCX and PDF. Disable exporter downsampling, or losslessly embed the original screenshot into its existing PDF image object and verify unchanged page geometry, text, bookmarks and links. Inspect actual PDF image dimensions; high-resolution source files alone do not satisfy this rule. Never resample a reduced export upward.

- `scripts/validate.py --mode final` checks manifest, local image existence/decoding/resolution, attribution/license/source fields, manuscript embedding refs, minimum asset counts, every registered entry’s own photo/reciprocal associations and Map A/B/... coverage. Manually reconcile all named venue cards against the inventory before release.
- `scripts/export_brochure.py` embeds JPEG/PNG bytes in DOCX; remotely linked / nonexistent media raises an error. It then verifies actual image files inside DOCX, image instances in PDF and H1/H2 page breaks.
- No FINAL badge/release if actual photos/maps are missing. If site licensing or web tools block all real image acquisition, report an explicit blocker rather than quietly substituting map links.
- Machine checks can verify physical embedded media and recorded provenance, not authenticate subject/license by themselves. An agent must inspect images and validate rights against original sources.

## Built-in deterministic media helpers

- `python scripts/fetch_media.py --project <TRIP_DIR>` downloads explicitly researched, licensed image URLs recorded as `download_url` in the manifest. This is not web image discovery; the agent must first verify actual source and rights. No bulk scraping.
- `scripts/capture_google_maps.py --config <capture.json> --output-dir <maps>` captures Google Maps panels with Playwright in a new browser context. Install Playwright and a compatible browser only when needed. Each config item supplies id, url, output, viewport_css and device_scale_factor; optional browser_executable selects an installed browser. The script records capture metadata; an agent must still visually inspect labels, place identity, attribution and final print readability. `map_from_geojson.py` remains a legacy research utility and does not satisfy the current final-map contract.
