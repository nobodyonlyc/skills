Deep multi-agent code review. PR number or branch: $ARGUMENTS

Gather changed files:

```bash
if echo "$ARGUMENTS" | grep -qE '^[0-9]+$'; then
  gh pr diff "$ARGUMENTS" --name-only
else
  git diff main..HEAD --name-only 2>/dev/null || git diff master..HEAD --name-only
fi
```

Spawn one review agent per changed file (up to 8 files; batch remaining files if more):

Each agent receives: the full file content + its diff, and reviews for:
- Correctness bugs
- Security issues  
- Performance problems
- Simplification opportunities

After all agents complete:

1. Merge findings, deduplicate, and sort by severity.
2. Present consolidated report:
   - 🔴 Critical (must fix before merge)
   - 🟡 Important (should fix)
   - 🔵 Suggestions (optional improvements)
3. Give overall verdict: **Approve** / **Request Changes** / **Needs Discussion**.
4. Ask if the user wants to apply any of the suggested fixes.
