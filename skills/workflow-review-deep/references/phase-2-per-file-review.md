# Phase 2 — Per-file Review

**Skills used:** [check-code-review](../../check-code-review/SKILL.md), [check-security-review](../../check-security-review/SKILL.md)

Each agent reviews its assigned file (full content + diff) on four axes:

- **Correctness bugs** — logic errors, wrong edge-case handling, broken contracts. → [check-code-review](../../check-code-review/SKILL.md)
- **Security issues** — injection, hardcoded secrets, auth/authorization gaps, unvalidated input. → [check-security-review](../../check-security-review/SKILL.md)
- **Performance problems** — N+1 queries, needless allocations, blocking I/O on hot paths. → [check-code-review](../../check-code-review/SKILL.md)
- **Simplification opportunities** — dead code, duplication, over-engineering.

Each finding must carry a **severity** (🔴 / 🟡 / 🔵), the **file:line**, and a concrete suggested change.

→ Aggregate in [Phase 3](phase-3-consolidate-verdict.md).
