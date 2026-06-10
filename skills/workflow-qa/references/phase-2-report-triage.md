# Phase 2 — Report & Triage

**Skills used:** [check-test-gen](../../check-test-gen/SKILL.md), [core-fix](../../core-fix/SKILL.md)

## 1. Merge into Deterministic QA Report
Consolidate the schemas from Agent 1, Agent 2, and Agent 3 into a single markdown report. See the [QA Report Example](../examples/qa-report-example.md) for the exact format.

### Flaky Test Handling
If Agent 2 identified any flaky tests:
- Automatically downgrade the verdict to `CONDITIONAL PASS` at best.
- List the flaky tests as `High` severity blockers.

## 2. Triage Findings
For any ❌, flaky test, or high-severity finding:
- Propose the **minimal fix** (via [core-fix](../../core-fix/SKILL.md)).
- Propose the **test** that would guard it (via [check-test-gen](../../check-test-gen/SKILL.md)).

## 3. Decide with the User
Ask the user: fix the issues now, or document them for follow-up? (In `auto` mode, decide and log per [autonomy-mode](../../../resources/autonomy-mode.md) — default to fixing high-severity blockers and deferring low.)
- **Fix now** → hand off to [workflow-bugfix](../../workflow-bugfix/SKILL.md) for each blocker. Each inherits that workflow's **iteration cap** (5), so a stubborn blocker blocks rather than looping unbounded.
- **Defer** → record them so the next session can pick them up (e.g., create a task in `task.md` or `.harness/features.json`).

→ Once resolved or deferred, proceed to [Phase 3](phase-3-verify-checkpoint.md).
