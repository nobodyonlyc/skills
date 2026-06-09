# Example — mock UI from an FE SPEC (task tracker)

Input: `/workflow-prototype docs/spec/frontend.md`

## Phase 1 — FE SPEC & method
Read `docs/spec/frontend.md`. Coverage checklist extracted:
- **Login** — email + password fields, inline validation, "forgot password" link, error state.
- **Board** — 3 columns (Todo/Doing/Done), task cards, drag affordance, filter bar, empty-column state.
- **Task detail** — title, description, assignee, status dropdown, comments list, save/cancel.

Method chosen with the user → **A. HTML/CSS** (no Figma needed).

## Phase 2 — Generate the mock
Built with [dev-fe-developer](../../dev-fe-developer/SKILL.md) rules: `login.html`, `board.html`, `task.html` + shared `styles.css`; cohesive palette, Inter font, responsive. All data hardcoded (sample tasks/users), navigation links wired, hover/validation/empty states shown. **No** API calls, no backend, no DB. Checklist fully crossed off.

## Phase 3 — Preview & feedback loop
- Served via `python3 -m http.server 8000`; gave the user `http://localhost:8000/login.html` and screenshotted each screen.
- **Round 1 feedback:** "board cards need a priority badge; login needs a logo." → regenerated `board.html` + `login.html`, re-previewed.
- **Round 2 feedback:** "add a task detail empty-comments state." → added that state, re-previewed.
- **Round 3:** user approves all screens. ✅

Handoff: approved static mock is the design reference for the real frontend (→ [workflow-feature](../../workflow-feature/SKILL.md)). It contains no backend/DB and is not the shipped UI.
