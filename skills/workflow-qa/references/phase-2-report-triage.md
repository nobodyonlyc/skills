# Phase 2 — Report & Triage

**Skills used:** [check-test-gen](../../check-test-gen/SKILL.md), [core-fix](../../core-fix/SKILL.md)

## 1. Merge into one QA report
```
## QA Report — <feature/PR>
Date: <today>

### Functional coverage
<from Agent 1>

### Edge cases
<from Agent 2>

### Regression risks
<from Agent 3>

### Overall verdict
PASS / FAIL / CONDITIONAL PASS
Blocking issues: <list or "none">
```

## 2. Triage findings
- For any ❌ or high-severity finding, propose the **minimal fix** (via [core-fix](../../core-fix/SKILL.md)) and the **test** that would guard it (via [check-test-gen](../../check-test-gen/SKILL.md)).

## 3. Decide with the user
Ask the user: fix the issues now, or document them for follow-up?
- **Fix now** → hand off to [workflow-bugfix](../../workflow-bugfix/SKILL.md) for each blocker.
- **Defer** → record them so the next session can pick them up.
