# Prompt and Kickoff System

## Contents

1. Kickoff pack
2. Project initialization prompt
3. Task-state workflow
4. Generic `TASKS.md` template
5. Prompt guide template
6. Session prompt contract
7. Acceptance and handoff

## 1. Kickoff pack

Create a project-ready starter system appropriate to the chosen stack. Typical
contents:

```text
ProjectName/
├── README.md
├── TASKS.md
├── docs/
│   ├── ProjectPlan.md
│   ├── Architecture.md
│   ├── TestPlan.md
│   └── PromptLibrary.md
├── prompts/
│   ├── GlobalEngineeringContract.md
│   ├── SessionPromptTemplate.md
│   └── PhaseXXSessionYY.md
├── config/
│   └── sample-config.json
├── data/
│   └── sample/
├── .env.example
├── .gitignore
└── dependency manifest for the selected stack
```

Adapt the tree; do not create empty ritual folders. Include exact installation,
version verification, first-run, troubleshooting, and uninstall/recovery steps
for the selected operating systems and CPU architectures when setup guidance is
requested.

Initialize `TASKS.md` once, then update task state; do not instruct the user to
overwrite the entire file for every session. Keep completed work, active task,
decisions, known issues, test evidence, and next task visible.

Draft the kickoff files and every prompt in English unless the user explicitly
requests a specified language version.

## 2. Project initialization prompt

Every project must contain exactly one initialization prompt before the first
implementation unit. Name it consistently, such as `INIT Project
Initialization`, and keep it separate from the numbered implementation units.
Its job is to materialize and verify the approved project structure, not to
build product features.

Use this canonical template, adapting paths and manifests to the approved stack:

````markdown
# INIT - Project Initialization

## Role
Act as the setup partner for [Project Name]. Work only in the repository root.

## Read First
- Read [authoritative plan or specification paths].
- Confirm the approved stack, operating system, package manager, and project
  root before creating files.
- If an existing repository is not empty, inspect and preserve working files;
  do not recreate or overwrite them blindly.

## Objective
Create the approved folder/file structure and foundational project-control
files so later implementation units can begin from a reproducible baseline.

## Structure to Create
```text
[Paste the project-specific approved tree here.]
```

## Required Initialization
1. Create only the directories and files shown in the approved tree.
2. Initialize `README.md` with project purpose, prerequisites, setup, run, test,
   and recovery placeholders grounded in the approved plan.
3. Initialize the canonical `TASKS.md` with all approved unit IDs and titles,
   activating only the first implementation unit.
4. Create `.gitignore`, `.env.example` with placeholders only when applicable,
   and the selected dependency manifest with compatible baseline versions.
5. Create baseline architecture, test-plan, and configuration files named in
   the approved tree.
6. Add minimal health-check or placeholder code only when the stack requires it
   to verify initialization; do not implement product features.

## Verification
- Print the resulting tree.
- Run dependency/configuration validation appropriate to the selected stack.
- Confirm no secrets, credentials, real personal data, caches, or generated
  build artifacts were added.
- Report created files, preserved existing files, commands run, results, and
  unresolved setup issues.

## Acceptance Criteria
- The actual tree matches the approved project-specific tree.
- Foundational control/configuration files exist and contain no fabricated
  project results.
- The baseline validation succeeds, or every blocker is recorded accurately.
- No later implementation unit or competition-only material has been started.

## Do Not Do
- Do not invent folders that have no approved purpose.
- Do not overwrite working files without explicit approval.
- Do not hard-code secrets or install unapproved infrastructure.
- Do not implement features from later units.
- Do not add competition files unless competition preparation was explicitly
  requested.

## Stop Condition
Stop after the structure and initialization checks pass. Do not begin the first
implementation unit.
````

The prompt pack must show this init prompt first. Folder creation must not be
left as an implied manual step or postponed into a later session prompt.

## 3. Task-state workflow

Before each coding session:

1. open the repository root;
2. read `README.md`, `TASKS.md`, relevant architecture, and current code;
3. verify environment and current tests;
4. create a checkpoint;
5. activate exactly one bounded session task.

After each session:

1. run required tests and manual checks;
2. compare results with acceptance criteria;
3. record changed files and evidence;
4. update decisions and known issues;
5. stop at the declared boundary;
6. prepare the next session without implementing it.

## 4. Generic `TASKS.md` template

Use this as the canonical project-state pattern. Derive all bracketed content
from the authoritative proposal, approved project plan, and implementation-unit
map. Never retain names, rules, unit codes, counts, or domain assumptions from
an example project.

