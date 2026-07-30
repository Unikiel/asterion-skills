# Start-from-Scratch and Continuity Workflow

## Contents

1. Required artifact
2. Operational model
3. Guide stages
4. One-time audit prompt
5. Unit execution controller
6. Manual acceptance and checkpoints
7. Pause, resume, and rollback
8. Validation gate

## 1. Required artifact

When a formal BigBang pack includes a starter workspace and implementation
prompts, create a separate project-specific operational guide named:

```text
[ProjectName]_Start_From_Scratch_Guide.docx
[ProjectName]_Start_From_Scratch_Guide.pdf
```

The conceptual kickoff preparation guide explains prerequisites and what will
be built. This operational guide explains exactly how to begin, verify, pause,
resume, and recover. Keep both when both are useful; do not merge them into an
ambiguous overview.

The guide must stand alone after download. Do not require the original ChatGPT
conversation. Use English-only ASCII filenames even when the guide content is
in another requested language.

## 2. Operational model

Use this invariant:

```text
prepare -> extract -> open root -> baseline checkpoint -> audit only
        -> activate one unit -> implement -> test -> inspect -> accept
        -> checkpoint -> next unit
```

State which of these two routes applies:

- **Prepared-starter route (default for a packaged BigBang starter):** extract
  the already materialized starter, create the baseline checkpoint, run the
  audit, then begin the first unit. Do not rerun `INIT`.
- **Empty-workspace route:** run the one approved `INIT` prompt exactly once,
  verify its structure, create the initialized baseline checkpoint, run the
  audit, then begin the first unit.

Never combine both routes or ask `INIT` to overwrite a prepared starter.

Only one implementation unit may be active. Store the full approved unit
checklist in one persistent `TASKS.md`. Store unit prompts as separate files.
Never ask the user to paste every prompt at once or replace `TASKS.md` with a
fresh template at each session.

The coding agent assists implementation; the student or teacher owns acceptance.
At least one relevant test or manual check must be personally run and understood
by the student before a unit is closed.

## 3. Guide stages

Adapt these stages to the approved stack, operating systems, and coding agent.
Do not include commands that were not checked against the actual starter.

### Stage A - Prepare the machine

- List required tools and supported versions.
- Provide exact version-check commands.
- Identify optional tools separately.
- Record actual versions in `docs/EnvironmentRecord.md`; never invent missing
  results.

### Stage B - Extract the starter safely

- Copy the complete starter directory to a simple local path with English-only
  characters.
- State explicitly that the packaged starter is already initialized and that
  `INIT` is retained as the reproducible scaffolding contract, not a prompt to
  rerun against those files.
- Do not develop inside the ZIP or an automatically synchronized folder when
  that may cause file locking, path, or generated-file problems.
- Show the expected initial tree and the files that prove the correct root was
  opened.

### Stage C - Open and verify the project root

- Open the directory containing `README.md` and `TASKS.md`.
- Provide operating-system-appropriate listing and path checks.
- Stop if the expected control files are absent.

### Stage D - Create the baseline checkpoint

- Initialize version control when the starter is not already a repository.
- Add the approved starter, create a baseline commit, then verify clean status
  and the checkpoint identifier.
- For the empty-workspace route, execute and verify `INIT` before creating this
  initialized baseline. For the prepared-starter route, do not execute `INIT`.
- If a repository already exists, preserve its history and create an appropriate
  checkpoint without reinitializing it blindly.
- Explain local identity configuration only when the tool requests it.

### Stage E - Run a one-time workspace audit

The first coding-agent interaction is audit-only:

- read the authoritative plan, `README.md`, `TASKS.md`, architecture, test plan,
  decision/co-build logs, and global engineering contract;
- confirm the complete persistent unit checklist and the intended first unit;
- record the real environment;
- inspect for secrets, personal data, conflicting structures, unexpected
  generated files, and setup blockers;
- report files changed and stop;
- do not implement product features or begin the first unit.

Commit the environment record separately after human review.

### Stage F - Execute exactly one unit

Before changes:

- require a clean or truthfully documented working tree;
- record the current checkpoint identifier;
- confirm prerequisite units passed;
- activate only the intended unit in `TASKS.md`;
- preserve completed history, decisions, known issues, failed-test evidence,
  and the full checklist.

During work:

- follow the unit prompt and global contract;
- keep changes within scope;
- leave the project runnable after each small step;
- save evidence under a predictable path such as `evidence/[UnitID]/`;
- update the required logs.

