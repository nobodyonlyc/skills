# Engineering Principles (shared by all `dev-*` skills)

Cross-cutting principles every implementation skill applies, regardless of component type. The per-component skills ([dev-be-developer](../skills/dev-be-developer/SKILL.md), [dev-fe-developer](../skills/dev-fe-developer/SKILL.md), [dev-cli-tool-developer](../skills/dev-cli-tool-developer/SKILL.md), [dev-batch-developer](../skills/dev-batch-developer/SKILL.md), [dev-db-designer](../skills/dev-db-designer/SKILL.md)) reference this so the rules live in one place. Language-specific rules stay in [conventions/](conventions/).

## 1. Code to the requirement (trace, don't guess)
Implement exactly what the User Story asks — no more (gold-plating), no less (silent gaps).
- **List the acceptance criteria** of the US (`user_visible_behavior` + any SPEC items) before writing code.
- **Map each criterion → the code and the test that proves it.** Keep this map in the feature's `docs/design-docs/<id>/` notes or the PR description.
- A criterion with no test is **not done**. Code with no matching criterion is **out of scope** — drop it or raise a new US (WIP=1).
- When the requirement is ambiguous, **ask-user** (click-select the interpretation); never invent behavior.

## 2. Architecture before code (set the shape first)
Decide the module's shape before typing implementation:
- Restate the **overall architecture** the feature fits into (from `docs/SYSTEM_ARCHITECTURE.md`) and the **layer/boundary** this change belongs in (domain / application / infrastructure / presentation, or the component's equivalent).
- Define the **module boundary**: its responsibility, its public interface, what it depends on (depend on interfaces, not concretions), and what must NOT leak across the boundary.
- Sketch data flow in / out. Only then implement.

## 3. Design patterns (use the right one, don't over-engineer)
Reach for a pattern when it removes real duplication or decouples a real axis of change — not by default.
- **Repository / Adapter** — isolate persistence and external services behind an interface so business logic is testable and swappable.
- **Strategy** — when one behavior has several interchangeable algorithms (pricing, ranking, export format) selected at runtime.
- **Factory** — when construction is non-trivial or the concrete type is chosen at runtime.
- **Observer / pub-sub** — when one change must fan out to several decoupled reactions (events, webhooks).
- **Decorator / middleware** — to layer cross-cutting concerns (auth, logging, caching) without touching core logic.
- **Anti-pattern guard:** do not add a pattern for a single, stable implementation. A function is better than a one-strategy Strategy. Name the axis of change a pattern buys you; if there isn't one, skip it.

## 4. Design for extension (open to add, closed to modify)
Assume the code will change. Make the likely changes cheap and the risky ones contained.
- **Open/Closed:** new behavior should be addable by adding code (a new strategy, handler, plugin), not by editing a growing `if/else`/`switch` over types.
- **No hardcoded lists** of things that grow — drive them from config, a registry, or a table. Adding the Nth case must not mean editing N call sites.
- **Stable interfaces, swappable implementations** — depend on an interface/trait at the boundary so an implementation can be replaced (e.g. swap the payment provider) without touching callers.
- **Separate configuration from logic** — limits, feature flags, and provider choices live in config, not literals buried in code.
- **Extension points where variation is expected**, but don't pre-build abstractions for variation you don't yet have (YAGNI). Extensible ≠ speculatively generic.

## 5. Clean code (named, not implied)
- **Single Responsibility** per function/module; small functions that do one thing.
- **Meaningful names**; no abbreviations that need a decoder. Names follow [conventions/](conventions/).
- **DRY** within reason — extract real duplication, tolerate incidental similarity.
- **No dead code, no commented-out code, no leftover TODOs** that are really unfinished work (raise a US instead).
- **Comments explain "why", never "what"** — the code shows what (see the convention files).

## 6. Paradigm & style (FP vs OOP — right tool for the job)
Do not be dogmatic about one paradigm. Pick per problem, and follow the language's idiom.
- **Logic & data transformation** → prefer **pure functions and immutable data**: no hidden state, trivial to test, safe under the concurrency a team workflow implies. Default for parsers, calculators, mappers, validators, reducers.
- **Entities with identity, lifecycle, and invariants** (User, Order, Cart) → use **OOP/encapsulation**: bundle the state with the rules that protect its invariants behind a boundary, so nothing can put it in an illegal state.
- **Composition over inheritance** by default — compose small pieces (functions, traits/interfaces, components). Reach for inheritance only for a genuine, stable "is-a" relationship; never to share code.
- **Push side effects to the edges** — keep I/O, DB, network, and clock in the infrastructure/presentation layer; keep the domain core pure and deterministic. (This is the same boundary the layered architecture in §2 already draws.)
- **Follow the language idiom, don't import a foreign paradigm:**
  - Rust → data + traits + iterators, immutability by default, `Result`/`Option` over exceptions.
  - TypeScript / Python → mixed; pure functions for transforms, classes for entities and stateful services.
  - Go → structs + small interfaces, composition; avoid faux-OOP class hierarchies.
- **Anti-dogma guard:** no class with a single method that should be a function; no deep inheritance tree; no "everything immutable" that fights the language. Optimize for clarity and testability, not paradigm purity.

## How a `dev-*` skill applies this
1. Trace to requirement (§1) → 2. Set architecture & boundary (§2) → implement, choosing patterns deliberately (§3) and designing for the changes you expect (§4), keeping it clean (§5) → then the skill's own verification/Definition-of-Done.
