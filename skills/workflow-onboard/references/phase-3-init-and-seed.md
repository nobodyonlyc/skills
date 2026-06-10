# Phase 3 — Safe Init & Seed

**Skill used:** [plan-us-backlog-generator](../../plan-us-backlog-generator/SKILL.md)

Goal: bring the harness state machine online over the existing repo and seed real work — without clobbering anything.

## 1. Run harness init (non-destructive)
```bash
./harness init
```
`harness init` is safe by design: it only creates `CLAUDE.md`, `AGENTS.md`, and `init.sh` **if they do not already exist**, appends (never rewrites) `.gitignore` entries, and seeds `.harness/features.json` only when absent. It prints which existing files it **skipped** — read that output.

## 2. Merge harness rules into existing entrypoint files
For every file `harness init` reported as skipped because the project already had one (`CLAUDE.md` / `AGENTS.md` / `init.sh`):
- **Do not overwrite it.** Open it and merge the harness operating rules in as an added section (Startup loop, WIP=1, Definition of Done, durable-vs-transient, the `./harness resume` / `verify` / `session stop` commands).
- Preserve the project's existing instructions verbatim; only add.
- Show the user the diff of what you added.

## 3. Seed the backlog
Drive [plan-us-backlog-generator](../../plan-us-backlog-generator/SKILL.md) to create the initial backlog from two sources:
1. **Current-state features** the survey revealed (so the backlog reflects what already exists, marked `passing` only where a real verification confirms it — otherwise `not_started`).
2. **The requested work** the user named in Phase 1.

Present the proposed User Stories and get approval (**ask-user**) before `./harness add`. For each, attach a verification command drawn from the project's own test commands (Phase 1), so the Definition-of-Done gate is real.

## 4. Confirm restartability
```bash
./init.sh          # the standard startup path now runs the project's build/test
./harness resume   # shows the seeded backlog and the computed next step
```
Both must succeed (modulo the known-failing baseline from Phase 2).

## 5. Hand off — STOP
Onboarding is complete. **Do not start implementing a feature in this session** (WIP = 1). Summarize what was created (docs, init.sh, backlog), state the baseline, and hand control back so the user picks the first feature to run through [Route 2](../../workflow-intake/references/route-2-us-execution.md).
