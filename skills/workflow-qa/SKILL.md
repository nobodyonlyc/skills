---
name: workflow-qa
description: Orchestrate a multi-agent workflow to run comprehensive automated and manual testing plans.
---

QA target: $ARGUMENTS

Multi-agent QA workflow: fan out functional, edge-case, and regression analysis in parallel, consolidate into one verdict, and verify against the harness CLI.

## Skills this workflow drives
- [check-qa](../check-qa/SKILL.md) — the structured QA pass each analyst follows.
- [check-test-gen](../check-test-gen/SKILL.md) — write missing tests to cover gaps the analysts find.
- [check-code-review](../check-code-review/SKILL.md) — cross-check suspect changes spotted during analysis.
- [core-fix](../core-fix/SKILL.md) — implement the minimal fix for blocking findings.

## Phases
1. **Parallel Analysis** → [references/phase-1-parallel-analysis.md](references/phase-1-parallel-analysis.md)
   Functional tester + Edge-case hunter + Regression analyst run in parallel against the changed code. **Includes running actual test suites.**
2. **Report & Triage** → [references/phase-2-report-triage.md](references/phase-2-report-triage.md)
   Merge findings into one deterministic QA report with a verdict. Propose fixes for blockers and ask the user how to proceed.
3. **Verification & Checkpoint** → [references/phase-3-verify-checkpoint.md](references/phase-3-verify-checkpoint.md)
   Run `./harness verify` and `./harness session stop` to sync state.

## Examples
- **[QA Report Example](examples/qa-report-example.md)**: A complete, merged report from Phase 2.

## Hard Gates
- Every claimed behavior must be checked against actual code/tests — mark each ✅ / ❌ / ⚠️.
- A FAIL or any high-severity finding blocks a PASS verdict until resolved or explicitly deferred by the user.
- You MUST run `./harness verify` in Phase 3 if the project uses Harness.
