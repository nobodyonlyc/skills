---
name: batch-autotest
description: >-
  Specialized skill for batch processing automation testing. Receives SPEC documents,
  analyzes requirements, generates test cases using standard testing techniques,
  creates test data covering all scenarios, and executes tests in parallel using subagents.
  Outputs follow a standard Markdown table format.
---

# Batch AutoTest Skill

## Overview

This skill guides the agent through the batch autotest process in 5 phases:
1. **SPEC Analysis** — Analyze SPEC documents, extract business rules, input/output fields, constraints, boundaries, data states, and database interactions.
2. **TestCase Generation** — Generate test cases using Batch Test Data Matrix (normal, boundary, null/empty/space, invalid, encoding, volume, state, rerun), and classify them into **3 Test Automation Levels** (Level 1 - Fully Automated, Level 2 - Human-in-the-loop, Level 3 - Manual/Handoff).
3. **TestData Generation** — Create test data sets covering all valid, invalid, boundary, edge cases, mutated file structures, and DB pre-states corresponding to the automation levels.
4. **Test Execution** — Execute Level 1 programmatically; execute Level 2 programmatically but ask user for manual verdict approval; skip and hand off Level 3.
5. **Report Aggregation** — Aggregate results, calculate statistics by Level, compile Handoff list, and generate a final test report.

## Critical Rules

### 1. Language Alignment Rule
- The Agent (including the main orchestrator agent and all subagents) must identify the language of the input SPEC/document or user prompt.
- All generated output files (spec analysis, test cases, test data, execution results, and final reports), log outputs (including execution status logs shown to the user), internal reasoning/thinking blocks, and all chat communications (logs, status updates, agent answers, and user interactions) must be written in the **exact same language** as the input (e.g., if the SPEC or user prompt is in Japanese, all thinking, logging, and replies must be entirely in Japanese without mixing English or Vietnamese).

### 2. Source Code Integrity and Error Reporting (Testing only, do not modify source code)
- The workflow is designed only to test the application's source code. Absolutely no modifications or mock code injections to the production source code are allowed during testing.
- If a testcase fails due to a bug in the application, the Agent must only record, show, and report the detailed error. The Agent must not modify the source code to fix the bug or alter test cases to cover it up.

### 3. Unified Output Folder (Centralized Storage)
- All intermediate and final output documents generated from each step must be saved together in a single folder for each run (e.g., `test_runs/run_<timestamp>_<run_id>/`).

### 4. Review Gates (Quality Control & Approval)
- After each phase, the Agent must print a summary report of the phase results directly in the agent chat conversation (instead of creating a file on disk).
- The Agent must use the ask_question tool to present an interactive choice: "Is Phase X output satisfactory?". If the user approves and chooses to proceed ("Everything is fine"), the Agent proceeds to the next phase.

### 5. Tracking Duration and Token Usage
- The Agent must record the initial timestamp and token usage at the start of the pipeline.
- Upon pipeline completion, the Agent must compute the total elapsed time and tokens used, display them in the final chat response, and save them in the final report 5_final_report.md.

### 6. Sandbox Permission Optimization (Auto-write Authorization)
- At the very beginning of the pipeline (Phase 1 / Quick Start), the Agent must proactively invoke the `ask_permission` tool with `Action="write_file"` and `Target` set to the absolute path of the workspace. 
- This authorizes the environment once, enabling automated file writing and folder creation under the `test_runs/` directory without repeatedly interrupting the user with permission popups.

## Dependencies

No external skill dependencies. The agent only needs file read/write capabilities and subagent creation.

## Quick Start

1. Receive SPEC document (Markdown or JSON).
2. Identify the language of the input and set it as the execution language.
3. Proactively call the `ask_permission` tool for `write_file` access on the workspace directory to enable automatic file writing.
4. Read `references/spec_analysis_guide.md` (in English) for SPEC analysis.
5. Follow phase workflows: WF1 → WF2 → WF3 → WF4 → WF5.
5. Perform interactive review gates for each phase: print a summary report directly in the chat, and call the `ask_question` tool to ask if the output is okay. Proceed to the next phase only upon user approval.
6. Save final results using the formats in `references/output_format_guide.md`, including duration and token usage metadata.

