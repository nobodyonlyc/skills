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

## 4. Folder Structure (mandatory — matches Atomic Design tiers)
```
src/
  components/
    atoms/        # Button, Input, Badge, Icon, Spinner, Avatar
    molecules/    # FormField, SearchBar, CardHeader, AlertBanner, Dropdown
    organisms/    # DataTable, NavBar, ProductCard, CommentThread, Modal
    templates/    # Page layout wrappers — no domain data (DashboardLayout, AuthLayout)
    pages/        # Route containers — wire organisms to state/data
  hooks/          # Shared hooks: useDebounce, usePagination, useAuth, useToast
  utils/          # Pure helpers: formatDate, truncateText, slugify
  types/          # Shared TypeScript interfaces (ApiResponse, PaginatedResult)
```
**Extraction rule:** if the same UI pattern appears in ≥2 places, extract it before adding a third occurrence. A component in `pages/` that copies markup from another page is a DRY violation.

## 5. Paradigm lean (see [engineering-principles §6](../engineering-principles.md))
- **Functional components + hooks**; pure render from props/state, no class components.
- Treat state as **immutable** (return new objects/arrays); derive don't duplicate; keep components composable.
- Push side effects into `useEffect`/data-fetching hooks; keep presentational components pure (props in, UI out).
