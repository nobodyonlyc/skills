---
name: workflow-bootstrap
description: Coordinates the project setup sequence from phoning/interviewing the user, generating the spec/backlog, and building the project skeleton.
---

Bootstrap project using: $ARGUMENTS

Multi-agent orchestration to take a project from an idea description to a structured, restartable codebase. Run the phases in order. Each phase has a detailed playbook in [`references/`](references/); see [`examples/`](examples/) for a full worked run.

## Skills this workflow drives
- [plan-architecture-agent](../plan-architecture-agent/SKILL.md) — interviews the user and produces `docs/SYSTEM_ARCHITECTURE.md` (Phase 1).
- [plan-us-backlog-generator](../plan-us-backlog-generator/SKILL.md) — turns the architecture doc into a User-Story backlog (Phase 2, Subagent A).
- [plan-project-skeleton-generator](../plan-project-skeleton-generator/SKILL.md) — scaffolds folders, config, and baseline tests from the architecture doc (Phase 2, Subagent B).
- [dev-db-designer](../dev-db-designer/SKILL.md) — consulted by the skeleton agent when the architecture defines a database.

> `us-backlog-generator` and `project-skeleton-generator` cannot run independently — both consume `docs/SYSTEM_ARCHITECTURE.md` produced in Phase 1. This workflow is their entry point.

## Phases
1. **Requirements Analysis & Tech Discovery** → [references/phase-1-architecture.md](references/phase-1-architecture.md)
   Interview the user, evaluate project size & persona, output `docs/SYSTEM_ARCHITECTURE.md`.
2. **Parallel Scaffold & Backlog Generation** → [references/phase-2-backlog-and-skeleton.md](references/phase-2-backlog-and-skeleton.md)
   Run the backlog generator and skeleton scaffolder as parallel subagents, then merge & verify.
3. **Verification & Initial Handoff** → [references/phase-3-verify-handoff.md](references/phase-3-verify-handoff.md)
   Run `./init.sh`, confirm baseline passes, print backlog, then STOP for feature selection.

## Hard gates
- The user must approve the User-Story backlog before it is written via `./harness add`.
- After Phase 3, **STOP** — do not start any feature implementation. Hand control back so the user (or another agent) picks one feature (WIP = 1).
