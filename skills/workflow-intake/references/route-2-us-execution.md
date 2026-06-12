# Route 2 — US execution + task decomposition

The shared execution core. Reached to implement a single User Story (directly in Case 2, or after the backlog is built in Routes 1 & 3). One US at a time (WIP = 1).

## Auto-advance — read first
Before executing, read `.harness/context.json` and compute the **auto-advance** mode (see [context-schema.md](../../plan-architecture-agent/references/context-schema.md)):
- Use `auto_advance` if present; otherwise it **defaults ON for `user_role == "Non-Technical"`** and OFF for `Developer`.
- **OFF (default for dev):** after each US reaches `passing`, **STOP** and hand back so the user picks the next US — the classic behaviour in Step 5.
- **ON (default for non-tech):** do **not** stop between stories. After a US is `passing`, immediately select the next-highest-priority unfinished US (`./harness resume` / `./harness status`) and start it, chaining until the backlog is exhausted. Non-tech users find a stop-and-wait-per-US flow confusing — it looks stuck — so keep moving.

Auto-advance changes **only the human handoff between stories**. It does **not** relax **WIP = 1** (still one US at a time), the full per-task gates (review / test / `./harness verify`), or approval of any irreversible action. **Hard stops that always return control even when ON:** backlog exhausted, a US/task `blocked`, `./harness verify` fails and can't be auto-resolved, or a deploy/release/destructive action needs sign-off. Print `./harness report` at each US boundary so the user can watch progress.

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
The parent US moves to `passing` only after all its child-tasks are `passing`. Then:
- **Auto-advance OFF:** **STOP** and hand back for the next US selection.
- **Auto-advance ON:** print `./harness report`, then immediately select the next-highest-priority unfinished US and return to Step 1 — no wait — unless a hard stop applies (backlog exhausted, next US `blocked`, verify failing, or sign-off needed).

## Gates
- **ask-user** before/after each task; on feedback, redo that task. **Under auto-advance**, suppress the *routine* "shall I proceed / is this OK" confirmations between tasks and stories — but still ask when a genuine requirement ambiguity or an irreversible/outward-facing action arises.
- Never mark a task `passing` without its verification actually succeeding. (Auto-advance never overrides this.)
