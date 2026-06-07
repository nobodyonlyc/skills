---
name: workflow-feature
description: Orchestrate a multi-agent workflow to plan, implement, test, and verify a new feature.
---

Feature request: $ARGUMENTS

This is a multi-agent feature development workflow. Run the following agents IN PARALLEL:

**Agent 1 — Requirements analyst**: Read the codebase structure, existing patterns, and related code. Produce: (1) list of files that will need to change, (2) list of questions that must be answered before implementation, (3) risks or constraints to be aware of.

**Agent 2 — Test strategist**: Find existing tests, identify the test framework and conventions. Produce: a test plan describing what test cases are needed and how to structure them for this feature.

After both agents complete:

1. Present their findings to the user and resolve any open questions.
2. Draft an implementation plan: which files change, in what order, what each change does.
3. Get user approval on the plan.
4. Implement the feature following the plan, running tests after each logical step.
5. Run the full test suite and confirm everything passes.
6. Summarize: files changed, tests added, anything deferred.
