---
name: workflow-bugfix
description: Orchestrate a multi-agent workflow to investigate, locate, fix, and verify a bug.
---

Bug report: $ARGUMENTS

Multi-agent bug investigation workflow. Run the following agents IN PARALLEL:

**Agent 1 — Root cause investigator**: 
* Search the codebase for all code paths related to the reported bug. Trace the data flow. Use the [explain](file:///home/zrik/workspace/projs/harness/.agents/skills/explain/SKILL.md) skill to inspect code logic.
* Identify the exact line(s) where the bug originates and why it happens.

**Agent 2 — Impact analyst**: 
* Find all callers, tests, and related code that could be affected by a fix.
* Identify regression risk areas. Check git log for related recent changes.
* If the bug is database-related, consult the [db-designer](file:///home/zrik/workspace/projs/harness/.agents/skills/db-designer/SKILL.md) guidelines for safe alterations.

---

## Execution Sequence

### Step 1: Alignment & Fix Proposal
1. Present the root cause and impact analysis.
2. Propose the minimal fix using the [fix](file:///home/zrik/workspace/projs/harness/.agents/skills/fix/SKILL.md) skill guidelines — change only what's needed to fix the root cause.
3. Get user approval before applying.

### Step 2: Implement Code Fix
1. Apply the fix carefully, preserving existing code styling and commenting.
2. If changing specific components, leverage:
   * [fe-developer](file:///home/zrik/workspace/projs/harness/.agents/skills/fe-developer/SKILL.md) for UI fixes.
   * [be-developer](file:///home/zrik/workspace/projs/harness/.agents/skills/be-developer/SKILL.md) for API logic errors.
   * [batch-developer](file:///home/zrik/workspace/projs/harness/.agents/skills/batch-developer/SKILL.md) for ETL pipeline failures.

### Step 3: Add Regression Test
1. Add a regression test (using [test-gen](file:///home/zrik/workspace/projs/harness/.agents/skills/test-gen/SKILL.md) skill) that triggers the bug condition and asserts the correct, fixed behavior.

### Step 4: Quality Gate & Code Review
1. Review the git diff using the [code-review](file:///home/zrik/workspace/projs/harness/.agents/skills/code-review/SKILL.md) skill to ensure the bug fix doesn't introduce side-effects.

### Step 5: Verification & Checkpoint (Definition of Done)
1. Run the project verification suite using the [qa](file:///home/zrik/workspace/projs/harness/.agents/skills/qa/SKILL.md) skill.
2. Execute the Harness verify check:
   ```bash
   ./harness verify <feature_id>
   ```
3. Report: root cause explanation, fix details, test added, and regression risk assessment.
