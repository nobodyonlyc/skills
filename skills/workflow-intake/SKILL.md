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
| **2. Execute a US** | a backlog US id; "do F12" | Route 2 — analyse the US, split into child-tasks (`F<id>-T<n>`), dispatch each to [workflow-feature](../workflow-feature/SKILL.md) / [workflow-bugfix](../workflow-bugfix/SKILL.md) / [workflow-qa](../workflow-qa/SKILL.md) / [workflow-review-deep](../workflow-review-deep/SKILL.md). *(playbook: F26)* |
| **3. Add feature to a harness project** | existing harness repo + new capability | Route 3 — read source via docs ([core-explain](../core-explain/SKILL.md)) → BA → SPEC → add US → update shared docs → Route 2. *(playbook: F27)* |
| **4. Legacy integration** | "add harness to &lt;non-harness project&gt;" | Route 4 — not supported: notify the user and stop. *(playbook: F28)* |

> Route playbooks under `references/route-*.md` are added by F24–F28. Until a playbook exists, dispatch to the named existing workflow directly.

## Cross-cutting rules (every step, every route)
- **Task tracking** — record each step as a harness task; a US splits into child-tasks per [task-convention](../../resources/task-convention.md).
- **Full gates** — every task runs review / test / verify / handoff.
- **Ask-user gate** — stop before/after each step and ask the user; on feedback, **redo that step** before moving on.
