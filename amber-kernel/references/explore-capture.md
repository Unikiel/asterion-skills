# Writing an explore capture

Use `scripts/explore_capture.py` after following [explore.md](explore.md) and actually reading the sources. Browsing, following citations, and synthesis are agent work using the available web/browser tools; this helper makes no network requests and cannot establish that a claim is true.

The helper requires the existing Python/PyYAML runtime. It creates one Markdown file in an existing intake directory, with no parse state-directory requirement and no edits to established notes.

## Prepare a researched report

Write the report JSON in the task's writable scratch/workspace location outside the vault. The example below is illustrative fixture content, not a claim that these example URLs were researched:

```json
{
  "version": 1,
  "url": "https://example.org/article",
  "title": "Understanding the article's mechanism and evidence",
  "accessed": "2026-09-12",
  "status": "complete",
  "seed_source": "S1",
  "body": "## Summary\n\nExplain what the target actually says. [S1]\n\n## Deeper understanding\n\nExplain relevant context from the original evidence. [S2]\n\n## Interpretation and limitations\n\nLabel interpretation and retain uncertainty. [S1], [S2]\n\n## Open questions\n\nState a useful unresolved question.",
  "sources": [
    {
      "id": "S1",
      "url": "https://example.org/article",
      "title": "Target article",
      "status": "read",
      "locator": "Relevant section"
    },
    {
      "id": "S2",
      "url": "https://example.org/original-evidence",
      "title": "Original supporting evidence",
      "status": "read"
    }
  ]
}
```

Required top-level fields are `version`, `url`, `title`, `accessed`, `status`, `seed_source`, `body`, and `sources`. Use an actual access date, not the example date. The requested URL is retained separately from optional `resolved_url`; the seed source must match one of them. Query parameters and fragments are preserved because they may identify meaningful content.

Each source has a unique `S1`, `S2`, … ID, a URL, title, and access status. It may have its own `accessed` date, `locator`, and `limitation`. Missing publication metadata can stay missing; when known, include it in the body or established properties, clearly separate from access dates. For media and collections, include `kind` and `modalities` as below. Source status `read` means the relevant evidence was actually inspected using the declared methods, not necessarily that it was plain text.

| Status | Requirements |
| --- | --- |
| Report `complete` | The bounded exploration is complete; all listed sources are read. This does not mean exhaustive research or proven truth. |
| Report `partial` | Nonempty `coverage_note`; the seed is at least partially read; cite only available material. |
| Report `blocked` | Nonempty `coverage_note`; seed status is `unavailable`; body describes access limitations and next steps, not guessed source claims. |
| Source `read` | Relevant source content was actually read. |
| Source `partial` | Some content was read; a nonempty `limitation` identifies the missing coverage. |
| Source `unavailable` | Nonempty `limitation`; this source may be an unverified lead, but cannot support a body citation. |

Use `[S1]` labels close to factual claims in `body`. The writer converts them to usable Markdown links and appends a source ledger. A researched body must cite the seed. Undefined/unavailable citation IDs and attempts to redefine citation destinations are refused. The agent remains responsible for accurate attribution, copyright limits, and whether every factual claim has appropriate support; label assistant synthesis separately.

Optional `properties` is a mapping following an already established vault convention. Omit it when no schema is established: provenance appears in the body by default. Do not inject `status: processed` or parse-completion metadata. If an applicable template has other body headings, use them within `body` rather than adding a second frontmatter block.

## Preview and save

### Multimedia source ledger

For files, videos, audio, images, channels/playlists, or a mixed page, follow [explore-media.md](explore-media.md). Source `kind` accepts `web`, `text`, `document`, `image`, `audio`, `video`, `channel`, `playlist`, or `file`. Known YouTube URL shapes and filename extensions supply a fallback hint if omitted; explicitly declare the actual type when a generic file extension is misleading. YouTube video/channel/playlist kinds must match the identified target.

Example of one source record for transcript access without visual inspection:

