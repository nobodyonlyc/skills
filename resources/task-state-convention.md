# Task-State Convention (crash recovery)

`.harness/features.json` records **which** features exist and their coarse status. It does not record **where inside a task** the work currently is — that state used to live only in the chat context, so a crashed session lost it. This convention makes the in-flight state durable.

## The state file

One committed markdown file per active feature or child-task:

```
.harness/tasks/<feature_id>.md      # e.g. .harness/tasks/F46.md, .harness/tasks/F24-T2.md
```

- **Created** by the workflow right after `./harness start <id>`.
- **Updated and committed at every phase boundary** (see the workflow skills' phase checkpoints). A crash then loses at most one phase.
- **Kept** after the feature passes — it is the durable record of decisions; `harness clean` must never touch `.harness/tasks/`.

## Template

Checkbox markers: `[ ]` not started · `[/]` in progress · `[x]` done. Tick `[x]` **only** when that exact step is genuinely finished — never tick ahead.

```markdown
# Task State — <feature_id>: <title>

- Mode: gated | auto
- Collab: solo | team (when team: also `Assignee: <name>` and `Branch: feat/<id>`)
- Workflow: workflow-feature | workflow-bugfix | ...
- Started: <ISO timestamp>

## Acceptance criteria (from the US — each ends [x], mapped to its proof)
- [ ] <criterion 1> → code: <path> · test: <test name/path>
- [ ] <criterion 2> → code: <path> · test: <test name/path>

## Phase checklist (Definition of Done — one box per mandatory step, not per phase)
### Phase 1 — Analysis & plan
- [ ] Acceptance criteria listed (above)
- [ ] Plan approved (docs/design-docs/<id>/plan.md)
- [ ] (UI only) mockup approved

### Phase 2 — Build · Test · Review loop (iteration: N)
- [ ] Implementation complete
- [ ] Unit tests written AND passing (not existence checks)
- [ ] Code review clean (last report: .harness/reports/review-N.md)
- [ ] Security review done (if it touches auth / external input / secrets / queries / shell / crypto)

### Phase 3 — Verify & handoff
- [ ] Integration / regression tests pass (or the covering test US is green)
- [ ] `./harness verify <id>` succeeded
- [ ] Evidence written to docs/design-docs/<id>/evidence.md (non-empty — hook-enforced before `passing`)
- [ ] Progress / handoff updated

## Evidence
- docs/design-docs/<id>/evidence.md  (committed QA/review/verify summary — survives `harness clean`)

## Decisions
- <ISO timestamp> — chose X over Y because <reason> (approved by user / auto mode)

## Next step
<single concrete next action a fresh session should take>
```

Rules:
- **Granular checklist:** one checkbox **per mandatory step** of the Definition of Done (above), not one per phase. A reader must be able to see, step by step, exactly what was done — the coarse 3-phase form hid skipped work.
- **Acceptance criteria:** one box per criterion of the US, each mapped to the code + the test that proves it. **All criteria must be `[x]` before the feature can be `passing`.**
- **Keep it in sync — including `auto` mode:** update **and commit** the file at **every phase boundary AND before setting `passing`**. `auto` mode only suppresses ask-user gates; it does **NOT** suspend state-keeping. A task file frozen at an early step while the feature is already `passing` is a process failure — the #1 reason you can't tell from the file whether the work was done.
- **Evidence is gated:** `docs/design-docs/<id>/evidence.md` must be non-empty before `./harness verify <id>` is allowed to mark the feature `passing` — enforced by `hooks/harness-phase-guard.sh` (Gate 3).
- **Decisions** records every ask-user answer or auto-mode decision — a recovering session must not re-ask settled questions.
- **Next step** is always present and always concrete ("re-run `cargo test`, fix the 2 failures in commands.rs", not "continue").
- Artifact pointers follow the file-based communication rule: paths only, no content.

## Recovery procedure (fresh session, crashed predecessor)

1. `./harness status` → find the `in_progress` feature.
2. Read `.harness/tasks/<id>.md` → phase checklist + next step.
3. `git log --oneline -5` → confirm the last phase checkpoint commit matches the checklist.
4. Continue from **Next step**. Do not redo completed phases; do not re-ask decided questions.
