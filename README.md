# Asterion Skills

A growing collection of reusable AI-agent skills for specialized tasks across a
wide range of domains. Individual skills may support planning, analysis,
creation, automation, education, research, engineering, validation, or other
workflows.

Each skill has its own purpose and operating model. Future additions may explore
domains beyond project development and tutoring.

Current skills include **BigBang**, which turns a proposal or concept into a
buildable project system, and **Amber Kernel**, which operates an Obsidian vault
as a contract-locked personal knowledge system.

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

### Amber Kernel

Amber Kernel locks a small vault contract first, maps the vault onto that
contract, then keeps operating on the live notes.

Its workflow supports:

- Convention lock and path mapping before any write
- Vault discovery, audit, empty-vault bootstrap, and safe restructuring
- Note create, edit, merge, move, rename, delete, and link integrity
- YAML properties, templates, daily notes, attachments, Canvas, and Bases
- Research capture into source, atomic, synthesis, and project notes
- Search, query, plugin, theme, snippet, and cssclass workflows
- Local-first privacy; no plugin install, Sync change, or external send unless
  requested

Amber Kernel does not rewrite existing notes until the contract is locked and
the affected paths are mapped. It invents structure only when a convention slot
is empty or the user requests a redesign.

## Repository structure

```text
asterion-skills/
├── README.md
├── LICENSE.md
├── bigbang/
│   ├── SKILL.md
│   ├── agents/
│   │   └── openai.yaml
│   ├── assets/
│   │   └── icon.svg
│   └── references/
│       ├── hardware-workflow.md
│       ├── project-standards.md
│       ├── prompt-and-kickoff-system.md
│       └── start-from-scratch-workflow.md
└── amber-kernel/
    ├── SKILL.md
    ├── agents/
    │   └── openai.yaml
    ├── assets/
    │   └── icon.svg
    └── references/
        ├── kernel-contract.md
        ├── vault-bootstrap.md
        ├── note-operations.md
        ├── research-to-pkm.md
        └── plugin-and-query-workflows.md
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

For Amber Kernel, copy:

```text
amber-kernel/
```

Do not copy only `SKILL.md`. BigBang and Amber Kernel both rely on their
`references/` files for operating rules.

The exact installation location depends on the environment in which the skill
will run. After installation, confirm that the entry file is available at:

```text
<skills-directory>/bigbang/SKILL.md
<skills-directory>/amber-kernel/SKILL.md
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

Invoke Amber Kernel explicitly with a request such as:

> Use `$amber-kernel` to lock this vault's kernel contract and map the existing
> notes onto it.

Other examples:

> Use `$amber-kernel` to initialize an empty Obsidian vault with the smallest
> useful foundation.

> Use `$amber-kernel` to turn these sources into durable notes without creating
> a second taxonomy.

> Use `$amber-kernel` to add a Bases view for active projects using the locked
> property schema.

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

## Amber Kernel output model

Depending on the request, Amber Kernel can produce:

- A locked convention fingerprint and path map
- Vault audits and incremental restructure plans
- New or updated notes, templates, daily notes, and attachments
- Source, atomic, synthesis, map-of-content, and project notes
- Canvas, Bases, Search, and plugin-query artifacts
- Theme, snippet, or cssclass changes only when appearance work is requested

Amber Kernel reports the lock, map, changed vault-relative paths, and unresolved
risks. It does not install plugins or send vault content to external services
unless the user explicitly authorizes that action.

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

When proposing changes to Amber Kernel, preserve the lock-then-adapt gate and
keep observed vault conventions distinguishable from adopted ones.

## License

The Asterion Skills collection is available under the
[MIT License](LICENSE.md).
