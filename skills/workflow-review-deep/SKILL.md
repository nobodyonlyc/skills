---
name: workflow-review-deep
description: Orchestrate a multi-agent workflow to perform a deep-dive security, correctness, and architecture review.
---

Deep multi-agent code review. PR number or branch: $ARGUMENTS

Multi-agent deep review: fan out one reviewer per changed file, then consolidate into a single verdict. Each phase has a detailed playbook in [`references/`](references/); see [`examples/`](examples/) for a full worked run.

## Skills this workflow drives
- [check-code-review](../check-code-review/SKILL.md) — correctness, performance, and simplification review per file (Phase 2).
- [check-security-review](../check-security-review/SKILL.md) — injection, secrets, auth, and input-validation review per file (Phase 2).
- [check-refactor](../check-refactor/SKILL.md) — shape the suggested cleanups when the user opts to apply fixes (Phase 3).
- [check-pr-review](../check-pr-review/SKILL.md) — frame the consolidated verdict as a PR review (Phase 3).

## Phases
1. **Gather & Fan-out** → [references/phase-1-gather-fanout.md](references/phase-1-gather-fanout.md)
   Collect the changed files (PR or branch diff) and spawn one review agent per file (batch beyond 8).
2. **Per-file Review** → [references/phase-2-per-file-review.md](references/phase-2-per-file-review.md)
   Each agent reviews its file for correctness, security, performance, and simplification.
3. **Consolidate & Verdict** → [references/phase-3-consolidate-verdict.md](references/phase-3-consolidate-verdict.md)
   Merge, dedupe, sort by severity, give a verdict, and optionally apply fixes.

## Hard gates
- Sort every finding by severity (🔴 Critical / 🟡 Important / 🔵 Suggestion) before presenting.
- Give one explicit verdict: **Approve** / **Request Changes** / **Needs Discussion**, and ask before applying any fix.
