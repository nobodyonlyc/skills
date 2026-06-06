Bug report: $ARGUMENTS

Multi-agent bug investigation workflow. Run the following agents IN PARALLEL:

**Agent 1 — Root cause investigator**: Search the codebase for all code paths related to the reported bug. Trace the data flow. Identify the exact line(s) where the bug originates and why it happens.

**Agent 2 — Impact analyst**: Find all callers, tests, and related code that could be affected by a fix. Identify regression risk areas. Check git log for related recent changes.

After both agents complete:

1. Present the root cause and impact analysis.
2. Propose the minimal fix — change only what's needed to fix the root cause.
3. Get user approval before applying.
4. Apply the fix.
5. Add a regression test that would have caught this bug.
6. Run the full test suite.
7. Report: cause, fix applied, test added, regression risk assessment.
