# Phase 1 — Gather & Fan-out

Collect the set of changed files to review.

```bash
if echo "$ARGUMENTS" | grep -qE '^[0-9]+$'; then
  gh pr diff "$ARGUMENTS" --name-only
else
  git diff main..HEAD --name-only 2>/dev/null || git diff master..HEAD --name-only
fi
```

## Fan-out
- Spawn **one review agent per changed file**, up to 8 in parallel.
- If there are more than 8 files, **batch** the remainder into follow-up waves so every file is covered.
- Each agent receives the **full file content + its diff**.

→ Each agent runs [Phase 2](phase-2-per-file-review.md).
