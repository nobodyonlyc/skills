# TypeScript React Frontend Conventions

## 1. Naming Conventions
- Components: `[Name].tsx` (PascalCase for files exporting React components)
- Hooks: `use[Name].ts` (camelCase)
- State/Stores: `[name].store.ts` or `[name].slice.ts`
- Utils/Helpers: `[name].util.ts`
- Interfaces/Types: `[name].type.ts`
- Styles: `[name].module.css` (if using CSS modules)

## 2. Business Logic Comments
- NEVER use inline comments to explain "What" or "How" code works. UI logic should be clean and declarative.
- Use comments ONLY to explain "Why" (e.g., "Adding 50ms timeout to prevent Safari rendering bug").

## 3. Module-level README
- Every major feature module or complex component folder (e.g., `features/checkout/`) MUST contain a local `README.md`.
- Explain the layout, local state management, props API, and interactions with global stores.

## 4. Paradigm lean (see [engineering-principles §6](../engineering-principles.md))
- **Functional components + hooks**; pure render from props/state, no class components.
- Treat state as **immutable** (return new objects/arrays); derive don't duplicate; keep components composable.
- Push side effects into `useEffect`/data-fetching hooks; keep presentational components pure (props in, UI out).
