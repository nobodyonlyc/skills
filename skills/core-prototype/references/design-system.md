# Design System & CSS Patterns

When building prototypes, always apply a cohesive design system rather than relying on default browser styling or haphazard CSS rules.

## Pick a style direction first (do not default to "generic blue + Inter")
The token block below is a **neutral starting skeleton, not the look to ship**. Pasting it verbatim is the #1 cause of bland, identical-looking prototypes. Before writing CSS, commit to a concrete **style direction** and tailor every token to it:
- Name the feel in a few words — e.g. *minimal/editorial*, *warm/friendly*, *bold/high-contrast*, *calm/professional*, *playful/rounded*, *dense/data-heavy (dashboard)*.
- Choose a **real font pairing** (a heading/display face + a readable body face) instead of system-Inter-only, and a deliberate **accent hue** — not the default blue unless the brand calls for it.
- Match radius / shadow / density to the feel (playful → larger radius, softer shadows; data-heavy → tight radius, compact spacing).

When this runs inside the [common design phase](../../workflow-intake/references/common-design-phase.md), present **2–3 distinct directions** (each with a sample token preview) and let the user pick before committing `docs/spec/design-system.md`.

## Responsive Breakpoints
Always design mobile-first or ensure a responsive fluid layout using the following standard breakpoints:
- **Mobile (Default)**: `0px` to `639px` (1 column, stacked)
- **Tablet**: `640px` to `1023px` (Grid starts to expand)
- **Desktop**: `1024px+` (Multi-column, complex sidebars)

Use `@media (min-width: ...)` to apply progressively enhanced styles.

## CSS Patterns
Prefer modern CSS layout modules.
- **Flexbox**: Use for 1-dimensional layouts (navbars, button groups, vertically centered modal content).
- **Grid**: Use for 2-dimensional layouts (dashboards, image galleries, complex forms).

Avoid using floats or absolute positioning for structural layouts unless absolutely necessary.

## UI State & JavaScript
Write vanilla JavaScript to make the prototype feel alive. Essential interactions include:
- Toggling sidebars on mobile/tablet breakpoints.
- Opening and closing modals, dropdowns, and accordions.
- Simulating empty states vs. populated states.

## Design Tokens (Custom Properties)
Define your core design tokens at the `:root` level so you can reuse them everywhere. A complete token set is what separates a polished mock from a default-looking one — define **all** of these categories (retune the values to your chosen style direction; the numbers below are only an example skeleton):

```css
:root {
  /* Brand & semantic colors — recolor to your direction, don't ship the default blue */
  --primary: #2563eb;
  --primary-hover: #1d4ed8;
  --accent: #7c3aed;            /* a deliberate secondary accent */
  --success: #16a34a;
  --warning: #d97706;
  --danger:  #dc2626;
  --info:    #0284c7;

  /* Surfaces & text */
  --background: #f8fafc;
  --surface: #ffffff;
  --surface-2: #f1f5f9;          /* subtle raised/sunken surface */
  --text-main: #0f172a;
  --text-muted: #64748b;         /* must still meet AA on --background */
  --border: #e2e8f0;
  --ring: rgb(37 99 235 / 0.45); /* visible keyboard focus ring */

  /* Typography — a real scale + a deliberate pairing, not Inter-only */
  --font-heading: 'Sora', 'Inter', system-ui, sans-serif;
  --font-body: 'Inter', system-ui, -apple-system, sans-serif;
  --text-xs: 0.75rem;   --text-sm: 0.875rem;  --text-base: 1rem;
  --text-lg: 1.125rem;  --text-xl: 1.5rem;    --text-2xl: 2rem;  --text-3xl: 2.5rem;
  --leading-tight: 1.2; --leading-normal: 1.5;
  --weight-normal: 400; --weight-medium: 500; --weight-semibold: 600; --weight-bold: 700;

  /* Spacing — 4/8pt grid; use these, never arbitrary px */
  --space-1: 0.25rem; --space-2: 0.5rem; --space-3: 0.75rem; --space-4: 1rem;
  --space-6: 1.5rem;  --space-8: 2rem;   --space-12: 3rem;   --space-16: 4rem;

  /* Radius & elevation scale */
  --radius-sm: 6px; --radius-md: 10px; --radius-lg: 16px; --radius-full: 9999px;
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);

  /* Motion — makes interactions feel alive */
  --ease: cubic-bezier(0.4, 0, 0.2, 1);
  --dur-fast: 120ms; --dur-base: 200ms;
}
```

Then use the tokens consistently: focus rings via `box-shadow: 0 0 0 3px var(--ring)`, hover transitions via `transition: all var(--dur-base) var(--ease)`, semantic colors for status (badges, validation, toasts). Add a `[data-theme="dark"]` override block if the direction calls for dark mode.

## Placeholders & Assets
- **Images**: Do not use empty divs with `[Image]`. Use a service like `https://placehold.co/800x600` or Unsplash Source (if available) for realistic imagery.
- **Icons**: Use SVG icons inline or import a library like Phosphor Icons or Heroicons via CDN.
- **Copy**: Do not use "Lorem Ipsum" if possible. Write realistic placeholder text (e.g., "Welcome back, Jane Doe" instead of "Title Goes Here").
