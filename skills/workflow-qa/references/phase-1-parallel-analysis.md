# Phase 1 — Parallel Analysis

**Skills used:** [check-qa](../../check-qa/SKILL.md), [check-test-gen](../../check-test-gen/SKILL.md), [check-code-review](../../check-code-review/SKILL.md)

Spawn all three agents **IN PARALLEL**, each following the [check-qa](../../check-qa/SKILL.md) skill's discipline.

## Agent 1 — Functional tester
- **Task:** Read the changed code and acceptance criteria (PR description, commit messages, or task). Verify each claimed behavior is actually implemented; use [check-code-review](../../check-code-review/SKILL.md) to inspect suspect changes.
- **Output:** behaviors verified ✅, missing ❌, or ambiguous ⚠️.

## Agent 2 — Edge-case hunter
- **Task:** Analyze the changed code for edge cases, error-handling gaps, and boundary conditions — input validation, null checks, error branches, off-by-one. Note where a [check-test-gen](../../check-test-gen/SKILL.md) test is missing.
- **Output:** ranked list of edge cases by severity (high/medium/low).

## Agent 3 — Regression analyst
- **Task:** Identify which existing features are most at risk from the changes; trace data flow and shared code paths.
- **Output:** regression risks with the specific code paths connecting old features to new changes.

→ Proceed to [Phase 2](phase-2-report-triage.md).
