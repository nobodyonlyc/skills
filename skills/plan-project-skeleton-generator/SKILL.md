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

## Step 3: Codebase Generation Strategy

### A. Frontend (FE) Source Code
For frontend components, **do not write boilerplate files manually**. Use standard generator tools in non-interactive/silent modes. Make sure to target the `source/` directory:
* **Vite (React, Vue, Svelte, etc.)**: 
  ```bash
  npx -y create-vite@latest source/<app-name> -- --template <template-name>
  ```
* **Next.js**: 
  ```bash
  npx -y create-next-app@latest source/<app-name> --ts --tailwind --eslint --app --src-dir --import-alias "@/*" --use-npm
  ```
* **Vue CLI / Nuxt**: Use their respective silent/non-interactive CLI flags, targeting `source/`.
* Post-generation cleanup: Keep dependencies clean, verify scripts in `package.json`, and ensure standard build and dev environments are runnable.

### B. Backend Server, Batch Job, CLI Tool, and others
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
