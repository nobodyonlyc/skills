# Harness enforcement rules (Antigravity)

> **Activation: ALWAYS ON.** Antigravity has no hook/gate mechanism, so the guards
> that run automatically under Claude Code (phase guard, backlog guard) **do not
> run here**. YOU are the only enforcement. Self-check every gate below *before*
> the relevant action — nothing will stop you if you skip it.

## 0. Intake routing (never skip to code)
ALL requests route through classification first. Classify intent into one case, then follow that flow — never jump straight to writing code or features:
- **Case 1 — New project** → run `/harness-bootstrap`.
- **Case 2 — Add feature / execute a US** → run `/harness-execute-us`.
- **Case 3 — Bugfix** → reproduce → root-cause → fix → regression test.
- **Case 4 — Prototype only** → run `/harness-prototype`.

## 1. Phase guard — bootstrap artifacts (HARD GATE)
Do **not** run `./harness add`, `./harness start`, or create/edit application code (anything under `src/ app/ pages/ components/ lib/ packages/ server/ api/`, or `package.json`/`Cargo.toml`/`pyproject.toml`/`go.mod`) until **all** of these exist and are non-empty:
- `docs/SYSTEM_ARCHITECTURE.md`
- `docs/BA.md`
- at least one `docs/spec/*.md`

If they don't exist yet, you are still in design. Build them first (`/harness-bootstrap`).

## 2. Phase guard — design phase for UI projects (HARD GATE)
If `docs/spec/frontend.md` exists, the project has a UI. Then do **not** run `./harness start` or write application code until **both** exist:
- `docs/spec/design-system.md` (approved design system / `:root` tokens)
- `prototype/*.html` (mock UI rendered from `docs/spec/frontend.md`, browser-previewed and user-approved)

The backlog (`./harness add`, Phase 3) **is** allowed before the prototype — only US *execution* is gated. This is the step most often skipped: after the backlog is created, the prototype gets bypassed. Do not bypass it. Run `/harness-prototype` and get explicit approval before any US.

## 3. Backlog persistence (HARD GATE)
A drafted backlog that was never written is a silent failure. After the user approves the User-Story backlog, run `./harness add` for **every** story, then `./harness status` to confirm. Never end a turn with `.harness/features.json` holding only the placeholder while an architecture exists.

## 4. WIP = 1 + auto-advance
- **WIP = 1:** one feature/US at a time; one active feature at a time.
- **Auto-advance:** read `.harness/context.json`. Effective `auto_advance` = the field if present, else **defaults ON when `user_role == "Non-Technical"`**, OFF for `Developer`.
  - **ON:** after a US reaches `passing`, do **not** stop to ask the user to start the next one — immediately pick the next-highest-priority unfinished US and continue, chaining until the backlog is exhausted. A non-tech user finds stop-and-wait-per-US confusing (it looks stuck), so keep moving.
  - **OFF:** stop after each US and hand back for selection.
  - Auto-advance never relaxes WIP=1 or any verification. **Always return control on a hard stop:** backlog exhausted, a US `blocked`, `./harness verify` failing, or a deploy/release/destructive action needing sign-off.

## 5. Per-US Definition of Done (never weaken)
A US/task moves to `passing` only when ALL hold:
- behaviour implemented,
- **code review** done (correctness, security, simplification),
- **tests** written/updated and passing,
- **`./harness verify <id>` actually ran and succeeded**,
- evidence recorded.
Never mark `passing` without the verification actually succeeding. Adding code is not completion.

## 6. Subagents & artifact-driven communication
- Antigravity supports dynamic subagents — use them for parallel independent work (per-component SPEC authoring, PM coverage review, the design critic), each with its own isolated context.
- Any output/log/test-result longer than ~10 lines goes to a file under `.harness/reports/` or `.harness/logs/`; pass the **path**, not the contents, between agents.
- Durable state (approved plans, BA, SPECs, final evidence) goes to `docs/design-docs/<feature_id>/` and `.harness/tasks/<feature_id>.md` — not chat.

## 7. Trace
After running a workflow, record it: `./harness trace --skill <name> --purpose "<why>" --result "<outcome>"`.

## 8. End of session
`./harness session stop` → `./harness clean` → commit → finish with `./harness report` printed in chat.
