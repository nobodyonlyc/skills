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
   - Edge cases (empty, zero, null, boundary values)
   - Error cases (invalid input, external failures)
   - Any business rules or invariants in the code

3. **One test per behavior** — Name tests descriptively: `should_return_error_when_input_is_empty`, not `test_function`.

4. **No mocking unless necessary** — Prefer real implementations. Only mock external I/O (network, filesystem, time).

Write the tests to the appropriate file. Ask before creating a new test file if unsure of the convention.
