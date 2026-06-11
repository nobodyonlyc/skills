---
name: workflow-prototype
description: Generate a mock UI from the FE SPEC (HTML/CSS, or Figma via an MCP connector), preview it in the browser, and iterate on feedback. UI only — no backend, DB, or business logic.
---

Mock UI request: $ARGUMENTS

This workflow produces a **mock UI only**. It renders every screen and interaction described in the **frontend SPEC**, using stubbed/placeholder data. **No backend, no database, no real business logic.** Generate by one of two methods, preview in the browser, and loop on feedback until the user approves.

> **Scale check:** this is the right skill for a **whole app / the full FE SPEC** (many screens, coverage checklist). For just **1–2 screens** — e.g. a single feature's design gate — use the lightweight [core-prototype](../core-prototype/SKILL.md) instead.

## Skills this workflow drives
- [dev-fe-developer](../dev-fe-developer/SKILL.md) — styling, layout, component, and accessibility rules for the mock.
- [core-explain](../core-explain/SKILL.md) — read existing FE patterns / design tokens to reuse (optional).
- **Senior Product Designer critic** (Phase 3) — scores the rendered screens against the [quality rubric](../core-prototype/references/quality-rubric.md) before the user sees them.

> **Quality bar:** every screen must pass the [quality rubric](../core-prototype/references/quality-rubric.md) (8 dimensions), styled from the approved `docs/spec/design-system.md` tokens. Coverage (all screens exist) is necessary but not sufficient — a rendered-but-ugly screen is not done.

## Phases
1. **FE SPEC & method** → [references/phase-1-spec-and-method.md](references/phase-1-spec-and-method.md)
   Read the FE SPEC (`docs/spec/frontend.md`); enumerate **every screen + function**; pick the generation method with the user.
2. **Generate the mock** → [references/phase-2-generate-mock.md](references/phase-2-generate-mock.md)
   Produce all screens per the SPEC using the chosen method — HTML/CSS, or Figma via an MCP connector. Placeholder data only.
3. **Critic review, preview & feedback loop** → [references/phase-3-preview-feedback.md](references/phase-3-preview-feedback.md)
   Screenshot + design-critic review against the rubric and batch-fix **before** the user sees it; then show it in the browser, collect feedback, regenerate or add screens, repeat until approved.

## Two generation methods
- **A. HTML/CSS** — self-contained static files (+ minimal JS only for navigation/interaction states), served locally and opened in the browser.
- **B. Figma (via MCP)** — build the frames in Figma using an available Figma MCP connector; share the file/frame link for review.

## Hard gates / scope
- **UI only.** Never implement or stub a backend, database, or business logic — this is not the production build.
- **Cover the whole FE SPEC** — every screen and every function it lists; track coverage against a checklist.
- **Pass the quality rubric** — each screen must clear all 8 dimensions of the [quality rubric](../core-prototype/references/quality-rubric.md), styled from the approved design-system tokens.
- **Design-critic review before the user** — screenshot + critique against the rubric and batch-fix before any user preview (Phase 3 step 0).
- **Browser preview is mandatory** before asking for feedback.
- **Iterate until approved** — each round of feedback → regenerate/extend the affected screens → re-preview. Repeat as many times as needed.
- The approved mock guides the real FE build later (e.g. [workflow-feature](../workflow-feature/SKILL.md)); it is not itself the shipped UI.
