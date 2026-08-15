---
name: amber-kernel
description: Operate Obsidian vaults as durable personal knowledge systems. Use for vault bootstrapping, convention lock and vault mapping, Markdown note creation and editing, YAML properties, wikilinks, embeds, tags, aliases, templates, daily notes, attachments, research capture and synthesis, note moves or renames, link integrity, JSON Canvas (.canvas), Bases (.base), Obsidian Search, themes, snippets, cssclasses, and installed plugin or query workflows. Do not use for ordinary Markdown outside an Obsidian vault.
---

# Amber Kernel

Manage an Obsidian vault as a coherent knowledge system while preserving its conventions, graph integrity, and local-first privacy.

## Route the task

Read only the references needed for the request:

- Always read [kernel-contract.md](references/kernel-contract.md) before changing a vault or recommending a broad redesign.
- Read [vault-bootstrap.md](references/vault-bootstrap.md) when discovering, auditing, initializing, or restructuring a vault.
- Read [note-operations.md](references/note-operations.md) when creating, editing, moving, renaming, deleting, linking, templating, or changing properties, Canvas, or Bases files.
- Read [research-to-pkm.md](references/research-to-pkm.md) when converting sources, PDFs, web research, meeting material, or raw captures into durable notes.
- Read [plugin-and-query-workflows.md](references/plugin-and-query-workflows.md) when working with core plugins, community plugins, Search, Bases, Dataview, Tasks, Templater, query-driven views, themes, snippets, or cssclasses.

Read multiple references when the task crosses those boundaries.

## Execute

1. Resolve the vault root, normally the nearest directory containing `.obsidian/` or the directory explicitly identified by the user.
2. Inspect relevant settings and representative files before inferring conventions. Do not treat one note as a complete schema.
3. Lock the kernel contract before any write. State the fingerprint, distinguish observed conventions from adopted ones, and map affected paths onto that lock.
4. Establish the requested outcome, affected vault-relative paths, invariants, and validation checks.
5. Only then make the smallest coherent change. Preserve unrelated content, unknown fields, formatting conventions, and application-managed state.
6. Validate every changed format and check references affected by creates, moves, renames, or deletions.
7. Report the locked contract, path map, changed vault-relative paths, important decisions, and unresolved risks.

Do not install plugins, contact external services, publish notes, or alter Sync behavior unless the user explicitly authorizes that action.
