# Phase 1 — Research & Interface Spec

**Skill used:** [core-explain](../../core-explain/SKILL.md)

Spawn both agents **IN PARALLEL**.

## Agent 1 — Stack researcher
- **Skill:** [core-explain](../../core-explain/SKILL.md)
- **Task:** Scan the existing codebase for languages, frameworks, and libraries already in use; find similar code to reuse or adapt.
- **Output:** (1) recommended tech stack for the prototype, (2) existing snippets to reuse, (3) gotchas/constraints from the current setup.

## Agent 2 — Interface designer
- **Task:** Define the minimal interface from the prototype description: inputs, outputs, and the single core interaction.
  - UI → describe the screens/components (a real mockup comes in [Phase 2](phase-2-ui-design-gate.md), not here).
  - API/CLI/library → define the function signatures or commands.
- **Output:** a concrete interface spec (not implementation).

## Converge
Present the stack recommendation + interface spec to the user. Confirm or adjust before proceeding.

→ If there is a UI, go to [Phase 2](phase-2-ui-design-gate.md). Otherwise jump to [Phase 3](phase-3-build-handoff.md).
