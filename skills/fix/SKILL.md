---
name: fix
description: Analyze a bug report or error stack trace, pinpoint the root cause, and implement a robust fix.
---

Bug to fix: $ARGUMENTS

Gather context:

```bash
git status
git log --oneline -10
```

Follow this workflow:

1. **Understand** — Read the relevant files. Identify the root cause, not just the symptom.
2. **Reproduce** — Show the exact condition that triggers the bug (input, state, sequence of events).
3. **Fix** — Apply the minimal change that addresses the root cause. Don't refactor unrelated code.
4. **Verify** — Run existing tests. If the bug had no test, add one that would have caught it.
5. **Confirm** — Summarize: what was wrong, what changed, and how to verify the fix works.

If the bug description is unclear, ask one focused question before proceeding.
