---
name: amber-kernel
description: Operate Obsidian vaults in place with parse for incoming ideas and documents, and explore for deeper URL or multimedia research saved to intake. Explore pages, files, images, audio, videos, and YouTube channels through available extraction tools with cited evidence and explicit coverage. Also use for tagging, linking, filing, optional development and integration, note operations, templates, attachments, Canvas, Bases, Search, and installed plugin or appearance workflows. Do not use for ordinary Markdown outside an Obsidian vault.
---

# Amber Kernel

Operate the user's Obsidian vault while preserving their intent, voice, conventions, graph integrity, and local-first privacy. Do not impose a second-brain framework or infer a taxonomy from folder names alone.

Existing vaults are adopted in place. Routine work never creates, renames, merges, or deletes directories. Requested file moves and intake batches may use existing destinations after a dry-run mapping and reference checks. Empty-vault bootstrap and explicitly requested structural redesign are separate tasks.

## Route the task

Read only the references needed for the request:

- Always read [kernel-contract.md](references/kernel-contract.md) before changing a vault or recommending a broad redesign.
- Read [vault-bootstrap.md](references/vault-bootstrap.md) when discovering, auditing, initializing, or discussing structure.
- Read [parse.md](references/parse.md) when the user invokes parse or asks to digest, tag, connect, or file incoming ideas and documents. Development and substantive integration are optional and off unless requested or covered by an explicit standing preference.
- Read [explore.md](references/explore.md) when the user invokes `explore <url>` or asks to investigate a URL and save its knowledge in the vault. Read the target and supporting sources, then create one cited intake note. For files, images, audio, videos, channels, playlists, or mixed media, also read [explore-media.md](references/explore-media.md). This does not automatically invoke parse.
- Read [note-operations.md](references/note-operations.md) when creating, editing, moving, renaming, deleting, linking, templating, or changing properties, Canvas, or Bases files.
- Read [research-to-pkm.md](references/research-to-pkm.md) when converting sources, PDFs, web research, meeting material, or raw captures into durable notes.
- Read [plugin-and-query-workflows.md](references/plugin-and-query-workflows.md) when working with core plugins, community plugins, Search, Bases, Dataview, Tasks, Templater, query-driven views, themes, snippets, or cssclasses.

Read multiple references when the task crosses those boundaries.

Read [toolkit.md](references/toolkit.md) before using deterministic helpers. For parse manifests, saved plans, and recovery, also read [parse-runtime.md](references/parse-runtime.md).

## Execute

1. Resolve the vault root, normally the nearest directory containing `.obsidian/` or the directory explicitly identified by the user.
2. Inspect relevant settings and representative files before inferring conventions. Do not treat one note as a complete schema.
3. Record the relevant convention fingerprint and directory snapshot. A “lock” in supporting workflows means this scoped record, not a permanent design decision or an extra approval gate. Reuse it while evidence still matches.
4. Establish affected files and a validation baseline. Show the dry-run mapping and collision findings before moves; a requested processing batch already authorizes its routine edits, moves, and reference repairs.
5. Apply the smallest coherent change. Preserve unrelated content, unknown fields, formatting, and application-managed state. Use the saved-plan runtime for intake edits and moves so originals remain recoverable.
6. Validate affected formats and references against the baseline; compare directory snapshots. Defer uncertain items with reasons while completing independent clear work.
7. Return a concise receipt of created, edited, moved, and unresolved files, plus any developed or integrated material.

Do not install plugins, contact external services, publish notes, or alter Sync behavior unless the user explicitly authorizes that action.

An explicit explore request authorizes reading the supplied URL, relevant public supporting sources, focused public searches, and creation of the intake note. It does not authorize external transmission of private vault content, sign-in, or other external mutations.
