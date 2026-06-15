---
name: workflow-bugfix
description: Orchestrate a multi-agent workflow to investigate, locate, fix, and verify a bug.
---

Bug report: $ARGUMENTS

Multi-agent bug investigation workflow that coordinates diagnostic and correction tasks. Each phase has a detailed playbook in [`references/`](references/); see [`examples/`](examples/) for a full worked run.

## Skills this workflow drives
- [core-explain](../core-explain/SKILL.md) — trace data flow and inspect the suspect code logic (Phase 1).
- [dev-db-designer](../dev-db-designer/SKILL.md) — consulted when the bug is database-related (Phase 1).
- [check-test-gen](../check-test-gen/SKILL.md) — write the failing regression test that pins the bug (Phase 2).
- [core-fix](../core-fix/SKILL.md) — implement the minimal, root-cause fix (Phase 2).
- [dev-be-developer](../dev-be-developer/SKILL.md) / [dev-fe-developer](../dev-fe-developer/SKILL.md) / [dev-batch-developer](../dev-batch-developer/SKILL.md) — component-specific fix guidance (Phase 2).
- [check-code-review](../check-code-review/SKILL.md) — review the fix diff (Phase 2).
- [check-qa](../check-qa/SKILL.md) — full verification pass before the checkpoint (Phase 3).

## Phases
1. **Parallel Investigation & Analysis** → [references/phase-1-investigation.md](references/phase-1-investigation.md)
   Root-cause investigator + impact analyst run in parallel; align on a fix proposal.
2. **Implement · Test · Review Loop** → [references/phase-2-fix-test-review-loop.md](references/phase-2-fix-test-review-loop.md)
   Write a failing regression test, apply the minimal fix, loop until tests pass and review is clean.
3. **Verification & Checkpoint** → [references/phase-3-verify-checkpoint.md](references/phase-3-verify-checkpoint.md)
   Run the QA suite, `./harness verify`, and report root cause + fix + test + regression risk.

## Hard gates
- **Autonomy mode**: honor the run's mode (`gated` default / `auto`) per [autonomy-mode](../../resources/autonomy-mode.md). In `auto`, ask-user gates become logged decisions — except the always-stop list, which always halts.
- **Durable task state**: maintain `.harness/tasks/<id>.md` per the [task-state convention](../../resources/task-state-convention.md) — created at start, its granular checklist **updated and committed at every phase boundary AND before marking `passing`** (in `auto` mode too — auto suppresses ask-user, never state-keeping). `evidence.md` must be non-empty before verify (hook-enforced).
- **Strict File-Based Communication**: Do NOT pass error logs or code snippets via chat messages. When Reviewers/Testers output files to `.harness/reports/`, send ONLY the file path to the Developer subagent.
- The regression test must **fail before** the fix and **pass after** — never claim a fix without it.
- Keep the fix minimal and within scope; a feature moves to `passing` only after `./harness verify` succeeds.
