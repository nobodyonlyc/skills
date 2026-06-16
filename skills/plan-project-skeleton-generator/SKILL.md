---
name: plan-project-skeleton-generator
description: Automatically creates standard project structures (folders, configuration files) and initial baseline tests based on the architecture specification.
---

> **[Persona Directive]** You must execute this skill acting in the role of a **DevOps Engineer**. Adopt their exact mindset, priorities, and vocabulary. Do NOT spawn a subagent for this.


Generate project skeleton for: $ARGUMENTS

> Orchestrated by [workflow-bootstrap](../workflow-bootstrap/SKILL.md) (Phase 2). Requires `docs/SYSTEM_ARCHITECTURE.md` from [plan-architecture-agent](../plan-architecture-agent/SKILL.md); consults [dev-db-designer](../dev-db-designer/SKILL.md) for schema — does not run independently.

Follow these step-by-step instructions to read the system architecture design and generate the appropriate workspace and code structure.

## Step 1: Read Architecture Specification
Before generating any files, read the system design document (typically `docs/SYSTEM_ARCHITECTURE.md` or a specification document provided in the argument).
Analyze the system components to identify:
1. **Component Types**: Frontend (FE), Backend Server (API/Web), Batch Jobs, CLI Tools, Daemon/Workers.
2. **Tech Stack**: Language, Framework, and Database of choice for each component.
3. **Directory Layout**: Workspace structure (e.g., mono-repo vs. multi-repo layout).

## Step 2: Establish the Directory Layout
1. **Repository Root (`/`)**: This environment is strictly for AI Agent control. Do NOT generate application code here. However, you MUST initialize the standard Harness documentation structure at the repository root:
   - `docs/design-docs/`: For Architectural Decision Records (ADRs).
   - `docs/product-specs/`: For business requirements.
   - `docs/DOMAIN_GLOSSARY.md`: The ubiquitous language dictionary.
   - `docs/SYSTEM_MAP.md`: High-level architecture map and domain boundaries.
2. **Application Root (`/source/`)**: Create a dedicated `source/` wrapper directory. All application source code, workspaces, frameworks, and related configs MUST be generated inside this `source/` directory. For example, a monorepo will have `source/apps/` and `source/packages/`.
3. Initialize global application configurations inside `source/` (e.g., `source/.gitignore`, `source/.env.example`, `source/README.md`).
4. **Project structure diagram (MANDATORY GATE — confirm before creating any file or folder)**: Output the full proposed directory tree and present it via ask-user. Do NOT create any file, run any scaffold tool, or write any code until the user approves the structure. This is the earliest and cheapest point to catch structural mistakes — wrong choices here propagate into every User Story.

   Example format:
   ```
   /                          ← harness root (no app code here)
     docs/
       SYSTEM_ARCHITECTURE.md
       BA.md
       spec/
         frontend.md
         backend.md
         database.md
     source/                  ← all application code lives here
       apps/
         web/                 ← Next.js (React)
           src/
             components/
               atoms/         ← Button, Input, Badge
               molecules/     ← FormField, CardHeader
               organisms/     ← NavBar, DataTable
               templates/     ← DashboardLayout
               pages/         ← route containers
             hooks/
             utils/
             types/
         api/                 ← Node.js / Express
           src/
             common/
               dto/
               errors/
               utils/
             base/
               base.repository.ts
               base.service.ts
             modules/
               [feature]/
       packages/
         shared-types/        ← types shared across apps
   ```
   Annotate each major folder with its responsibility. For FE components, show the `atoms/molecules/organisms` tiers. For BE, show the `common/base/modules` tiers. For any folder that does not map to the convention, explain why.

## Step 3: Codebase Generation & Dependency Strategy

> **CRITICAL DEPENDENCY RULE**: Whenever initializing a project or adding libraries (e.g., in `package.json`, `Cargo.toml`, `requirements.txt`, `go.mod`), you MUST specify explicit and exact versions.
> - **Prioritize LTS (Long-Term Support) or the latest Stable versions**.
> - Do NOT use `latest`, `*`, or floating version ranges (e.g., `^1.0.0` or `~1.0`) that could cause unpredictable builds in the future.
### A. Intelligent Scaffolding (All Frameworks)
Do not write boilerplate files manually. You must **evaluate the tech stack** and choose the official, community-standard scaffolding tool (e.g., `npx create-next-app`, `npx create-vite`, `cargo new`, `django-admin startproject`, `spring init`).
* Run the chosen generator tool in non-interactive/silent mode, targeting the `source/` directory.
* Post-generation cleanup: Verify scripts in `package.json`/`Cargo.toml` and ensure standard build and dev environments are runnable.

