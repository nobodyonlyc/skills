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
- [workflow-bugfix](../workflow-bugfix/SKILL.md) — each failing finding becomes a bugfix story (the repair half of the loop).
- [core-fix](../core-fix/SKILL.md) — implement the minimal fix for small, in-scope blocking findings inline.

## 5-Phase Pipeline
1. **Phase 1: SPEC Analysis**: Extract Business Rules (BR) and Equivalence Partitions from the feature spec before analyzing the code.
2. **Phase 2: TestCase Generation**: Build a 2D Test Matrix (Normal, Boundary, Null, Format, Volume). Classify every test into Automation Levels. Treat Level 2 (Human-in-the-loop) cases identically to Level 3 (Manual Handoff) to avoid blocking runs.
3. **Phase 3: TestData & Scripts**: Use `check-test-gen` to generate test data enforcing the **Fault Isolation Principle**.
4. **Phase 4: Parallel Execution**: Fan out subagents for Fully Automated (Level 1) tests. Mark Level 2/3 cases as `HANDOFF`.
5. **Phase 5: Report Aggregation**: Output a comprehensive report (`5_final_report.md`) containing a Coverage Matrix, Pass Rate, and the detailed Manual Handoff List for testers.
6. **Phase 6: Fix & re-test loop (until green)**: For each failing finding, **don't stop at reporting** — route it through the repair loop: small in-scope defects → [core-fix](../core-fix/SKILL.md); anything non-trivial → spawn a **`bugfix` story** ([workflow-bugfix](../workflow-bugfix/SKILL.md)) with a regression test that **fails before** the fix and **passes after**. Then **re-run the affected suite** (back to Phase 4). Repeat until the suite is **green** (or the user explicitly defers a finding). A QA/test US is `passing` only when its suite is green.

## Examples
- **[QA Report Example](examples/qa-report-example.md)**: A complete, merged report from Phase 2.

## Hard Gates
- Every claimed behavior must be checked against actual code/tests — mark each ✅ / ❌ / ⚠️.
- A FAIL or any high-severity finding blocks a PASS verdict until resolved or explicitly deferred by the user.
- **Failures loop, they don't just get logged:** fix (inline or via a bugfix story) → re-run the suite → repeat until green. Silencing/skipping a test is never "resolved".
- You MUST run `./harness verify` in Phase 3 if the project uses Harness.
