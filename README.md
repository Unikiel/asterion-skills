# Asterion Skills

A growing collection of reusable AI-agent skills for specialized tasks across a
wide range of domains. Individual skills may support planning, analysis,
creation, automation, education, research, engineering, validation, or other
workflows.

Each skill has its own purpose and operating model. Future additions may explore
domains beyond project development and tutoring.

| | Skill | Use it when you need to |
| --- | --- | --- |
| 💥 | **[BigBang](#skill-bigbang)** | Turn a proposal into a buildable project and teaching pack |
| 🔶 | **[Amber Kernel](#skill-amber-kernel)** | Operate an existing Obsidian vault in place |
| 🧭 | **[Periplus](#skill-periplus)** | Research a trip and write a finished Seven Ninths brochure |

🗂️ [Skills](#available-skills) · 🌳 [Structure](#repository-structure) · 📥 [Install](#installation) · ▶️ [Usage](#usage) · 🛠️ [Contributing](#contributing)

## <a id="available-skills"></a>🗂️ Available skills

### <a id="skill-bigbang"></a>💥 BigBang

BigBang helps preserve an original proposal as the authoritative baseline while
adding the engineering and teaching structure needed to complete the project.

Its workflow supports:

- Baseline extraction and requirement traceability
- Feasibility, scope, risk, and architecture analysis
- Workload-based 60-minute tutoring sessions
- A dedicated Vibe Coding environment-setup module
- A one-time project initialization prompt
- Phase-by-phase implementation prompts with acceptance criteria
- Safe pause, resume, checkpoint, rollback, and recovery procedures
- Software, AI, data, research, scientific, and ESP32/IoT projects
- Testing, deployment, documentation, and release validation
- Polished DOCX/PDF project packs and equation validation when requested
- Hardware bills of materials, wiring diagrams, system diagrams, and module
  bring-up guides when physical components are involved
- Optional competition materials only when explicitly requested

English is the default drafting language. Other language versions are generated
only when explicitly requested.

### <a id="skill-amber-kernel"></a>🔶 Amber Kernel

Amber Kernel follows the user's vault conventions and preserves their original
thinking. Its **parse** subskill digests, tags, links, and files incoming ideas
and documents. Developing rough ideas and integrating their substance into
existing notes are independently optional.

Its **explore** subskill takes a URL, reads it and relevant supporting sources,
and saves one cited research capture in the existing intake directory. It
records partial or blocked access honestly and leaves final filing to parse.

Explore also handles multimedia URLs: text/files, images, recordings, videos,
and YouTube channels or playlists. It separates speech/text and visual evidence,
keeps timestamps or page/slide locators, and records coverage. Channel and playlist
exploration defaults to every accessible video, with a deduplicated inventory,
per-video knowledge, and durable progress across batches. There is no fixed video
count or duration cap. Media interpretation uses available tools; missing extraction
capabilities and incomplete discovery remain explicit limitations.

Its workflow supports:

- Scoped convention records and previews before file moves
- Vault discovery, audit, adoption in place, and empty-vault bootstrap
- Batch intake through parse, with explicit optional development and integration
- URL exploration with source trails, deeper explanations, and cited intake captures
- Multimedia evidence, timed captions, document text, and resumable exploration of all channel videos
- Saved edit plans, recoverable originals, repeat protection, and interruption recovery
- Note create, edit, merge, move, rename, delete, and link integrity
- YAML properties, templates, daily notes, attachments, Canvas, and Bases
- Research capture into source, atomic, synthesis, and project notes
- Search, query, plugin, theme, snippet, and cssclass workflows
- Local-first privacy; no plugin install, Sync change, or external send unless
  requested

Routine work preserves existing directories and introduces no compulsory
taxonomy. An explicit structural redesign is a separate task. The Python helpers
require Python 3.10+ and PyYAML; applying intake plans requires a configured local
state directory outside the vault on the same filesystem. Unsupported dynamic
references are deferred rather than rewritten blindly. See
[parse](amber-kernel/subskills/parse/instructions.md) and the
[runtime protocol](amber-kernel/subskills/parse/references/parse-runtime.md) for usage and limits.

### <a id="skill-periplus"></a>🧭 Periplus

Periplus 2.5.0 researches a destination and writes a complete Seven Ninths
Travel Brochure in the same request. The required inputs are the destination,
the trip dates, the outbound origin, the return destination, and the outbound
and return transport. Each leg may be flight, rail, bus, ferry, driving, or a
combination, and the two endpoints may be different cities. Service numbers are
optional. A booked hotel and other preferences are optional. A trip may contain
more than one date period.

The skill text and examples are English. A traveler may write the request in
any language. The brochure narrative defaults to Simplified Chinese unless
another output language is requested. Important places use Chinese and English
names; Japan also includes the original script, verified kana, and Hepburn
romanization.

Its workflow supports:

- Live research with source URLs, retrieval dates, and uncertainty labels
- Date-applicable services, with arrival, immigration, baggage, and boarding buffers
- The historic Seven Ninths section set, adapted to the destination
- A licensed photo card for every attraction, nested facility, shop, restaurant, and hotel
- A separate hotel access map, plus a real map for each area
- Same-day Around Area excursions titled by destination name
- A day-by-day itinerary for the active dates, anchored to the supplied journey and hotel when given
- Finished DOCX and PDF named from the year, country, city, and every date period
- The legacy cover, a real three-level contents table, the brochure header, page numbers, and a new page for every level-1 and level-2 heading
- English text in Oswald, with Chinese and Japanese on a CJK font
- A local Codex runner, `scripts/generate.py`, when the skill is invoked from the command line

Periplus does not book travel. It does not invent schedules, prices, addresses, or availability, and it keeps internal reasoning out of the guide. If research or export cannot run, it reports that blocker instead of treating a scaffold or Markdown draft as the finished guide.

## <a id="repository-structure"></a>🌳 Repository structure

```text
asterion-skills/
├── README.md
├── LICENSE.md
├── bigbang/
│   ├── SKILL.md
│   ├── agents/
│   │   └── openai.yaml
│   ├── assets/
│   │   └── icon.svg
│   └── references/
│       ├── hardware-workflow.md
│       ├── project-standards.md
│       ├── prompt-and-kickoff-system.md
│       └── start-from-scratch-workflow.md
├── amber-kernel/
│   ├── SKILL.md
│   ├── agents/
│   │   └── openai.yaml
│   ├── assets/
│   │   └── icon.svg
│   ├── scripts/
│   │   ├── amber_kernel.py
│   │   ├── vault_links.py
│   │   ├── vault_state.py
│   │   ├── run_tests.py
│   │   └── test_amber_kernel.py
│   ├── subskills/
│   │   ├── parse/
│   │   │   ├── instructions.md
│   │   │   ├── references/
│   │   │   │   └── parse-runtime.md
│   │   │   └── scripts/
│   │   │       ├── parse_batch.py
│   │   │       └── test_parse_batch.py
│   │   └── explore/
│   │       ├── instructions.md
│   │       ├── references/
│   │       │   ├── explore-capture.md
│   │       │   ├── explore-collections.md
│   │       │   └── explore-media.md
│   │       └── scripts/
│   │           ├── explore_capture.py
│   │           ├── media_extract.py
│   │           ├── test_explore_capture.py
│   │           ├── test_explore_collections.py
│   │           └── test_media_extract.py
│   └── references/
│       ├── kernel-contract.md
│       ├── vault-bootstrap.md
│       ├── note-operations.md
│       ├── research-to-pkm.md
│       ├── toolkit.md
│       └── plugin-and-query-workflows.md
└── periplus/
    ├── SKILL.md
    ├── VERSION
    ├── agents/
    │   └── openai.yaml
    ├── assets/
    │   ├── icon.svg
    │   └── Seven_Ninths_Master_Skeleton.md
    ├── examples/
    │   ├── natural_language_requests.md
    │   └── trip_request.json
    ├── prompts/
    ├── references/
    │   ├── request.schema.json
    │   ├── content_specifications.md
    │   ├── around_area.md
    │   ├── itinerary_engine.md
    │   ├── source_protocol.md
    │   ├── legacy_layout_contract.md
    │   ├── multilingual_names_and_pronunciation.md
    │   ├── media_acquisition_and_maps.md
    │   ├── filename_and_date_periods.md
    │   ├── reader_contract.md
    │   ├── service_selection.md
    │   ├── kobe_reference_contract.md
    │   ├── coverage_matrix.md
    │   └── delivery_qa.md
    └── scripts/
        ├── generate.py
        ├── export_brochure.py
        ├── fetch_media.py
        ├── map_from_geojson.py
        ├── media_utils.py
        ├── reader_qa.py
        ├── trip_dates.py
        ├── version.py
        ├── validate.py
        └── test_skill.py
```

Each skill directory directly under the repository root is self-contained and
installable. Its entry point must be `SKILL.md`.

## ➕ Adding a new skill

Use this checklist whenever a new skill joins Asterion Skills:

1. Choose a lowercase, hyphen-separated skill name, such as
   `workflow-automator`.
2. Create a self-contained directory at `<skill-name>/` directly under the
   repository root.
3. Put the required `SKILL.md` at the root of that directory.
4. Add `agents/openai.yaml` for user-facing skill metadata.
5. Add only the supporting directories the skill actually needs, such as
   `references/`, `scripts/`, `assets/`, `prompts/`, or `examples/`.
6. Validate the complete skill directory with the current official skill
   validator.
7. Test at least one realistic invocation before publishing.
8. Audit the new files for credentials, private data, absolute local paths,
   internal identifiers, caches, and project-specific residue.
9. Update this README using the maintenance checklist below.

Do not put a separate `README.md`, installation guide, changelog, or other
repository-facing documentation inside an installable skill directory. Keep
those materials at the Asterion Skills repository level. Periplus keeps a short
`README.md` and `INSTALL.md` because its instructions and Codex installers
already refer to them; collection discovery still lives in this README.

### README maintenance checklist

For every newly onboarded skill, update:

1. **Available skills** — add a heading with the skill's name, purpose, main
   capabilities, and any important trigger or limitation.
2. **Repository structure** — add the new `<skill-name>/` tree and list
   its meaningful bundled resources.
3. **Installation** — mention any installation detail that differs from the
   standard “copy the complete skill folder” procedure.
4. **Usage** — add one short, realistic invocation example.
5. **Output model** — add a skill-specific output section only when its outputs
   are not already clear from the capability summary.
6. **License or attribution** — update this only when the new skill includes
   third-party material or has requirements beyond the repository license.

Keep the README concise. Describe what users need to discover, install, and
invoke each skill; keep operational instructions for the AI agent inside that
skill's `SKILL.md` and bundled references.

## <a id="installation"></a>📥 Installation

Copy the complete folder for the skill you want to install into a skills
directory supported by your ChatGPT or Codex environment.

**💥 BigBang** — copy:

```text
bigbang/
```

**🔶 Amber Kernel** — copy:

```text
amber-kernel/
```

**🧭 Periplus** — copy:

```text
periplus/
```

Do not copy only `SKILL.md`. BigBang and Amber Kernel rely on their
`references/` files. Periplus also relies on `prompts/`, `examples/`,
`assets/`, and `scripts/`.

Periplus includes `install_codex.ps1` and `install_codex.sh` for installing a
packaged ZIP into the local Codex skills directory. Inside this repository,
copying the `periplus/` folder is the install path. Rendering the brochure
needs Python with `python-docx`, `markdown-it-py`, `Pillow`, and `pymupdf`,
plus LibreOffice for DOCX-to-PDF. English type is Oswald; install that font
on the rendering computer before publishing. The command-line runner also
needs an authenticated Codex CLI with web research available.

The exact installation location depends on the environment in which the skill
will run. After installation, confirm that the entry file is available at:

```text
<skills-directory>/bigbang/SKILL.md
<skills-directory>/amber-kernel/SKILL.md
<skills-directory>/periplus/SKILL.md
```

## <a id="usage"></a>▶️ Usage

### 💥 BigBang

> Use `$bigbang` to transform this student proposal into a complete
> InnovationLab project and teaching pack.

> Use `$bigbang` to evaluate this app concept and create a realistic project
> plan with session-based implementation prompts.

> Use `$bigbang` to rebuild this ESP32 proposal into a complete hardware project
> pack, including wiring, bring-up, testing, and safety guidance.

> Use `$bigbang` to create a competition version of this project.

BigBang adds competition-specific materials only when the request explicitly
places the project in a competition context.

### 🔶 Amber Kernel

> Use `$amber-kernel` to parse LandingField in my vault, following its existing
> conventions and preserving my original thinking.

> Use `$amber-kernel` to parse this batch and develop the rough ideas, without
> integrating their substance into existing notes.

> Use `$amber-kernel` to parse these sources and integrate relevant contributions
> into existing notes.

> Use `$amber-kernel` to initialize an empty Obsidian vault with the smallest
> useful foundation.

> Use `$amber-kernel` to turn these sources into durable notes without creating
> a second taxonomy.

> Use `$amber-kernel` to add a Bases view for active projects using the locked
> property schema.

> `$amber-kernel explore https://example.org/article` — read the page, trace
> relevant evidence, and save a cited note in LandingField. Replace the example
> URL with the real target.

> `$amber-kernel explore https://example.org/paper` — focus on the methodology
> and limitations; explain in Chinese.

> `$amber-kernel explore https://www.youtube.com/@CHANNEL` — inventory all videos,
> extract knowledge from every accessible item, and save a cited capture in LandingField.
> Large channels continue in resumable batches with explicit coverage and pending work.
> Replace CHANNEL with the intended creator's handle.

> `$amber-kernel explore VIDEO_URL` — focus on the mechanisms, inspect speech
> and relevant visuals, and cite timestamps. Replace VIDEO_URL with the target.

### 🧭 Periplus

> `$periplus` Prepare Kyoto, Japan for November 5–11, 2026. Outbound by
> shinkansen from Tokyo Station to Kyoto Station. Return by shinkansen from
> Kyoto Station to Osaka Station. Hotel: booked hotel name and address, if
> known. Focus on architecture, museums, trains, photography, and minimal walking.

A service number is optional. The same request can be written in Chinese,
Japanese, or another language. The brochure stays in Simplified Chinese unless
the request names another output language. Split stays keep every date period
in the published filename.

## 💥 BigBang output model

Depending on the request, BigBang can produce:

- Project and feasibility plans
- Architecture and requirements-traceability documents
- Session-based tutoring plans
- Kickoff and start-from-scratch guides
- Initialization and implementation prompt packs
- Student and teacher guides
- Testing, deployment, and recovery documentation
- Research, presentation, and demonstration materials
- Starter workspaces and packaged deliverables
- Hardware documentation for projects involving physical modules

The exact deliverables and session count are determined by the project workload.
BigBang does not impose a fixed 20-session plan and does not label a complete
project as an MVP unless the source proposal or user explicitly requires MVP
scope.

## 🔶 Amber Kernel output model

Depending on the request, Amber Kernel can produce:

- A locked convention fingerprint and path map
- Vault audits and incremental restructure plans
- Intake digests, meaningful links, and a receipt of filed or deferred items
- Recoverable local edit plans and journals for intake and file moves
- New or updated notes, templates, daily notes, and attachments
- Source, atomic, synthesis, map-of-content, and project notes
- Canvas, Bases, Search, and plugin-query artifacts
- Theme, snippet, or cssclass changes only when appearance work is requested

Amber Kernel reports the lock, map, changed vault-relative paths, and unresolved
risks. It does not install plugins or send vault content to external services
unless the user explicitly authorizes that action.

Run the deterministic helper tests from the repository root with:

```text
python amber-kernel/scripts/run_tests.py
```

## 🧭 Periplus output model

A finished Periplus 2.5.0 run produces a trip project whose public files are named from the year, country, city, and every date period:

- `2026.Japan.Tokyo.0711-0712.0717-0719.docx`
- `2026.Japan.Tokyo.0711-0712.0717-0719.pdf`

The internal manuscript stays at `exports/Seven_Ninths_Travel_Brochure.md`. A public Markdown copy uses the same date-based filename only when the traveler asks for Markdown.

The guide keeps the Seven Ninths cover, a clickable three-level contents table with real page numbers, the header **Seven Ninths Travel Brochure** on every page, and a current/total page footer. Every level-1 and level-2 heading starts a new page. Each catalogue entry has its own licensed photo. Hotels also have an access map, and each area has a geographic map. Credits live in `research/MEDIA_MANIFEST.json`. English text uses Oswald. The guide does not include the assistant's internal reasoning.

Working files may include a normalized request, a task record, an evidence ledger, an entry catalogue, and a quality report. A supplied booked hotel is the travel base. Hotel and transport recommendations stay labeled as unbooked.

Run the release tests from the repository root with:

```text
python -m unittest discover -s periplus/scripts -p "test_*.py"
```

## <a id="contributing"></a>🛠️ Contributing

Contributions are welcome when they preserve the following principles:

1. Keep each skill self-contained.
2. Place its `SKILL.md` at the root of its skill folder.
3. Keep reusable detailed guidance in `references/`, deterministic helpers in
   `scripts/`, output resources in `assets/`, and phase prompts or examples
   only when the skill actually uses them.
4. Do not include credentials, private or personal information, local absolute
   paths, internal skill identifiers, generated caches, or project-specific
   residue.
5. Validate changes before submitting them.
6. Keep user-facing examples and documentation in English by default.

When proposing changes to BigBang, preserve the student's intellectual ownership
and keep baseline requirements distinguishable from recommended refinements.

When proposing changes to Amber Kernel, preserve the lock-then-adapt gate and
keep observed vault conventions distinguishable from adopted ones.

When proposing changes to Periplus, keep autonomous brochure generation, the
Seven Ninths section coverage, source traceability, one licensed photo per
catalogue entry, date-period filenames, and the DOCX plus PDF completion gate.
Do not turn a missing journey endpoint, an unreadable source, or a failed
export into invented facts or a claimed final guide.

## 📄 License

The Asterion Skills collection is available under the
[MIT License](LICENSE.md).
