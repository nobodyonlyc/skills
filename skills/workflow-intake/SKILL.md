---
name: workflow-intake
description: Classify any incoming prompt into one of 4 cases and dispatch it to the matching harness flow.
---

Incoming request: $ARGUMENTS

The single entry point for the harness. **Classify** the prompt, **confirm** the classification with the user, record the work as harness tasks, then **dispatch** to the matching route. Every step is gated by **ask-user** and re-done on feedback. Detailed classification playbook is in [`references/`](references/); see [`examples/`](examples/) for a worked run.

## Phase 0 — Classify & confirm
Decide which of the 4 cases the prompt is, using the signals in [references/phase-0-classify.md](references/phase-0-classify.md). Present the classification to the user (the **ask-user** capability, see [agent-tool-mapping](../../resources/agent-tool-mapping.md)) and get explicit confirmation **before** dispatching. If the user corrects it, re-classify.

## Dispatch table (the 4 routes)
| Case | Signal | Dispatch |
|---|---|---|
| **1. New project** | empty / greenfield repo; "build me a …" | Route 1 — new-project intake (BA → per-component SPEC → US backlog → common design), see [references/route-1-new-project.md](references/route-1-new-project.md). Drives [workflow-bootstrap](../workflow-bootstrap/SKILL.md). |
| **2. Execute a US** | a backlog US id; "do F12" | Route 2 — analyse the US, split into child-tasks (`F<id>-T<n>`), dispatch each to [workflow-feature](../workflow-feature/SKILL.md) / [workflow-bugfix](../workflow-bugfix/SKILL.md) / [workflow-qa](../workflow-qa/SKILL.md) / [workflow-review-deep](../workflow-review-deep/SKILL.md). See [references/route-2-us-execution.md](references/route-2-us-execution.md). |
| **3. Add feature to a harness project** | existing harness repo + new capability | Route 3 — read source via docs ([core-explain](../core-explain/SKILL.md)) → BA → SPEC → add US → update shared docs → Route 2. See [references/route-3-add-feature.md](references/route-3-add-feature.md). |
| **4. Legacy onboarding** | "add harness to &lt;non-harness project&gt;" | Route 4 — dispatch [workflow-onboard](../workflow-onboard/SKILL.md): survey → docs → safe `harness init` (no clobber) → seed backlog. See [references/route-4-onboarding.md](references/route-4-onboarding.md). |

> Routes 1 & 3 share the [common design phase](references/common-design-phase.md) (basic DB design + mock UI) before per-US execution.

## Phase 0.5 — Pick autonomy mode
Determine the run's autonomy mode per [autonomy-mode](../../resources/autonomy-mode.md) and record it in the task-state file's `Mode:` field:
- Default is **`gated`** — stop at every ask-user gate.
- Switch to **`mode: auto`** only when the user explicitly asks for an unattended / long autonomous run. In `auto`, ask-user gates become logged decisions, but the always-stop list still halts for irreversible/outward-facing actions.

## Phase 0.6 — Pick collaboration mode (solo vs team)
Decide whether the repo is worked **solo** or by a **team**, and record it in the task-state file's `Collab:` field. This changes how Route 2 claims and integrates each feature (see [route-2 "Collaboration mode"](references/route-2-us-execution.md#collaboration-mode--read-alongside-auto-advance)).
- **`solo`** (default) — one agent/person at a time. Global **WIP = 1**; checkpoints land on the current branch; no `--assignee`/`--branch`.
- **`team`** — multiple people/agents share the repo concurrently. Each feature is claimed per-person on its own branch and integrated through a PR review gate: `./harness start <id> --assignee <name> --branch`, **WIP = 1 enforced per assignee**. Follow [branch-convention](../../resources/branch-convention.md) + [state-merge-convention](../../resources/state-merge-convention.md); full end-to-end flow in [docs/team-workflow.md](../../../docs/team-workflow.md).

**Detect team mode** when: the user says multiple people/agents share the repo, asks for an assignee/branch, **or** `.harness/features.json` already has any feature with a non-empty `assignee`/`branch`. When the signal is ambiguous, **ask-user** (click-select `solo` vs `team`). Auto-advance (Route 2) is a **solo-only** convenience — in `team` mode each assignee holds their own single feature, so do not auto-chain another assignee's stories.

## Cross-cutting rules (every step, every route)
- **Task tracking** — record each step as a harness task; a US splits into child-tasks per [task-convention](../../resources/task-convention.md).
- **Full gates** — every task runs review / test / verify / handoff.
- **Ask-user gate** — in `gated`, stop before/after each step and ask the user; on feedback, **redo that step**. In `mode: auto`, decide and log per [autonomy-mode](../../resources/autonomy-mode.md) instead of stopping (except the always-stop list). When the question is a **choice** (confirm classification, pick a route/method, approve/revise), present **click-select options**, not a free-text prompt — see [agent-tool-mapping](../../resources/agent-tool-mapping.md).
