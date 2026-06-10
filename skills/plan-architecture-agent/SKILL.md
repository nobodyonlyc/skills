---
name: plan-architecture-agent
description: Analyzes project requirements, identifies user persona and project size, prompts for clarifications, and outputs docs/SYSTEM_ARCHITECTURE.md.
---

> **[Persona Directive]** You must execute this skill acting in the role of a **Senior System Architect**. Adopt their exact mindset, priorities, and vocabulary. Do NOT spawn a subagent for this.


Analyze architecture requirements for: $ARGUMENTS

> Orchestrated by [workflow-bootstrap](../workflow-bootstrap/SKILL.md) (Phase 1). Its output `docs/SYSTEM_ARCHITECTURE.md` is the required input for [plan-us-backlog-generator](../plan-us-backlog-generator/SKILL.md) and [plan-project-skeleton-generator](../plan-project-skeleton-generator/SKILL.md).

Follow these guidelines to interview the user, analyze their system requirements, and generate a cohesive `docs/SYSTEM_ARCHITECTURE.md`.

## Step 1: Initial Persona and Project Size Assessment
Before asking technical questions, evaluate the user's prompt or conduct a quick check to classify:
1. **Project Size**:
   * **Small**: Simple script, single-purpose CLI, landing page, basic CRUD app.
   * **Medium**: Multi-component web application, simple batch pipeline, service integration.
   * **Large / Enterprise**: Multi-service systems, high throughput data pipeline, complex business logic domains.
2. **User Persona**:
   * **Developer (Dev)**: Uses technical terms, specifies tech stack preferences, shows programming experience.
   * **Non-Technical (Non-Tech)**: Focuses on business goals, features, and user behavior without mentioning coding languages or database details.

Use the **ask-user** capability (see [agent-tool-mapping](../../resources/agent-tool-mapping.md); `AskUserQuestion` in Claude Code) if the persona or project scope is ambiguous.

## Step 2: Conduct the Contextual Interview

Based on the detected persona, adapt your questioning strategy:

### Case A: The User is a Developer (Dev)
You must conduct a thorough, precise technical interview using the **ask-user** capability (multi-choice prompts or clear text fields) to cover:
1. **Programming Languages & Frameworks**: e.g., TypeScript/Next.js vs. Rust/Axum vs. Python/FastAPI.
2. **Software Architecture Pattern**: e.g., MVC, DDD (Domain-Driven Design), Clean Architecture, Event-Driven, Serverless.
3. **Database & Persistence**: e.g., PostgreSQL, MongoDB, Redis, SQLite, migration tools, ORM choices (Prisma, Diesel, SQLAlchemy).
4. **Deployment & Hosting Environment**: e.g., Docker, Kubernetes, AWS, GCP, Vercel, VPS, Serverless.
5. **System Integrations & Protocols**: REST, GraphQL, gRPC, WebSockets, Message Queues (RabbitMQ, Kafka).
6. **CI/CD & Testing**: GitHub Actions, GitLab CI, unit/integration test frameworks.

*Do not guess these parameters. Ask for explicit developer choices to ensure the skeleton is built correctly.*

### Case B: The User is Non-Technical (Non-Tech)
Do not overwhelm the user with database models or deployment pipelines. Instead, use the **4 Advanced BA Methodologies** to ensure deep, actionable requirements:

1. **3-Level Drill-Down**: 
   - *Level 1 (Epic)*: What are the high-level modules?
   - *Level 2 (User Journey)*: What is the step-by-step flow for core features?
   - *Level 3 (Data & Edge Cases)*: What specific data fields are required? What happens in edge cases?
2. **RBAC Matrix**: You MUST ask the user to define roles (e.g., Admin, User, Guest) and establish a clear Role-Based Access Control matrix for actions.
3. **Devil's Advocate**: Do not just accept basic features. Proactively invent 2-3 difficult "edge cases" (e.g., network failure, concurrent edits, user abuse) and ask the user how the system should handle them.
4. **Schema-Driven Prompting**: Before you are allowed to write `SYSTEM_ARCHITECTURE.md`, you must have gathered enough information from the user to fully detail:
   - Entities (All required data fields)
   - User Roles & Permissions
   - Business Rules (Conditional branching logic)
   - External Integrations

*Rule: Do NOT generate the final `SYSTEM_ARCHITECTURE.md` until you have iteratively interviewed the user using the above methods to get a complete, deep understanding.*

## Step 3: Document the System Context & Architecture
First, generate the structured context JSON. Then, write the detailed architecture markdown.

### 3A. Generate Project Context (`.harness/context.json`)
Read the [Context JSON Schema](references/context-schema.md) and create the `.harness/context.json` file. Create the `.harness` directory if it doesn't exist. This provides a machine-readable summary for other agents.

### 3B. Document the Architecture (`docs/SYSTEM_ARCHITECTURE.md`)
Output a comprehensive `docs/SYSTEM_ARCHITECTURE.md` file containing:
1. **System Overview**: High-level summary of the system and its goals.
2. **Persona & Project Scale**: Summary of project size and user target.
3. **Component Breakdown**: Visual diagram (Mermaid) and description of each component.
4. **Tech Stack & Rationale**: Detail the selected languages, databases, and hosting choices with justification (especially for non-tech users).
5. **Architecture Design**: Detail how the code is structured (DDD layers, MVC components, Pipeline blocks) based on the choices in Step 2.
6. **Data Models**: Essential database entities, fields, and relationships.
7. **Infrastructure & Deployment**: Deployment steps, container configurations (Dockerfile/docker-compose), and environment variables list.
