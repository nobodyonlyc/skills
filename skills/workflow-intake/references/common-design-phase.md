# Common design phase (Routes 1 & 3)

Runs after analysis and **before** per-US execution. Produces two shared artifacts that the US implementations build on: a basic DB design and an approved mock UI. Reused by [Route 1](route-1-new-project.md) and Route 3.

## 1. Basic DB design
From the BA and the tech-stack SPEC, drive [dev-db-designer](../../dev-db-designer/SKILL.md) to produce a **basic schema** (core entities, relationships, key constraints) under `docs/spec/database.md` / migration stubs. Keep it foundational — full per-feature schema work happens inside each US.

## 2. Mock UI
If the project has a UI, generate the **mock UI** from the FE SPEC via [workflow-prototype](../../workflow-prototype/SKILL.md) (UI only — no backend/DB):
- It renders **every screen + function** in `docs/spec/frontend.md`.
- Method: standalone **HTML/CSS**, or **Figma via an MCP connector** if the SPEC requires it.
- Mandatory **browser preview**, then iterate: present → feedback → regenerate/extend → re-preview, until the user approves every screen.

## Gates
- **ask-user** approval is required for both the DB design and the mock UI before leaving this phase; on feedback, redo that artifact.
- Record each artifact as a harness task where useful ([task-convention](../../../resources/task-convention.md)).

→ Once both are approved, proceed to per-US execution via [Route 2](route-2-us-execution.md).
