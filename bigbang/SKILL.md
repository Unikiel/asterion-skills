---
name: bigbang
description: Build complete InnovationLab project systems with authoritative-baseline preservation, mandatory architecture freeze, prepared starter workspace, automatic bounded-session orchestration, durable TASKS state, per-session Git commits, safe pause/resume, exact-target validation, demoable-system acceptance, and full validated packaging.
---

# BigBang Skill v3.0

## Mission
Turn a student proposal, research idea, software/AI/data concept, scientific investigation, or hardware prototype into a source-aligned, teachable, runnable, recoverable, auditable, demoable InnovationLab system.

## Mandatory Gates

### 1. Architecture Freeze
Before generating documents, prompts, TASKS, starter code, or diagrams:
- lock controller count and exact controller models;
- lock sensor/module ownership per controller;
- lock network topology and aggregation point;
- lock data ownership and deployment model;
- for hardware, lock framework/IDE/core/compile target, pins, buses, addresses, and reserved/strapping constraints;
- record exclusions and deprecated assumptions.

For multi-controller systems create a controller inventory and ownership matrix. Any architecture change invalidates stale downstream artifacts and requires regeneration/revalidation.

### 2. Exact Hardware Platform Lock
Do not treat a family name as interchangeable with a concrete target. ESP32-C3, ESP32-S3, and generic ESP32 assumptions are not equivalent.
If toolchains are available, compile against the exact target before release. If not, state that compile validation was not run.

### 3. Mandatory Start-from-Scratch Entrance
Formal starter+prompt packs must expose:
```text
00_START_HERE/
├── START_HERE.md
├── Start_From_Scratch_Guide.md
├── Kickoff_and_Environment_Guide.md
├── Pause_and_Resume_Guide.md
└── First_Run_Checklist.md
```
The route must work without the original chat and must clearly distinguish prepared-starter versus empty-workspace initialization.

### 4. Mandatory Per-Session Git Commit
Every accepted implementation session follows:
`inspect -> checkpoint -> implement -> test -> evidence -> state update -> commit -> stop`

A session cannot be accepted until:
- required checks pass;
- evidence exists;
- TASKS/state is updated;
- its own Git commit exists;
- commit hash is recorded.

Never silently batch multiple accepted sessions into one commit.

### 5. Mandatory Traceable TASKS.md
TASKS.md is a durable ledger, not a disposable checklist. Preserve:
- architecture/version lock;
- full approved session list;
- exactly one active session;
- per-session status and acceptance criteria;
- tests/evidence;
- changed files;
- blockers/known issues;
- commit hash/tag;
- rollback checkpoint;
- resume checkpoint and exact next action.

Update it in place. Never replace it with a fresh template each session.

### 6. Mandatory Safe Pause / Resume
Every formal pack needs a project-specific pause/resume guide.

Pause records active session, completed steps, changed/uncommitted files, actual tests/results, blockers, exact next action, and rollback/checkpoint.

Resume reads Git state, TASKS, active prompt, global contract, decisions/logs, and evidence; continues only the active session; preserves failed evidence/history; works in a fresh agent conversation.

### 7. Automatic Prompt Orchestration
When automatic mode is requested, generate real repository-resident orchestration:
- session manifest;
- machine-readable state;
- durable TASKS.md;
- active-prompt discovery;
- prerequisite and architecture guards;
- block/resume behavior;
- evidence state;
- per-session Git commit verification;
- state transition and next-session activation.

Do not fake automation with comment-only scripts or placeholders.

### 8. No-Placeholder Completion
Do not label a pack FULL/complete/final/demo-ready if mandatory areas contain empty folders, README-only placeholders, TODO-only implementations, comment-only automation, or title-only prompts.

### 9. Demoable Final-System Gate
For build-oriented projects, define and trace an end-to-end demo route. Documents/prompts/starter code are enabling artifacts, not the endpoint. Distinguish validated-now, requires physical/manual validation, deployment-not-exercised, and optional future work.

