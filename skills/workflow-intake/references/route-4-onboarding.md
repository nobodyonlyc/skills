# Route 4 — Legacy onboarding

Reached when [Phase 0](phase-0-classify.md) classified the prompt as **Case 4**: the user wants to bring the harness into an existing, active project that does **not** yet use harness tooling.

## Action
Dispatch [workflow-onboard](../../workflow-onboard/SKILL.md). It:
1. Surveys the existing codebase ([core-explain](../../core-explain/SKILL.md) fan-out) — languages, frameworks, and the project's own build/test commands.
2. Writes navigation docs (`docs/SYSTEM_MAP.md`, glossary) and an `init.sh` wired to those real commands, and records the baseline test state.
3. Runs `harness init` **without clobbering** existing files (merging harness rules into an existing `CLAUDE.md`/`AGENTS.md`), then seeds a backlog from current state + the requested work.
4. Stops and hands off so the user picks the first feature via [Route 2](route-2-us-execution.md).

## Gates
- **ask-user** first: confirm this is an onboard (not a rewrite) and confirm the discovered build/test commands before writing anything.
- **Never overwrite** existing source or entrypoint files — merge, don't replace.
- If the repo turns out to be empty/greenfield, route to [Route 1](route-1-new-project.md) (new project) instead.

## Decline fallback
If the user does **not** want to onboard (e.g. they only wanted information, or prefer to start fresh), do not scaffold or change any files. Offer [Route 1](route-1-new-project.md) for a clean start, then stop and return control.
