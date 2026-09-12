# Kernel contract

Apply this contract to every vault mutation and every broad structural recommendation.

## Authority

1. Follow the user's stated goal and boundaries.
2. Preserve explicit vault rules, templates, schemas, established local conventions, and the existing directory tree.
3. Prefer current Obsidian-native formats and official behavior.
4. Introduce a new convention only in an empty vault or when the user explicitly requests a non-structural convention.

Do not silently reinterpret a user's organizational system. Surface conflicts and choose the narrowest assumption that keeps work moving.

References to a “locked contract” mean a scoped record of observed conventions, explicit user decisions, affected paths, and exclusions. State it concisely before edits and reuse it while evidence matches. It is neither a permanent taxonomy nor a separate permission gate. Absence of a convention does not authorize inventing one during intake.

## Existing-vault structure invariant

For a vault with `.obsidian/` or user content, take the directory tree as immutable:

- Do not create, rename, move, merge, or delete directories.
- Do not scaffold standard folders, add a parallel taxonomy, or normalize paths.
- New notes, attachments, Canvases, and Bases may be placed only in existing directories.
- User-directed moves or renames of specific files may use existing source and destination directories. Repair references and dry-run first.
- Routine operations exclude folder moves and taxonomy migrations. Treat a subsequent explicit structural redesign request as a separate task governed by that request and applicable permissions.
- Do not treat an explicit request to improve the vault as permission to redesign its structure.

Bootstrap scaffolding is permitted only when the target directory is empty.

## Content invariants

- Keep the vault usable as local files without requiring a cloud service.
- Preserve valid Markdown, YAML frontmatter, JSON Canvas, and Base YAML.
- Preserve unrelated note content, unknown properties, unknown Canvas/Base fields, and user ordering where practical.
- Keep internal references resolvable after user-directed file moves and renames.
- Use vault-relative paths with `/` inside Obsidian links, including on Windows.
- Maintain the established property type for a property name across the vault.
- Keep filenames portable. Avoid `# | ^ : %% [[ ]]` in link targets and operating-system-invalid filename characters.
- Treat private vault content as private. Send content to an external service only with explicit authorization.

## Inspect before acting

- Confirm the vault root and affected paths.
- Snapshot the existing directory tree.
- Inspect `.obsidian/app.json`, enabled core/community plugin lists, and only the plugin settings relevant to the task.
- Sample neighboring notes and applicable templates to infer link style, property schema, tag style, date format, headings, attachment location, and naming.
- Check destination collisions, duplicate basenames, and incoming references before moving or renaming a file.
- Distinguish observed conventions from proposed ones.

## Mutation discipline

- Make the smallest coherent edit set and dry-run deterministic mutations.
- Never overwrite a same-named note without inspecting it and choosing an explicit merge or replacement strategy.
- Do not mass-normalize formatting or metadata during a focused task.
- Treat `.obsidian/workspace*.json`, caches, Sync state, and plugin-generated state as application-managed. Edit them only when explicitly requested and the schema is understood.
- Do not install, enable, disable, or configure plugins unless requested.
- Scope bulk content operations with a dry-run mapping and collision report before applying them.
- A requested parse batch authorizes routine source edits, moves between existing directories, and affected-reference repairs. Optional development and substantive integration require a request or an explicit standing preference; do not repeatedly ask after authorization.
- Use recoverable saved plans for parse mutations and note moves. Keep plans, originals, and run state outside the vault in a configured existing directory on the vault's filesystem for atomic writes.
- Treat deletion and broad rewrites as destructive; confirm unclear scope and prefer recoverable deletion.

## Validation contract

After a change:

1. Parse or structurally inspect each changed format.
2. Check changed wikilinks, Markdown links, embeds, Canvas file nodes, and Base references.
3. Verify that Canvas node/edge IDs remain unique and every edge endpoint exists.
4. Verify that properties remain valid YAML with unique top-level keys.
5. Compare new integrity findings with the pre-change state so pre-existing issues are not reported as regressions.
6. Compare the directory snapshot. For an existing vault, any directory change is a regression.
7. Report created, edited, moved, and deleted vault-relative files plus unresolved risks.
