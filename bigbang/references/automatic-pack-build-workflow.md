# Automatic Pack Build Workflow v3

1. Source ingestion and requirement traceability.
2. Architecture Freeze: controller inventory, module ownership, network/data/deployment lock, exact hardware platform lock, exclusions.
3. Define the final end-to-end demo path.
4. Decompose workload into bounded 60-minute sessions; keep 2–4h environment setup separate and reserve 2h software / 4h hardware contingency.
5. Generate internally consistent documents.
6. Materialize a non-empty prepared starter with meaningful code/config/tests; do not use ritual placeholder folders.
7. Generate INIT, WORKSPACE_AUDIT, GlobalEngineeringContract, one prompt per session, TASKS/STATUS/SESSION_STATE, evidence directories, and session manifest.
8. In automatic mode implement real transitions:
   `AUDIT -> READY -> ACTIVE -> BLOCKED|VALIDATING -> ACCEPTED -> COMMITTED -> NEXT`.
   COMMITTED requires validation, evidence, state update, and recorded Git commit hash.
9. Run exact-target validation where possible.
10. Reject release for stale architecture, missing entrance, missing pause/resume, untraceable TASKS, missing session Git governance, comment-only automation, title-only prompts, or placeholder-only starter modules.
11. Package full release + starter ZIP where applicable, SHA-256 manifest, extraction test, truthful release notes.
