# /harness-execute-us

Implement User Stories one at a time (WIP = 1), each with **full review + test + verify** gates, then auto-advance to the next when configured. This is the loop that, on Antigravity, tends to skip review/test and stop too early — do not.

> Hard gate first: if `docs/spec/frontend.md` exists, do NOT start a US until `docs/spec/design-system.md` and `prototype/*.html` exist and are approved (run `/harness-prototype`). Do not write app code or run `./harness start` before bootstrap artifacts exist.

## Step 0 — Compute auto-advance
Read `.harness/context.json`. Effective `auto_advance` = `true`→ON, `false`→OFF, else (absent) **ON for `user_role == "Non-Technical"`, ASK for `Developer`**. Remember it for Step 6.

## Step 1 — Select & analyse the US
Pick the highest-priority unfinished US (`./harness resume` / `./harness status`). Read it from `.harness/features.json` and its SPEC. Identify the components it touches and its acceptance criteria. `./harness start <id>`.

## Step 2 — Decompose into child-tasks
Split the US into child-tasks `F<id>-T<n>` and `./harness add` them up front so the breakdown is durable. A small US may stay a single item.

## Step 3–5 — Per task: implement → review → test → verify (WIP = 1)
Work tasks **one at a time**. For **each** task run the full gate set before it is `passing`:
1. **Implement** the behaviour (backend: secure/clean layering; frontend: build from the approved prototype as the design reference; bugfix: reproduce → root-cause → fix).
2. **Code review** — review the diff for correctness, logic errors, security, and simplification. Fix what it finds. (Spawn a reviewer subagent for non-trivial diffs; write the report to `.harness/reports/`.)
3. **Tests** — write/update unit + integration/regression tests for the change and run them; they must pass.
4. **`./harness verify <id>`** — must actually run and **succeed**. Never mark a task `passing` on code alone.
5. **Handoff** — record evidence; update task state.

Each of review and test is **mandatory** — a task with code but no review and no passing tests is **not** done.

## Step 6 — Close the US & advance
The parent US moves to `passing` only after **all** child-tasks are `passing` (each verified). Then print `./harness report` (shows the US's test/verify results), offer to run the app (`./run.sh`), and:
- **Auto-advance ON:** immediately return to Step 1 for the next-highest-priority unfinished US — **no waiting** — unless a hard stop applies.
- **ASK (dev default):** do **not** go idle — show an interactive choice prompt: **[Run next US]** / **[Run several / all remaining]** (then chain like ON) / **[Stop here]**.
- **Auto-advance OFF:** STOP and hand back for the next US selection.

**Hard stops (always return control, even when auto-advance is ON):** backlog exhausted, a US/task `blocked`, `./harness verify` failing and not auto-resolvable, or a deploy/release/destructive action needing sign-off.

## Gates
- WIP = 1 throughout. Never weaken or skip `./harness verify`.
- Under auto-advance, suppress routine "shall I proceed?" prompts between tasks/stories, but still ask on genuine requirement ambiguity or an irreversible/outward-facing action.
- Never mark `passing` without verification actually succeeding.
