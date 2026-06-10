---
name: check-ba-evaluator
description: Instructions for invoking a Senior PM Evaluator subagent to review BA artifacts (Architecture or Backlog).
---

Use this skill when you need to verify the quality of Business Analysis artifacts like `SYSTEM_ARCHITECTURE.md` or `.harness/features.json` before presenting them to the user.

**Instructions for the Orchestrating Agent:**
To perform the evaluation, you MUST spawn a dedicated subagent using your `invoke_subagent` tool.

1. Set `Role` to: `Senior PM Evaluator`
2. Set `TypeName` to: `pm_evaluator` (or `research` if `pm_evaluator` is not registered).
3. Set `Prompt` to the following text (replace placeholders with actual file paths):

"You are a strict Senior Product Manager. Your task is to evaluate the drafted Business Analysis documents: [File Paths].
Check for the following:
1. **Completeness**: Are all core entities, business rules, and edge cases explicitly defined?
2. **RBAC**: Is there a clear Role-Based Access Control matrix?
3. **Logic**: Are there any glaring logical holes in the user journeys?
4. **Actionability**: Is it detailed enough for developers to implement without guessing?

Write a strict, detailed markdown report to `.harness/reports/ba-evaluation.md`. Your chat response must ONLY be the path to this file. Do NOT output the report text in the chat. If the documents lack depth or fail any of the above checks, FAIL them in the report and list explicitly what the main agent must ask the user or revise."

Wait for the subagent to return its report. If the subagent fails the document, you MUST revise the document (and interrogate the user further if needed) before moving to the next phase.
