# Phase 5 — Verification & Initial Handoff (final phase)

> This is the **last** phase. Prerequisites: the backlog + skeleton are merged ([phase-3-backlog-and-skeleton.md](phase-3-backlog-and-skeleton.md)), and — for a project with a UI — the **common design phase** is complete: `docs/spec/design-system.md` and the mock UI/prototype are approved and committed ([SKILL.md](../SKILL.md) Phase 4 / [common-design-phase](../../workflow-intake/references/common-design-phase.md)). Do not hand off with the design phase skipped on a UI project.

## Steps
1. Run the environment startup script:
   ```bash
   ./init.sh
   ```
2. Confirm the workspace compiles cleanly and all baseline tests pass. If `init.sh` fails, fix the scaffold before handing off — never hand off a broken baseline.
3. Print the backlog:
   ```bash
   ./harness status
   ```

## Hard gate — STOP
- **Do not start any feature implementation.**
- Tell the user bootstrapping is complete, display the final backlog, and ask them to select a single feature (WIP = 1) to proceed with, or invite other team members to pick up tasks.
- Feature work continues in [workflow-feature](../../workflow-feature/SKILL.md).
