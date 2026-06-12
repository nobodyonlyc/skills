# /harness-bootstrap

Take a new project from an idea to a structured, restartable, backlog-tracked codebase. Run the phases **in order**. Do not skip Phase 2 (BA + SPECs) or Phase 4 (prototype) — skipping them is the #1 cause of a thin backlog and a missing/empty prototype.

> No hooks run on Antigravity. Self-enforce the hard gates from the `harness` rule at every step.

## Phase 1 — Architecture & persona
Interview the user:
1. **Persona & size:** classify the user as **Developer** (names tech/stack) or **Non-Technical** (talks goals/features). Pick **size** (Small / Medium / Enterprise). Ask the user to confirm their role.
2. **Non-tech:** don't ask tech/stack jargon — but DO interview deeply on the *product* (see the structured BA discovery in Phase 2): propose the stack yourself, and put every product decision to them as a question with a proposed answer. **Dev:** grill them on business edge cases before accepting tech choices.
3. Write `docs/SYSTEM_ARCHITECTURE.md` (goals, components, tech stack + rationale, architecture pattern).
4. Write `.harness/context.json` (machine-readable): `project_name`, `user_role` (Developer|Non-Technical), `auto_advance` (optional bool — defaults ON for Non-Technical), `size`, `platform[]`, `techstack{}`, `architecture_pattern`.
5. **GATE:** spawn a Senior PM subagent to review the architecture; revise on fail. Then confirm with the user.

## Phase 2 — BA + per-component SPECs
1. **Structured BA discovery — ask many focused questions, not few.** Before writing `docs/BA.md`, interview the user in a few batched **ask-user** rounds (click-select, each question carrying a proposed default in plain language — never tech jargon for a non-tech user). Cover **every** dimension, asking a focused follow-up on anything vague:
   1. **Users & roles** — who uses it; what each role may do.
   2. **Core jobs / journeys** — the main step-by-step flow each user wants.
   3. **Scope line** — must-have-for-v1 vs later.
   4. **Business rules** — limits, approvals, pricing, statuses, ownership, who-sees-what.
   5. **Edge cases (plain terms)** — concurrent actions, payment fails, unauthorized attempts, etc.
   6. **Key data** — the core entities + important fields.
   7. **Outside connections** — payments, email/SMS, social login, maps, file storage.
   8. **Success & scale** — how many users, speed, privacy/compliance.
   Then write `docs/BA.md` (goals, personas, journeys, in/out of scope), spawn a PM-evaluator subagent for gaps, bring remaining gaps back as **more** focused questions, and confirm `docs/BA.md` with the user. Breadth over brevity — more questions now save a wrong build later.
2. For **each component the architecture actually has**, write a detailed SPEC under `docs/spec/` — author them **concurrently** with one subagent per component:
   - FE → `docs/spec/frontend.md` (every screen, flow, component)
   - BE → `docs/spec/backend.md` (every endpoint/service, API contract, layers)
   - DB → `docs/spec/database.md` (entities, relationships, constraints)
   - CLI → `docs/spec/cli.md` (commands, flags) · TOOL/batch → `docs/spec/<tool>.md`
3. Run **one combined PM review** over the whole SPEC set (single subagent, one report) to catch cross-SPEC gaps (e.g. an endpoint with no screen). Apply all fixes in one pass, then present the SPEC set to the user as **one packet** for confirmation.
- **GATE:** `docs/BA.md` + the relevant `docs/spec/*` MUST exist before Phase 3 — the backlog reads them. Skipping this produces an architecture-only (thin) backlog.

## Phase 3 — Backlog + skeleton
Run **`/harness-backlog`** (generates the US backlog from the architecture + ALL SPECs, runs the coverage check, gets approval, persists via `./harness add`). In parallel, a subagent scaffolds the project skeleton (dirs, config, `.gitignore`, `.env.example`, baseline smoke tests) from the architecture.
- **GATE:** confirm `.harness/features.json` actually contains the approved stories (`./harness status` shows more than the placeholder) and the scaffold exists.

## Phase 4 — Common design phase (UI projects)
1. **Basic DB design:** from BA + tech SPEC, produce a basic schema in `docs/spec/database.md`.
2. **If the project has a UI** (`docs/spec/frontend.md` exists): establish & approve `docs/spec/design-system.md` first (offer 2–3 distinct style directions with sample `:root` tokens — don't default to generic blue+Inter), then run **`/harness-prototype`** to render the mock UI and get approval. Browser preview is mandatory; iterate until approved.
3. **Commit the design-phase artifacts before any feature work:** `git add docs/spec docs/SYSTEM_ARCHITECTURE.md prototype && git commit -m "design phase"`.
- **GATE (hard):** the design system and the mock UI/prototype are approved and committed before any US implementation. Skip the UI sub-steps only if the project genuinely has no UI.

## Phase 5 — Verify & execute
1. Run `./init.sh`, confirm baseline passes, print `./harness status`.
2. Then go to US execution:
   - **Auto-advance ON** (default for Non-Technical): flow straight into `/harness-execute-us` for the first US and keep chaining.
   - **OFF** (default for Developer): STOP and let the user pick the first US (WIP = 1).

## Hard gates recap
- BA + `docs/spec/*` exist before the backlog (Phase 2 → 3).
- User approves the backlog before `./harness add`.
- UI projects: design system + prototype approved & committed before any feature code (Phase 4).
- Never weaken `./harness verify`.
