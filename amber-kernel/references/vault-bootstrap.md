# Vault bootstrap

Use this workflow to discover an unfamiliar vault, initialize an empty vault, or plan a structural redesign.

## Discover the current system

1. Locate the vault root by `.obsidian/` or explicit user identification.
2. Inventory top-level folders and counts of `.md`, `.canvas`, `.base`, and attachment formats. Exclude `.obsidian`, `.trash`, `.git`, and caches from content analysis.
3. Inspect relevant configuration:
   - `app.json` for file/link behavior and default locations.
   - `core-plugins.json` for available native workflows.
   - `community-plugins.json` and installed plugin manifests for optional semantics.
   - Daily Notes, Templates, attachment, and unique-note settings when present.
4. Sample multiple notes from each major folder plus templates. Record observed filename, link, frontmatter, heading, tag, and date conventions.
5. Identify operational risks: duplicate basenames, unresolved links, inconsistent property types, orphaned attachments, invalid Canvas JSON, and invalid Base YAML.

Summarize the result as a convention fingerprint, not a content dump. Lock that fingerprint before initializing, extending, or migrating anything.

## Choose a bootstrap mode

- **Empty vault:** lock the smallest useful foundation, then create only the parts needed now.
- **Existing coherent vault:** extend its conventions; avoid a parallel taxonomy.
- **Existing inconsistent vault:** propose phases and a dry-run migration map before changing paths or metadata.
- **Imported vault:** separate source preservation from later normalization.

## Minimal empty-vault foundation

Use the user's preferred system when provided. Otherwise propose this neutral starting point, lock it as the adopted contract, and create only the parts needed now:

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

## Establish navigation

- Provide one obvious entry note or map of content when the user wants guided navigation.
- Prefer links and properties that serve retrieval over decorative metadata.
- Use folders for lifecycle or ownership boundaries, links for relationships, and properties for queryable facts.
- Keep tags few and purposeful; avoid duplicating the full folder hierarchy as tags.
- Configure Daily Notes, Templates, and attachments through documented settings or clear user instructions. Do not modify workspace layout files.

## Restructure safely

1. Define the desired end state and lock it as the kernel contract.
2. Produce a vault-relative `source -> destination` mapping onto that lock.
3. Detect collisions, case-only renames, duplicate basenames, and affected references.
4. Apply a small representative batch first when the migration is broad.
5. Validate links and queries before continuing.
6. Leave a concise migration record in the task response; create a vault note only if requested.

Prefer incremental changes that keep old retrieval paths working through aliases or updated links.
