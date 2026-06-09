# Route 1 — New-project intake

Reached when [Phase 0](phase-0-classify.md) classified the prompt as **Case 1 (new project)** and the user confirmed. Goal: turn a greenfield idea into an analysed, scoped, backlog-tracked project, then hand each US to execution.

This route is the orchestrated front of [workflow-bootstrap](../../workflow-bootstrap/SKILL.md); it adds an explicit **BA + per-component SPEC** step before the backlog.

## Steps

### 1. Interview — size, user role, high-level SPEC
Drive [plan-architecture-agent](../../plan-architecture-agent/SKILL.md) to interview the user: project **size**, **user role/persona**, and the high-level **SPEC** (goals, tech stack, components). Output: `docs/SYSTEM_ARCHITECTURE.md`.

### 2. Generate the BA (business analysis)
From the interview, write `docs/BA.md`: business goals, stakeholders/personas, core user journeys, in-scope vs out-of-scope. Confirm it with the user (**ask-user**) before continuing.

### 3. Per-component detailed SPEC
For **each component present** in the architecture, write a detailed SPEC under `docs/spec/`:
- **FE** → `docs/spec/frontend.md` (screens, flows, components; see [dev-fe-developer](../../dev-fe-developer/SKILL.md)).
- **BE** → `docs/spec/backend.md` (API contract, layers; see [dev-be-developer](../../dev-be-developer/SKILL.md)).
- **DB** → `docs/spec/database.md` (entities, relationships; see [dev-db-designer](../../dev-db-designer/SKILL.md)).
- **CLI** → `docs/spec/cli.md` (commands, flags; see [dev-cli-tool-developer](../../dev-cli-tool-developer/SKILL.md)).
- **TOOL / batch** → `docs/spec/<tool>.md` (see [dev-batch-developer](../../dev-batch-developer/SKILL.md)).

Only generate SPECs for components that actually exist in this project. Confirm each SPEC with the user.

### 4. Create the US backlog
Drive [plan-us-backlog-generator](../../plan-us-backlog-generator/SKILL.md) to parse the BA + SPECs into User Stories. Present the proposed backlog as a table and get explicit user approval **before** writing it via `./harness add`.

### 5. Common design phase
Hand off to the shared **common design phase** (basic DB design + mock UI) before per-US execution. *(playbook: F25)*

### 6. Execute each US
Run each US through **Route 2** — split into child-tasks and dispatch to the matching workflow. *(playbook: F26)*

## Gates
- Stop and **ask-user** after the interview, the BA, each SPEC, and the backlog. On feedback, redo that step.
- Record each step as a harness task where useful ([task-convention](../../../resources/task-convention.md)).
- After the backlog is approved, follow the harness rule: **STOP** and let the user pick one US (WIP = 1) — execution is Route 2, not part of this route.
