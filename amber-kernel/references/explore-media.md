# Multimedia exploration

Use this workflow for files, images, recordings, video, creator channels, playlists, and pages containing relevant mixed media. Follow [explore.md](explore.md); the output remains one cited knowledge capture in existing intake for later parse.

## Discover content and capabilities

Inspect the supplied URL, redirects, available content type, and relevant linked assets. Extensions are hints, not proof of what was fetched. Inventory meaningful article text, downloads, diagrams, clips, recordings, captions, and source references. Ignore decorative images and unrelated assets; do not download a whole site.

Use available browser/web tools and applicable document, PDF, spreadsheet, image, audio, or video capabilities. Read an unfamiliar tool's instructions first. The local helper discovers optional dependencies without installing them or claiming they work. Prefer accessible public transcripts and existing capabilities. If a required adapter is absent, preserve useful evidence and declare the gap; installing a model, plugin, or external service is a separate setup action under the applicable authorization.

Keep temporary extraction artifacts outside the vault. Acquire only accessible media needed for the authorized analysis through supported tools. Do not bypass authentication, paywalls, download restrictions, or URL-display restrictions; never download media merely to work around a display restriction. Preserve privacy and applicable source/tool copyright limits.

## Evidence by medium

| Medium | Inspect | Preserve |
| --- | --- | --- |
| TXT, Markdown, HTML, structured text | Actual decoded content and meaningful record/section boundaries | URL and section, line, or record locators |
| PDF, Word, slides, spreadsheets | Text plus relevant tables, charts, figures, formulas, or slide layout; use available OCR when needed | Page, slide, sheet/cell locators and extraction limitations |
| Image, figure, chart, scan | Actually view the image; use OCR when useful; inspect labels, axes, units, and relationships | Figure/image locator; observations versus inference and OCR uncertainty |
| Audio/podcast | Actual audio analysis or available transcript/ASR; establish speakers only from evidence | Timestamps, transcript origin, uncertain words and uninspected sound information |
| Video | Speech/captions plus relevant frames, demonstrations, diagrams, and on-screen text | Timestamped claims and separate audio/visual coverage |
| Mixed page | Combine relevant modalities and follow underlying evidence | Cite the asset supporting the claim, not merely the landing page |

Text extraction is not visual understanding. OCR is not chart interpretation. A transcript may omit a silent demonstration, tone, sound event, or on-screen correction. Titles, thumbnails, descriptions, and comments support metadata claims; they do not establish what the media actually contains.

Record transcript origin: creator captions, automatic captions, official transcript, or local ASR. Without inspected visuals, ordinary video research remains partial. If the user explicitly requests transcript-only analysis, record that scope exclusion; do not call missing visuals “not applicable” merely because tools could not access them.

## YouTube video

Recognize watch URLs, short links, Shorts, and live/archive video links. A watch URL with a playlist parameter remains a single-video request unless the user asks for the playlist. Preserve supplied timestamps as focus hints and state the ranges actually analyzed.

1. Read the actual video page. Establish visible title, creator, duration, chapters, and publication date; these are metadata, not the lesson itself.
2. Retrieve readable captions/transcript using the public page or an available authorized tool. YouTube provides a [transcript interface for captioned videos](https://support.google.com/youtube/answer/15930243?hl=en). Mark automatic captions and verify consequential names, numbers, and terms; [automatic captions may be inaccurate or unavailable](https://support.google.com/youtube/answer/6373554?hl=en).
3. If no usable transcript exists, use an available audio-capable tool or authorized local transcription setup. If neither exists, record missing speech evidence; do not fabricate a transcript.
4. Inspect relevant visual sequences using actual video/frame/browser tools. Focus on important explanations, charts, demonstrations, or chapter changes; record timestamps and sampling gaps. A thumbnail is not video inspection. Qualify visual claims when visuals are inaccessible.
5. Extract concepts, mechanisms, arguments, examples, evidence, caveats, and questions. Trace credible references to primary evidence. Separate creator claims, corroboration, and assistant synthesis.
6. Cite the video with useful timestamp links. A source ID may accompany precise timestamp links in the body. The helper can construct a timestamp link, but cannot verify what occurs there.

## YouTuber/channel or playlist

A channel URL calls for exploration of its content, not just its profile. Inspect the channel, visible video list, and relevant playlists. Distinguish self-description from observations about sampled content.

Default to up to three accessible videos. Choose for the user's focus, or explain a mix of current and foundational/recurring topics visible in the listing. Apply the video workflow to each; record every video as its own source. Do not claim statistical representativeness or full-channel coverage. If fewer are accessible, say so.

Synthesize what sampled videos teach, recurring concepts, disagreements or changes over time, and a useful learning path. Ground generalizations in those videos; do not equate popularity with correctness or invent expertise or private motives. Topics inferred only from titles remain metadata observations.

Record scope, selection rationale, selected source IDs, and important omissions. If only profile text and titles were accessible, create a partial metadata capture instead of claiming video knowledge extraction. For a playlist, preserve meaningful ordering and sample a few relevant entries; do not automatically consume all entries.

The normal research budget still applies. Additional media defaults: up to three items and up to 60 minutes of selected material. For long recordings, select relevant chapters/ranges and declare omissions. These are adjustable bounds, not quotas. A fully read transcript does not mean every frame was inspected.

## Coverage and local extraction

Use source `kind` and `modalities` as documented in [explore-capture.md](explore-capture.md). Record text, audio, visuals, and metadata separately, including methods, locators, and limitations. Missing required evidence makes coverage partial even if another modality was useful. Save synthesized knowledge rather than raw transcript dumps or hundreds of frame descriptions.

```text
python scripts/media_extract.py capabilities
python scripts/media_extract.py route URL
python scripts/media_extract.py extract LOCAL_FILE
python scripts/media_extract.py extract LOCAL_TEXT --encoding utf-16
python scripts/media_extract.py timestamp-url YOUTUBE_VIDEO_URL 192
```

Built-in extraction covers decoded text, HTML text, SRT/WebVTT timed cues, DOCX body paragraphs, and PPTX slide text. Optional `pypdf` supplies PDF text extraction. The helper never executes macros or page scripts. Local inputs and expanded Office content are bounded to 20 MiB. Images/audio/video and unsupported files return `needs-backend`; use actual media tools or retain partial coverage. It does not download, interpret visuals, run ASR, or perform OCR. Dependency presence and URL routing are discovery hints, not evidence of successful extraction.