```json
{
  "id": "S2",
  "url": "https://www.youtube.com/watch?v=abcdefghijk",
  "title": "Actual video title goes here",
  "kind": "video",
  "status": "partial",
  "limitation": "The transcript was read, but visuals were inaccessible.",
  "modalities": [
    {"type": "audio", "status": "observed", "method": "creator captions", "locator": "00:00–08:20; full caption text"},
    {"type": "visual", "status": "unavailable", "limitation": "No visual inspection was possible."}
  ]
}
```

Modality `type` is `text`, `audio`, `visual`, or `metadata`; each appears at most once per source. Status is `observed`, `partial`, `unavailable`, or `not_applicable`. Observed/partial entries require a nonempty `method` and coverage `locator`. Every status except observed needs a `limitation`, including the reason for an explicit scope exclusion. Methods distinguish captions, ASR, directly inspected audio, OCR, native document text, and actual frame/image viewing. Do not imply that reading captions inspected sound delivery or visuals.

Required declarations: video has audio and visual; audio has audio; image has visual; document has text; channel/playlist has metadata. Add other relevant modalities where needed. Document text read visually can be declared with that actual method. Missing required coverage cannot be omitted to claim completeness. `not_applicable` requires a legitimate scope reason, such as the user explicitly requesting transcript-only analysis; inaccessible media is `unavailable` instead.

A source with partial or unavailable modalities cannot use `status: read`, and a wholly inaccessible media source uses `unavailable`. The report's existing partial/blocked rules still apply. Known media sources require these declarations even when `kind` was inferred. These checks establish consistency, not independent proof of tool use.

For a channel or playlist seed with any access, include a top-level sampling record:

```json
{
  "sampling": {
    "scope": "Three selected videos; no claim of whole-channel coverage",
    "rationale": "Two relevant recent explanations and one foundational topic",
    "selected_sources": ["S2", "S3", "S4"]
  }
}
```

Selected IDs must identify cited non-seed sources with substantive text/audio/visual evidence, not only titles/thumbnails. Describe unavailable or excluded items in the coverage note/body. With no inspectable media, use an empty sample and partial coverage; metadata-only channel research cannot be complete. A fully blocked seed needs no sampling record. The generated note includes the scope, selection rationale, source IDs, and modality ledger.

### Commands

```text
python scripts/explore_capture.py VAULT REPORT.json
python scripts/explore_capture.py VAULT REPORT.json --apply
```

The first command validates and previews the path without writing to the vault. The second saves the requested note. `--intake EXISTING_DIRECTORY` overrides `LandingField` when appropriate. The normal agent workflow shows the preview then applies within the authorized explore request; only an explicit preview-only request stops before saving.

Filenames use `Explore - <descriptive title> - <URL hash>.md`, with portable characters and bounded title length. The URL hash avoids title collisions; the visible title inside the note remains descriptive. The helper checks for earlier captures by Input/Resolved URL headers and existing `url`/`source_url` properties throughout the vault, including notes moved or renamed by parse. It refuses filename collisions and never overwrites.

An unchanged repeated request returns `already-captured` with the prior note paths. For an explicit revisit, refresh, or new angle:

```text
python scripts/explore_capture.py VAULT REPORT.json --new-capture --apply
```

This produces a separate dated capture and links earlier ones. Same-day revisits receive a numeric suffix. Existing notes remain intact. If a previously blocked capture now needs another attempt, that is a revisit; request scope can establish that intent without a repeated approval prompt.

## Verification and limitations

The helper validates report shape, URL syntax, source/coverage consistency, local link and format integrity deltas, property types, collision checks, and unchanged directories. It stages a file in the existing intake directory and uses exclusive atomic creation on a filesystem supporting hard links. A concurrent context change or filename collision stops creation. Ordinary I/O failures clean the temporary file; abrupt process termination can leave an `.amber-explore-*.tmp` file, which is not a completed capture. Inspect any such leftover before removing it.

The source ledger is an assertion supplied by the researching agent, not proof of access or independent fact verification. No websites are contacted by the helper or its unit tests. A live run depends on usable browser/web tools and actual source access. URLs requiring sign-in, missing transcripts, unreadable scans, or inaccessible pages may yield a partial or blocked capture.

Return the saved note link, the count of sources actually read (distinguishing partial reads where material), and unresolved limitations. Do not run parse or move the generated note out of intake unless requested.
