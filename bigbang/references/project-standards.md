# InnovationLab Project Standards

## Contents

1. Baseline analysis
2. Feasibility report
3. Architecture specification
4. Security and safety
5. Testing and evidence
6. Language and competition scope
7. Document and packaging standards

## 1. Baseline analysis

Create a baseline ledger before planning:

| Field | Required content |
| --- | --- |
| Problem | Concrete problem and why it matters |
| Users | Primary, secondary, admin, evaluator |
| Core claim | What the project demonstrates or investigates |
| Mandatory functions | Exact functions from the proposal |
| Inputs/outputs | Data, physical signals, media, reports, actions |
| Constraints | Deadline, skill, hardware, budget, platform, policy |
| Deliverables | Product, report, poster, deck, video, defense |
| Evaluation | Rubric and measurable success conditions |

Create a traceability matrix. Never lose baseline items during later refinement.
When recommendations conflict with the baseline, explain the tradeoff and keep
the baseline version visible until the user approves a change.

## 2. Feasibility report

Assess:

- educational and research contribution;
- technical feasibility and dependency maturity;
- data access, quality, licensing, and sample size;
- mathematical or scientific validity;
- hardware availability, environmental constraints, and failure modes;
- privacy, security, age appropriateness, ethics, and content safety;
- budget, schedule, student workload, and mentor workload;
- deployment, offline/demo fallback, maintainability, and reproducibility;
- differentiation and evidence quality;
- competition narrative only when the user explicitly requests competition
  preparation.

Use a risk register with probability, impact, early warning, prevention,
fallback, owner, and verification. Use Plan A/Plan B only when both are genuinely
useful; state the trigger for switching.

## 3. Architecture specification

Cover applicable layers:

1. experience: roles, journeys, pages, accessibility, responsive behavior;
2. domain: entities, rules, permissions, state transitions;
3. application: components, services, APIs, jobs, AI pipeline;
4. data: schema, validation, migration, persistence, backup;
5. integration: devices, third parties, protocols, failure handling;
6. operations: environments, deployment, logs, monitoring, rollback;
7. research: hypothesis, variables, controls, metrics, uncertainty.

Give exact model/SKU and protocol where known. Mark unknown values as decisions
to resolve rather than fabricating specifics.

## 4. Security and safety

- Put secrets in `.env`; provide `.env.example` with placeholders only.
- Add `.env`, credentials, private data, generated secrets, and local databases
  to `.gitignore` as appropriate.
- Apply least privilege, server-side authorization, input validation, safe file
  upload handling, rate limits, audit logging, and dependency review as needed.
- Use synthetic or anonymized sample data.
- Separate authentication from authorization. Define a permission matrix for
  multi-role systems.
- State domain safety boundaries. For health-related projects, avoid diagnosis
  and emergency claims; provide escalation language appropriate to the product.
- For AI output, store provenance/evidence, flag uncertainty, use manual review,
  and provide deterministic fallbacks for demonstrations.

## 5. Testing and evidence

Define tests before implementation:

- unit tests for logic and transformations;
- integration tests across boundaries;
- end-to-end tests for critical user journeys;
- data/model evaluation with appropriate metrics and baselines;
- hardware module tests before system integration;
- security, privacy, invalid-input, failure, and recovery tests;
- usability/accessibility and device/browser tests;
- deployment smoke test and offline/demo fallback rehearsal.

Every acceptance criterion must be observable. Save screenshots, logs, test
reports, sample outputs, measurements, commit/checkpoint references, and
research notes as evidence. Keep a defect log and do not hide known limitations.

## 6. Language and competition scope

- Draft project plans, teaching materials, technical documents, prompts, and
  reports in English by default.
- Generate Chinese, bilingual, or another specified-language version only when
  the user explicitly requests it.
- Keep English-only ASCII filenames and folder names regardless of the requested
  content language.
- Treat competition participation as optional. Add rubric mapping, judging
  strategy, differentiation claims, competition evidence, poster/deck
  optimization, defense questions, or submission packaging only after an
  explicit user request.
- Do not infer competition scope merely because a project is polished,
  innovative, research-oriented, or intended for student presentation.

## 7. Document and packaging standards

- Use English-only ASCII filenames and folder names.
- Use consistent naming, titles, terminology, versions, session numbers, and
  diagrams across all artifacts.
- Use polished typography, proper spacing, useful tables, readable captions,
  page breaks, headers/footers, and a table of contents for long documents.
- Create teacher and student versions separately when requested; do not leak
  solutions into student materials.
- Use native structured equations and validate their rendered output.
- Render DOCX and PDF page by page. Inspect for overflow, clipping, blank pages,
  orphan headings, broken tables, unreadable diagrams, missing glyphs, and
  malformed equations.
- Compare the final package against a manifest and traceability matrix.
- Include source files, generated documents, and configuration samples only
  when relevant; never include credentials, caches, build junk, or private data.

## 8. Architecture Freeze and Change Control

This section extends, and does not replace, Sections 1–7 above.

Before downstream generation, create an authoritative architecture freeze that
records, as applicable:

- exact controller/service count;
- component and sensor ownership;
- network topology;
- data aggregation and persistence boundaries;
- deployment topology;
- exact hardware/firmware target;
- explicitly excluded and deprecated assumptions.

All project plans, diagrams, session prompts, starter files, TASKS state, tests,
and deployment documents must reference the same frozen architecture version.

If architecture changes later:

1. log the decision and rationale;
2. identify every affected downstream artifact;
3. regenerate or repair those artifacts;
4. re-run relevant validation;
5. update the traceability matrix.

Do not preserve stale architecture merely because it appeared in an earlier
generated pack.

## 9. No-Placeholder Completion Standard

A BigBang package must not be described as `FULL`, `complete`, `final`,
`production-ready`, or `demo-ready` when a mandatory area consists only of:

- an empty folder;
- a README-only placeholder;
- TODO-only implementation;
- comment-only automation;
- title-only session prompts;
- file-presence checks presented as runtime validation.

Prepared starters may be intentionally incomplete according to the approved
session design, but every mandatory foundation must contain meaningful,
runnable/testable material appropriate to that stage.

## 10. Demoable Final-System Gate

For build-oriented projects, document count is not the completion criterion.

Define the end-to-end demonstration path early and trace it through the session
map, starter, tests, and final handoff. Separate clearly:

- generated;
- validated in the current environment;
- requires student/manual/physical verification;
- deployment not exercised;
- optional future extension.

Do not claim physical operation, cloud deployment, sensor success, or live API
success without the corresponding evidence.
