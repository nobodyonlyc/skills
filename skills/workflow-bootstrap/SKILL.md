---
name: workflow-bootstrap
description: Coordinates the project setup sequence from phoning/interviewing the user, generating the spec/backlog, and building the project skeleton.
---

Bootstrap project using: $ARGUMENTS

This is a multi-agent orchestration workflow to initialize a target project from an idea description to a structured codebase.

## Execution Sequence

### Step 1: Requirements Analysis & Tech Discovery
Execute the [architecture-agent](file:///home/zrik/workspace/projs/harness/.agents/skills/architecture-agent/SKILL.md) skill to interview the user.
* **Objective**: Evaluate project size and user persona (Dev vs. Non-Tech).
* **Task**: Perform the contextual interview (deep technical questions for Devs, friendly suggestions for Non-Techs) to determine languages, databases, hosting, and architecture.
* **Output**: Generate `docs/SYSTEM_ARCHITECTURE.md`.

### Step 2: Formulate Backlog (User Stories)
Execute the [us-backlog-generator](file:///home/zrik/workspace/projs/harness/.agents/skills/us-backlog-generator/SKILL.md) skill.
* **Objective**: Translate the generated system architecture spec into actionable developer task backlog stories.
* **Task**: Read `docs/SYSTEM_ARCHITECTURE.md` and parse the system components into structured stories.
* **Output**: Populate the Harness database and write them to `.harness/features.json` using the `./harness add` command.

### Step 3: Scaffold Codebase Skeleton
Execute the [project-skeleton-generator](file:///home/zrik/workspace/projs/harness/.agents/skills/project-skeleton-generator/SKILL.md) skill.
* **Objective**: Automatically create directory structures, configuration files, and baseline tests.
* **Task**: Read `docs/SYSTEM_ARCHITECTURE.md` to identify components and technologies. Apply matching workspace templates (from `project-skeleton-generator/resources/folder_structures.md`).
* **Output**: Generate workspace configuration (e.g. `docker-compose.yml`, `.gitignore`, `.env.example`) and subdirectories for each component.

### Step 4: Verification Gate
Run the environment startup script:
```bash
./init.sh
```
* **Verify**: Confirm that the workspace is fully compiled and all newly generated baseline smoke tests pass out of the box.
* **Handoff**: Execute `./harness status` to print the backlog, leaving the project ready for feature development!
