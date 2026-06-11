# Rust Conventions

## 1. Naming Conventions
- Modules/Files: snake_case (e.g., `user_controller.rs`, `billing_service.rs`).
- Group files cleanly in `mod.rs` (or equivalent directory modules).
- Traits: PascalCase for trait names. Define traits in `traits.rs` or `interfaces.rs` if heavily abstracted.
- Data Models/Structs: `models.rs` or `[name]_model.rs`.

## 2. Business Logic Comments
- Use `///` for documentation comments on public structs and functions.
- NEVER use inline `//` comments to explain "What" or "How" code works. Rust code should be idiomatic and self-explanatory.
- Use `//` comments ONLY to explain "Why" (e.g., "Using Arc<Mutex> here because the external C library requires thread safety").

## 3. Module-level README
- Every major crate or significant module directory MUST contain a local `README.md` (or detailed module-level `//!` doc comments at the top of `lib.rs` / `mod.rs`).
- Explain the module's boundaries, trait implementations, and lifetime guarantees.

## 4. Paradigm lean (see [engineering-principles §6](../engineering-principles.md))
- Data + behavior via **traits**, not inheritance; **immutability by default** (`let`, not `let mut`, unless needed).
- Prefer **iterators / combinators** over manual mutable loops for transforms; pure functions for logic.
- `Result`/`Option` + `?` over panics/exceptions; push side effects to the edges.
