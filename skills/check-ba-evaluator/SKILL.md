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

## Mode B — Backlog coverage review (SPEC → US)

Use this mode to verify the **User-Story backlog actually covers every item in the SPECs** before it is confirmed (driven by [plan-us-backlog-generator](../plan-us-backlog-generator/SKILL.md) Step 2.5). The recurring failure it catches: a backlog generated from the high-level architecture that **misses User Stories** only defined in the detailed SPECs.

Spawn the subagent with `Role: Senior PM Evaluator` and set `Prompt` to:

"You are a strict Senior Product Manager who knows these SPECs cold. Read the detailed SPECs ([docs/spec/*.md]) and the drafted backlog (`.harness/features.json`).
Build a **coverage matrix**: every screen in the FE SPEC, every endpoint/function in the BE SPEC, every entity/migration in the DB SPEC, and every business rule in the BA → mapped to the User Story (or stories) that covers it.
List explicitly **every SPEC item that NO User Story covers** — these are the gaps. For each gap, propose the missing User Story (title, area, behavior, a verification command).
Write the coverage matrix and the gap list to `.harness/reports/backlog-coverage.md`. Your chat response must ONLY be the path to this file. If any SPEC item is uncovered, FAIL the backlog and list the missing stories the main agent must add."

Wait for the report. If it fails, **add the missing User Stories** and re-run this coverage review until every SPEC item is covered, before presenting the backlog to the user.
