---
name: check-code-review
description: Review code changes for correctness, logic errors, security risks, and opportunities for simplification.
---

> **[Orchestrator Instructions]** Do NOT execute this skill yourself. You MUST use the invoke_subagent tool to spawn an independent subagent with the Role: **Principal Engineer**.


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

Review the changes and write a report to `.harness/reports/code-review.md`. Your chat response must ONLY be the path to this file (e.g. "Review complete. See .harness/reports/code-review.md"). Do NOT output the report text in the chat.

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
