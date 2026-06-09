# Phase 3 — Verification & Checkpoint (Definition of Done)

**Skill used:** [check-qa](../../check-qa/SKILL.md)

Run only after the [Phase 2](phase-2-fix-test-review-loop.md) loop completes cleanly (test passes, review clean).

## Steps
1. Run the project verification suite via the [check-qa](../../check-qa/SKILL.md) skill.
2. Run the Harness verify check (auto-commits a checkpoint on success):
   ```bash
   ./harness verify <feature_id>
   ```
3. Report:
   - **Root cause** — what actually caused the bug.
   - **Fix details** — what changed and why it's minimal.
   - **Test added** — the regression test that now guards it.
   - **Regression risk** — anything still worth watching.

For a deeper pre-merge pass, hand off to [workflow-review-deep](../../workflow-review-deep/SKILL.md).