```markdown
# TASKS.md - [Project Name]

## Project Goal
[One concise statement of the complete project outcome and its alignment to the
authoritative plan.]

## Global Rules
- [Baseline-derived factual, scientific, safety, privacy, or ethical rule]
- [Architecture or data-integrity rule]
- [Security and secret-management rule]
- [Scope or evidence rule]

## Current Unit
Unit code: [Exact current unit ID from the approved plan]
Unit title: [Exact current unit title from the approved plan]
Unit focus: [Bounded outcome copied or normalized from the prompt guide]
Current prompt: [Paste or link only the current unit prompt]

## Acceptance Criteria for Current Unit
- [Criterion 1]
- [Criterion 2]
- [Criterion 3]

## Completed Units
- [ ] [Unit ID] - [Unit title]
- [ ] [Unit ID] - [Unit title]
- [ ] [Continue for every approved implementation unit]

## Decisions
- [Decision, rationale, date or unit]

## Known Issues
- [Issue, impact, owner, next action]

## Last Test Evidence
- Automated:
- Manual:
- Data/model/device:
- End-to-end demo path:

## Next Unit
- [Exact next unit ID and title; preparation only, not implementation]
```

Generate the checklist from the approved unit map rather than copying a fixed
example. Preserve authoritative unit IDs and titles exactly, whether they use
phase/session codes, numbered milestones, research stages, or another scheme.
Add or rename evidence categories only when the project requires it; for
example, hardware projects may separate firmware, power, sensor, actuator, and
physical safety evidence.

Initialize this file once. At each unit boundary, update fields in place:

1. mark the current unit complete only after its acceptance checks pass;
2. retain completed-unit history, decisions, issues, and evidence;
3. activate only the next approved unit;
4. do not paste the full multi-unit prompt guide into `Current prompt`;
5. do not erase unresolved issues or failed-test evidence;
6. do not add a unit or change its scope without updating the authoritative
   plan and traceability map.

## 5. Prompt guide template

Place the single initialization prompt first, then use one prompt per
implementation unit. Preserve the source plan's exact unit IDs and titles when
they are authoritative. Draft prompts in English unless the user explicitly
requests a specified language version.

```text
[Unit ID] [Unit Title]

Project context:
You are building [project name], a [positioning statement].

Goal for this unit:
[One precise goal]

Files to create or modify:
- [path]
- [path]

Implementation requirements:
1. [requirement]
2. [requirement]
3. [requirement]

Tests and checks:
- [test]
- [command]
- [manual check]

Acceptance criteria:
- [criterion]
- [criterion]

Do not do:
- Do not implement future units early.
- Do not hard-code secrets.
- Do not fabricate data or results.

TASKS.md update:
Mark this unit complete only after tests/checks pass. Record known issues and next unit.
```

## 6. Session prompt contract

Use this structure in every concrete Vibe Coding prompt:

```markdown
# Role
Act as the implementation partner for this bounded InnovationLab session.

# Read First
List the exact project files and prior decisions to inspect.

# Current State
Summarize what already works, known issues, and the active phase/session.

# Session Objective
State one testable outcome.

# Scope
List the exact functions, components, files, and data in scope.

# Requirements
Give functional, UI, data, scientific, mathematical, hardware, and operational
requirements that apply.

# Implementation Sequence
Provide small ordered steps, each leaving the project runnable.

# Files
List files to create, modify, and explicitly preserve.

# Tests and Acceptance Criteria
Give commands, manual checks, expected results, and evidence to save.

# Security and Safety
State secret, privacy, licensing, physical, and domain-specific constraints.

# Do Not Do
List out-of-scope changes, forbidden shortcuts, and architecture boundaries.

# Completion Report
Require changed files, test results, remaining limitations, and next safe step.

# Stop Condition
Stop when this session's criteria pass; do not begin the next session.
```

Make prompts concrete enough to execute without guessing. Never ask the coding
agent to recreate the project blindly, replace working architecture without
approval, suppress errors, hard-code secrets, invent test results, or claim a
feature works without running its checks.

## 7. Acceptance and handoff

Each phase ends with:

- requirement traceability review;
- runnable demo of the phase's vertical slice;
- automated and manual test evidence;
- documentation update;
- checkpoint and rollback path;
- unresolved-risk decision;
- explicit entry criteria for the next phase.

The final handoff includes setup, run, test, deploy, backup/recovery,
troubleshooting, architecture, data/model/device notes, known limitations, and a
rehearsed demo route.
