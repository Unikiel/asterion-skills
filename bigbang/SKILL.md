---
name: bigbang
description: Transform a student proposal, research idea, app concept, AI system, data project, or hardware prototype into a complete InnovationLab project system. Use when Codex must analyze feasibility, preserve an authoritative baseline, define appropriate scope and architecture, design a workload-based 60-minute tutoring plan, create a project initialization prompt plus Vibe Coding session prompts, produce teacher/student/project documentation, or validate and package InnovationLab deliverables. Apply to software, AI, data, scientific, and ESP32/IoT projects; add competition materials only when explicitly requested and include the hardware-specific workflow whenever physical modules are involved.
---

# BigBang

Turn an initial idea into a buildable, teachable, testable, and presentable
InnovationLab project. Preserve the student's intellectual ownership while
adding the engineering structure required to finish successfully.

## Operating principles

1. Treat the user's latest named proposal or uploaded plan as the authoritative
   baseline. Extract its mandatory functions, intended users, research question,
   constraints, outputs, and any explicitly stated competition context before
   recommending changes.
2. Separate baseline requirements from justified refinements. Never silently
   replace the student's concept with a different project.
3. Default to a complete, real project deliverable. Do not add competition
   positioning, rubric optimization, judging strategy, defense material, or
   competition-specific evidence unless the user explicitly requests it. Use
   “MVP” only when the user or authoritative baseline explicitly requires MVP
   scope.
4. Size the course from actual research, engineering, testing, and presentation
   work. Never impose a fixed 20-session structure or advertise a session count
   in titles merely to fit a template.
5. Keep public-facing material polished and audience-appropriate. Remove
   internal notes, implementation chatter, and student/parent-unfriendly
   narration.
6. Prefer phase-by-phase execution with verification gates over one giant
   implementation prompt.
7. Draft all project content in English by default. Produce Chinese, bilingual,
   or another language version only when the user explicitly requests that
   language.
8. Include exactly one project initialization prompt before all implementation
   units. It must create the approved folder/file structure and foundational
   control files without implementing later product features.
9. Make operational continuity explicit. A student must be able to start from
   an extracted starter workspace, execute exactly one bounded unit, verify it,
   pause safely, and resume later without overwriting task history or relying
   on the original chat.

## Required workflow

### 1. Intake and baseline extraction

- Read every supplied proposal or artifact completely.
- Build a requirements traceability table with source requirement, normalized
  interpretation, planned implementation, verification method, and status.
- Record unknowns and contradictions. Ask only questions whose answers would
  materially change architecture, scope, safety, cost, or schedule.
- Identify student background, available equipment, platform, deadline,
  explicitly stated competition rubric, requested language, and required
  deliverable formats when provided.
- Distinguish mandatory, recommended, enhancement, and out-of-scope items.

### 2. Feasibility and scope gate

- Evaluate educational value, scientific/research validity, engineering
  feasibility, data availability, safety, privacy, cost, schedule, and demo
  resilience. Evaluate competition value only when competition participation is
  explicitly in scope.
- State assumptions and major risks with concrete mitigations.
- Select a coherent stack and explain consequential choices. Avoid needless
  technologies and duplicate infrastructure.
- Define the smallest complete vertical slice, then the full target and optional
  enhancements. A vertical slice must demonstrate the core claim end to end.
- Define measurable success criteria before scheduling implementation.

Read [project-standards.md](references/project-standards.md) for the required
analysis, architecture, security, documentation, and quality standards.

### 3. Architecture and execution map

- Describe users, journeys, pages/interfaces, components, services, data model,
  APIs/protocols, AI or mathematical pipeline, persistence, deployment, and
  observability as applicable.
- Provide a readable system concept/logic diagram.
- Map every requirement to phases, sessions, artifacts, tests, and final
  evidence.
- Keep architecture diagrams conceptually accurate; do not make diagrams
  decorative substitutes for specifications.

### 4. Time model

- Use 60-minute core sessions.
- Determine the number of core sessions from workload; compress to roughly
  20–24 only when the user asks and depth can be preserved.
- Add a separate 2–4 hour Vibe Coding environment-setup module.
- Add independent contingency time:
  - pure software: 2 class hours;
  - any hardware integration: 4 class hours.
- Do not count setup or contingency hours as core sessions.
- Show phase totals, core total, setup total, contingency total, and overall
  commitment separately.

### 5. Course and session design

- Organize core sessions into phases with explicit entry and exit gates.
- Place one initialization prompt before the first implementation unit. Require
  it to create the approved project tree, `README.md`, `TASKS.md`,
  `.gitignore`, `.env.example` when applicable, dependency manifest, and
  baseline documentation/configuration appropriate to the stack. It must verify
  the resulting structure and stop before feature implementation.
- For every session specify:
  - goal and prior-state check;
  - knowledge and research concepts;
  - implementation or experiment;
  - files/components/modules affected;
  - structured Vibe Coding prompt;
  - manual work the student must perform;
  - test and acceptance criteria;
  - evidence to save;
  - security/safety rules;
  - “Do not do” constraints;
  - checkpoint/rollback note;
  - homework or next-session preparation when useful.
