# resources/archive — Superseded templates

Templates created early (feature **F18** — "harness report and planning templates"), before the BA/SPEC/architecture/evidence machinery (F22+) existed. Each has since been **replaced** by an artifact the live flow generates automatically, so no skill references them anymore. Kept for provenance only — do **not** wire them back into the flow.

| File | Replaced by |
|---|---|
| `project_context_template.md` | `docs/SYSTEM_ARCHITECTURE.md` + `docs/BA.md` + `docs/DOMAIN_GLOSSARY.md` (the harness deliberately keeps these split; one combined doc would create a second source of truth). |
| `brainstorming_template.md` | The design-note of [`dev-system-design`](../../skills/dev-system-design/SKILL.md) ("Alternatives considered / Trade-offs") + the Pattern Selection Gate of [`dev-design-patterns`](../../skills/dev-design-patterns/SKILL.md). |
| `harness_report_template.md` | `docs/design-docs/<id>/evidence.md` (auto-written by `./harness verify`) + `./harness report` (CLI backlog report) + the Phase-3 report of `workflow-feature`/`workflow-bugfix`. |