## Workflow

### Phase 1: SPEC Analysis

- **Input**: SPEC document (Markdown/JSON)
- **Output**: Structured analysis saved to `{run_dir}/1_spec_analysis.md` (following template `templates/spec_analysis_output.md`)

Steps:
1. Read the entire SPEC document.
2. Extract **business rules** — list all business rules with unique IDs (`BR-xxx`).
3. Extract **input fields** — name, data type, constraints, required/optional status.
4. Extract **output fields** — name, data type, description.
5. Identify **constraints & boundaries** — min/max values, length, format, allowed values.
6. Extract **data states** — list all record/batch processing states.
7. Extract **impacted database tables** — list target/source tables and actions (CRUD).
8. Determine **equivalence partitions** — divide inputs into valid/invalid groups.
9. List **error conditions** — all possible error scenarios.
10. **REVIEW GATE (Interactive & Brainstorming)**:
    - Print a summary report of the SPEC analysis directly in the agent chat conversation.
    - Call the `ask_question` tool to ask: "Is the SPEC analysis (Phase 1) output satisfactory?".
    - If approved, proceed to Phase 2.

Reference: `references/spec_analysis_guide.md`

### Phase 2: TestCase Generation

- **Input**: SPEC Analysis output from Phase 1
- **Output**: TestCase suite saved to `{run_dir}/2_testcases.md` (following template `templates/testcase_output.md`)

Steps:
1. Create **Batch Test Data Matrix** — Map input fields & global batch scenarios against test characteristics (normal, boundary, null/empty/space, invalid, encoding, volume, state, rerun). Refer to `references/testcase_design_guide.md#8-batch-test-data-matrix`.
2. Generate TestCases covering all dimensions (Normal, Boundary, Decision Table, State Transition, DB CRUD, Mutation, Fault Tolerance, Pairwise, Negative).
3. Classify all TestCases into **3 Automation Levels** (Level 1, Level 2, Level 3) in the **Test Case Automation & Triage Sheet** (refer to `references/test_automation_levels_guide.md`). Write Handoff instructions for Level 3 cases.
4. Assign priority (Critical/High/Medium/Low) and category to each testcase.
5. Create a **traceability matrix** — mapping testcases ↔ SPEC requirements.
6. **REVIEW GATE (Interactive & Brainstorming)**:
    - Print a summary report of the TestCase design, including Traceability and Batch Test Data Matrix coverage, directly in the agent chat.
    - Conduct a Three-Amigos review (QA, Developer, BA) to ensure no edge cases are missed.
    - Call the `ask_question` tool to ask: "Is the TestCase generation (Phase 2) output satisfactory?".
    - If approved, proceed to Phase 3.

Reference: `references/testcase_design_guide.md`, `references/field_test_checklist_guide.md`, and `references/test_automation_levels_guide.md`

### Phase 3: TestData Generation

- **Input**: TestCase suite from Phase 2 + constraints from Phase 1
- **Output**: Test data sets saved to `{run_dir}/3_testdata.json` (following schema `templates/testdata_schema.json`)

Steps:
1. Load the JSON schema from `templates/testdata_schema.json` as the structural template (Method 4).
2. Generate **valid data** for Normal/Boundary testcases.
3. Generate **invalid data** for Negative testcases, ensuring the **Isolation Principle** (Method 1: only one constraint is violated per testcase, and other fields remain valid).
4. Generate **edge case data** — Unicode, injection, very large values.
5. Generate **mutated data sets** — create corrupted input files (e.g. wrong column counts or delimiters) for mutation testcases.
6. Prepare **database pre-state scripts** — scripts to set up DB records for CRUD and state transition testcases.
7. Prepare **system interruption triggers** — mock commands or scripts to cut connections or fill disk space during Phase 4 execution.
8. Generate **combination data** — multiple invalid fields.
9. Run the validation script (Method 1): Execute `python workflows/scripts/validate_testdata.py {run_dir}/3_testdata.json 1_spec_analysis.md` to programmatically verify constraint compliance and isolation rules.
10. If the validation script fails, analyze the output logs, fix the test data in `{run_dir}/3_testdata.json`, and re-run the validation until it passes.
11. **REVIEW GATE (Interactive & Brainstorming)**:
    - Print a summary report of the Test Data generation directly in the agent chat conversation.
    - Call the `ask_question` tool to ask: "Is the TestData generation (Phase 3) output satisfactory?".
    - If approved, proceed to Phase 4.

