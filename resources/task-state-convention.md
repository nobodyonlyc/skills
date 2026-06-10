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

```markdown
# Task State — <feature_id>: <title>

- Mode: gated | auto
- Workflow: workflow-feature | workflow-bugfix | ...
- Started: <ISO timestamp>

## Phase checklist
- [x] Phase 1 — analysis & plan approved (plan: docs/design-docs/<id>/plan.md)
- [ ] Phase 2 — build/test/review loop (iteration: 2, last report: .harness/reports/review-2.md)
- [ ] Phase 3 — QA + verify + handoff

## Decisions
- <ISO timestamp> — chose X over Y because <reason> (approved by user / auto mode)

## Next step
<single concrete next action a fresh session should take>
```

Rules:
- **Phase checklist** mirrors the workflow's phases exactly; the line for the active phase carries enough detail (iteration counter, artifact pointers) to resume mid-phase.
- **Decisions** records every ask-user answer or auto-mode decision — a recovering session must not re-ask settled questions.
- **Next step** is always present and always concrete ("re-run `cargo test`, fix the 2 failures in commands.rs", not "continue").
- Artifact pointers follow the file-based communication rule: paths only, no content.

## Recovery procedure (fresh session, crashed predecessor)

1. `./harness status` → find the `in_progress` feature.
2. Read `.harness/tasks/<id>.md` → phase checklist + next step.
3. `git log --oneline -5` → confirm the last phase checkpoint commit matches the checklist.
4. Continue from **Next step**. Do not redo completed phases; do not re-ask decided questions.
