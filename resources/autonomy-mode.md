# Autonomy Mode (gated vs auto)

The harness pipeline gates many steps behind **ask-user** confirmation. That is right for interactive work but fights the goal of long, unattended runs. Autonomy mode lets a run choose once, up front, how much it stops for the user.

## The two modes

| | `gated` (default) | `auto` |
|---|---|---|
| Per-step ask-user gates | Stop and wait for the user | Decide autonomously, log the decision, continue |
| Plan / design approval | User must approve | Agent approves its own plan, records rationale |
| Always-stop list (below) | Stop | **Still stop** |
| Best for | Interactive work, team members, first run | Overnight / long autonomous runs the user explicitly asked for |

**Default is `gated`.** `auto` is opt-in: the user enables it explicitly (e.g. "run F30 in auto mode", "do this unattended"). A teammate running intake for the first time is never surprised by the agent deciding on its own.

## Where the mode is set and stored
- Chosen **once** at intake ([workflow-intake](../skills/workflow-intake/SKILL.md) Phase 0). If the user did not ask for `auto`, it is `gated`.
- Written to the task-state file `.harness/tasks/<id>.md` `Mode:` field (see [task-state-convention](task-state-convention.md)) so a recovering session inherits it without re-asking.

## Logged decisions (auto mode)
When `auto` skips an ask-user gate, it MUST record the decision so the run is auditable. Append to the `## Decisions` section of the task-state file:
```
- <ISO timestamp> — [auto] <what was decided> because <reason>; alternative considered: <X>
```
The user reviews the full decision chain after the run. A decision that is wrong is recoverable from this log; a decision that was never recorded is not.

## Always-stop list (overrides BOTH modes)
Even in `auto`, STOP and ask the user before:
- Deleting or overwriting data/files **outside the active feature's scope**.
- `git push --force`, history rewrites, or pushing to a shared/protected branch.
- Deploying to production or any non-local environment.
- Destructive schema/data migrations (drop/alter that loses data).
- Anything touching payments, credentials, secrets, or external side effects (sending email, calling paid APIs at scale).
- Work that exceeds the active feature's scope (WIP = 1) — surface it, don't silently expand.

These are irreversible or outward-facing; autonomy never extends to them. When in doubt, treat it as always-stop.
