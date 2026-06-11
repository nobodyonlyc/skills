# Phase 3 — Preview & feedback loop

The mock is not done until it has passed a **design-critic review**, the user has **seen it in the browser**, and **approved every screen**.

## 0. Design-critic review BEFORE the user sees it (mandatory)
Don't offload quality to the user. Run an internal review pass first, then fix, then present:

1. **Screenshot every screen.** Use the Preview MCP (`preview_start` → `preview_screenshot`) or a browser/screenshot tool to capture each screen at **mobile and desktop** widths. (Method B/Figma: export frame images.)
2. **Spawn a design critic.** Spawn a subagent with `Role: Senior Product Designer` whose prompt is: *"Score each attached screen against the [quality rubric](../../core-prototype/references/quality-rubric.md) (8 dimensions + quick gate). For every screen, list each dimension's verdict and a concrete, actionable fix for any Fail. Write the report to `.harness/reports/prototype-critique.md`; your chat response is ONLY that path."* Pass the screenshots and the rubric path. (This is the same single-pass, batched review used for BA — one report covering all screens, not one critic per screen.)
3. **Batch-fix.** Apply **all** of the critique's fixes in a single revision pass (update tokens/CSS/HTML), then re-screenshot the changed screens. Re-run the critic **at most once** to confirm. Only then proceed to show the user.

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
