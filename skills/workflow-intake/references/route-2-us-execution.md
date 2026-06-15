# Route 2 — US execution + task decomposition

The shared execution core. Reached to implement a single User Story (directly in Case 2, or after the backlog is built in Routes 1 & 3). One US at a time (WIP = 1).

## Auto-advance — read first
Before executing, read `.harness/context.json` and compute the **auto-advance** mode (see [context-schema.md](../../plan-architecture-agent/references/context-schema.md)):
- Use `auto_advance` if present; otherwise it **defaults to ASK for `Developer`** and **ON for `user_role == "Non-Technical"`**.
- **ASK (default for dev):** after each US reaches `passing`, do **not** go idle waiting for a prompt — present an **interactive choice** (ask-user) for what to do next (see Step 5). The user picks one US, a continuous run of several, or stop. This is the default so the session never stalls silently between stories.
- **ON (default for non-tech):** do **not** stop or ask between stories. After a US is `passing`, immediately select the next-highest-priority unfinished US (`./harness resume` / `./harness status`) and start it, chaining until the backlog is exhausted. Non-tech users find a stop-and-wait-per-US flow confusing — it looks stuck — so keep moving.
- **OFF (opt-in):** hard stop and hand back after each US (only if the user explicitly wants a manual handoff every time).

Auto-advance changes **only the human handoff between stories**. It does **not** relax **WIP = 1** (still one US at a time), the full per-task gates (review / test / `./harness verify`), or approval of any irreversible action. **Hard stops that always return control even when ON:** backlog exhausted, a US/task `blocked`, `./harness verify` fails and can't be auto-resolved, or a deploy/release/destructive action needs sign-off. Print `./harness report` at each US boundary so the user can watch progress.

## Collaboration mode — read alongside auto-advance
Honor the `Collab:` mode chosen in [workflow-intake Phase 0.6](../SKILL.md) (`solo` default / `team`). It controls **how a feature is claimed and integrated**:

- **`solo`** — start with `./harness start <id>`; checkpoints land on the current branch; the US merges/commits directly. Auto-advance may chain the next US as described above.
- **`team`** — each feature is owned and isolated so concurrent agents/people don't collide:
  1. **Claim on a branch:** `./harness start <id> --assignee <name> --branch` → creates/checks out `feat/<id>` and records the owner. **WIP = 1 is per assignee**, so teammates each hold one active feature; do **not** auto-advance into another assignee's stories.
  2. **Work + verify on that branch:** `./harness verify <id>` checkpoint-commits onto `feat/<id>` and skips the commit if the index holds unrelated staged changes, so it never sweeps a teammate's work in.
  3. **Integrate via review, never direct-to-main:** when the US is `passing`, push `feat/<id>` and open a PR with [ship-pr-create](../../ship-pr-create/SKILL.md) → review ([workflow-review-deep](../../workflow-review-deep/SKILL.md)) → merge. Do **not** merge directly to `master`/`main`.
  4. **Resolve `features.json` conflicts** by the union rule in [state-merge-convention](../../../resources/state-merge-convention.md) (keep both sides' features; for same-id status edits keep the more-advanced status). Conventions: [branch-convention](../../../resources/branch-convention.md); full walkthrough: `docs/team-workflow.md`.

## Steps

### 1. Analyse the US
Read the US from `.harness/features.json` and its SPEC. Identify the components it touches and its acceptance criteria.

### 2. Decompose into child-tasks
Split the US into child-tasks (`F<id>-T<n>`) and `./harness add` them up front per the [task-convention](../../../resources/task-convention.md), so the breakdown is durable. Small US may stay a single item.

### 3. Dispatch each task to the matching workflow
Per task, pick the workflow by the US `area` / task type:
- New behaviour / feature work (`core`/`api`/`ui`/`db`/…) → [workflow-feature](../../workflow-feature/SKILL.md). Its Code·Test·Review loop means the feature's **Unit Tests** are written and pass before it is `passing`.
- A defect (`bugfix`) → [workflow-bugfix](../../workflow-bugfix/SKILL.md): reproduce → failing regression test → minimal fix → test passes → re-run the broader suite.
- A test / QA story (`test`/`qa` — IT/E2E/regression/perf/security) → [workflow-qa](../../workflow-qa/SKILL.md).
- A pre-merge deep review → [workflow-review-deep](../../workflow-review-deep/SKILL.md).

### 4. Full gates per task — testing is a loop, not a checkpoint
Each task runs review / test / `./harness verify` / handoff before it is `passing`. Work tasks one at a time (WIP = 1).

A **`test`/`qa` US is only `passing` when its suite is green**, so it drives the **outer loop**: a failure does not just get reported — it **spawns a `bugfix` story** (`./harness add … --area bugfix`), which is executed via [workflow-bugfix](../../workflow-bugfix/SKILL.md), after which the **suite is re-run**. Repeat until green (or the user explicitly defers a finding). Bugs surfaced by `./harness verify` or by the user enter the backlog the same way. Never close a test US by silencing/skipping the failing assertion.

### 5. Close the US
The parent US moves to `passing` only after all its child-tasks are `passing`. Then **print `./harness report`** — which now shows the US's **test/verify results** (the UT pass/fail summary), so the user sees the outcome, not just a flag.

**Offer to run the app** so the user can check the result live: if `run.sh` exists, point them at `./run.sh` (or the project's run command). In **gated** mode, ask-user whether to run it now (click-select **[Run it]** / **[Skip]**); if yes and it's a long-running dev server, start it and report how to view (URL/port). In **auto** mode, don't block — note that `./run.sh` is available and keep going. Running the app is a manual check, never a substitute for the UT/verify gate.

Then continue per the auto-advance mode:
- **ASK (default for dev):** do **not** go idle. Present an **interactive choice** (ask-user; Claude Code `AskUserQuestion`) — show the just-finished US and the next-up one — with options:
  - **[Run next US]** — start the next-highest-priority unfinished US (return to Step 1), then ask again at its close.
  - **[Run several / all remaining]** — switch to continuous chaining (behave as ON) for the rest of this session: keep starting the next US without asking, until the backlog is exhausted or a hard stop hits. (Optionally persist by setting `auto_advance: true` in `.harness/context.json` if the user wants it to stick.)
  - **[Stop here]** — hand back.
  Never replace this with a plain "let me know when you want the next one" idle message — that is the stall this mode exists to prevent.
- **ON (non-tech / chosen "run several"):** immediately select the next-highest-priority unfinished US and return to Step 1 — no wait — unless a hard stop applies (backlog exhausted, next US `blocked`, verify failing, or sign-off needed).
- **OFF (opt-in):** **STOP** and hand back for the next US selection.

**Hard stops always interrupt continuous runs** (ON or "run several") and return control regardless: backlog exhausted, a US `blocked`, `./harness verify` failing and not auto-resolvable, or a deploy/release/destructive action needing sign-off.

## Gates
- **ask-user** before/after each task; on feedback, redo that task. **Under auto-advance**, suppress the *routine* "shall I proceed / is this OK" confirmations between tasks and stories — but still ask when a genuine requirement ambiguity or an irreversible/outward-facing action arises.
- Never mark a task `passing` without its verification actually succeeding. (Auto-advance never overrides this.)
