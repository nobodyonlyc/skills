Gather git context to prepare a pull request:

```bash
git branch --show-current
git log main..HEAD --oneline 2>/dev/null || git log master..HEAD --oneline
git diff main..HEAD --stat 2>/dev/null || git diff master..HEAD --stat
git diff main..HEAD 2>/dev/null || git diff master..HEAD
```

Based on the output:

1. Analyze all commits and the full diff to understand what this PR does
2. Draft a PR with this structure:
   - **Title**: `<type>: <concise summary>` (under 70 chars)
   - **Summary**: 2-4 bullet points on what changed and why
   - **Test plan**: checklist of what to verify before merging
   - **Breaking changes**: list any if present, otherwise omit

3. Ask the user: approve as-is, edit the draft, or create the PR now via:
```bash
gh pr create --title "<title>" --body "<body>"
```
