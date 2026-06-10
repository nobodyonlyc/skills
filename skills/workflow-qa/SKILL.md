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

## 5-Phase Pipeline
1. **Phase 1: SPEC Analysis**: Extract Business Rules (BR) and Equivalence Partitions from the feature spec before analyzing the code.
2. **Phase 2: TestCase Generation**: Build a 2D Test Matrix (Normal, Boundary, Null, Format, Volume). Classify every test into Automation Levels. Treat Level 2 (Human-in-the-loop) cases identically to Level 3 (Manual Handoff) to avoid blocking runs.
3. **Phase 3: TestData & Scripts**: Use `check-test-gen` to generate test data enforcing the **Fault Isolation Principle**.
4. **Phase 4: Parallel Execution**: Fan out subagents for Fully Automated (Level 1) tests. Mark Level 2/3 cases as `HANDOFF`.
5. **Phase 5: Report Aggregation**: Output a comprehensive report (`5_final_report.md`) containing a Coverage Matrix, Pass Rate, and the detailed Manual Handoff List for testers.

## Examples
- **[QA Report Example](examples/qa-report-example.md)**: A complete, merged report from Phase 2.

## Hard Gates
- Every claimed behavior must be checked against actual code/tests — mark each ✅ / ❌ / ⚠️.
- A FAIL or any high-severity finding blocks a PASS verdict until resolved or explicitly deferred by the user.
- You MUST run `./harness verify` in Phase 3 if the project uses Harness.
