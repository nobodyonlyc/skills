---
name: workflow-qa
description: Orchestrate a multi-agent workflow to run comprehensive automated and manual testing plans.
---

QA target: $ARGUMENTS

This is a multi-agent QA workflow. Spawn the following agents IN PARALLEL:

**Agent 1 — Functional tester**: Read the changed code and acceptance criteria (from PR description, commit messages, or task description). Verify that each claimed behavior is actually implemented. Produce: list of behaviors verified ✅, missing ❌, or ambiguous ⚠️.

**Agent 2 — Edge case hunter**: Analyze the changed code for edge cases, error handling gaps, and boundary conditions. Look at input validation, null checks, error branches, and off-by-one risks. Produce: ranked list of edge cases by severity (high/medium/low).

**Agent 3 — Regression analyst**: Identify which existing features are most at risk from the current changes. Trace data flow and shared code paths. Produce: list of regression risks with the specific code paths that connect old features to new changes.

After all agents complete:

1. Merge findings into a single QA report:

```
## QA Report — <feature/PR>
Date: <today>

### Functional coverage
<from Agent 1>

### Edge cases
<from Agent 2>

### Regression risks
<from Agent 3>

### Overall verdict
PASS / FAIL / CONDITIONAL PASS
Blocking issues: <list or "none">
```

2. For any ❌ or high-severity findings, suggest the minimal fix.
3. Ask the user: fix the issues now, or document them for follow-up?
