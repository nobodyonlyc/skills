# AutoTest — Agent Instructions

## Skill: Batch AutoTest

You have access to the **batch-autotest** skill for automation testing batch processing.

### When to Use

Use this skill when the user requests any tasks related to:
- Analyzing SPEC documents
- Designing test cases for batch processing
- Generating test data
- Running automated tests
- Creating test reports

### How to Use

1. **Read the skill instructions** at `skills/batch-autotest/SKILL.md` — this is the main guide.
2. **Follow the 5-phase pipeline**:
   - Phase 1: SPEC Analysis → read `skills/batch-autotest/references/spec_analysis_guide.md`
   - Phase 2: TestCase Generation → read `skills/batch-autotest/references/testcase_design_guide.md`
   - Phase 3: TestData Generation → read `skills/batch-autotest/references/testdata_strategy_guide.md`
   - Phase 4: Parallel Test Execution (spawn multiple subagents)
   - Phase 5: Report Aggregation
3. **Output format** for each testcase result:

```markdown
| ID | Name | Status | Input | Expected | Actual | Error |
|---|---|---|---|---|---|---|
```

4. **Templates** are located at `skills/batch-autotest/templates/` — used as the output standard for each phase.
5. **Examples** are located at `skills/batch-autotest/examples/` — including sample SPEC, 31 testcases, test data, and a complete report.

### Important Rules

- **SPEC is the single source of truth** — all testcases and data must be traceable to the SPEC.
- **Each phase has an interactive Review Gate + Brainstorming** — after creating documents for each phase (SPEC analysis, testcases, test data), the agent MUST perform a thorough brainstorming session, present options, and allow the user to review the results and choose the next steps before moving to the next phase.
- **Phase 4 runs in parallel** — group testcases and create multiple subagents concurrently.
- **Do not skip negative testing** — always include testcases for null, empty, invalid, and boundary conditions.
- **Language Alignment Rule**: Dynamically detect the input language (e.g., from the SPEC document or the user prompt). All generated output files (spec analysis, test cases, test data, execution results, and reports), log outputs (including execution status logs shown to the user), internal reasoning/thinking blocks, and all chat communications (for both the main orchestrator agent and all subagents) must be in the exact same detected language (e.g., if the user prompts or SPEC is in Japanese, all thinking, logging, and replies must be entirely in Japanese without mixing English or Vietnamese).

### Directory Structure

```
skills/batch-autotest/
├── SKILL.md                     ← Read this file first
├── references/                  ← Detailed technical guides
│   ├── spec_analysis_guide.md
│   ├── testcase_design_guide.md
│   ├── testdata_strategy_guide.md
│   └── output_format_guide.md
├── templates/                   ← Output templates for each phase
│   ├── spec_analysis_output.md
│   ├── testcase_output.md
│   ├── testdata_output.md
│   └── test_report_output.md
└── examples/                    ← Complete examples
    ├── sample_batch_spec.md
    ├── sample_testcases.md
    ├── sample_testdata.json
    └── sample_report.md

workflows/                       ← Detailed workflows for each phase
├── wf1_spec_analysis.md
├── wf2_testcase_generation.md
├── wf3_testdata_generation.md
├── wf4_test_execution.md
├── wf5_report_aggregation.md
└── wf_full_pipeline.md
```

### Detailed Workflows

When you need to see the detailed workflow for each phase, read the files in the `workflows/` directory:
- `workflows/wf_full_pipeline.md` — full pipeline overview
- `workflows/wf1_spec_analysis.md` to `workflows/wf5_report_aggregation.md` — details for each phase
