# Route 4 — Legacy-integration guard

Reached when [Phase 0](phase-0-classify.md) classified the prompt as **Case 4**: the user wants to add the harness itself to an existing project that does **not** already use AI / harness tooling.

## Action
This is **not supported yet**. Do not modify the project.

1. Tell the user clearly that automated harness integration into a legacy (non-harness) project is **not yet implemented**.
2. Do **not** scaffold, init, or change any files.
3. Stop and return control.

## Suggested next step (offer, do not perform)
If the user instead wants to start fresh, point them at **Case 1 (new project)** / [Route 1](route-1-new-project.md). Onboarding an existing legacy codebase remains a future capability.
