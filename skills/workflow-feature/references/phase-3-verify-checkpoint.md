# Phase 3 — Verification & Checkpoint (Definition of Done)

**Skills used:** [check-qa](../../check-qa/SKILL.md), [check-security-review](../../check-security-review/SKILL.md)

Run only after the [Phase 2](phase-2-build-test-review-loop.md) loop completes cleanly.

## Steps
1. Run the full project verification pass via the [check-qa](../../check-qa/SKILL.md) skill.
1b. **Security gate (conditional).** If the change touches any sensitive surface — authentication/authorization, external input (API endpoints, forms, file uploads), secrets/credentials, SQL or query building, shell/command execution, cryptography, or CORS/headers — spawn a Security Auditor via [check-security-review](../../check-security-review/SKILL.md) (tier `strong`). For a purely internal change (docs, tests, behavior-preserving refactor) it may be skipped — log the skip reason in the task-state file. Treat findings by severity exactly like the [review exit criteria](../../check-code-review/SKILL.md): **Critical/High → return to [Phase 2](phase-2-build-test-review-loop.md)** (counts against the iteration cap); Medium → record as a follow-up; Low → optional.
2. **Retain evidence before clean (mandatory).** QA reports, review verdicts, and verify output live in `.harness/reports/`, which is gitignored and wiped by `./harness clean` — so the Definition-of-Done clause "evidence recorded" would otherwise be a lie. Distil the final evidence into committed `docs/design-docs/<feature_id>/evidence.md` (and record the pointer in the task-state file): the commands run, their results, links to any surviving report, and a timestamp. Keep it to pointers and summaries — no pasted long logs (file-based communication rule).
3. Final phase checkpoint: update `.harness/tasks/<feature_id>.md` (tick Phase 3, point at the evidence file) so the state file is in the verify commit. Then run the Harness verify check (auto-stages and commits a checkpoint on success; it skips the commit if the git index already has unrelated staged changes — commit those first):
   ```bash
   ./harness verify <feature_id>
   ```
4. Log progress and prepare the handoff file:
   ```bash
   ./harness session stop
   ```
5. Clean temporary logs and debug files (safe now that evidence is committed):
   ```bash
   ./harness clean
   ```
6. Summarize: files changed, tests added, and any deferred items.

## Hard gate — STOP
Before returning control, **run `./harness status` and show it in the chat** so the user sees what is done / in-progress / blocked after this US or task (per [AGENTS.md](../../../../AGENTS.md) End-Of-Session rule).

**Do not start any other feature or new task in this session.** Return control to the user so other developers or agents can participate. For a deeper review before merge, hand off to [workflow-review-deep](../../workflow-review-deep/SKILL.md).
