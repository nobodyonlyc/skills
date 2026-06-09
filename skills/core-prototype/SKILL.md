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

## Ground rules
- **UI only** — never build or stub a backend, DB, or real logic. Hardcode all sample data.
- **Static HTML/CSS** (+ minimal JS for navigation/interaction states only).
- **No placeholders text** like `[Image here]`/`TODO` — use icon libraries or placeholder images and realistic copy.
- Follow [dev-fe-developer](../dev-fe-developer/SKILL.md) styling rules (cohesive palette, typography, spacing, responsive, accessible).

## Workflow
1. **Confirm the screens** — which screen(s) and what each must show.
2. **Build** — write the HTML/CSS; wire navigation and show interaction states.
3. **Preview in the browser** — serve it (e.g. `python3 -m http.server`) and give the user a clickable URL or screenshots.
4. **Feedback loop** — on feedback, regenerate/extend the screen and re-preview; repeat until the user is happy.

If it doesn't render correctly on first preview, fix it before handing over.
