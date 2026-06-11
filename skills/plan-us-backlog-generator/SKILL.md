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

## Step 2: Formulate User Stories (Features)
For each identified feature or bootstrapping task, formulate a structured feature payload containing:
1. **ID**: Sequential identifier starting from the next available ID (e.g., if F01-F06 exist, start with `F07`, `F08`, etc.).
2. **Title**: Short, descriptive name (e.g., "User Registration Endpoint", "Dashboard UI Layout").
3. **Priority**: Numeric order of execution (lower numbers run first).
4. **Area**: Category of work (e.g., `core`, `db`, `api`, `ui`, `batch`, `security`).
5. **User Visible Behavior**: Detailed description of what behavior will be observed when the task is complete.
6. **Verifications**: A list of executable shell commands that will prove the task works out of the box (e.g., `cargo test`, `pytest tests/test_auth.py`, `[ -f src/auth.rs ]`).

## Step 2.5: Coverage check (mandatory — before showing the user)
Verify the drafted backlog **covers every item in the Step 1 inventory**. Build a coverage table: each SPEC item → the US that covers it. Any item with **no US is a gap** — add the missing User Story before proceeding.

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
