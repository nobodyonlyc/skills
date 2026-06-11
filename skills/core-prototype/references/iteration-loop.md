# Prototype Iteration Loop

The true value of a prototype is the ability to visualize it and refine it rapidly. Follow this cycle for every UI mockup.

## 1. Render and Host
Once the HTML, CSS, and JS are written (usually in a dedicated folder like `prototype/`), you must host it locally so the user can see it in their browser.

```bash
# Example: Using Python's built-in HTTP server
python3 -m http.server 8080 --directory prototype/
```

Provide the user with a clickable link: `http://localhost:8080`.

## 2. Self-review BEFORE the user sees it (mandatory)
Do not present a first draft blind. Critique your own output first — this is what raises quality instead of offloading every flaw onto the user:
1. **Screenshot it.** Use the Preview MCP (`preview_start` → `preview_screenshot`) or any browser/screenshot tool to capture each screen **at mobile and desktop widths**. If no screenshot capability exists, visually trace the rendered DOM/CSS instead.
2. **Score against the [quality rubric](quality-rubric.md).** Walk the 8 dimensions (hierarchy, spacing, contrast, typography, component states, realistic content, empty/loading/error, responsive) plus the quick gate.
3. **Fix every Fail in one pass** — overflowing text, weak hierarchy, missing hover/focus, cramped spacing, lorem/`[Image]`, low contrast — *then* move on. Don't ship known flaws to the user.

## 3. Present and Ask for Feedback
Only after the self-review passes, present the iteration:
- Highlight what was completed and which interaction states are wired up (e.g., "click 'Login' to see the error state").
- **Explicitly ask**: "Please open the link. How does this look? What would you like to tweak regarding the layout, colors, or spacing?"

## 4. Iterate
When the user provides feedback (e.g., "Make the header darker" or "The padding on mobile is too tight"):
1. Update the CSS/HTML files directly.
2. The local server will usually serve the updated files upon browser refresh.
3. Inform the user: "Updated. Please refresh your browser. Does that look better?"
4. Repeat until the user approves.
