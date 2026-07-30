# Asterion Skills

A growing collection of reusable AI-agent skills for specialized tasks across a
wide range of domains. Individual skills may support planning, analysis,
creation, automation, education, research, engineering, validation, or other
workflows.

Each skill has its own purpose and operating model. Future additions may explore
domains beyond project development and tutoring.

The first skill in this collection is **BigBang**, which transforms a student
proposal, research idea, application concept, AI or data system, scientific
project, or hardware prototype into a complete project system that is buildable,
teachable, testable, and presentable.

## Available skills

### BigBang

BigBang helps preserve an original proposal as the authoritative baseline while
adding the engineering and teaching structure needed to complete the project.

Its workflow supports:

- Baseline extraction and requirement traceability
- Feasibility, scope, risk, and architecture analysis
- Workload-based 60-minute tutoring sessions
- A dedicated Vibe Coding environment-setup module
- A one-time project initialization prompt
- Phase-by-phase implementation prompts with acceptance criteria
- Safe pause, resume, checkpoint, rollback, and recovery procedures
- Software, AI, data, research, scientific, and ESP32/IoT projects
- Testing, deployment, documentation, and release validation
- Polished DOCX/PDF project packs and equation validation when requested
- Hardware bills of materials, wiring diagrams, system diagrams, and module
  bring-up guides when physical components are involved
- Optional competition materials only when explicitly requested

English is the default drafting language. Other language versions are generated
only when explicitly requested.

## Repository structure

```text
asterion-skills/
├── README.md
├── LICENSE.md
├── bigbang/
│   ├── SKILL.md
│   ├── agents/
│   │   └── openai.yaml
│   └── references/
│       ├── hardware-workflow.md
│       ├── project-standards.md
│       ├── prompt-and-kickoff-system.md
│       └── start-from-scratch-workflow.md
└── future-skill/
    └── SKILL.md
```

Each skill directory directly under the repository root is self-contained and
installable. Its entry point must be `SKILL.md`.

## Adding a new skill

Use this checklist whenever a new skill joins Asterion Skills:

1. Choose a lowercase, hyphen-separated skill name, such as
   `workflow-automator`.
2. Create a self-contained directory at `<skill-name>/` directly under the
   repository root.
3. Put the required `SKILL.md` at the root of that directory.
4. Add `agents/openai.yaml` for user-facing skill metadata.
5. Add only the supporting directories the skill actually needs:
   `references/`, `scripts/`, and/or `assets/`.
6. Validate the complete skill directory with the current official skill
   validator.
7. Test at least one realistic invocation before publishing.
8. Audit the new files for credentials, private data, absolute local paths,
   internal identifiers, caches, and project-specific residue.
9. Update this README using the maintenance checklist below.

Do not put a separate `README.md`, installation guide, changelog, or other
repository-facing documentation inside an installable skill directory. Keep
those materials at the Asterion Skills repository level.

### README maintenance checklist

For every newly onboarded skill, update:

1. **Available skills** — add a heading with the skill's name, purpose, main
   capabilities, and any important trigger or limitation.
2. **Repository structure** — add the new `<skill-name>/` tree and list
   its meaningful bundled resources.
3. **Installation** — mention any installation detail that differs from the
   standard “copy the complete skill folder” procedure.
4. **Usage** — add one short, realistic invocation example.
5. **Output model** — add a skill-specific output section only when its outputs
   are not already clear from the capability summary.
6. **License or attribution** — update this only when the new skill includes
   third-party material or has requirements beyond the repository license.

Keep the README concise. Describe what users need to discover, install, and
invoke each skill; keep operational instructions for the AI agent inside that
skill's `SKILL.md` and bundled references.

## Installation

Copy the complete folder for the skill you want to install into a skills
directory supported by your ChatGPT or Codex environment.

For BigBang, copy:

```text
bigbang/
```

Do not copy only `SKILL.md`. BigBang relies on its `references/` files for
detailed project standards, prompt templates, hardware procedures, and
start-from-scratch guidance.

The exact installation location depends on the environment in which the skill
will run. After installation, confirm that the entry file is available at:

```text
<skills-directory>/bigbang/SKILL.md
```

## Usage

Invoke BigBang explicitly with a request such as:

> Use `$bigbang` to transform this student proposal into a complete
> InnovationLab project and teaching pack.

Other examples:

> Use `$bigbang` to evaluate this app concept and create a realistic project
> plan with session-based implementation prompts.

> Use `$bigbang` to rebuild this ESP32 proposal into a complete hardware project
> pack, including wiring, bring-up, testing, and safety guidance.

> Use `$bigbang` to create a competition version of this project.

BigBang adds competition-specific materials only when the request explicitly
places the project in a competition context.

## BigBang output model

Depending on the request, BigBang can produce:

- Project and feasibility plans
- Architecture and requirements-traceability documents
- Session-based tutoring plans
- Kickoff and start-from-scratch guides
- Initialization and implementation prompt packs
- Student and teacher guides
- Testing, deployment, and recovery documentation
- Research, presentation, and demonstration materials
- Starter workspaces and packaged deliverables
- Hardware documentation for projects involving physical modules

The exact deliverables and session count are determined by the project workload.
BigBang does not impose a fixed 20-session plan and does not label a complete
project as an MVP unless the source proposal or user explicitly requires MVP
scope.

## Contributing

Contributions are welcome when they preserve the following principles:

1. Keep each skill self-contained.
2. Place its `SKILL.md` at the root of its skill folder.
3. Keep reusable detailed guidance in `references/`, deterministic helpers in
   `scripts/`, and output resources in `assets/`.
4. Do not include credentials, private or personal information, local absolute
   paths, internal skill identifiers, generated caches, or project-specific
   residue.
5. Validate changes before submitting them.
6. Keep user-facing examples and documentation in English by default.

When proposing changes to BigBang, preserve the student's intellectual ownership
and keep baseline requirements distinguishable from recommended refinements.

## License

The Asterion Skills collection is available under the
[MIT License](LICENSE.md).
