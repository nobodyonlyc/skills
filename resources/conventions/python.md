# Python Conventions

## 1. Naming Conventions
- Files/Modules: snake_case (e.g., `user_controller.py`, `data_processor.py`).
- Classes: PascalCase.
- Functions/Variables: snake_case.
- Pydantic Models/Schemas: `[name]_schema.py` or placed in `schemas.py`.

## 2. Business Logic Comments
- Use Docstrings (`"""`) for all classes and functions to define inputs, outputs, and purpose.
- NEVER use inline `#` comments to explain "What" or "How" code works. 
- Use `#` comments ONLY to explain "Why" (e.g., "# Ignoring the SSL verification here due to internal proxy requirements").

## 3. Module-level README
- Every major package (a folder with `__init__.py`) or feature module MUST contain a local `README.md` explaining the domain flow and dependencies.

## 4. Paradigm lean (see [engineering-principles §6](../engineering-principles.md))
- **Mixed**: pure functions for transforms/logic; classes for entities and stateful services. Don't wrap a single function in a class.
- Prefer **comprehensions / generators** and immutable defaults; avoid mutating shared/global state.
- Composition over inheritance; use `@dataclass`/Pydantic for data, keep I/O at the edges.
