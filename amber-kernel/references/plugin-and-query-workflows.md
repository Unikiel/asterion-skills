# Plugin and query workflows

Use the least powerful mechanism that satisfies the retrieval or automation need.

## Discover capabilities

1. Inspect enabled native plugins in `.obsidian/core-plugins.json`.
2. Inspect enabled community plugin IDs in `.obsidian/community-plugins.json`.
3. Read the relevant installed plugin's `manifest.json` and only the settings/data required for the task.
4. Inspect existing queries and templates before introducing new syntax.

Never infer that a plugin is available merely because a note contains its syntax. Do not install, enable, disable, or update plugins unless requested.

## Choose the mechanism

- Use **links, properties, and folders** for durable structure.
- Use **Obsidian Search** for text, tag, path, link, task, and property retrieval that does not need a stored database view.
- Use **Bases** for native property-driven tables, lists, cards, maps, formulas, filters, grouping, and summaries.
- Use **Dataview** only when it is enabled and the requested transformation exceeds Bases or existing vault conventions already depend on it.
- Use **Tasks** only when it is enabled and task recurrence, dates, or task-specific querying is required.
- Use **Templates** for literal reusable content and **Templater** only when enabled and executable template logic is genuinely needed.

Prefer native features for portability unless the vault intentionally standardizes on a community plugin. Plugin, query, theme, and snippet work must follow the locked kernel contract and must not silently change folders, note types, tags, templates, or link style.

## Obsidian Search

Compose a narrow query from supported operators such as `path:`, `file:`, `tag:`, `property:`, `task:`, and link searches. Inspect the current official syntax before building a complex query because operators evolve.

When embedding search results, use an Obsidian `query` code block and keep the query readable:

````markdown
```query
path:"Projects" tag:#active
```
````

Official reference: [Search](https://obsidian.md/help/search).

## Bases

A `.base` file is YAML. A Base starts from vault files and narrows them with filters; there is no SQL-style source clause. Use note properties, `file.*` properties, and `formula.*` properties according to current native syntax.

```yaml
filters:
  and:
    - file.inFolder("Projects")
    - 'status == "active"'
views:
  - type: table
    name: Active projects
    order:
      - file.name
      - status
```

Preserve view-specific unknown keys and validate YAML. Prefer configuring unfamiliar view options in Obsidian, then inspecting the generated file. Official references: [Bases](https://obsidian.md/help/bases) and [Bases syntax](https://obsidian.md/help/bases/syntax).

## Community plugin queries

- Confirm the exact plugin and version before generating syntax.
- Prefer patterns already present in the vault.
- Keep plugin-specific fields isolated from native properties when their semantics differ.
- Validate a query in the plugin or against its current primary documentation when possible.
- Do not rewrite all stored queries during a focused change.

For Dataview, distinguish DQL, inline expressions, and DataviewJS. Avoid DataviewJS unless script-level capability is required; treat it as executable code. For Tasks and Templater, inspect configured date formats, folders, and user scripts before editing.

## Themes, snippets, and cssclasses

- Inspect the current theme, enabled snippets, and existing `cssclasses` before changing appearance.
- Do not switch themes, add snippets, or restyle the vault during note, research, or query work.
- Prefer `cssclasses` already used in the vault over new class names.
- Treat `.obsidian/snippets/*.css` and theme files as user-owned. Edit them only when the user asks for appearance work.
- Keep appearance changes from altering note structure, templates, or taxonomy.

## Plugin safety

- Treat plugin scripts and templates as executable content.
- Do not copy unknown code into the vault without inspection.
- Avoid embedding secrets, tokens, or machine-specific absolute paths in notes or plugin settings.
- Back up or preserve plugin data before schema-changing edits.
- Report portability costs when a workflow depends on a community plugin.
