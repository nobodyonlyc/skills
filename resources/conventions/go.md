# Go Conventions

## 1. Naming Conventions
- Files: snake_case, short and descriptive (e.g., `user.go`, `user_test.go`, `repository.go`). Go prefers shorter file names grouped by package.
- Packages: Lowercase, single-word names (e.g., `package auth`).
- Interfaces: End with `er` if single method (e.g., `Reader`, `Writer`).

## 2. Business Logic Comments
- Write package-level doc comments immediately before the `package` clause.
- Write doc comments for all exported names (starting with the name itself).
- NEVER use inline `//` comments to explain "What" or "How" code works. Go code should be idiomatic and simple.
- Use `//` comments ONLY to explain "Why".

## 3. Module-level README
- Every significant package (especially inside `internal/` or `pkg/`) MUST contain a local `README.md` or a robust `doc.go` file.
- Explain what the package does, its public API, and concurrency guarantees.
