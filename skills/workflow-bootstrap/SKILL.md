---
name: workflow-bootstrap
description: Coordinates the project setup sequence from phoning/interviewing the user, generating the spec/backlog, and building the project skeleton.
---

Bootstrap project using: $ARGUMENTS

Multi-agent orchestration to take a project from an idea description to a structured, restartable codebase. Run the phases in order. Each phase has a detailed playbook in [`references/`](references/); see [`examples/`](examples/) for a full worked run.

> **Entry point & scope — read first.** The backlog and every UI feature depend on artifacts that come *between* the architecture doc and the backlog, and *between* the backlog and execution. **Do not jump from architecture straight to the backlog, or from the backlog straight to feature work** — that silently skips the BA, the per-component SPECs, the design system, and the mock UI/prototype, and produces a backlog generated from the architecture alone (the #1 cause of missing User Stories). The normal front door is [workflow-intake](../workflow-intake/SKILL.md) Route 1, which sequences these for you. If you invoke this workflow directly, you are still responsible for **all five phases below** — Phases 2 and 4 are not optional for a project that has components/SPECs or a UI.

## Skills this workflow drives
- [plan-architecture-agent](../plan-architecture-agent/SKILL.md) — interviews the user and produces `docs/SYSTEM_ARCHITECTURE.md` (Phase 1).
- [dev-fe-developer](../dev-fe-developer/SKILL.md) / [dev-be-developer](../dev-be-developer/SKILL.md) / [dev-db-designer](../dev-db-designer/SKILL.md) / [dev-cli-tool-developer](../dev-cli-tool-developer/SKILL.md) — author the BA and the per-component SPECs under `docs/spec/` (Phase 2).
- [plan-us-backlog-generator](../plan-us-backlog-generator/SKILL.md) — turns the architecture doc **and the `docs/spec/*` SPECs** into a User-Story backlog (Phase 3, runs in the **main agent** — see its own "Do NOT spawn a subagent" directive).
- [plan-project-skeleton-generator](../plan-project-skeleton-generator/SKILL.md) — scaffolds folders, config, and baseline tests from the architecture doc (Phase 3, delegated subagent).
- [workflow-prototype](../workflow-prototype/SKILL.md) — renders the mock UI from `docs/spec/frontend.md`, styled with the approved design system (Phase 4, UI projects only).

> `us-backlog-generator` and `project-skeleton-generator` cannot run independently — both consume `docs/SYSTEM_ARCHITECTURE.md` produced in Phase 1. This workflow is their entry point.

## Phases
1. **Requirements Analysis & Tech Discovery** → [references/phase-1-architecture.md](references/phase-1-architecture.md)
   Interview the user, evaluate project size & persona, output `docs/SYSTEM_ARCHITECTURE.md`.
   *GATE*: After generating the document, use the [check-ba-evaluator](../check-ba-evaluator/SKILL.md) skill to spawn a Senior PM Subagent to review the architecture. If the subagent fails the document, revise it before proceeding.
2. **BA & per-component SPECs** → [workflow-intake/references/route-1-new-project.md](../workflow-intake/references/route-1-new-project.md) (steps 2–3)
   Write `docs/BA.md` (business goals, personas, journeys, in/out of scope; ask follow-ups on gaps), then a detailed SPEC under `docs/spec/` for **each component the architecture actually has** — `frontend.md`, `backend.md`, `database.md`, `cli.md`, … The per-component SPECs are independent, so **author them concurrently** (one SPEC-writer subagent per component in a single parallel batch), then run **one combined PM review** over the whole SPEC set ([check-ba-evaluator](../check-ba-evaluator/SKILL.md), single batched pass) and confirm them with the user as one packet — not a write→review→confirm cycle per file.
   *GATE*: `docs/BA.md` and the relevant `docs/spec/*` must exist before Phase 3 — the backlog generator reads them. Skipping this is what produces an architecture-only backlog.
3. **Scaffold & Backlog Generation** → [references/phase-3-backlog-and-skeleton.md](references/phase-3-backlog-and-skeleton.md)
   Generate the backlog (main agent) and scaffold the skeleton (subagent) from the architecture + the Phase 2 SPECs, then merge & verify.
   *GATE*: After the backlog is generated, use the [check-ba-evaluator](../check-ba-evaluator/SKILL.md) skill to spawn a Senior PM Subagent to review the backlog against the architecture and SPECs. Only ask the user for final approval if the PM subagent passes it.
4. **Common Design Phase (UI projects)** → [workflow-intake/references/common-design-phase.md](../workflow-intake/references/common-design-phase.md)
   Basic DB design, then — if the project has a UI — establish & approve `docs/spec/design-system.md`, then drive [workflow-prototype](../workflow-prototype/SKILL.md) to render the mock UI from `docs/spec/frontend.md`. Browser preview is mandatory; iterate until approved. Commit the design-phase artifacts before any feature work.
   *GATE*: ask-user approval of the design system and the mock UI before leaving this phase. Skip the UI sub-steps only if the project genuinely has no UI.
5. **Verification & Initial Handoff** → [references/phase-5-verify-handoff.md](references/phase-5-verify-handoff.md)
   Run `./init.sh`, confirm baseline passes, print backlog, then STOP for feature selection.

## Hard gates
- `docs/BA.md` and the per-component `docs/spec/*` exist **before** the backlog is generated (Phase 2 → Phase 3).
- The user must approve the User-Story backlog before it is written via `./harness add`.
- For a project with a UI, the design system and the mock UI/prototype are approved and committed **before** any feature implementation (Phase 4). This is now **hook-enforced**: once `docs/spec/frontend.md` exists, `hooks/harness-phase-guard.sh` blocks `./harness start` and any app-code edit until `docs/spec/design-system.md` **and** `prototype/*.html` exist. The backlog (`./harness add`, Phase 3) is still allowed before the prototype — only US *execution* is gated. If you see `HARNESS PHASE GUARD: ... design phase is not finished`, you skipped Phase 4: build the prototype before starting any US.
- After Phase 5, **STOP** — do not start any feature implementation. Hand control back so the user (or another agent) picks one feature (WIP = 1).
