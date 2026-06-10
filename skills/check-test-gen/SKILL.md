---
name: check-test-gen
description: Generate comprehensive unit, integration, or regression tests for a target module or function.
---

> **[Persona Directive]** You must execute this skill acting in the role of a **SDET (Software Development Engineer in Test)**. Adopt their exact mindset, priorities, and vocabulary. Do NOT spawn a subagent for this.


Generate tests for: $ARGUMENTS

Read the target file and find the test framework in use:

```bash
cat "$ARGUMENTS" 2>/dev/null || find . -name "$ARGUMENTS" | head -3
# Detect test framework
ls package.json pyproject.toml go.mod Cargo.toml 2>/dev/null | head -3
find . -name "*.test.*" -o -name "*_test.*" -o -name "test_*.py" | head -5
```

Generate tests following these principles:

1. **Match existing patterns** — Use the same test framework, file naming convention, and assertion style as existing tests in this project.

2. **Cover these cases**:
   - Happy path (typical valid input)
   - Edge cases (empty, zero, null, boundary values: `$Min, $Max, $Min-1, $Max+1`)
   - Error cases (invalid input, external failures)
   - Any business rules or invariants in the code

3. **Domain-Specific Testing Rules (MANDATORY)**:
   - **Frontend (FE)**: When generating End-to-End or UI automation tests, you MUST use **Playwright**.
   - **Backend (BE/API)**: You MUST explicitly assert HTTP status codes (200, 400, 401, 403, 404, 500) and verify correct endpoint routing.
   - **Database (DB)**: Implement **Post-State Validation**. Any test that modifies data (Insert/Update/Delete) MUST execute a subsequent query directly against the DB to verify the new state, rather than blindly trusting the API's success response.

4. **Fault Isolation Principle (CRITICAL for Negative Tests)**: When generating invalid inputs or error cases, the test MUST isolate exactly ONE invalid parameter/constraint while keeping all other parameters perfectly valid. Do not combine multiple invalid fields in a single negative test case.

4. **One test per behavior** — Name tests descriptively: `should_return_error_when_input_is_empty`, not `test_function`.

4. **No mocking unless necessary** — Prefer real implementations. Only mock external I/O (network, filesystem, time).

Write the tests to the appropriate file. Ask before creating a new test file if unsure of the convention.
