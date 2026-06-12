<!-- HARNESS-ANTIGRAVITY-ENFORCEMENT -->
## Cross-tool rules (Claude Code · Codex · Antigravity)

These rules apply to **all three agents**. Where they differ is only the concrete tool each one uses.

### Universal — gates are interactive choice prompts (ALL agents)
Every "confirm / approve / stop for the user" gate below means: **pause and ask the user with an interactive choice prompt**, present **selectable options** (e.g. **[Proceed]** / **[I want changes]**, mark the recommended), and **wait for the answer in the same session**. Do **NOT** end the turn with a plain "let me know when you're ready" message and go idle — the chat is paused awaiting a click, not finished. Use your runtime's tool:
- **Claude Code** → `AskUserQuestion` with an `options` array.
- **Codex** → `ask_question` with the choices as selectable options.
- **Antigravity** → its interactive choice prompt with the options listed.

Whenever the answer is a discrete set (yes/no, approve/revise, pick a method), use clickable options — never a free-text "reply to continue".

### Gate enforcement — for agents WITHOUT Claude Code's hooks (Codex & Antigravity)
Claude Code enforces the gates below mechanically via `.claude/settings.json` hooks. **Codex and Antigravity do not run those hooks**, so on those two you MUST self-check each gate before the relevant action. (Antigravity also has the full rules in `.agent/rules/harness.md` and self-contained playbooks in `.agent/workflows/` run via `/`.)

- **Route first.** Classify every request (new project / add-feature / execute-US / bugfix) before writing any code. New project → `/harness-bootstrap`.
- **Bootstrap gate.** Do not run `./harness add`/`./harness start` or create/edit app code until `docs/SYSTEM_ARCHITECTURE.md`, `docs/BA.md`, and at least one `docs/spec/*.md` exist.
- **Design-phase gate.** If `docs/spec/frontend.md` exists (UI project), do not run `./harness start` or write app code until **both** `docs/spec/design-system.md` and `prototype/*.html` exist, are browser-previewed, and user-approved. `./harness add` (backlog) is allowed before the prototype; only US *execution* is gated. The prototype must produce **real files** under `prototype/` — a verbal "done" with no files is a failure.
- **Backlog completeness.** Generate the backlog from the architecture **and every `docs/spec/*`** (not the architecture alone), run the coverage check, get user approval, then `./harness add` every story. Never end with an empty/placeholder backlog while an architecture exists.
- **Per-US Definition of Done.** Each US/task is `passing` only after: implemented + **code review** + **tests passing** + **`./harness verify <id>` actually succeeded** + evidence recorded. Review and test are mandatory, not optional.
- **WIP = 1 + auto-advance.** One US at a time. Read `.harness/context.json`: `auto_advance` defaults ON for `user_role == "Non-Technical"` — then after a US passes, immediately start the next-highest-priority one without waiting (chain to backlog exhaustion). Hard stops always return control: backlog exhausted, US `blocked`, verify failing, or deploy/destructive action needing sign-off.
<!-- /HARNESS-ANTIGRAVITY-ENFORCEMENT -->
