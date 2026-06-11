# Common design phase (Routes 1 & 3)

Runs after analysis and **before** per-US execution. Produces the shared artifacts the US implementations build on: a basic DB design, an approved **design system**, and an approved mock UI. Reused by [Route 1](route-1-new-project.md) and Route 3.

## 1. Basic DB design
From the BA and the tech-stack SPEC, drive [dev-db-designer](../../dev-db-designer/SKILL.md) to produce a **basic schema** (core entities, relationships, key constraints) under `docs/spec/database.md` / migration stubs. Keep it foundational — full per-feature schema work happens inside each US.

## 2. Design system (establish FIRST, if the project has a UI)
Before drawing any screen, decide the project's visual language once and persist it to **`docs/spec/design-system.md`** (committed). This is the single source of truth every later prototype — the initial mock **and** each per-US screen — reads and reuses, so the UI stays consistent instead of each prototype reinventing its own look.

`docs/spec/design-system.md` must capture:
- **Style direction** — a few words on the intended feel (e.g. "minimal, professional" / "playful, rounded").
- **Color palette**, **typography** (font families + size scale), **spacing scale**, **breakpoints**, and **component conventions** (button/input/card styles, radius, shadows).
- A copy-pasteable **`:root { … }` CSS custom-property block** holding the actual token values, so an HTML/CSS prototype can drop it straight in.

Get explicit **ask-user** approval of the design system **before** generating screens.

## 3. Mock UI
If the project has a UI, generate the **mock UI** from the FE SPEC via [workflow-prototype](../../workflow-prototype/SKILL.md) (UI only — no backend/DB), **styled with the approved `docs/spec/design-system.md` tokens**:
- It renders **every screen + function** in `docs/spec/frontend.md`.
- Method: standalone **HTML/CSS/JS**, or **Figma via an MCP connector** if the SPEC requires it.
- Mandatory preview — **browser** for HTML/CSS/JS, or the **MCP tool** for Figma — then iterate: present → feedback → regenerate/extend → re-preview, until the user approves every screen. Feedback that changes the look updates `design-system.md` so it stays the source of truth.

## Gates
- **ask-user** approval is required for the DB design, the **design system**, and the mock UI before leaving this phase; on feedback, redo that artifact.
- Record each artifact as a harness task where useful ([task-convention](../../../resources/task-convention.md)).

→ Once all are approved, proceed to per-US execution via [Route 2](route-2-us-execution.md).
