# Example — UI prototype: "Kanban board drag-and-drop"

Input: `/workflow-prototype a kanban board where I can drag cards between columns`

## Phase 1 — research & interface
- **Stack researcher ([core-explain](../../core-explain/SKILL.md))** finds the repo already uses React + Vite and has `@dnd-kit` in `package.json` → recommend reusing it.
- **Interface designer** specifies: 3 columns (Todo/Doing/Done), a card with title, drag to move. Core interaction = drag-and-drop.
- User confirms the spec.

## Phase 2 — UI design gate (blocking)
- A standalone `mockup.html` is built ([dev-fe-developer](../../dev-fe-developer/SKILL.md)) with 3 styled columns and sample cards, fully static.
- Presented to user. User: "make the columns wider and add a card count badge."
- Mockup edited and re-presented. User: "approved." ✅ — only now does logic begin.

## Phase 3 — build · run · handoff
- Single-file React prototype built with `@dnd-kit` ([core-prototype](../../core-prototype/SKILL.md)), cards in local state (no backend, [dev-be-developer](../../dev-be-developer/SKILL.md) stub noted).
- Run via `npm run dev`; screenshot/output shows dragging a card from Todo → Doing.
- Handoff: state is in-memory (hardcoded seed cards); production needs persistence + multi-user sync. Effort: **M**.