At the boundary:

- run the specified automated and manual checks;
- report actual results and changed files;
- stop before the next unit.

### Stage G - Review and accept manually

The guide must tell the user how to inspect repository status and the actual
diff. Provide a project-specific checklist covering:

- only intended files changed;
- `TASKS.md` still contains every approved unit;
- only the active unit changed state;
- required evidence exists;
- no future-unit work, secret, or real personal data was added;
- the student can explain the change and has completed assigned manual work.

If every criterion passes, commit and optionally tag the verified checkpoint.
If any criterion fails, keep the current unit active, record the failure, and
repair only that unit. Never mark a unit complete merely because the coding
agent says it is complete.

### Stage H - Advance

Activate the next approved unit only after the current checkpoint passes.
Repeat the same controller pattern through the final release gate.

## 4. One-time audit prompt

Generate a project-specific prompt from this contract:

```text
Read the listed project-control and design files completely before acting.
Inspect the initialized workspace and report its actual structure.
Confirm the persistent approved unit checklist and the intended first unit.
Record only environment versions that are actually available.
Check for secrets, personal data, unexpected generated files, and structural
conflicts. Report blockers and files changed.
Do not implement product features. Do not begin the first unit.
Stop after the workspace audit.
```

List exact existing paths. Do not retain filenames from another project.

## 5. Unit execution controller

Generate a short controller prompt for each unit or a clearly parameterized
reusable controller:

```text
Begin [Project Name] [Unit ID] only.
Read the authoritative control files, global contract, and [Unit ID] prompt.
Before changes, confirm repository status, the checkpoint identifier,
prerequisites, and the active unit. Activate [Unit ID] in TASKS.md without
overwriting history. Execute only [Unit ID], run its checks, save evidence
under [evidence path], update the required logs, report changed files and
actual results, and stop before [Next Unit ID].
```

The controller does not replace the detailed unit prompt.

## 6. Manual acceptance and checkpoints

For every unit, specify:

- pre-unit checkpoint identifier;
- expected changed-file boundary;
- automated checks and exact commands;
- manual checks and responsible person;
- evidence path and minimum evidence;
- pass/fail decision rule;
- successful commit message pattern;
- optional checkpoint tag pattern;
- exact behavior after failure.

Do not prescribe `git add .` when broad staging could capture secrets,
unrelated work, large data, or generated artifacts. Prefer reviewing status and
staging intended paths explicitly. Use broad staging only when the verified
starter and project policy make it safe.

## 7. Pause, resume, and rollback

### Pause

The pause instruction must require:

1. current unit and completed steps;
2. changed files and uncommitted work;
3. tests run with actual results;
4. blockers and known issues;
5. exact next safe action;
6. checkpoint or rollback recommendation;
7. truthful updates to `TASKS.md` and the co-build log.

Do not mark the unit complete unless every acceptance criterion passed. Create
a local WIP checkpoint only when the partial state is coherent and the project
policy allows it.

### Resume

On return:

- open the same project root;
- inspect status and recent checkpoints before changes;
- read `TASKS.md`, the active unit prompt, the global contract, decision log,
  co-build log, and latest evidence;
- summarize completed work, remaining work, and unresolved failures;
- continue only the active unit;
- do not repeat completed work, erase history, fabricate results, or begin the
  next unit.

Agent-specific conversation-resume commands may be offered as optional
conveniences, but repository state and project files are authoritative. The
workflow must still work in a new coding-agent conversation.

### Rollback

Name the exact verified checkpoint and prefer non-destructive recovery. Do not
erase failed-test evidence or unresolved issues. Do not recommend destructive
version-control commands as the default recovery path.

## 8. Validation gate

Before release:

- confirm the guide selects exactly one initialization route and does not rerun
  `INIT` against the packaged starter;
- compare every referenced path with the packaged starter;
- compare every unit ID/title with the authoritative session map;
- verify the first active unit in `TASKS.md`;
- test or syntax-check all commands that can be checked safely;
- confirm the audit prompt cannot start feature work;
- confirm each controller stops at one unit;
- confirm failure leaves the current unit active;
- confirm pause/resume works without the original chat;
- render and inspect the DOCX and PDF page by page;
- verify command blocks, tables, page breaks, filenames, and cross-references.

Do not ship a generic guide containing another project's paths, unit count,
commands, or assumptions.
