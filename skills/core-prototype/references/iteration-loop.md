# Prototype Iteration Loop

The true value of a prototype is the ability to visualize it and refine it rapidly. Follow this cycle for every UI mockup.

## 1. Render and Host
Once the HTML, CSS, and JS are written (usually in a dedicated folder like `prototype/`), you must host it locally so the user can see it in their browser.

```bash
# Example: Using Python's built-in HTTP server
python3 -m http.server 8080 --directory prototype/
```

Provide the user with a clickable link: `http://localhost:8080`.

## 2. Present and Ask for Feedback
When presenting the first iteration:
- Highlight what was completed.
- Note any specific interactions that are wired up (e.g., "You can click the 'Login' button to see the error state").
- **Explicitly ask**: "Please open the link. How does this look? What would you like to tweak regarding the layout, colors, or spacing?"

## 3. Capture Screenshots (If Applicable)
If you have access to a browser MCP or screenshot tool, you can capture the rendered page yourself to review visual correctness before showing it to the user. Fix glaring CSS issues (like overflowing text) before the user sees it.

## 4. Iterate
When the user provides feedback (e.g., "Make the header darker" or "The padding on mobile is too tight"):
1. Update the CSS/HTML files directly.
2. The local server will usually serve the updated files upon browser refresh.
3. Inform the user: "Updated. Please refresh your browser. Does that look better?"
4. Repeat until the user approves.
