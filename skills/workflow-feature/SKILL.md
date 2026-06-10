---
name: workflow-feature
description: Orchestrate a multi-agent workflow to plan, implement, test, and verify a new feature.
---

Feature request: $ARGUMENTS

Multi-agent feature development workflow that coordinates analysts, developers, and testers around a single feature (WIP = 1). Each phase has a detailed playbook in [`references/`](references/); see [`examples/`](examples/) for a full worked run.

## Skills this workflow drives
- [core-explain](../core-explain/SKILL.md) — read and understand existing code/patterns (Phase 1).
- [dev-db-designer](../dev-db-designer/SKILL.md) — schema & migration design when DB changes are needed (Phase 1 & 2).
- [check-test-gen](../check-test-gen/SKILL.md) — plan and write the test suite (Phase 1 strategy, Phase 2 execution).
- [dev-be-developer](../dev-be-developer/SKILL.md) / [dev-fe-developer](../dev-fe-developer/SKILL.md) / [dev-cli-tool-developer](../dev-cli-tool-developer/SKILL.md) / [dev-batch-developer](../dev-batch-developer/SKILL.md) — implementation, chosen by component type (Phase 2).
- [check-code-review](../check-code-review/SKILL.md) — review the diff each loop iteration (Phase 2).
- [check-qa](../check-qa/SKILL.md) — full verification pass before the checkpoint (Phase 3).

## Phases
1. **Confirmation, Analysis & Planning** → [references/phase-1-analysis-planning.md](references/phase-1-analysis-planning.md)
   Confirm the target feature (WIP=1), run Requirements Analyst + Test Strategist in parallel, approve the plan and (if UI) the design.
2. **Code · Test · Review Loop** → [references/phase-2-build-test-review-loop.md](references/phase-2-build-test-review-loop.md)
   Iterate: parallel FE/BE implementation → run tests → code review, looping until clean.
3. **Verification & Checkpoint** → [references/phase-3-verify-checkpoint.md](references/phase-3-verify-checkpoint.md)
   Run the QA suite, `./harness verify`, session stop, clean, then STOP.

## Hard gates
- **Durable task state**: maintain `.harness/tasks/<id>.md` per the [task-state convention](../../resources/task-state-convention.md) — created at start, updated and committed at every phase boundary, so a crashed session can resume.
- **Strict File-Based Communication**: Do NOT pass error logs or code snippets via chat messages. When Reviewers/Testers output files to `.harness/reports/`, send ONLY the file path to the Developer subagent.
- Work on exactly **one** feature (WIP = 1). Confirm the target with the user before any work.
- If the feature has UI, get explicit approval of a visual mockup **before** writing implementation code (see Phase 1).
- A feature only moves to `passing` after `./harness verify <id>` succeeds with evidence.
