# Phase 3 — Verification & Checkpoint (Definition of Done)

**Skill used:** [check-qa](../../check-qa/SKILL.md)

Run only after the [Phase 2](phase-2-build-test-review-loop.md) loop completes cleanly.

## Steps
1. Run the full project verification pass via the [check-qa](../../check-qa/SKILL.md) skill.
2. Final phase checkpoint: update `.harness/tasks/<feature_id>.md` (tick Phase 3, point at the QA evidence) so the state file is included in the verify commit. Then run the Harness verify check (auto-stages and commits a checkpoint on success; it skips the commit if the git index already has unrelated staged changes — commit those first):
   ```bash
   ./harness verify <feature_id>
   ```
3. Log progress and prepare the handoff file:
   ```bash
   ./harness session stop
   ```
4. Clean temporary logs and debug files:
   ```bash
   ./harness clean
   ```
5. Summarize: files changed, tests added, and any deferred items.

## Hard gate — STOP
**Do not start any other feature or new task in this session.** Return control to the user so other developers or agents can participate. For a deeper review before merge, hand off to [workflow-review-deep](../../workflow-review-deep/SKILL.md).
