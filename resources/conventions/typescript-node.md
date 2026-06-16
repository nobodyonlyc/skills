# TypeScript Node.js Backend Conventions

## 1. Naming Conventions
- Controllers: `[name].controller.ts`
- Services: `[name].service.ts`
- Repositories: `[name].repository.ts`
- DTOs/Schemas: `[name].dto.ts` or `[name].schema.ts`
- Middlewares: `[name].middleware.ts`
- Utils: `[name].util.ts`
- Interfaces/Types: `[name].interface.ts` or `[name].type.ts`

## 2. Business Logic Comments
- NEVER use inline comments to explain "What" or "How" code works. The TypeScript code and variable names should be self-documenting.
- Use comments ONLY to explain "Why" a specific implementation was chosen (e.g., "Workaround for API rate limit").

## 3. Module-level README
- Every newly created or significantly modified module (e.g., `domain/users/` or `application/billing/`) MUST contain a local `README.md`.
- This `README.md` should explain the internal logic, module boundaries, external dependencies, and data flow.

## 4. Folder Structure (mandatory — prevents cross-module duplication)
```
src/
  common/           # Shared across all feature modules
    dto/            # PaginationDto, IdParamDto, CursorDto
    errors/         # NotFoundError, ValidationError, ForbiddenError (extend BaseError)
    validators/     # Reusable Zod/class-validator schemas
    utils/          # Pure helpers: paginate.util.ts, hash.util.ts, date.util.ts
  base/
    base.repository.ts    # Generic CRUD: findById, findAll, create, update, softDelete
    base.service.ts       # Guard wrappers: ensureExists(), ensureOwner()
  modules/          # One folder per domain feature
    [feature]/
      [feature].controller.ts
      [feature].service.ts
      [feature].repository.ts   # extends BaseRepository
      [feature].dto.ts
```
**Extraction rule:** logic shared by ≥2 services or repositories belongs in `common/` or `base/`, not copy-pasted into both.

## 5. Paradigm lean (see [engineering-principles §6](../engineering-principles.md))
- **Mixed**: pure functions for transforms/use-cases; classes for entities and stateful services (repositories, gateways).
- Favor `readonly` / immutable data and `const`; composition over inheritance; depend on interfaces at boundaries.
- Keep side effects (DB, HTTP) in the infrastructure layer; domain stays pure and unit-testable.
