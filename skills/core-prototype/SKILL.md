---
name: core-prototype
description: Single-agent quick mock UI — render a screen or two as static HTML/CSS for fast visual feedback. UI only, no backend or DB.
---

Mock UI to build: $ARGUMENTS

The lightweight, single-agent path for a **mock UI**. Use it to throw together one or a few screens as static **HTML/CSS** for quick visual feedback. **UI only** — placeholder data, no backend, no database, no business logic.

> For the full, SPEC-driven mock (every screen/function from `docs/spec/frontend.md`, choice of HTML/CSS or Figma-via-MCP, mandatory browser preview + feedback loop), use [workflow-prototype](../workflow-prototype/SKILL.md).

```bash
ls -la
find . -name "package.json" -o -name "*.css" | head -3   # reuse existing FE stack / tokens if any
```

## Ground Rules
- **UI only** — never build or stub a backend, DB, or real logic. Hardcode all sample data.
- **Static HTML/CSS/JS** — generate JavaScript to handle UI events (e.g., toggling sidebars, opening modals, dropdowns).
- **Responsive by default** — the prototype MUST support Mobile and Tablet modes seamlessly.
- **No placeholder text** like `[Image here]` or `TODO` — use placeholder images (e.g. `https://placehold.co/600x400`) and realistic copy.

## References
Please follow the guidelines in these references carefully:
- **[Design System & CSS Patterns](references/design-system.md)**: Standard tokens, typography, and responsive layout guidance.
- **[Iteration Loop](references/iteration-loop.md)**: The lifecycle for rendering, previewing, and refining the prototype.

## Examples
- **[Sample Prototype Output](examples/sample-prototype.md)**: See an example of a well-structured prototype.

## Workflow Phases
1. **Confirm Requirements**: Clarify the screen(s) and what they must show. Set up the basic layout.
2. **Apply Design Tokens**: Ensure your prototype adheres to `references/design-system.md`.
3. **Build the Mock**: Write the HTML/CSS with realistic content.
4. **Preview & Iterate**: Follow `references/iteration-loop.md` to host the files, show them to the user, and iterate on feedback.
