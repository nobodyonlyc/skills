---
name: workflow-feature
description: Orchestrate a multi-agent workflow to plan, implement, test, and verify a new feature.
---

Feature request: $ARGUMENTS

This is a multi-agent feature development workflow. Run the following agents IN PARALLEL:

**Agent 1 — Requirements analyst**: 
* Read the codebase structure, existing patterns, and related code. Use the [explain](file:///home/zrik/workspace/projs/harness/.agents/skills/explain/SKILL.md) skill to query core components.
* If database changes are needed, coordinate with the [db-designer](file:///home/zrik/workspace/projs/harness/.agents/skills/db-designer/SKILL.md) skill.
* Produce: (1) list of files that will need to change, (2) list of questions that must be answered before implementation, (3) risks or constraints to be aware of.

**Agent 2 — Test strategist**: 
* Find existing tests, identify the test framework and conventions.
* Plan required tests using the [test-gen](file:///home/zrik/workspace/projs/harness/.agents/skills/test-gen/SKILL.md) guidelines.
* Produce: a test plan describing what test cases are needed (happy path, edge cases) and how to structure them.

---

## Execution Sequence

### Step 1: Alignment & Implementation Plan
1. Present Agent 1 and 2 findings to the user and resolve any open questions.
2. Draft a precise implementation plan (which files change, in what order, what each change does).
3. Get user approval on the plan.

### Step 2: Source Code Implementation
Implement the feature logic. Delegate and strictly follow instructions based on the component type:
* **UI/Frontend**: Use the [fe-developer](file:///home/zrik/workspace/projs/harness/.agents/skills/fe-developer/SKILL.md) skill.
* **Server API/Web Server**: Use the [be-developer](file:///home/zrik/workspace/projs/harness/.agents/skills/be-developer/SKILL.md) skill.
* **Batch Jobs/ETL**: Use the [batch-developer](file:///home/zrik/workspace/projs/harness/.agents/skills/batch-developer/SKILL.md) skill.
* **CLI Command Tools**: Use the [cli-tool-developer](file:///home/zrik/workspace/projs/harness/.agents/skills/cli-tool-developer/SKILL.md) skill.

### Step 3: Test Generation & Execution
1. Generate complete test suites using the [test-gen](file:///home/zrik/workspace/projs/harness/.agents/skills/test-gen/SKILL.md) skill.
2. Run tests after each logical step to ensure stability.

### Step 4: Quality Gate & Code Review
1. Rà soát lại toàn bộ thay đổi thông qua skill [code-review](file:///home/zrik/workspace/projs/harness/.agents/skills/code-review/SKILL.md) to check for security vulnerabilities, memory leaks, and design errors.
2. Fix any issues found by the reviewer.

### Step 5: Verification and Checkpoint (Definition of Done)
1. Run the project verification suite via the [qa](file:///home/zrik/workspace/projs/harness/.agents/skills/qa/SKILL.md) skill.
2. Execute the Harness verify check:
   ```bash
   ./harness verify <feature_id>
   ```
   *Note: This automatically stages and commits a git checkpoint on success.*
3. Summarize the session: files changed, tests added, and any deferred items.