### B. Enterprise & Complex App Architecture
If the application requires complex domain logic, you must **not** just rely on the default scaffold tool's flat structure.
* You MUST overlay the chosen design pattern on top of the generated framework. Consult `resources/folder_structures.md` for the correct layout.
* Ensure folders like `domain/`, `application/`, `infrastructure/`, and `presentation/` (for DDD) or `models/`, `views/`, `controllers/` (for MVC) are explicitly created and structured properly.
* **Pre-create the reuse tiers from the start** — do not wait until duplication appears to add them:
  - **FE**: create `components/atoms/`, `components/molecules/`, `components/organisms/`, `components/templates/`, `components/pages/`, `hooks/`, `utils/`, `types/` (see [`typescript-react.md`](../../resources/conventions/typescript-react.md) §4).
  - **BE (Node/TS)**: create `common/dto/`, `common/errors/`, `common/utils/`, `base/` with `base.repository.ts` and `base.service.ts` stubs (see [`typescript-node.md`](../../resources/conventions/typescript-node.md) §4).
  - These folders must exist (even as empty dirs with a `.gitkeep`) so agents writing the first US know the structure and place code in the right tier from the beginning.

### C. Architecture Specific Guidelines
Select and apply the appropriate design pattern/architecture based on the component type and complexity:

1. **Backend Server / API Server**:
   * **Domain-Driven Design (DDD) / Clean Architecture** (Recommended for complex enterprise domains):
     * `domain/`: Entities, aggregates, value objects, domain events, repository interfaces.
     * `application/`: Use cases, CQRS commands/queries, application services, DTOs.
     * `infrastructure/`: Database adapters (ORM implementation, SQL files), external APIs, message broker adapters, configuration.
     * `interface/` or `presentation/`: Controllers, GraphQL resolvers, REST routes, middlewares.
   * **MVC (Model-View-Controller)** (For CRUD-focused or smaller web servers):
     * `models/`: Database schemas, data access logic.
     * `views/`: Templates or serialization layer (JSON responders).
     * `controllers/`: Request handling, validation, orchestrating model interactions.

2. **Batch Job / Data Processor**:
   * Use a **Pipeline (Reader-Processor-Writer)** or **Layered** architecture:
     * `reader/` or `input/`: Adapters for fetching data (SQL queries, CSV parsers, queue listeners).
     * `processor/` or `core/`: Business logic, validation, data transformation.
     * `writer/` or `output/`: Adapters for persistence (database upserts, file output, API requests).
     * `config/` or `scheduler/`: Task scheduling, retry mechanism, and error-handling setups.

3. **CLI Tool**:
   * Use a **Command Pattern** (Subcommand router):
     * `args/` or `parser/`: Argument definitions, validations, and flags configuration.
     * `commands/`: Individual subcommand execution handlers (e.g., `init.rs`, `status.rs`).
     * `core/`: Shared business logic, database wrappers.
     * `utils/`: Terminal formatting, logs, spinners.

4. **Background Daemon / Worker**:
   * Use an **Event-Driven / Worker Pool** pattern:
     * `job_queue/`: Queue connection, job registration.
     * `handlers/`: Individual worker tasks logic.
     * `telemetry/`: Healthchecks, logging, metrics.

## Step 4: Generate Baseline Tests (Definition of Done)
For every skeleton component generated:
1. Create a basic baseline test (smoke test/health check test) to prove the skeleton works out of the box.
2. The verification script should compile/run the project and execute the tests.
   * **Frontend**: e.g., `npm run test` or `npm run build`
   * **Backend/Rust**: e.g., `cargo test`
   * **Python**: e.g., `pytest`
3. Document how to run and verify the generated skeleton in a component-specific `README.md`.

## Step 5: Generate `run.sh` (run the app to check it live)
Create an executable **`run.sh`** at the repo root that launches the actual app for the chosen stack, so after each US the user can run the project and see the result immediately. It wraps the project's real dev/run command — do not invent one:
- Frontend / Node: `pnpm dev` / `npm run dev`
- Backend: `cargo run`, `uvicorn app:app --reload`, `go run ./cmd/...`, `pnpm start:dev`
- Multi-service: `docker compose up` (or start each service)

```bash
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/source"   # or wherever the app root is
exec <the stack's real run command>   # e.g. pnpm dev
```

Make it `chmod +x`. Keep it thin — one obvious way to start the app. Document the run command in the component README and in `.harness/context.json` if a run field exists. (`init.sh` = sync + verify; `run.sh` = start the app for manual checking — they are different.)