Reference: `references/testdata_strategy_guide.md`

### Phase 4: Test Execution (SubAgents)

- **Input**: TestCase suite + Test data sets
- **Output**: Raw results and execution logs saved to `{run_dir}/4_execution_results.json` and `{run_dir}/4_execution_log.txt`

Steps:
1. Filter out Level 3 TestCases from automatic run, marking them as `⏭️ SKIP` (Status: `HANDOFF`) with reason/instruction.
2. Group Level 1 & Level 2 TestCases and assign to subagents (or execute sequentially depending on dependencies).
3. For Level 1 TestCases: Subagents run programmatically and verify expected vs actual outputs automatically.
4. For Level 2 TestCases: Programmatically run, print logs & diffs directly to the user chat, propose verdict, and call the `ask_question` tool to collect manual human verdict.
5. Merge results from all subagents, verifying no testcase was missed.
6. **REVIEW GATE (Interactive & Brainstorming)**:
    - Print a summary report of the test execution (including auto run success rate and user verdict confirmations) directly in the agent chat.
    - Call the `ask_question` tool to ask: "Is the Test Execution (Phase 4) output satisfactory?".
    - If approved, proceed to Phase 5.

**SubAgent output format:**
```
| ID | Name | Status | Input | Expected | Actual | Error |
|---|---|---|---|---|---|---|
| TC-001 | Valid basic input | ✅ PASS | `{...}` | `{...}` | `{...}` | — |
```

### Phase 5: Report Aggregation

- **Input**: Execution results from Phase 4
- **Output**: Final reports saved to `{run_dir}/5_final_report.md` and `{run_dir}/5_report_raw.json` (following template `templates/test_report_output.md`)

Steps:
1. Aggregate all results (Level 1, Level 2, Level 3) into a single unified table.
2. Calculate statistics: total, passed, failed, skipped, and pass rate, categorized by Automation Level.
3. Analyze failed testcases: root cause, SPEC reference, and recommendations.
4. Compile the **Manual Integration Testing Handoff List** for all Level 3 testcases.
5. Create a coverage matrix: SPEC requirement ↔ testcase status.
6. Generate final Markdown and JSON reports (with duration, token metrics, and Handoff List).
7. **REVIEW GATE (Interactive & Brainstorming)**:
    - Print a summary report of the final aggregation directly in the agent chat conversation.
    - Call the `ask_question` tool to ask: "Is the Final Report (Phase 5) satisfactory?".

## Output Format

All testcase results must follow the format:

| ID | Name | Status | Input | Expected | Actual | Error |
|---|---|---|---|---|---|---|

Fields:
- **ID**: TestCase identifier (TC-001, TC-002, ...)
- **Name**: Brief description of the test case
- **Status**: `✅ PASS`, `❌ FAIL`, or `⏭️ SKIP`
- **Input**: Input data (JSON inline or referenced)
- **Expected**: Expected output according to the SPEC
- **Actual**: Actual output observed
- **Error**: Detailed error description if FAIL, `—` if PASS

## Common Mistakes

1. **Not reviewing output vs SPEC** — Every phase MUST have a review gate. Bad SPEC analysis leads to incorrect test cases.
2. **Missing negative testcases** — Do not test only the happy path. There must be test cases for null, empty, invalid types, and overflow.
3. **Test data not matching constraints** — Generated data must follow constraints in the SPEC.
4. **No traceability** — Every testcase must map back to a requirement in the SPEC.
5. **Language Mismatch** — Outputting files or chatting in a language different from the input SPEC/prompt language.
