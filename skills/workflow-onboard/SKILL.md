---
name: workflow-onboard
description: Onboard the harness into an existing (legacy / non-harness) codebase — survey it, document it, wire init.sh to its own build/test, init harness without clobbering, and seed a backlog.
---

Onboard target: $ARGUMENTS

Multi-agent workflow that brings an **existing codebase under harness control** without rewriting it. This is the bridge between greenfield ([workflow-bootstrap](../workflow-bootstrap/SKILL.md)) and adding work to an already-harnessed repo ([Route 3](../workflow-intake/references/route-3-add-feature.md)): the project is real and active, but has never had the harness. Each phase has a playbook in [`references/`](references/); see [`examples/`](examples/) for a full worked run.

## Skills this workflow drives
- [core-explain](../core-explain/SKILL.md) — read and map the existing code, patterns, and build/test commands (Phase 1).
- [plan-us-backlog-generator](../plan-us-backlog-generator/SKILL.md) — seed the backlog from current state + the requested work (Phase 3).
- [dev-db-designer](../dev-db-designer/SKILL.md) — consulted only if the survey finds a database whose schema must be documented.

## Phases
1. **Survey & discovery** → [references/phase-1-survey.md](references/phase-1-survey.md)
   Fan-out readers map the repo: languages, frameworks, entry points, and the project's **own** build/test/run commands. Output a survey report.
2. **Documentation & baseline** → [references/phase-2-docs-and-baseline.md](references/phase-2-docs-and-baseline.md)
   Generate `docs/SYSTEM_MAP.md` + glossary, write `init.sh` using the project's real commands, and capture the **baseline test state** (green or known-failing) before any harness work.
3. **Safe init & seed** → [references/phase-3-init-and-seed.md](references/phase-3-init-and-seed.md)
   Run `harness init` without clobbering existing files, merge the harness operating rules into the project's existing CLAUDE.md/AGENTS.md, seed the backlog, then hand off to [Route 2](../workflow-intake/references/route-2-us-execution.md).

## Hard gates
- **Never clobber**: do not overwrite an existing `CLAUDE.md`, `AGENTS.md`, `init.sh`, `.gitignore`, or any source file. Where the project already has one, **merge** the harness section in and tell the user what changed. `harness init` itself skips existing files and reports them; honor that.
- **Ask-user before touching the repo**: confirm the classification (this is a legacy onboard, not a rewrite) and the discovered build/test commands before writing anything.
- **Baseline honesty**: record the real starting test state. If the project's tests already fail, capture that as a *known-failing baseline* — do not "fix" it as part of onboarding, and do not block onboarding on it. Subsequent feature work must not be stacked on a baseline the user has not acknowledged.
- **Durable artifacts**: the survey report and `SYSTEM_MAP.md` go to committed locations (`docs/`), not transient `.harness/reports/` (see the task-state and durable-vs-transient rules in [AGENTS.md](../../../AGENTS.md) and [task-state-convention](../../resources/task-state-convention.md)).
- After seeding the backlog, **STOP** — hand control back so the user picks one feature (WIP = 1). Do not start implementation in the onboarding session.
