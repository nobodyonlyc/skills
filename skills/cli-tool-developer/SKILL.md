---
name: cli-tool-developer
description: Guides the agent in developing interactive, user-friendly, and standard command-line interface (CLI) tools.
---

Develop CLI feature for: $ARGUMENTS

Follow these guidelines to design, implement, and verify command-line interfaces, scripts, and automation tools.

## Step 1: Design Command Interface (CLI Parser)
Choose a reliable command-line parsing library (e.g., `clap` for Rust, `commander` or `yargs` for Node.js, `click` or `argparse` for Python).
Structure commands and arguments logically:
1. **Commands & Subcommands**: Use hierarchical subcommands for different operations (e.g., `tool init`, `tool status`, `tool verify <id>`).
2. **Flags and Options**:
   * `-h`, `--help`: Automatically generate clear usage documentation.
   * `-v`, `--version`: Output the current tool version.
   * `-V`, `--verbose`: Enable debug logging.
   * `--json` / `--quiet`: Control output format for automation compatibility.

## Step 2: Input and Output Routing (Stdout vs. Stderr)
Always route console outputs correctly so that the tool integrates nicely with shell scripting (piping):
1. **Stdout (Standard Output)**: Output *only* the direct result of the command (e.g., database tables, query outputs, requested information).
2. **Stderr (Standard Error)**: Output logs, diagnostics, progress spinners, warnings, and error messages here. This ensures shell commands can filter outputs (e.g., `tool status > output.txt` will not save progress logs to the file).
3. **Stdin (Standard Input)**: When appropriate, allow the tool to accept input data from pipes (e.g., `cat input.json | tool parse`).

## Step 3: Terminal UX & Visuals
1. **ANSI Colors**: Use terminal colors to highlight critical status information. Use standard mappings:
   * **Green**: Successful operations.
   * **Red**: Failures and fatal errors.
   * **Yellow**: Warning or action-required alerts.
   * **Cyan/Blue**: Informational or active tasks.
2. **Spinners & Progress Bars**: For synchronous long-running operations, display an active spinner or progress indicator in stderr. Ensure the spinner is disabled when stdout is not a TTY (interactive terminal).
3. **Clean Tabular Data**: Format multi-row results into clean ASCII tables with well-aligned headers.

## Step 4: Correct Exit Codes
Exit codes are critical for scripts and CI/CD pipelines. Never exit with `0` if an operation failed:
* **`0`**: Command completed successfully.
* **`1`**: General errors (validation failed, resource not found).
* **`2`**: Incorrect CLI usage (missing arguments, invalid flags).
* **`127` / custom**: Specific application failure states.

## Step 5: Verification (Definition of Done)
1. Write unit tests for business logic detached from the terminal wrapper.
2. Write integration/end-to-end tests that run the compiled binary, pass arguments, and verify:
   * Correct exit codes.
   * Expected patterns in `stdout` and `stderr`.
   * Standard error flows when invalid flags are provided.
