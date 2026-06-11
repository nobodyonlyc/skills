# Route 1 — New-project intake

Reached when [Phase 0](phase-0-classify.md) classified the prompt as **Case 1 (new project)** and the user confirmed. Goal: turn a greenfield idea into an analysed, scoped, backlog-tracked project, then hand each US to execution.

This route is the orchestrated front of [workflow-bootstrap](../../workflow-bootstrap/SKILL.md); it adds an explicit **BA + per-component SPEC** step before the backlog.

## Steps

### 1. Interview — size, user role, high-level SPEC
Drive [plan-architecture-agent](../../plan-architecture-agent/SKILL.md) to interview the user: project **size**, **user role/persona**, and the high-level **SPEC** (goals, tech stack, components). Output: `docs/SYSTEM_ARCHITECTURE.md`.

### 2. Generate the BA (business analysis)
From the interview, write `docs/BA.md`: business goals, stakeholders/personas, core user journeys, in-scope vs out-of-scope. 
**Follow-up Interview (Crucial)**: After drafting the BA, analyze it for gaps. If the BA reveals hidden complexities, missing constraints, or edge cases, ask the user targeted follow-up questions before writing technical specs. 
Confirm the final `docs/BA.md` and the answers with the user (**ask-user**) before continuing.

### 3. Per-component detailed SPEC (author in parallel)
The per-component SPECs are **independent of each other** — they all derive from the same approved architecture + BA. Author them **concurrently**: spawn one SPEC-writer subagent per component **in a single parallel batch** (FE, BE, DB, CLI, … — only the components that actually exist), each writing its own `docs/spec/*` file. Do not write them one-after-another and confirm each in turn; wall-clock then ≈ the slowest single SPEC instead of the sum.

For **each component present** in the architecture, write a detailed SPEC under `docs/spec/`:
- **FE** → `docs/spec/frontend.md` (screens, flows, components; see [dev-fe-developer](../../dev-fe-developer/SKILL.md)).
- **BE** → `docs/spec/backend.md` (API contract, layers; see [dev-be-developer](../../dev-be-developer/SKILL.md)).
- **DB** → `docs/spec/database.md` (entities, relationships; see [dev-db-designer](../../dev-db-designer/SKILL.md)).
- **CLI** → `docs/spec/cli.md` (commands, flags; see [dev-cli-tool-developer](../../dev-cli-tool-developer/SKILL.md)).
- **TOOL / batch** → `docs/spec/<tool>.md` (see [dev-batch-developer](../../dev-batch-developer/SKILL.md)).

Only generate SPECs for components that actually exist in this project. Once the parallel batch returns, run **one combined PM review** over all the new SPECs at once ([check-ba-evaluator](../../check-ba-evaluator/SKILL.md), single batched pass — not one spawn per file) to catch cross-SPEC inconsistencies (e.g. an endpoint in the BE SPEC with no screen in the FE SPEC). Apply all findings in a single revision pass, then present the SPEC set to the user for confirmation as one packet.

### 4. Create the US backlog
Drive [plan-us-backlog-generator](../../plan-us-backlog-generator/SKILL.md) to parse the BA **and the detailed `docs/spec/*` SPECs** into User Stories. Before presenting, run its **coverage check** (Step 2.5): a PM subagent ([check-ba-evaluator](../../check-ba-evaluator/SKILL.md) Mode B) verifies every SPEC item — screen, endpoint, entity, business rule — maps to a US, and the gaps are filled. Then present the proposed backlog as a table (click-select approve/revise) and get explicit user approval **before** writing it via `./harness add`.

### 5. Common design phase
Hand off to the shared [common design phase](common-design-phase.md) (basic DB design + mock UI) before per-US execution.

### 6. Execute each US
Run each US through [Route 2](route-2-us-execution.md) — split into child-tasks and dispatch to the matching workflow.

## Gates
- Stop and **ask-user** after the interview, the BA, the **SPEC set** (all per-component SPECs presented together as one packet, not one gate per file), and the backlog. On feedback, redo that step.
- Record each step as a harness task where useful ([task-convention](../../../resources/task-convention.md)).
- After the backlog is approved, follow the harness rule: **STOP** and let the user pick one US (WIP = 1) — execution is Route 2, not part of this route.
