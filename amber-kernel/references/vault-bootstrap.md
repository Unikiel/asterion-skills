# Vault bootstrap

Use this workflow to discover an unfamiliar vault, initialize an empty vault, or discuss a structural redesign without applying one to an existing vault.

## Discover the current system

1. Locate the vault root by `.obsidian/` or explicit user identification.
2. Snapshot the complete directory tree. Inventory top-level folders and counts of `.md`, `.canvas`, `.base`, and attachment formats. Exclude `.obsidian`, `.trash`, `.git`, and caches from content analysis.
3. Inspect relevant configuration:
   - `app.json` for file/link behavior and default locations.
   - `core-plugins.json` for available native workflows.
   - `community-plugins.json` and installed plugin manifests for optional semantics.
   - Daily Notes, Templates, attachment, and unique-note settings when present.
4. Sample multiple notes from each major folder plus templates. Record observed filename, link, frontmatter, heading, tag, and date conventions.
5. Identify operational risks: duplicate basenames, unresolved links, inconsistent property types, orphaned attachments, invalid Canvas JSON, and invalid Base YAML.

Summarize the result as a convention fingerprint, not a content dump.

## Choose an operating mode

- **Empty directory:** offer the minimal foundation below; apply it only after the user accepts or explicitly requests initialization.
- **Existing coherent vault:** adopt it in place and extend only its existing conventions and directories.
- **Existing inconsistent vault:** report inconsistencies and offer non-structural, file-local repairs. A proposed alternate structure may be discussed, but do not apply it.
- **Imported vault:** preserve the import boundary and current directory tree. Normalize content only within existing files and directories after verification.

The presence of `.obsidian/`, any user content, or any existing directory makes the target an existing vault for structure-preservation purposes.

## Minimal empty-vault foundation

Use the user's preferred system when provided. Otherwise propose this neutral starting point and create only the parts needed now:

```text
Inbox/
Notes/
Projects/
Sources/
Daily/
Templates/
Attachments/
```

Keep the initial schema small. A practical baseline is:

```yaml
---
aliases: []
tags: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: active
---
```

Do not add every property to every note. Define note-type templates only after repeated usage demonstrates stable fields.

## Establish navigation non-invasively

- Add an entry note or map of content only in an existing directory selected from observed conventions.
- Prefer links and properties that serve retrieval over decorative metadata.
- Use the vault's current folder roles; do not overlay a new lifecycle or ownership hierarchy.
- Keep tags few and purposeful; avoid duplicating the full folder hierarchy as tags.
- Do not create new folders for Daily Notes, Templates, or attachments in an existing vault. Use configured existing locations or ask the user to create/configure them in Obsidian.
- Do not modify workspace layout files.

## Structural redesign requests

Routine adoption and parse do not restructure directories. Requested file moves or intake batches may use existing directories after collision, basename, and reference checks. Treat an explicit structural redesign request as a separate task governed by that request and applicable permissions; do not infer it from a request to improve or process the vault.

Always compare the post-operation directory snapshot with the baseline. Any difference in an existing vault is a regression.
