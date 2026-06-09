# Common design phase (Routes 1 & 3)

Runs after analysis and **before** per-US execution. Produces two shared artifacts that the US implementations build on: a basic DB design and an approved mock UI. Reused by [Route 1](route-1-new-project.md) and Route 3.

## 1. Basic DB design
From the BA and the tech-stack SPEC, drive [dev-db-designer](../../dev-db-designer/SKILL.md) to produce a **basic schema** (core entities, relationships, key constraints) under `docs/spec/database.md` / migration stubs. Keep it foundational — full per-feature schema work happens inside each US.

## 2. Mock UI
If the project has a UI, drive [dev-fe-developer](../../dev-fe-developer/SKILL.md) to build a **mock UI**:
- Default: standalone **HTML/CSS** the user can open.
- Use **Figma** instead only if the SPEC explicitly requires it.
- Iterate until the user approves (reuse dev-fe-developer's mandatory UI design gate): present → feedback → revise → re-present, repeat until explicit approval.

## Gates
- **ask-user** approval is required for both the DB design and the mock UI before leaving this phase; on feedback, redo that artifact.
- Record each artifact as a harness task where useful ([task-convention](../../../resources/task-convention.md)).

→ Once both are approved, proceed to per-US execution via [Route 2](route-2-us-execution.md).
