# Phase 3 — Verification & Initial Handoff

Prerequisite: backlog + skeleton merged in [Phase 2](phase-2-backlog-and-skeleton.md).

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
