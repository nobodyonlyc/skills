# Phase 1 — Survey & Discovery

**Skill used:** [core-explain](../../core-explain/SKILL.md)

Goal: understand the existing codebase well enough to document it and wire the harness to it — **without changing anything yet**.

## 1. Confirm scope (ask-user)
Confirm with the user that this is a **legacy onboard**: an existing, active codebase that has never used the harness. Confirm what work they want to do next (it seeds the backlog in Phase 3). If the repo is actually empty/greenfield, stop and route to [workflow-bootstrap](../../workflow-bootstrap/SKILL.md) instead.

## 2. Fan-out survey (spawn-subagents)
Run independent readers in parallel ([agent-tool-mapping](../../../resources/agent-tool-mapping.md)), each blind to the others, so one search angle does not miss what another would find:

- **Structure reader** — top-level layout, module/package boundaries, where source vs tests vs config live. Respect progressive disclosure (`AGENTS.md`): read existing `README.md`/`RULES.md` per directory rather than scanning blindly.
- **Toolchain reader** — language(s), framework(s), and the project's **own commands** from its manifests: `package.json` scripts, `Cargo.toml`, `Makefile`, `pyproject.toml`, `go.mod`, `pom.xml`, plus CI config (`.github/workflows`, `.gitlab-ci.yml`) — CI is the most reliable source of the real build/test/lint commands.
- **Entry-point reader** — how the app is built, run, and tested today; main entry files; how it is deployed if visible.
- **Data reader** (only if a database is present) — schema/migrations; consult [dev-db-designer](../../dev-db-designer/SKILL.md) to describe it.

## 3. Consolidate
Write a single survey report to `docs/design-docs/onboard/survey.md` (committed, not transient). It must capture:
1. **Languages & frameworks** with versions where known.
2. **Build / test / run / lint commands** — verbatim, copy-pasteable. Mark which are confirmed (found in CI or a manifest) vs guessed.
3. **Module map** — the domains/components and what each does.
4. **Entry points** and how to run the app locally.
5. **Open questions / risks** for the user.

## 4. Confirm the commands (ask-user)
Present the discovered build/test/run commands and the module map. Get explicit confirmation — these commands become `init.sh` and the per-feature verifications, so a wrong guess here poisons every later gate.

→ Proceed to [Phase 2](phase-2-docs-and-baseline.md).
