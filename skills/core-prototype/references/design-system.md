# Design System & CSS Patterns

When building prototypes, always apply a cohesive design system rather than relying on default browser styling or haphazard CSS rules. 

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
Define your core design tokens at the `:root` level so you can reuse them easily. Even for a quick mock, define:

```css
:root {
  /* Colors */
  --primary: #2563eb;
  --primary-hover: #1d4ed8;
  --background: #f8fafc;
  --surface: #ffffff;
  --text-main: #0f172a;
  --text-muted: #64748b;
  --border: #e2e8f0;

  /* Typography */
  --font-sans: 'Inter', system-ui, -apple-system, sans-serif;

  /* Spacing */
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 2rem;

  /* Borders & Shadows */
  --radius: 8px;
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
}
```

## Placeholders & Assets
- **Images**: Do not use empty divs with `[Image]`. Use a service like `https://placehold.co/800x600` or Unsplash Source (if available) for realistic imagery.
- **Icons**: Use SVG icons inline or import a library like Phosphor Icons or Heroicons via CDN.
- **Copy**: Do not use "Lorem Ipsum" if possible. Write realistic placeholder text (e.g., "Welcome back, Jane Doe" instead of "Title Goes Here").
