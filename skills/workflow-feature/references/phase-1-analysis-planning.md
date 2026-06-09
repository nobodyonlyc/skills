# Phase 1 — Feature Confirmation, Analysis & Planning

**Skills used:** [core-explain](../../core-explain/SKILL.md), [dev-db-designer](../../dev-db-designer/SKILL.md), [check-test-gen](../../check-test-gen/SKILL.md)

## 1. Confirm the target feature
Inspect `.harness/features.json` (or run `./harness status`) and identify the single highest-priority unfinished feature. Ask the user for explicit confirmation (the **ask-user** capability) to work on it. **WIP = 1** — only one feature at a time.

Once confirmed, mark it active so the harness state machine reflects reality and enforces WIP = 1:
```bash
./harness start <feature_id>     # add --force only if you must override the current active feature
```
This moves the feature to `in_progress`. Do not skip this — jumping straight to `verify` later leaves the lifecycle (`not_started → in_progress → passing`) broken.

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

## 4. MANDATORY UI Design gate (only if the feature has UI)
If the feature includes UI, present a layout wireframe or visual mockup (static HTML or image) **first**. Obtain explicit approval of the design **before** starting any implementation code. Iterate on the mockup until approved.

→ Proceed to [Phase 2](phase-2-build-test-review-loop.md).
