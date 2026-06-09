# Example — Bug: "Login fails for emails with + alias"

Input: `/workflow-bugfix users with a+tag@gmail.com cannot log in, 401 returned`

## Phase 1 — investigation
- **Subagent A ([core-explain](../../core-explain/SKILL.md))** traces login flow and finds `apps/api/auth/normalize.ts` strips everything after `+`, mutating the stored email lookup key.
- **Subagent B** reports the same normalize function is used by signup and password-reset → fixing it affects 3 paths; recent commit `e21f` introduced the strip.
- Agreed fix proposal: stop stripping the `+` alias in the lookup key.

## Phase 2 — fix · test · review loop
- **Subagent C ([check-test-gen](../../check-test-gen/SKILL.md))** writes a test: signup + login with `a+tag@gmail.com` → expects 200. It **fails** (401) against current code, confirming the bug.
- **Subagent D ([core-fix](../../core-fix/SKILL.md))** removes the `+`-strip in `normalize.ts`, keeping case-lowering. Test now **passes**.
- Reviewer ([check-code-review](../../check-code-review/SKILL.md)) checks signup & reset paths still pass their tests → **clean**.

## Phase 3 — verify & checkpoint
```
$ ./harness verify F12   # qa pass + verifications → PASS, commits checkpoint
```
Report: root cause = over-eager email normalization (commit e21f); fix = 1 line in `normalize.ts`; regression test added; low remaining risk (shared paths re-tested).
