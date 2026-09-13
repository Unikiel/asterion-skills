# Deterministic toolkit

Use `scripts/amber_kernel.py` when its command matches the task. It emits JSON, is dry-run by default, requires `--apply` for writes, rejects destinations whose parent directory does not already exist, and never edits `.obsidian` configuration.

Run `python scripts/amber_kernel.py --help` or a subcommand with `--help` for exact arguments.

## Capability map

| Workflow | Command | Mutation behavior |
| --- | --- | --- |
| Discover conventions and settings | `inspect VAULT` | Read-only |
| Link, YAML, Canvas, and Base audit | `inspect VAULT --audit` or `validate VAULT` | Read-only; `validate` exits 2 on findings |
| Empty-vault foundation | `bootstrap DIRECTORY` | Refuses any non-empty target |
| Create or template a note | `create-note VAULT PATH` | Existing parent only; refuses overwrite |
| Tags, aliases, and other properties | `set-properties VAULT PATH` | Refuses a type change for an existing property |
| Append without rewriting unrelated text | `append-note VAULT PATH TEXT` | Existing file only |
| Move or rename one note | `move-note VAULT SOURCE DESTINATION --plan-output PLAN` | Saved-plan reference repair; applying requires an external `--state-dir` on the same filesystem |
| Daily note | `daily-note VAULT` | Reads Daily Notes settings; existing parent only |
| Copy and embed an attachment | `attach VAULT NOTE SOURCE` | Uses configured or explicit existing attachment directory |
| Create JSON Canvas | `create-canvas VAULT PATH` | Existing parent only; validates IDs and endpoints |
| Create native Base YAML | `create-base VAULT PATH --yaml ...` | Existing parent only; preserves native YAML semantics |
| Store Obsidian Search | `write-query VAULT PATH QUERY` | Creates in existing parent or appends when requested |
| Source/research capture | `research-source VAULT PATH --title ...` | Creates provenance-separated source note in existing parent |
| Cross-source synthesis | `synthesis-note VAULT PATH --title ... --source ...` | Requires every source link to resolve uniquely |
| Inspect plugin capabilities | `plugins VAULT` | Read-only; reports manifests and enabled state |

The helper does not install or configure plugins, call external services, delete content, create folders in an existing vault, or perform broad migrations. Handle richer synthesis and plugin-specific query authoring through the relevant reference workflow after inspecting the vault.

For parse batches, use `subskills/parse/scripts/parse_batch.py` as documented in [parse-runtime.md](../subskills/parse/references/parse-runtime.md). It accepts agent-authored semantic decisions, validates a saved edit plan, preserves originals in an external journal, and supports repeat-safe application and recovery. Single-note moves use this same engine. Routine single-file commands other than moves retain their simpler dry-run/apply behavior; they do not provide batch journals.

For URL explorations, research through available web/browser tools following [explore.md](../subskills/explore/instructions.md), then use `subskills/explore/scripts/explore_capture.py VAULT REPORT.json` to preview and add `--apply` to create the note. See [explore-capture.md](../subskills/explore/references/explore-capture.md) for source-ledger validation, coverage status, duplicate handling, and explicit revisits. This writer makes no network requests and needs no parse recovery state for creating a new file.

## Safe execution

For multimedia exploration, `subskills/explore/scripts/media_extract.py` provides URL routing hints, local text/document/caption extraction, timestamp links, and capability discovery. It never downloads media or pretends to transcribe or inspect images. Follow [explore-media.md](../subskills/explore/references/explore-media.md) to use actual media tools and declare gaps.

1. Run `inspect --audit` and retain its result as the baseline.
2. Run the desired mutation without `--apply`; review the reported paths and reference updates.
3. For intake and moves, apply the saved plan through `python subskills/parse/scripts/parse_batch.py apply PLAN --state-dir STATE --apply`. For other commands, run again with `--apply` only when the preview matches the request.
4. Run `validate` and compare findings with the baseline.
5. Verify the directory snapshot is unchanged.

The tools require Python 3.10+ and PyYAML. The batch runtime additionally requires an existing local state directory outside the vault on the same filesystem for atomic writes. It reports unsupported dependencies instead of treating simple substitutions as complete reference repair.
