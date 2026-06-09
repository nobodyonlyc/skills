---
name: workflow-prototype
description: Orchestrate a multi-agent workflow to rapidly prototype, test, and refine a new idea.
---

Prototype request: $ARGUMENTS

Multi-agent rapid-prototyping workflow: research the stack, get the UI design approved, then build the smallest thing that demonstrates the idea. Each phase has a detailed playbook in [`references/`](references/); see [`examples/`](examples/) for a full worked run.

## Skills this workflow drives
- [core-explain](../core-explain/SKILL.md) — scan the existing codebase for reusable stack & code (Phase 1, Stack researcher).
- [dev-fe-developer](../dev-fe-developer/SKILL.md) — build the viewable UI mockup and the UI of the prototype (Phase 2 & 3).
- [dev-be-developer](../dev-be-developer/SKILL.md) — stub/implement the minimal backend or API surface (Phase 3).
- [core-prototype](../core-prototype/SKILL.md) — single-file, speed-first build guidance for the core concept (Phase 3).

## Phases
1. **Research & Interface Spec** → [references/phase-1-research-interface.md](references/phase-1-research-interface.md)
   Parallel: Stack researcher + Interface designer. Present and confirm with the user.
2. **MANDATORY UI Design Gate** → [references/phase-2-ui-design-gate.md](references/phase-2-ui-design-gate.md)
   If there is a UI, build a real viewable mockup, iterate until the user explicitly approves. Hard gate.
3. **Build · Run · Handoff** → [references/phase-3-build-handoff.md](references/phase-3-build-handoff.md)
   Build the smallest working prototype, run it, show real output, and write handoff notes.

## Hard gates
- If the prototype has a UI, **do not write any prototype logic** until the user has explicitly approved the visual mockup (Phase 2). Iterate on the mockup as many times as requested.
- Keep it a prototype — hardcode/stub everything that isn't the core concept, and say so in the handoff.
