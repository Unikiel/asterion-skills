# Kernel contract

Apply this contract to every vault mutation and every broad structural recommendation.

## Authority

1. Follow the user's stated goal and boundaries.
2. Preserve explicit vault rules, templates, schemas, and established local conventions.
3. Prefer current Obsidian-native formats and official behavior.
4. Introduce a new convention only when the vault has none or the user requests a redesign.

Do not silently reinterpret a user's organizational system. Surface conflicts and choose the narrowest assumption that keeps work moving.

## Lock then adapt

Do not create, rewrite, move, rename, or delete vault content until a kernel contract is locked and the affected paths are mapped onto it. Read-only discovery and audits may stop after the fingerprint.

Reuse a lock from this conversation when it still matches vault evidence. Relock when the request changes folders, note types, templates, tags, link style, daily-note rules, or appearance conventions.

State the lock in the task response. Scope it to the conventions the change depends on. Use a full fingerprint for bootstrap, redesign, research intake, or taxonomy work:

```text
Vault root:
Mode: empty | coherent | inconsistent | imported
Folders:
Note types:
Properties:
Links:
Tags:
Templates:
Daily notes:
Attachments:
Plugins in play:
Appearance:
Observed vs adopted:
Exclusions:
Path map:
```

- **Observed** fields come from the vault.
- **Adopted** fields are new conventions being introduced now.
- Adopt a new convention only when that slot is empty or the user requested a redesign.
- Map existing notes onto the locked contract. Do not create a parallel taxonomy.
- Preserve wording, filenames, and links unless the user asked for a rewrite or the map requires a path change.

## Invariants

- Keep the vault usable as local files without requiring a cloud service.
- Preserve valid Markdown, YAML frontmatter, JSON Canvas, and Base YAML.
- Preserve unrelated note content, unknown properties, unknown Canvas/Base fields, and user ordering where practical.
- Keep internal references resolvable after moves, renames, and deletions.
- Use vault-relative paths with `/` inside Obsidian links, including on Windows.
- Maintain the established property type for a property name across the vault.
- Keep filenames portable. Avoid `# | ^ : %% [[ ]]` in link targets and operating-system-invalid filename characters.
- Treat private vault content as private. Send content to an external service only with explicit authorization.

## Inspect before acting

- Confirm the vault root and affected paths.
- Inspect `.obsidian/app.json`, enabled core/community plugin lists, and only the plugin settings relevant to the task.
- Sample neighboring notes and applicable templates to infer link style, property schema, tag style, date format, headings, attachment location, and naming.
- Check destination collisions, duplicate basenames, and incoming references before moving or renaming.
- Distinguish observed conventions from proposed ones.
- Write the lock and path map before the first mutation.

## Mutation discipline

- Do not mutate until the lock and map are stated.
- Make the smallest coherent edit set.
- Never overwrite a same-named note without inspecting it and choosing an explicit merge or replacement strategy.
- Do not mass-normalize formatting or metadata during a focused task.
- Treat `.obsidian/workspace*.json`, caches, Sync state, and plugin-generated state as application-managed. Edit them only when explicitly requested and the schema is understood.
- Do not install, enable, disable, or configure plugins unless requested.
- Scope bulk operations with a dry-run mapping and collision report before applying them.
- Treat deletion, broad rewrites, and taxonomy migrations as destructive; confirm unclear scope and prefer recoverable deletion.

## Validation contract

After a change:

1. Parse or structurally inspect each changed format.
2. Check changed wikilinks, Markdown links, embeds, Canvas file nodes, and Base references.
3. Verify that Canvas node/edge IDs remain unique and every edge endpoint exists.
4. Verify that properties remain valid YAML with unique top-level keys.
5. Compare new integrity findings with the pre-change state so pre-existing issues are not reported as regressions.
6. Report the locked contract, path map, created, edited, moved, and deleted vault-relative paths, plus unresolved risks.
