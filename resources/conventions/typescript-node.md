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
