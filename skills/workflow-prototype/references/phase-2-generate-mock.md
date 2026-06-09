# Phase 2 — Generate the mock

**Skill used:** [dev-fe-developer](../../dev-fe-developer/SKILL.md) (styling, layout, component & a11y rules).

Generate **every screen** on the [Phase 1](phase-1-spec-and-method.md) checklist. **UI only** — all data is hardcoded/placeholder; no API calls, no backend, no database, no real logic.

## Method A — HTML/CSS
- One file per screen (or a single page with client-side navigation); a shared stylesheet for consistency.
- Use realistic placeholder content and assets — never `[Image here]` or `TODO` (use icon libraries / placeholder images).
- Make navigation between screens work, and show interaction **states** (hover/focus/active, validation, loading, empty) with minimal JS — but forms/buttons are visually complete and non-functional.
- Follow [dev-fe-developer](../../dev-fe-developer/SKILL.md): cohesive palette, typography, spacing, responsive (mobile-first), accessible semantics.

## Method B — Figma (via MCP)
- Use the Figma MCP connector to create one frame per screen, mirroring the same coverage checklist.
- Apply the same design rules; link components/states where the connector supports it.

## Done criteria
Every screen and every function on the checklist is rendered. Cross off the checklist as you go; if the SPEC implies a state you cannot show statically, mock it visually and note it.

→ Proceed to [Phase 3](phase-3-preview-feedback.md).
