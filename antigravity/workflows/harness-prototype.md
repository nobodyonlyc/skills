# /harness-prototype

Render a **mock UI** from the frontend SPEC as real, openable files, review it against a quality bar, **preview it in the browser**, and loop on feedback until the user approves. UI only — **no backend, no database, no business logic**.

> This is the step that fails most on Antigravity: the agent "does prototype" but creates no files and never previews. Do **not** finish this workflow until real files exist under `prototype/` AND the user has seen them in a browser AND approved every screen.

## Phase 1 — SPEC & checklist
1. Read `docs/spec/frontend.md`. Enumerate **every screen and every function/interaction** it lists into an explicit **coverage checklist** — you will tick each off.
2. Confirm the generation method with the user:
   - **A. HTML/CSS/JS** (default) — self-contained static files, minimal JS only for navigation/interaction states.
   - **B. Figma via MCP** — build frames using a Figma MCP connector; share the link.

## Phase 2 — Generate the mock (create actual files)
Default method A:
1. If `docs/spec/design-system.md` exists, extract its `:root { … }` token block into **`prototype/tokens.css`** and link it from every screen, so all screens are visually consistent. If no design system exists yet, establish one first (offer 2–3 style directions, get approval) and write it to `docs/spec/design-system.md`.
2. For **each screen on the checklist**, create a real file: `prototype/<screen-name>.html` (+ shared `prototype/tokens.css`, optional `prototype/app.js` for nav). Use **placeholder/stubbed data only**.
3. Render **every screen and every function** on the checklist — including empty/loading/error states where the SPEC implies them. Tick each off. Coverage is necessary but not sufficient: each screen must also look right (clear visual hierarchy, spacing rhythm, AA contrast, real-looking content, component states, responsive at mobile + desktop).
4. **Never** implement or stub a backend/DB/business logic.

## Phase 3 — Critic review → browser preview → feedback loop
**0. Design-critic review BEFORE the user sees it (mandatory).**
   - Screenshot every screen at **mobile and desktop** widths (use the Preview/screenshot capability, or open files in a browser and capture).
   - Spawn a **Senior Product Designer** subagent: *"Score each screen against the 8-dimension quality rubric (visual hierarchy, spacing, contrast, typography, component states, realistic content, empty/loading/error, responsive). For each screen list each dimension's verdict + a concrete fix for any Fail. Write the report to `.harness/reports/prototype-critique.md`; reply only with that path."*
   - **Batch-fix** all findings in one pass, re-screenshot changed screens, re-run the critic at most once.

**1. Show it in the browser (mandatory).** Serve the files (e.g. `python3 -m http.server` in `prototype/`) and give the user a **clickable URL**, or open each screen in the browser and present screenshots. Walk through the screens against the Phase 1 checklist so coverage is visible.

**2. Collect feedback** per screen (ask the user).

**3. Iterate.** Change → regenerate that screen and re-preview. Missing → generate it (Phase 2) and re-preview. Repeat the preview → feedback → regenerate loop **as many times as needed**. Do not finish while the user still has feedback. Feedback that changes the look updates `docs/spec/design-system.md` so it stays the source of truth.

**4. Approve & hand off.** When the user explicitly approves all screens, the mock is done. Commit `prototype/` + `docs/spec/design-system.md`. It is a **design reference** for the real FE build (later, in `/harness-execute-us`) — not the shipped UI, and still has no backend/DB.

## Hard gates
- UI only — never a backend/DB/business logic.
- Cover the whole FE SPEC — every screen + function, tracked on the checklist.
- Design-critic review before the user; browser preview before asking for feedback; iterate until approved.
- Real files must exist under `prototype/` — a verbal "prototype done" with no files is a failure.
