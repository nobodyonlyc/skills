# Phase 1 — Parallel Analysis

**Skills used:** [check-qa](../../check-qa/SKILL.md), [check-test-gen](../../check-test-gen/SKILL.md), [check-code-review](../../check-code-review/SKILL.md)

Spawn all three agents **IN PARALLEL**, each following the [check-qa](../../check-qa/SKILL.md) skill's discipline. Ensure the test suite is actually executed as part of this phase.

## 0. Pre-requisite: Execute Tests
Before analysis, run the automated tests and capture coverage metrics if available:
```bash
npm test -- --coverage # Or cargo test, pytest, etc.
```

## Agent 1 — Functional tester
- **Task:** Read the changed code and acceptance criteria (PR description, commit messages, or task). Verify each claimed behavior is actually implemented. Use [check-code-review](../../check-code-review/SKILL.md) to inspect suspect changes. Compare against actual test execution results.
- **Output Schema:** 
  - `verified_behaviors`: List of ✅
  - `missing_behaviors`: List of ❌
  - `ambiguous_behaviors`: List of ⚠️

## Agent 2 — Edge-case hunter
- **Task:** Analyze the changed code for edge cases, error-handling gaps, and boundary conditions (input validation, null checks, error branches, off-by-one). Identify missing automated tests. Check test execution logs for flaky tests.
- **Output Schema:** 
  - `edge_cases`: List of {description, severity: high|medium|low, missing_test: boolean}
  - `flaky_tests`: List of tests that failed intermittently.

## Agent 3 — Regression analyst
- **Task:** Identify which existing features are most at risk from the changes; trace data flow and shared code paths. Analyze coverage delta to see if old code lost test coverage.
- **Output Schema:**
  - `regression_risks`: List of {description, code_path, severity: high|medium|low}
  - `coverage_delta`: Note any drops in coverage percentage.

→ Proceed to [Phase 2](phase-2-report-triage.md).
