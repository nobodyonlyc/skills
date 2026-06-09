# QA Report Example

```markdown
## QA Report — PR #142 (Auth Refactor)
Date: 2024-06-09

### 1. Functional Coverage
✅ Valid token grants access to `/dashboard`
✅ Expired token redirects to `/login`
❌ Refresh token flow is missing (API returns 404)
⚠️ Role-based access control (Admin vs User) is ambiguous in the code

### 2. Edge Cases & Flaky Tests
- **High**: Null token payload crashes the parser (Missing test).
- **Medium**: Extremely long tokens (>4KB) cause header truncation.
- **Flaky**: `auth.test.ts: "should timeout after 30s"` failed 1 out of 3 runs.

### 3. Regression Risks
- **High**: `src/middleware.ts` is shared with the legacy API. Changes here risk breaking `v1` endpoints.
- **Coverage**: Dropped from 85% to 81% due to untested error branches in `TokenValidator`.

### 4. Overall Verdict
**Verdict**: 🔴 FAIL
**Blocking Issues**:
1. Refresh token flow missing.
2. Null token parser crash.
3. Flaky timeout test.

### Proposed Fixes (Action Required)
- **Fix 1**: Implement `POST /auth/refresh` in `src/auth.controller.ts`.
- **Fix 2**: Add `if (!payload) return null` in `TokenValidator.ts` + unit test.

*How would you like to proceed? (Fix now / Defer)*
```
