# CLAUDE.md — Agent Pointer

> **Single source of truth:** [AGENTS.md](AGENTS.md). Read it first for full instructions.
> This file is a thin pointer so Claude Code auto-loads the project guidance; do not duplicate content here — keep `AGENTS.md` canonical.

## This project uses the batch-autotest skill

This repo is a SPEC-driven **batch automation testing** project. The reusable capability lives in the
**batch-autotest** skill at [skills/batch-autotest/SKILL.md](skills/batch-autotest/SKILL.md).

### When to use
Any request to: analyze a SPEC document, design test cases for batch processing, generate test data,
run automated tests, or produce a test report.

### How to use
1. Read [skills/batch-autotest/SKILL.md](skills/batch-autotest/SKILL.md) — the main guide.
2. Follow the 5-phase pipeline (orchestrator: [workflows/wf_full_pipeline.md](workflows/wf_full_pipeline.md)):
   - Phase 1 SPEC Analysis → `workflows/wf1_spec_analysis.md`
   - Phase 2 TestCase Generation → `workflows/wf2_testcase_generation.md`
   - Phase 3 TestData Generation → `workflows/wf3_testdata_generation.md`
   - Phase 4 Parallel Test Execution → `workflows/wf4_test_execution.md`
   - Phase 5 Report Aggregation → `workflows/wf5_report_aggregation.md`
3. Use templates in `skills/batch-autotest/templates/` and examples in `skills/batch-autotest/examples/`.
4. Store all run outputs under `test_runs/run_<timestamp>_<run_id>/`.

### Key rules (see AGENTS.md for the full list)
- **SPEC is the single source of truth** — every test case and datum traces back to the SPEC.
- **Testing only — never modify the application source code** to make a test pass; record and report bugs instead.
- **Interactive Review Gate after every phase** — print a summary, then ask the user before proceeding.
- **Do not skip negative testing** — always include null/empty/invalid/boundary cases.
- **Language Alignment Rule** — detect the input language (SPEC or user prompt) and produce all output
  files, logs, reasoning, and replies in that exact same language.
