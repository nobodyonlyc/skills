<!-- HARNESS-ANTIGRAVITY-ENFORCEMENT -->
## Cross-tool enforcement (Antigravity & any agent without hooks)

Claude Code enforces the gates below via hooks. Agents **without** a hook mechanism (e.g. Antigravity) get **no automatic enforcement** — so you MUST self-check these before the relevant action. Full rules: `.agent/rules/harness.md`. Self-contained playbooks (run via `/`): `.agent/workflows/harness-bootstrap.md`, `harness-backlog.md`, `harness-prototype.md`, `harness-execute-us.md`.

- **Route first.** Classify every request (new project / add-feature / execute-US / bugfix) before writing any code. New project → `/harness-bootstrap`.
- **Bootstrap gate.** Do not run `./harness add`/`./harness start` or create/edit app code until `docs/SYSTEM_ARCHITECTURE.md`, `docs/BA.md`, and at least one `docs/spec/*.md` exist.
- **Design-phase gate.** If `docs/spec/frontend.md` exists (UI project), do not run `./harness start` or write app code until **both** `docs/spec/design-system.md` and `prototype/*.html` exist, are browser-previewed, and user-approved. `./harness add` (backlog) is allowed before the prototype; only US *execution* is gated. The prototype must produce **real files** under `prototype/` — a verbal "done" with no files is a failure.
- **Backlog completeness.** Generate the backlog from the architecture **and every `docs/spec/*`** (not the architecture alone), run the coverage check, get user approval, then `./harness add` every story. Never end with an empty/placeholder backlog while an architecture exists.
- **Per-US Definition of Done.** Each US/task is `passing` only after: implemented + **code review** + **tests passing** + **`./harness verify <id>` actually succeeded** + evidence recorded. Review and test are mandatory, not optional.
- **WIP = 1 + auto-advance.** One US at a time. Read `.harness/context.json`: `auto_advance` defaults ON for `user_role == "Non-Technical"` — then after a US passes, immediately start the next-highest-priority one without waiting (chain to backlog exhaustion). Hard stops always return control: backlog exhausted, US `blocked`, verify failing, or deploy/destructive action needing sign-off.
<!-- /HARNESS-ANTIGRAVITY-ENFORCEMENT -->
