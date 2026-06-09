# Example — QA pass on "Export tasks to CSV" (F07)

Input: `/workflow-qa F07`

## Phase 1 — parallel analysis
- **Functional tester ([check-qa](../../check-qa/SKILL.md) + [check-code-review](../../check-code-review/SKILL.md)):** ✅ export button present, ✅ CSV headers correct, ⚠️ filename not asserted anywhere.
- **Edge-case hunter:** 🔴 high — empty list path untested; 🟡 medium — very large list may buffer in memory; notes a missing [check-test-gen](../../check-test-gen/SKILL.md) case for unicode in task titles.
- **Regression analyst:** task list render shares `formatRow()` with the print view → low risk but flagged.

## Phase 2 — report & triage
```
## QA Report — F07
### Overall verdict: CONDITIONAL PASS
Blocking issues: empty-list export untested (high)
```
- Proposed: add an empty-list test ([check-test-gen](../../check-test-gen/SKILL.md)); the streaming fix already covers large lists.
- User chooses **fix now** → handed to [workflow-bugfix](../../workflow-bugfix/SKILL.md); unicode-title test deferred to backlog.
