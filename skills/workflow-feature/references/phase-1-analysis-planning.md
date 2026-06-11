# Phase 1 — Feature Confirmation, Analysis & Planning

**Skills used:** [core-explain](../../core-explain/SKILL.md), [dev-db-designer](../../dev-db-designer/SKILL.md), [check-test-gen](../../check-test-gen/SKILL.md)

## 1. Confirm the target feature
Inspect `.harness/features.json` (or run `./harness status`) and identify the single highest-priority unfinished feature. Ask the user for explicit confirmation (the **ask-user** capability) to work on it. **WIP = 1** — only one feature at a time.

Once confirmed, mark it active so the harness state machine reflects reality and enforces WIP = 1:
```bash
./harness start <feature_id>     # add --force only if you must override the current active feature
```
This moves the feature to `in_progress`. Do not skip this — jumping straight to `verify` later leaves the lifecycle (`not_started → in_progress → passing`) broken.

Immediately create the durable task-state file `.harness/tasks/<feature_id>.md` per the [task-state convention](../../../resources/task-state-convention.md), and keep it updated at every phase boundary. This file is what lets a fresh session resume mid-task after a crash.

For a feature large enough to split, decompose it into child-tasks (`F<id>-T<n>`) and `./harness add` them up front per the [child-task convention](../../../resources/task-convention.md), then work them one at a time (WIP = 1).

## 2. Parallel analysis (spawn-subagents)
Run both subagents **IN PARALLEL** using the **spawn-subagents** capability ([agent-tool-mapping](../../../resources/agent-tool-mapping.md); `Agent`/`Task` in Claude Code):

### Subagent A — Requirements Analyst
- **Skill:** [core-explain](../../core-explain/SKILL.md); consult [dev-db-designer](../../dev-db-designer/SKILL.md) if DB changes are needed.
- **Task:** Read the codebase structure, existing patterns, and related code.
- **Output:** (1) list of files to change, (2) open questions, (3) risks/constraints.

### Subagent B — Test Strategist
- **Skill:** [check-test-gen](../../check-test-gen/SKILL.md)
- **Task:** Find existing tests and frameworks; plan the required tests.
- **Output:** a test plan with happy-path and edge-case cases.

## 3. Present analysis & approve plan
Present both subagents' findings, align on open questions, draft the implementation plan, and get user approval.

Once approved, persist the plan where a crashed session can recover it: write it to `docs/design-docs/<feature_id>/plan.md` and commit it. BA notes and per-component SPECs belong there too (`docs/design-docs/<feature_id>/{ba,spec-*}.md`). `.harness/reports/` is **transient only** (gitignored, wiped by `harness clean`) — never the sole home of an approved plan, spec, or decision.

## 4. MANDATORY UI Design gate (only if the feature has UI)
If the feature includes UI, produce and get approval of a mock **before** writing any implementation code:
- **1–2 screens** (the common case for a single feature) → drive [core-prototype](../../core-prototype/SKILL.md) — the lightweight single-agent path, static HTML/CSS for fast feedback.
- **Many screens / a whole flow** → drive [workflow-prototype](../../workflow-prototype/SKILL.md) instead (multi-agent, covers the full FE SPEC with a browser-preview loop).

Reuse `docs/spec/design-system.md` (the project's approved palette/typography/spacing/components) so the new screen matches the established look; extend that file if the screen needs a genuinely new token. Either way: preview the mock — **browser** for HTML/CSS/JS, **MCP tool** for Figma — then iterate (present → feedback → regenerate → re-preview) until the user explicitly approves. Only then start implementation.

## 5. Phase checkpoint
Update `.harness/tasks/<feature_id>.md` (tick Phase 1, record decisions and the plan path) and commit:
```bash
git add .harness/tasks/<feature_id>.md docs/design-docs/<feature_id>/
git commit -m "phase-checkpoint: <feature_id> phase 1 (plan approved)"
```
A crash after this point resumes directly into Phase 2.

→ Proceed to [Phase 2](phase-2-build-test-review-loop.md).
