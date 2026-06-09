# Route 3 — Add a feature to an existing harness project

Reached when [Phase 0](phase-0-classify.md) classified the prompt as **Case 3**: the repo already uses the harness and the prompt asks for a *new* capability not yet in the backlog.

## Steps

### 1. Understand the existing source
Read the existing codebase via its docs and code using [core-explain](../../core-explain/SKILL.md): the architecture (`docs/SYSTEM_ARCHITECTURE.md`), current SPECs, and the modules the new feature will touch. Summarise what already exists and what the new feature must integrate with.

### 2. Analyse the new feature → BA → SPEC
Write the business analysis for the new capability and a detailed SPEC for each component it affects (append to / extend `docs/spec/`). Confirm with the user (**ask-user**).

### 3. Add US to the backlog
Drive [plan-us-backlog-generator](../../plan-us-backlog-generator/SKILL.md) to turn the new SPEC into User Stories; present them and get approval before `./harness add`.

### 4. Update shared docs
Update the shared design artifacts the feature changes — DB design, SPECs, and the mock UI — via the [common design phase](common-design-phase.md) as needed.

### 5. Execute
Run each new US through [Route 2](route-2-us-execution.md).

## Gates
- **ask-user** after the source review, the BA/SPEC, the backlog, and any shared-doc update; on feedback, redo that step.
- Record steps as harness tasks ([task-convention](../../../resources/task-convention.md)).
