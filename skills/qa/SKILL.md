---
name: qa
description: Perform a structured QA pass on current changes or a feature, testing happy path, edge cases, and regression risks.
---

QA target: $ARGUMENTS (feature name, PR number, or file path — leave blank to QA current changes)

Gather what's being tested:

```bash
git diff main...HEAD --stat 2>/dev/null || git diff --stat HEAD~1
git log --oneline -5
```

Run a structured QA pass:

## 1. Acceptance criteria check

- What is this feature/fix supposed to do? List the expected behaviors.
- Verify each one is actually implemented (read the code, run if possible).
- Flag any acceptance criteria that are missing or only partially implemented.

## 2. Happy path

Walk through the primary use case step by step. For each step:
- What input/action?
- What is the expected output/state?
- Does the code produce that? (Check logic, not just syntax.)

## 3. Edge cases

Systematically test these categories — mark each ✅ pass / ❌ fail / ⚠️ untested:

| Category | Examples |
|---|---|
| Empty / null | empty string, null/undefined, empty array/object |
| Boundary | min/max values, off-by-one, first/last item |
| Concurrency | race conditions, double-submit, stale data |
| Permissions | unauthenticated user, wrong role, expired token |
| Error states | network failure, timeout, invalid input from external source |
| Large input | 10k items, very long strings, deeply nested objects |

## 4. Regression risk

List 3-5 existing features most likely to break from this change. Check each one in the code.

## 5. QA report

Output a report:
```
## QA Report — <feature>

### ✅ Passing
- ...

### ❌ Failing
- <issue>: <expected> vs <actual>

### ⚠️ Needs manual testing
- ...

### Verdict
PASS / FAIL / CONDITIONAL PASS (needs fix before merge)
```
