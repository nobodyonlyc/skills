---
name: plan-us-backlog-generator
description: Reads the architecture document and parses the roadmap into a backlog of User Stories inside .harness/features.json.
---

Generate backlog for: $ARGUMENTS

> Orchestrated by [workflow-bootstrap](../workflow-bootstrap/SKILL.md) (Phase 2). Requires `docs/SYSTEM_ARCHITECTURE.md` from [plan-architecture-agent](../plan-architecture-agent/SKILL.md) — does not run independently.

Follow these guidelines to read a system architecture specification and populate the Harness feature backlog.

## Step 1: Read the System Architecture
Open and read the system design document (e.g., `docs/SYSTEM_ARCHITECTURE.md`). Identify:
1. **Core Components**: Web server, UI frontend, DB schema, background workers.
2. **Setup Dependencies**: Which components need to be bootstrapped first (typically Database -> Backend API -> Frontend UI).
3. **Key Features**: List the core business functions (e.g., user login, product catalog, checkout, email dispatch).

## Step 2: Formulate User Stories (Features)
For each identified feature or bootstrapping task, formulate a structured feature payload containing:
1. **ID**: Sequential identifier starting from the next available ID (e.g., if F01-F06 exist, start with `F07`, `F08`, etc.).
2. **Title**: Short, descriptive name (e.g., "User Registration Endpoint", "Dashboard UI Layout").
3. **Priority**: Numeric order of execution (lower numbers run first).
4. **Area**: Category of work (e.g., `core`, `db`, `api`, `ui`, `batch`, `security`).
5. **User Visible Behavior**: Detailed description of what behavior will be observed when the task is complete.
6. **Verifications**: A list of executable shell commands that will prove the task works out of the box (e.g., `cargo test`, `pytest tests/test_auth.py`, `[ -f src/auth.rs ]`).

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
