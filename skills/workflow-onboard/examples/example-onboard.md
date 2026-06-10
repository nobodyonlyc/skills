# Example — Onboarding a legacy Express API

A worked run of [workflow-onboard](../SKILL.md) on an existing Node/Express service that has never used the harness. The user's prompt was *"add the harness to my orders-api repo and I want to add idempotency keys to the payment endpoint next."*

---

## Phase 1 — Survey & Discovery

**Confirm scope (ask-user):** "This is `orders-api`, an existing Express service — onboard it (not rewrite), and the first new work is idempotency keys on `/payments`. Correct?" → user confirms.

**Fan-out survey** (4 parallel readers) found:

- **Structure reader:** `src/routes`, `src/services`, `src/db` (Knex), `test/` (Jest). Per-dir READMEs in `src/services`.
- **Toolchain reader:** Node 20, Express 4, Knex + PostgreSQL, Jest. From `package.json` scripts and `.github/workflows/ci.yml`:
  - install: `npm ci`
  - build: *(none — runtime JS)*
  - test: `npm test` (Jest)
  - lint: `npm run lint` (ESLint)
- **Entry-point reader:** `src/index.js` boots Express on `PORT`; routes mounted in `src/routes/index.js`; run locally with `npm run dev`.
- **Data reader:** Knex migrations in `migrations/`; `orders`, `payments`, `customers` tables.

**Survey report** written to `docs/design-docs/onboard/survey.md`. Commands marked *confirmed* (found in CI).

**Confirm commands (ask-user):** present the command list + module map → user confirms `npm test` is the real gate.

## Phase 2 — Documentation & Baseline

- Wrote `docs/SYSTEM_MAP.md`: the route → service → db layering, the three tables, and the local-run instructions.
- Seeded `docs/DOMAIN_GLOSSARY.md` with *order*, *payment intent*, *idempotency key*.
- `init.sh` did not exist → created one running `npm ci` then `npm test`, then `./harness status`.
- **Baseline** (`docs/design-docs/onboard/baseline.md`): ran `npm test` → **108 passed, 2 failing** in `test/payments.legacy.test.js` (pre-existing, unrelated to our work). Recorded as a **known-failing baseline**; not fixed during onboarding.
- Phase checkpoint committed.

## Phase 3 — Safe Init & Seed

**`./harness init`** output:
```
Created AGENTS.md
Skipped existing files (left untouched): CLAUDE.md, init.sh
Onboarding an existing project? Merge the harness operating rules into these files; do not overwrite them.
Created starter features.json
Harness initialized successfully!
```

- `CLAUDE.md` already existed → **merged** a "Harness Operating Rules" section (startup loop, WIP=1, DoD, `./harness resume`/`verify`/`session stop`) below the project's existing instructions; showed the user the diff. Did **not** overwrite.
- `init.sh` was the one created in Phase 2 → left as is.

**Seed the backlog** (drove `plan-us-backlog-generator`), approved by the user:
| id | title | status | verification |
|---|---|---|---|
| F01 | Orders CRUD API (existing) | not_started* | `npm test -- orders` |
| F02 | Payments endpoint (existing) | not_started* | `npm test -- payments` |
| F03 | Idempotency keys on /payments (requested) | not_started | `npm test -- idempotency` |

\* existing features marked `not_started`, not `passing` — they only become `passing` once a real `./harness verify` confirms them, never assumed.

**Confirm restartability:**
```
./init.sh          # npm ci + npm test (108 pass / 2 known-failing) + harness status
./harness resume   # shows F01–F03, next step: "./harness start F03"
```

## Hand off — STOP
Onboarding complete: `docs/SYSTEM_MAP.md`, glossary, `init.sh`, merged `CLAUDE.md`, and a 3-item backlog. Baseline = 2 known-failing legacy tests (acknowledged by the user). No feature implemented in this session. Control returned to the user to `./harness start F03` and run it through [Route 2](../../workflow-intake/references/route-2-us-execution.md).
