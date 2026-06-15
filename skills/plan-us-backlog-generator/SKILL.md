---
name: plan-us-backlog-generator
description: Reads the architecture document and parses the roadmap into a backlog of User Stories inside .harness/features.json.
---

> **[Persona Directive]** You must execute this skill acting in the role of a **Product Owner**. Adopt their exact mindset, priorities, and vocabulary. Do NOT spawn a subagent for this.


Generate backlog for: $ARGUMENTS

> Orchestrated by [workflow-bootstrap](../workflow-bootstrap/SKILL.md) (Phase 2). Requires `docs/SYSTEM_ARCHITECTURE.md` from [plan-architecture-agent](../plan-architecture-agent/SKILL.md) — does not run independently.

Follow these guidelines to read a system architecture specification and populate the Harness feature backlog.

## Step 1: Read the architecture AND the detailed SPECs
Read the high-level design (`docs/SYSTEM_ARCHITECTURE.md`) for structure, **and every detailed SPEC** under `docs/spec/` — `frontend.md`, `backend.md`, `database.md`, `cli.md`, and any tool SPEC. The architecture is high-level; the **work items live in the detailed SPECs**. Reading only the architecture is the #1 cause of a backlog that misses User Stories.

Build an explicit **inventory of every work item** the SPECs define — you will check the backlog against it in Step 2.5:
1. **Core Components & dependencies**: bootstrap order (typically Database → Backend API → Frontend UI).
2. **FE** — every **screen** and major interaction in `docs/spec/frontend.md`.
3. **BE** — every **endpoint / service function** in `docs/spec/backend.md`.
4. **DB** — every **entity / migration** in `docs/spec/database.md`.
5. **Business functions** named in the BA / architecture (login, catalog, checkout, email dispatch, …).
6. **Quality & test work** (from the architecture's *Testing & Quality Strategy*): the cross-component **integration tests** (API↔DB, service↔service, FE↔API), the **end-to-end / regression** suites for the critical journeys, and any **performance / security** tests the NFRs require. These are work items in their own right — not folded into a single feature.

## Step 2: Formulate User Stories (Features)
For each identified work item, formulate a structured payload containing:
1. **ID**: Sequential identifier starting from the next available ID (e.g., if F01-F06 exist, start with `F07`, `F08`, etc.).
2. **Title**: Short, descriptive name (e.g., "User Registration Endpoint", "Checkout E2E regression").
3. **Priority**: Numeric order of execution (lower numbers run first).
4. **Area**: Category of work — `core`, `db`, `api`, `ui`, `batch`, `security`, and the quality types **`test`** (IT/E2E/regression/perf), **`qa`**, **`bugfix`**.
5. **User Visible Behavior**: Detailed description of what behavior will be observed when the task is complete.
6. **Verifications**: A list of executable shell commands that **actually exercise the behavior and assert on it** (e.g., `cargo test auth::`, `pytest tests/test_auth.py`, `playwright test checkout`). A bare existence check like `[ -f src/auth.rs ]` is **NOT** acceptance — it proves a file exists, not that it works. Existence checks may only *accompany* real tests, never replace them. Use the **tech stack's real test runner and its own selection syntax** (`cargo test <mod>::`, `go test ./pkg -run X`, `pytest path::node`, jest/vitest/…) and make sure the command **selects the intended tests and is non-vacuous** — a command that matches zero tests but still exits 0 is a false green. (Pitfall: selector flags don't transfer between runners — e.g. `--grep` is mocha/vitest, not jest.)

### The three kinds of story (testing & bugfix are first-class)
1. **Feature US (coding)** — implements behavior. Its `verifications` **MUST include that feature's Unit Tests** (real assertions on logic and edge cases), per the per-US Definition of Done. A feature with no UT is not done.
2. **Test US (`test`/`qa`)** — dedicated stories for the cross-cutting work that no single feature owns: **integration tests** at component seams, **end-to-end / regression** suites for the critical journeys, and **performance / security** tests from the NFRs. Sequence each one **after** the features it validates (its priority is higher-numbered), and verify it by running that suite. Executed via [workflow-qa](../workflow-qa/SKILL.md). A Test/QA US is only `passing` when its suite is **green** — so it runs a **loop**: any failure spawns a bugfix story (kind 3), gets fixed, then the suite is **re-run**, repeating until green.
3. **Bugfix US (`bugfix`)** — a first-class story type for a defect. Bugs are mostly **surfaced reactively** (a Test/QA US fails, `./harness verify` fails, or the user reports one) and added to the backlog as they appear; seed any *known* defects up front. Each bugfix US is executed via [workflow-bugfix](../workflow-bugfix/SKILL.md) as a **loop**: reproduce → write a **regression test that fails before the fix** → apply the minimal fix → the same test **passes after** → re-run the broader suite to confirm no new regressions, repeating if it surfaced more. Its `verifications` are that regression test.

> **Sequencing & loop:** UT ride with their feature (inner code·test·fix loop); IT/regression/E2E come **after** the feature group they cover and run an outer **test → fix → re-test loop until green**; a final regression/QA pass guards each milestone before release. Bugfix US slot in at the priority their severity demands.

## Step 2.5: Coverage check (mandatory — before showing the user)
Verify the drafted backlog **covers every item in the Step 1 inventory**. Build a coverage table: each SPEC item → the US that covers it. Any item with **no US is a gap** — add the missing User Story before proceeding. The coverage check explicitly includes **quality work**:
- **Every feature US lists real Unit Tests** in its verifications (not just existence checks). A feature US with no UT is a gap.
- **Every cross-component seam, critical journey, and NFR** from the Testing & Quality Strategy maps to a `test`/`qa` US. A seam/journey with no test US is a gap.
- At least one **regression / QA pass** guards the release (or each milestone).

Then run an **independent PM coverage review**: spawn a subagent via [check-ba-evaluator](../check-ba-evaluator/SKILL.md) in **backlog-coverage mode** — a Senior PM who reads the SPECs and the drafted backlog and reports any SPEC item (screen / endpoint / entity / business rule) that no US covers. The review returns the **full gap list in one report**: add **all** the missing User Stories in a single pass, then re-run the coverage review **at most once** to confirm. Do not add one story and re-spawn per gap — that cold-starts the reviewer repeatedly. Only a backlog that passes coverage goes to Step 3.

## Step 3: Present and Confirm Backlog with the User
Before registering any features, you MUST present the complete proposed backlog to the user for confirmation:
1. Format the proposed backlog as a clear Markdown table detailing the ID, Title, Area, Behavior, and Verification commands.
2. Clearly explain the dependency order and development sequence of these stories.
3. Explicitly ask the user for feedback or approval before proceeding.
4. **DO NOT** run the `./harness add` command or write to the database until the user has explicitly confirmed the backlog.

## Step 4: Populate the Backlog (Only After Confirmation)
Once the user approves the backlog, use the `./harness add` CLI command to register each feature:
```bash
./harness add <id> <title> --priority <p> --area <a> --behavior <b> --verifications <cmds...>
```
Ensure all verification commands are valid shell commands that can run in non-interactive environments.

## Step 5: Verification (Definition of Done)
1. Run `./harness status` to confirm all features are added correctly and sorted by priority.
2. Confirm `.harness/features.json` is updated and synced.
