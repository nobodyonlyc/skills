# Example — Deep review of PR #142

Input: `/workflow-review-deep 142`

## Phase 1 — gather & fan-out
`gh pr diff 142 --name-only` → 5 changed files. Spawn 5 review agents in parallel, each with file + diff.

## Phase 2 — per-file review
- `auth/session.ts` — 🔴 [check-security-review](../../check-security-review/SKILL.md): JWT verified without checking `exp`; 🟡 [check-code-review](../../check-code-review/SKILL.md): duplicated token-parse helper.
- `api/tasks.ts` — 🟡 N+1 query loading task owners.
- `web/TaskList.tsx` — 🔵 extract inline style to a class.
- `utils/csv.ts` — clean.
- `tests/tasks.test.ts` — 🔵 missing empty-list assertion.

## Phase 3 — consolidate & verdict
Report ([check-pr-review](../../check-pr-review/SKILL.md)):
- 🔴 Critical: missing JWT `exp` check.
- 🟡 Important: N+1 query; duplicated token parser.
- 🔵 Suggestions: inline style; missing test.

**Verdict: Request Changes** (one critical). User opts to apply the N+1 and dedupe cleanups now → shaped via [check-refactor](../../check-refactor/SKILL.md); the JWT fix is routed to [workflow-bugfix](../../workflow-bugfix/SKILL.md).