## Automatic Full-Pack Build
When requirements are sufficient:
1. inspect all baseline sources;
2. freeze authoritative requirements;
3. perform Architecture Freeze and exact platform lock;
4. define the end-to-end demo path;
5. resolve workload/session count and risks;
6. generate substantive DOCX/PDF project documentation when formal packs are requested;
7. materialize a meaningful prepared starter repository;
8. generate INIT contract, WORKSPACE_AUDIT, GlobalEngineeringContract, and one prompt per session;
9. create TASKS/STATUS/SESSION_STATE, evidence conventions, manifest, and automatic controller when requested;
10. run available exact-target validation;
11. render/visually inspect documents;
12. audit placeholders, secrets, absolute paths, stale architecture, generic hardware APIs, and session drift;
13. create SHA-256 manifests;
14. test ZIP extraction and entry points;
15. release only after the validation gate passes.

## Prepared-Starter Route
Preferred route:
1. extract prepared starter;
2. open `00_START_HERE/START_HERE.md`;
3. verify environment;
4. create baseline Git checkpoint if needed;
5. run WORKSPACE_AUDIT once;
6. execute S01 only;
7. test, save evidence, update state, commit, stop;
8. repeat one session at a time.

Never rerun INIT against a materialized prepared starter.

## Session Prompt Contract
Every session prompt must contain:
1. ID/title;
2. role and bounded context;
3. exact files to read first;
4. architecture/platform locks;
5. prior-state/active-unit checks;
6. pre-unit Git checkpoint;
7. precise objective;
8. allowed files;
9. preserved/forbidden files/areas;
10. implementation sequence;
11. automated/manual tests;
12. acceptance criteria;
13. evidence path;
14. safety/security rules;
15. TASKS/state update;
16. mandatory Git commit;
17. rollback point;
18. stop condition;
19. next unit name only.

## Persistent State
Create at minimum:
- TASKS.md
- STATUS.md
- SESSION_STATE.md
- authoritative plan/architecture
- decision log
- co-build log
- evidence/<UnitID>/
- session manifest in automatic mode

A machine-readable state file may mirror TASKS, but both must agree before transitions.

## Hardware Route
Read `references/hardware-workflow.md`. For every hardware project:
- enumerate controllers;
- create module ownership matrix;
- lock exact MCU/board and firmware target;
- validate board-specific APIs;
- provide isolated bring-up per controller/module;
- test serial before sensors;
- separate physical from simulated validation;
- never fabricate hardware readings;
- reserve independent hardware contingency time.

## Validation and Release
Read `references/validation-and-packaging.md`.
Applicable gates include architecture consistency, required-file audit, non-empty/placeholder audit, prompt/session consistency, TASKS/manifest consistency, per-session Git governance, pause/resume audit, exact-target compile/import/syntax checks, smoke tests, secret/path scans, stale/generic hardware API scan, DOCX/PDF visual QA, demo-route traceability, ZIP extraction, and SHA-256 verification.

Never convert file presence into a runtime-success claim.

## Completion Reporting
State what was generated, session/setup/contingency totals, architecture/platform lock, starter initialization status, exact first step, validations actually run, limitations/unexecuted checks, and artifact links.

Do not narrate fake background progress and do not give countdown estimates for work that cannot continue autonomously after the turn.

## Reference Evolution Rule - Merge, Do Not Replace

When enhancing BigBang itself, preserve the existing skill/reference contract
unless a rule is explicitly deprecated.

For an existing reference file:
1. read the whole current file;
2. preserve its existing domain-specific procedures and templates;
3. integrate the new rule at the closest semantic location, or append a clearly
   scoped extension section;
4. remove or rewrite old content only when it directly conflicts with an
   explicitly approved newer rule;
5. record the reason for each destructive edit;
6. compare original versus merged line/section coverage before packaging.

Never replace a mature reference with a shorter summary merely because the
summary contains newer ideas.
