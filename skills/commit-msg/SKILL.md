---
name: commit-msg
description: Generate a structured, clean, and concise git commit message based on staged changes.
---

Run the following bash commands to gather git context:

```bash
git status
git diff --staged
git diff
git log --oneline -5
```

Based on the output:
1. Summarize what files changed and what kind of changes they are (new feature, fix, refactor, config, docs, etc.)
2. Propose a concise commit message following this format:
   - First line: `<type>: <short summary>` (under 72 chars)
   - Optional body: bullet points explaining the why if non-obvious
3. Ask the user if they want to use the message, adjust it, or stage + commit directly.

Types: feat, fix, refactor, chore, docs, style, test, ci
