---
name: dev-fe-developer
description: Guides the agent in developing interactive, highly aesthetic, responsive frontend code, integrating APIs, and testing components.
---

> **[Persona Directive]** You must execute this skill acting in the role of a **Senior Frontend Engineer**. Adopt their exact mindset, priorities, and vocabulary. Do NOT spawn a subagent for this.


Develop Frontend feature for: $ARGUMENTS

Follow these guidelines to plan, implement, and verify frontend user interfaces, pages, or components.

## Step 1: Analyze UI Requirements & Setup
1. **Review system specs**: Understand user flows, required pages, and interactions.
2. **Examine framework & configurations**: Check whether the project uses Next.js, Vite (React/Vue), Tailwind CSS, or Vanilla CSS.
3. **Analyze design requirements**: Adhere to premium styling rules (dynamic animations, cohesive palettes, high-quality typography). Do not use browser defaults or generic colors.

## Step 2: UI Design, Mockup & Confirmation (MANDATORY)
Before writing any actual application code or merging UI features, you MUST execute a design/review loop:
1. **Create a visual mockup**: Either generate a UI design mockup image using the **generate-image** capability (see [agent-tool-mapping](../../resources/agent-tool-mapping.md)) if your runtime has one, or — the reliable fallback — build a standalone static mockup (e.g. static HTML/CSS file) demonstrating the exact layout, spacing, and colors.
2. **Host a preview**: Start a local Dev Server and print a clickable preview URL for the user to view the layout in their browser.
3. **Explain design choices**: Provide a clear explanation of the layout, color palette (e.g. custom HSL themes, sleek dark/light mode), typography, spacing, and transition details.
4. **Get confirmation**: Explicitly ask the user to confirm the design via the **ask-user** capability ([agent-tool-mapping](../../resources/agent-tool-mapping.md); `AskUserQuestion` in Claude Code). **DO NOT** write application component code or integrate the UI into the main application until the user has explicitly approved the design mockup.

## Step 3: Component Architecture Rules
When writing or modifying component files, follow these practices:
1. **Single Responsibility**: Keep components small, focused, and reusable. Split large UI files into modular subcomponents (e.g., `Button`, `Card`, `Header`).
2. **State Management**:
   * Use local state (`useState`, `ref`) for UI-only variables (e.g., open/close modal, active tab).
   * Use context or state-management libraries (Redux, Zustand, Vuex) only for global domain data.
   * Lift state up cleanly to avoid props drilling.
3. **Props Validation**: Define clear Typescript interfaces or PropType declarations for all components to prevent runtime crashes.

## Step 4: Premium Styling & Design Rules
To prevent low-effort or "ugly" interfaces, you MUST adhere to high-end design principles:
1. **Color Palette & Themes**: Use curated color palettes (e.g., tailored HSL/CSS variables such as `--primary`, `--neutral-800`). Avoid default colors like plain red, blue, green. Implement cohesive light and dark mode styling.
2. **Visual Depth & Texture**: Utilize subtle gradients, micro-borders (e.g., `1px solid rgba(255, 255, 255, 0.08)`), drop shadows (`box-shadow`), and glassmorphism (`backdrop-filter: blur()`) to create layering.
3. **Typography**: Always import and apply elegant typography (e.g. Google Fonts like Inter, Outfit, or Roboto) rather than using browser default sans-serif or serif fonts. Set proper hierarchy, line-heights, and letter-spacing.
4. **Layout & Responsiveness**: Use CSS Flexbox and Grid. Build responsive mobile-first layouts (with media queries like `@media (min-width: 768px)`). Ensure consistent padding and gap sizes.
5. **Micro-interactions & Transitions**: Add smooth hover, focus, and active state transitions (`transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1)`) on all buttons, links, inputs, and cards.
6. **No Placeholders**: Never write text like `[Image here]` or `TODO`. Use the **generate-image** capability for mock assets if available, or use beautiful icon libraries (e.g., Lucide, FontAwesome).

## Step 5: API Integration
1. **Data Fetching**: Use standard APIs (`fetch`, `axios`) or hooks (`react-query`, `swr`).
2. **Loading & Error Boundaries**: Always handle UI feedback for:
   * **Loading state**: Render skeleton loaders or spinners to prevent layout shifts.
   * **Error state**: Display friendly error notifications with a "Try Again" action button.
   * **Empty state**: Inform the user when no data is available with a call-to-action (CTA).
3. **Performance**: Prevent redundant API calls. Implement debouncing for search inputs and throttle event listeners.

## Step 6: SEO and Accessibility (a11y)
1. **Semantic HTML**: Use proper HTML tags (`<header>`, `<nav>`, `<main>`, `<section>`, `<footer>`, `<button>`, `<a>`) instead of nesting everything in `<div>` tags.
2. **Accessibility**: Add proper `alt` texts for images, specify `aria-label` or `aria-expanded` attributes on interactive components, and ensure high color contrast.
3. **SEO**: Set dynamic meta tags (title, description, open graph tags) for each page route.

## Step 7: Code Conventions & Documentation
Instead of hardcoded rules, you MUST apply the specific conventions based on the project's language and framework. Before writing code, consult the appropriate convention file:
- TypeScript/Node.js (Backend): [`typescript-node.md`](../../resources/conventions/typescript-node.md)
- TypeScript/React (Frontend): [`typescript-react.md`](../../resources/conventions/typescript-react.md)
- Rust: [`rust.md`](../../resources/conventions/rust.md)
- Python: [`python.md`](../../resources/conventions/python.md)
- Go: [`go.md`](../../resources/conventions/go.md)

1. **Naming Conventions**: Follow the file suffix rules defined in the convention file.
2. **Business Logic Comments**: Follow the 'Why over How' rule.
3. **Module-level README**: Every newly created module must contain a local `README.md` as mandated by the convention guidelines.

## Step 8: Component Verification (Definition of Done)
1. Write unit or component tests (e.g., using Vitest + React Testing Library) to verify component behavior.
   * Mock global context, routes, and API responses.
   * Test user click events, state changes, and edge-case rendering.
2. Build and run validation checks:
   * Execute build script: e.g., `npm run build` to detect compilation and TypeScript errors.
   * Run linter: e.g., `npm run lint` or `eslint .`.
3. Provide a preview or local dev URL (e.g., `http://localhost:5173`) if verifying UI layouts interactively.
