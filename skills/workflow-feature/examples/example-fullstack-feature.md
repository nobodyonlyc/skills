# Example — Full-stack feature: "Export tasks to CSV"

Input: `/workflow-feature F07 export tasks to CSV from the task list`

## Phase 1 — analysis & planning
- Confirm with user: F07 is the highest-priority unfinished feature → approved.
- **Subagent A (Requirements Analyst, [core-explain](../../core-explain/SKILL.md))** reports: touch `apps/api/routes/tasks.ts` (new `GET /tasks/export`), `apps/web/components/TaskList.tsx` (export button). Risk: large lists → stream the response.
- **Subagent B (Test Strategist, [check-test-gen](../../check-test-gen/SKILL.md))** plans: API test for CSV headers/rows, empty-list edge case, and a component test for the button click.
- UI is a single button → a quick mockup is shown and approved.

## Phase 2 — build · test · review loop
- **Iteration 1:** Backend dev ([dev-be-developer](../../dev-be-developer/SKILL.md)) adds the streaming CSV endpoint; Frontend dev ([dev-fe-developer](../../dev-fe-developer/SKILL.md)) adds the button calling it. Test Writer ([check-test-gen](../../check-test-gen/SKILL.md)) runs tests → the empty-list test **fails** (endpoint returns `null`).
- **Iteration 2:** Backend dev fixes empty-list to return a header-only CSV. Tests **pass**. Reviewer ([check-code-review](../../check-code-review/SKILL.md)) flags a missing `Content-Disposition` filename → fixed. Review **clean**.

## Phase 3 — verify & checkpoint
```
$ ./harness verify F07   # runs qa pass + verifications → PASS, commits checkpoint
$ ./harness session stop
$ ./harness clean
```
Summary: 2 files changed, 3 tests added, no deferred items. STOP — control returned to user.
