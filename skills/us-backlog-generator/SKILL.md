---
name: us-backlog-generator
description: Reads the architecture document and parses the roadmap into a backlog of User Stories inside .harness/features.json.
---

Generate backlog for: $ARGUMENTS

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

## Step 3: Populate the Backlog
Use the `./harness add` CLI command to register each feature:
```bash
./harness add <id> <title> --priority <p> --area <a> --behavior <b> --verifications <cmds...>
```
Ensure all verification commands are valid shell commands that can run in non-interactive environments.

## Step 4: Verification (Definition of Done)
1. Run `./harness status` to confirm all features are added correctly and sorted by priority.
2. Confirm `.harness/features.json` is updated and synced.