- Ensure prompts ask the coding agent to inspect existing state, preserve working
  behavior, make bounded changes, run tests, report changed files, and stop at
  the session boundary.

Read [prompt-and-kickoff-system.md](references/prompt-and-kickoff-system.md)
before creating kickoff files or session prompts.

Read
[start-from-scratch-workflow.md](references/start-from-scratch-workflow.md)
before creating an operational kickoff guide, starter workspace, pause/resume
instructions, or coding-agent handoff.

### 6. Deliverable system

Create only the documents relevant to the request, while keeping this canonical
coverage:

- authoritative project plan and feasibility report;
- session-based tutoring plan;
- kickoff preparation guide;
- standalone project-specific start-from-scratch guide;
- phase/session structured prompt pack;
- system/technical design;
- testing, integration, deployment, and recovery guide;
- student guide and teacher guide when teaching artifacts are requested;
- research/report, presentation, and demo materials when relevant;
- competition, judging, and defense materials only when explicitly requested;
- bill of materials and hardware guides for physical systems.

Draft document and prompt content in English unless the user explicitly asks
for a specified language version. Use English-only ASCII filenames and folder
names even when requested content is Chinese or bilingual. When formal project
packs are requested, default to polished DOCX and matching PDF, then package the
requested set in a clearly named ZIP. Do not force every task into all formats
when the user asks for a narrower output.

When a formal pack includes a starter workspace and session prompts, the
start-from-scratch guide is mandatory and separate from the conceptual kickoff
preparation guide. It must cover environment/version checks, safe extraction
and project-root selection, baseline version-control checkpoint, a one-time
audit that implements no features, one-unit execution, manual acceptance,
evidence storage, commit/tag checkpoints, failure handling, pause/resume, and
rollback. It must state whether the packaged starter is already initialized:
never tell the user to rerun `INIT` against a materialized starter. Adapt
commands to the selected operating system and coding agent; do not assume one
CLI.

### 7. Validation and release gate

- Verify requirement coverage, cross-document consistency, session totals,
  links, filenames, diagrams, equations, code/config samples, and package
  contents.
- Dry-audit the operational guide against the actual starter workspace:
  referenced files, unit IDs, commands, evidence paths, and first active unit
  must exist and agree with `TASKS.md` and the prompt pack.
- Render DOCX and PDF outputs and inspect every page visually.
- Verify all equations after rendering in both formats. Correct leaked markup,
  malformed fractions, duplicated symbols, broken subscripts/superscripts,
  missing delimiters, clipping, and unreadable formula graphics.
- Check that student-facing material contains no answer leakage or internal
  commentary and that teacher material contains the needed reasoning and
  solutions.
- Do not claim completion while any mandatory artifact, test, render check, or
  baseline requirement is unresolved.

## Conditional routes

### Mathematics, science, statistics, or technical formulas

Render every formula in polished display mathematics. Prefer native DOCX OMML
equations with structural fractions, sums, roots, scripts, Greek symbols, and
delimiters. Use high-quality typeset graphics only when native equations are not
feasible. Never leave formulas as plain-text linear notation, including in
tables, captions, and diagrams.

### Hardware, ESP32, sensors, or actuators

Read [hardware-workflow.md](references/hardware-workflow.md) completely. Apply
its bill-of-materials, power, wet/dry-zone, wiring, module bring-up, safety,
dry-run, integration, and validation gates. Produce both required hardware
diagrams in English by default: a physically realistic wiring architecture
diagram and a separate system concept/logic diagram. Use another language only
when the user explicitly requests it.

### AI and data systems

- Document data provenance, consent/licensing, preprocessing, evaluation,
  uncertainty, hallucination controls, caching/review, fallback behavior, and
  reproducibility.
- Keep secrets in environment variables and server-side boundaries. Never put
  API keys in client code, screenshots, sample files, or documents.
- Prefer source-checkable outputs and human review for consequential content.

## Prohibited shortcuts

- Do not invent a fixed session count.
- Do not call a complete project an MVP by default.
- Do not add competition framing or competition deliverables without an
  explicit user request.
- Do not default project content to Chinese or bilingual output.
- Do not omit the one-time project initialization prompt or scatter folder
  creation across later implementation units.
- Do not paste one oversized prompt and treat it as a curriculum.
- Do not expose secrets or use real personal data in samples.
- Do not present unverified scientific, factual, medical, or safety claims.
- Do not use copyrighted or official imagery without appropriate permission.
- Do not use labels such as “beginner,” “beginner-friendly,” “for beginners,”
  “foolproof,” or equivalent ability labels in final diagrams or public-facing
  deliverables.
- Do not imply multiple power adapters when one coherent adapter and regulated
  rails are intended.
- Do not deliver visually unverified equations, diagrams, DOCX files, or PDFs.
