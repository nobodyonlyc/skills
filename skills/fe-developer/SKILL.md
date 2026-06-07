---
name: fe-developer
description: Guides the agent in developing interactive, highly aesthetic, responsive frontend code, integrating APIs, and testing components.
---

Develop Frontend feature for: $ARGUMENTS

Follow these guidelines to plan, implement, and verify frontend user interfaces, pages, or components.

## Step 1: Analyze UI Requirements & Setup
1. **Review system specs**: Understand user flows, required pages, and interactions.
2. **Examine framework & configurations**: Check whether the project uses Next.js, Vite (React/Vue), Tailwind CSS, or Vanilla CSS.
3. **Analyze design requirements**: Adhere to premium styling rules (dynamic animations, cohesive palettes, high-quality typography). Do not use browser defaults or generic colors.

## Step 2: Component Architecture Rules
When writing or modifying component files, follow these practices:
1. **Single Responsibility**: Keep components small, focused, and reusable. Split large UI files into modular subcomponents (e.g., `Button`, `Card`, `Header`).
2. **State Management**:
   * Use local state (`useState`, `ref`) for UI-only variables (e.g., open/close modal, active tab).
   * Use context or state-management libraries (Redux, Zustand, Vuex) only for global domain data.
   * Lift state up cleanly to avoid props drilling.
3. **Props Validation**: Define clear Typescript interfaces or PropType declarations for all components to prevent runtime crashes.

## Step 3: Premium Styling & Design Rules
1. **Color Palette**: Use curated colors (e.g., HSL tailors, dark/light modes) with consistent variables (e.g., `--primary`, `--neutral-800`).
2. **Layout & Responsiveness**: Use CSS Flexbox and Grid. Always build with a mobile-first responsive layout (using media queries like `@media (min-width: 768px)`).
3. **Micro-interactions**: Add smooth transitions (`transition: all 0.3s ease`) on hovers, focuses, and active states.
4. **No Placeholders**: Never write text like `[Image here]` or `TODO`. Use `generate_image` tool for mock assets, or use beautiful icon libraries (e.g., Lucide, FontAwesome).

## Step 4: API Integration
1. **Data Fetching**: Use standard APIs (`fetch`, `axios`) or hooks (`react-query`, `swr`).
2. **Loading & Error Boundaries**: Always handle UI feedback for:
   * **Loading state**: Render skeleton loaders or spinners to prevent layout shifts.
   * **Error state**: Display friendly error notifications with a "Try Again" action button.
   * **Empty state**: Inform the user when no data is available with a call-to-action (CTA).
3. **Performance**: Prevent redundant API calls. Implement debouncing for search inputs and throttle event listeners.

## Step 5: SEO and Accessibility (a11y)
1. **Semantic HTML**: Use proper HTML tags (`<header>`, `<nav>`, `<main>`, `<section>`, `<footer>`, `<button>`, `<a>`) instead of nesting everything in `<div>` tags.
2. **Accessibility**: Add proper `alt` texts for images, specify `aria-label` or `aria-expanded` attributes on interactive components, and ensure high color contrast.
3. **SEO**: Set dynamic meta tags (title, description, open graph tags) for each page route.

## Step 6: Component Verification (Definition of Done)
1. Write unit or component tests (e.g., using Vitest + React Testing Library) to verify component behavior.
   * Mock global context, routes, and API responses.
   * Test user click events, state changes, and edge-case rendering.
2. Build and run validation checks:
   * Execute build script: e.g., `npm run build` to detect compilation and TypeScript errors.
   * Run linter: e.g., `npm run lint` or `eslint .`.
3. Provide a preview or local dev URL (e.g., `http://localhost:5173`) if verifying UI layouts interactively.
