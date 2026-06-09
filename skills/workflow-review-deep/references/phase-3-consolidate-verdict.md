# Phase 3 — Consolidate & Verdict

**Skills used:** [check-pr-review](../../check-pr-review/SKILL.md), [check-refactor](../../check-refactor/SKILL.md)

## 1. Merge findings
Collect every agent's findings from [Phase 2](phase-2-per-file-review.md), deduplicate, and sort by severity.

## 2. Present the consolidated report
Frame it as a PR review ([check-pr-review](../../check-pr-review/SKILL.md)):
- 🔴 **Critical** — must fix before merge.
- 🟡 **Important** — should fix.
- 🔵 **Suggestions** — optional improvements.

## 3. Verdict
Give one explicit verdict: **Approve** / **Request Changes** / **Needs Discussion**.

## 4. Optional fixes
Ask if the user wants to apply any suggested fixes. If yes, shape them with [check-refactor](../../check-refactor/SKILL.md) (behavior-preserving) — or hand correctness fixes to [workflow-bugfix](../../workflow-bugfix/SKILL.md).
