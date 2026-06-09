# Route 2 — US execution + task decomposition

The shared execution core. Reached to implement a single User Story (directly in Case 2, or after the backlog is built in Routes 1 & 3). One US at a time (WIP = 1).

## Steps

### 1. Analyse the US
Read the US from `.harness/features.json` and its SPEC. Identify the components it touches and its acceptance criteria.

### 2. Decompose into child-tasks
Split the US into child-tasks (`F<id>-T<n>`) and `./harness add` them up front per the [task-convention](../../../resources/task-convention.md), so the breakdown is durable. Small US may stay a single item.

### 3. Dispatch each task to the matching workflow
Per task, pick the workflow by task type:
- New behaviour / feature work → [workflow-feature](../../workflow-feature/SKILL.md).
- A defect → [workflow-bugfix](../../workflow-bugfix/SKILL.md).
- A QA pass → [workflow-qa](../../workflow-qa/SKILL.md).
- A pre-merge deep review → [workflow-review-deep](../../workflow-review-deep/SKILL.md).

### 4. Full gates per task
Each task runs review / test / `./harness verify` / handoff before it is `passing`. Work tasks one at a time (WIP = 1).

### 5. Close the US
The parent US moves to `passing` only after all its child-tasks are `passing`. Then **STOP** and hand back for the next US selection.

## Gates
- **ask-user** before/after each task; on feedback, redo that task.
- Never mark a task `passing` without its verification actually succeeding.
