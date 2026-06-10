# Phase 2 — Documentation & Baseline

**Skills used:** [core-explain](../../core-explain/SKILL.md), [dev-db-designer](../../dev-db-designer/SKILL.md) (if a DB exists)

Goal: leave durable navigation docs and a wired-up, honest startup path — still without changing the project's own source.

## 1. Generate the system map
From the Phase 1 survey, write `docs/SYSTEM_MAP.md` (committed): the module map, entry points, and how the pieces fit. This is the "progressive disclosure" entry point future sessions read before touching a domain (per [AGENTS.md](../../../../AGENTS.md)). Seed `docs/DOMAIN_GLOSSARY.md` with the project's ubiquitous language if it has none.

## 2. Write init.sh using the project's OWN commands
Create (or merge into) `init.sh` so the standard startup path runs the project's real dependency sync + build + test — **the commands confirmed by the user in Phase 1**, not harness defaults. Examples:
- Node: `npm ci` / `npm run build` / `npm test`
- Python: `pip install -e .` / `pytest`
- Go: `go mod download` / `go test ./...`

If `init.sh` already exists, do not overwrite it — append the harness verification step and tell the user.

## 3. Capture the baseline test state (honesty gate)
Run the project's test command once and record the result in `docs/design-docs/onboard/baseline.md`:
- **Green** → record it as the clean baseline; future features must keep it green.
- **Red / partially failing** → record exactly which tests fail as a **known-failing baseline**. Do **not** fix them as part of onboarding (out of scope), and do **not** block onboarding. The user must acknowledge this baseline before feature work begins, so later sessions don't mistake pre-existing failures for regressions.

## 4. Phase checkpoint
Commit the docs and `init.sh`:
```bash
git add docs/SYSTEM_MAP.md docs/DOMAIN_GLOSSARY.md docs/design-docs/onboard/ init.sh
git commit -m "phase-checkpoint: onboard phase 2 (docs + baseline)"
```

→ Proceed to [Phase 3](phase-3-init-and-seed.md).
