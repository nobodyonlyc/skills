# Phase 3 — Preview & feedback loop

The mock is not done until the user has **seen it in the browser** and **approved every screen**.

## 1. Show it in the browser (mandatory)
- **Method A (HTML/CSS):** serve the files with a local static server (e.g. `python3 -m http.server` or a dev server) and give the user a **clickable URL**, or open it in the browser. If your runtime has a browser/preview capability, use it to render and screenshot each screen.
- **Method B (Figma):** share the Figma file / frame link.

Walk the user through the screens against the Phase 1 checklist so coverage is visible.

## 2. Collect feedback (ask-user)
Ask the user for feedback per screen via the **ask-user** capability ([agent-tool-mapping](../../../resources/agent-tool-mapping.md)).

## 3. Iterate (loop)
For each piece of feedback:
- **Change** to an existing screen → regenerate that screen and re-preview.
- **Missing** screen/function → generate it ([Phase 2](phase-2-generate-mock.md)) and re-preview.

Repeat the preview → feedback → regenerate loop **as many times as needed**. Do **not** finish while the user still has feedback.

## 4. Approve & hand off
When the user explicitly approves all screens, the mock is done. It is a **design reference** for the real frontend build (hand off to [workflow-feature](../../workflow-feature/SKILL.md)) — not the shipped UI, and still contains no backend/DB.
