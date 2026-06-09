---
name: check-code-review
description: Review code changes for correctness, logic errors, security risks, and opportunities for simplification.
---

Gather the current changes to review:

```bash
git status
git diff --staged
git diff
```

If $ARGUMENTS is provided, treat it as a specific file or directory to focus on:
```bash
[ -n "$ARGUMENTS" ] && git diff -- "$ARGUMENTS" && git diff --staged -- "$ARGUMENTS"
```

Review the changes and report:

## Bugs & Correctness
- Logic errors, edge cases not handled, broken error paths
- Incorrect assumptions about input types or ranges

## Security
- Any injection risks, exposed secrets, missing input validation

## Simplification
- Unnecessary complexity, duplicated logic, better built-ins available

## Format each finding as:
`[severity] file:line — description — suggested fix`

Severities: 🔴 bug | 🟡 smell | 🔵 nit

Keep the review concise — only findings worth acting on. Skip obvious style issues handled by linters.
