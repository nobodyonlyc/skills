# Child-Task Convention

The harness CLI tracks **features (User Stories)** only — there is no separate task table. To let a US be split into smaller, individually-verified steps, **a child-task is just a feature** created by convention. No schema/Rust change is required.

## ID scheme
`F<parent>-T<n>` — e.g. the 3rd task of `F24` is `F24-T1`, `F24-T2`, `F24-T3`.

## Creating a child-task
Use the normal `./harness add`, with `--area task` and the parent recorded in the behavior/notes:

```bash
./harness add F24-T1 "Interview: project size & user role" \
  --priority 2401 \
  --area task \
  --behavior "parent: F24. Ask size/role via ask-user; output captured in docs/SYSTEM_ARCHITECTURE.md." \
  --verifications "grep -q 'Persona' docs/SYSTEM_ARCHITECTURE.md"
```

- **`--area task`** marks the row as a child-task (so `./harness status` is filterable).
- **`parent: F<id>`** as the first token of `--behavior` records the parent link.
- **Priority** = `parent_priority * 100 + n` (F24 → 2401, 2402, …). This keeps child-tasks grouped and sorted **after** all top-level US in `./harness status`.

## Lifecycle (each child-task runs the full harness gates)
A child-task is a first-class harness item, so it goes through the same loop as any feature:

```
./harness start  F24-T1            # WIP = 1 — one active item at a time
   … implement → review → test → handoff …
./harness verify F24-T1            # runs its verifications, marks passing, git checkpoint
./harness block  F24-T1 --reason "<blocker>"   # if it cannot proceed
```

Every child-task must pass **review / test / verify / handoff** before it is `passing` (see the workflow skills it is dispatched to).

## How workflows use this
When a workflow executes a US (see [workflow-feature](../skills/workflow-feature/SKILL.md), [workflow-bugfix](../skills/workflow-bugfix/SKILL.md), and the intake router's Route 2):
1. Analyse the US and decompose it into child-tasks (`F<id>-T<n>`).
2. `./harness add` each task up front so the breakdown is durable in `.harness/features.json`.
3. Work them one at a time (WIP = 1), recording each significant step as its own task where useful.
4. The parent US moves to `passing` only after all its child-tasks are `passing`.

This makes every step of a prompt durable and restartable: a new session can read `./harness status`, see the parent US and its `F<id>-T<n>` children, and continue exactly where the last one stopped.
