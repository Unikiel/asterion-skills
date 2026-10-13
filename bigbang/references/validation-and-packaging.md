# Validation and Packaging v3

Release blockers:
- mandatory missing/empty folders;
- README-only mandatory implementation modules;
- comment-only automation;
- prompt-printing or state-only controllers that never invoke a coding agent;
- manual prompt copy-and-paste as the primary execution route;
- missing single-command automatic kickoff/resume path;
- title-only session prompts;
- stale architecture/controller ownership;
- generic hardware API assumptions;
- missing START_HERE / Start_From_Scratch / Pause_and_Resume;
- untraceable TASKS;
- missing per-session Git completion gate;
- manifest/state/TASKS inconsistency;
- claiming FULL while mandatory validation is unresolved.

Run applicable parsing, exact-target compile/import/syntax checks, smoke/automated tests, secret/private-data scan, absolute-path/project-residue scan, stale API scan, DOCX/PDF rendering+visual QA, demo-route traceability, ZIP extraction test, SHA-256 verification.

Package size may be a sanity signal but never proof of completeness.

Report precisely what was and was not executed.
