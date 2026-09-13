# Note operations

Operate only after the kernel contract is locked. Reuse the current lock and do not invent a second schema. Use the vault's observed conventions when multiple Obsidian-supported forms exist.

## Properties and Markdown

Place properties as YAML frontmatter at the beginning of a note:

```yaml
---
aliases:
  - Alternate title
tags:
  - project
status: active
related:
  - "[[Another note]]"
created: 2026-08-15
reviewed: false
---
```

- Keep each property key unique within a note.
- Preserve types across the vault: text, list, number, boolean, date, date-time, or tags.
- Quote wikilinks in YAML values.
- Use `aliases`, `tags`, and `cssclasses`; do not introduce deprecated singular keys.
- Keep property values atomic; Markdown formatting is not rendered there.

Use `[[Note]]` or URL-encoded Markdown links according to the vault setting. Use vault-relative `/` paths. Link to headings with `[[Note#Heading]]`, blocks with `[[Note#^block-id]]`, and alternate display text with `[[Note|label]]`. Prefix with `!` for embeds.

Official references: [Properties](https://obsidian.md/help/properties), [Internal links](https://obsidian.md/help/links), [Embed files](https://obsidian.md/help/embeds), and [Callouts](https://obsidian.md/help/callouts).

## Create

1. Resolve the intended folder and filename against vault conventions.
2. Check for same-name and same-topic notes before creating.
3. Reuse the applicable template and property schema.
4. Add only meaningful links and metadata.
5. Validate frontmatter and link targets.

## Edit or merge

- Preserve the author's voice and unrelated sections.
- Merge properties by semantic role and type; do not concatenate incompatible values.
- Avoid duplicate headings and repeated content.
- When combining notes, preserve source paths through updated links or aliases as appropriate.

## Move or rename

Use the saved-plan runtime described in [parse-runtime.md](../subskills/parse/references/parse-runtime.md), including for single-note moves through `amber_kernel.py move-note`. Applying a move requires an existing state directory outside the vault on the same filesystem. Do not fall back to raw filesystem moves when the helper defers an ambiguous or unsupported reference.

1. Check destination collisions, case-only behavior, duplicate basenames, and target filename safety.
2. Find incoming wikilinks, Markdown links, embeds, Canvas file nodes, and Base/plugin queries containing the old path.
3. Move the file and update only references that resolve to that file; preserve display text and aliases.
4. Validate old and new path references. Raw filesystem moves do not guarantee Obsidian's in-app link-update behavior.

## Delete

- Confirm the exact target when scope is not explicit.
- Check backlinks, embeds, Canvas nodes, queries, and attachments that depend on it.
- Prefer the vault/system trash when practical.
- Do not delete an attachment solely because one reference was removed; confirm that no other note uses it.

## Templates and daily notes

- Read the configured template and daily-note folders before creating files.
- Preserve supported template tokens literally unless the active templating engine is known.
- Match the configured daily-note filename format and location.
- Merge template properties with existing frontmatter rather than creating a second YAML block.

## Canvas

Treat `.canvas` as JSON Canvas. Preserve unknown fields. Keep node and edge IDs unique, ensure every edge endpoint names an existing node, and use vault-relative file paths for file nodes. Common node types are `text`, `file`, `link`, and `group`.

Validate JSON after every edit. Official specification: [JSON Canvas 1.0](https://jsoncanvas.org/spec/1.0/).

## Bases

Treat `.base` as YAML. Preserve unknown and view-specific fields. Common top-level keys include `filters`, `formulas`, `properties`, `summaries`, and `views`. Validate referenced note, file, and formula properties against the vault.

Do not substitute Dataview syntax for native Bases syntax. Official references: [Bases](https://obsidian.md/help/bases) and [Bases syntax](https://obsidian.md/help/bases/syntax).
