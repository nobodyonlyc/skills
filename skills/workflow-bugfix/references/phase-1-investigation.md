# Phase 1 — Parallel Investigation & Analysis

**Skills used:** [core-explain](../../core-explain/SKILL.md), [dev-db-designer](../../dev-db-designer/SKILL.md)

Run both subagents **IN PARALLEL** using the **spawn-subagents** capability ([agent-tool-mapping](../../../resources/agent-tool-mapping.md); `Agent`/`Task` in Claude Code).

## Subagent A — Root Cause Investigator
- **Role:** Codebase Debugger
- **Skill:** [core-explain](../../core-explain/SKILL.md)
- **Task:** Search all code paths related to the reported bug and trace the data flow.
- **Output:** the exact line(s) where the bug originates, plus a diagnostic context.

## Subagent B — Impact Analyst
- **Role:** Regression Analyst
- **Skill:** consult [dev-db-designer](../../dev-db-designer/SKILL.md) if the bug is database-related.
- **Task:** Find all callers, tests, and related code a fix could affect; check git logs for recent changes.
- **Output:** a regression-risk assessment and a list of impacted components.

## Align
Once both complete, present findings to the user (the **ask-user** capability) and agree on a fix proposal before touching code.

If this bug maps to a tracked feature, mark it active so the lifecycle reflects reality:
```bash
./harness start <feature_id>     # --force only to override the current active feature (WIP = 1)
```
If the fix is blocked (e.g. needs an upstream change or an undecided decision), record it instead:
```bash
./harness block <feature_id> --reason "<what is blocking>"
```
For a multi-step fix, split it into child-tasks (`F<id>-T<n>`) via the [child-task convention](../../../resources/task-convention.md) so each step is tracked and verified independently.

→ Proceed to [Phase 2](phase-2-fix-test-review-loop.md).
