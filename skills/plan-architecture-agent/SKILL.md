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

Ask the user to confirm these via the **ask-user** capability — and **present them as click-select options, never free-text prompts** (per the [ask-user click-select rule](../../resources/agent-tool-mapping.md#ask-user-prefer-click-select-options-all-three-agents)). In Claude Code, one `AskUserQuestion` call with these as separate questions, each with an `options` array:
- **Your role** → options: `Developer / Technical` (you pick the stack) · `Non-technical` (propose the optimal solution for me).
- **Project size** → options: `Small` (CLI / simple local app) · `Medium` (full web app FE+BE) · `Large / Enterprise` (multi-service).
- **Application type** → options: `Web Application` · `CLI Tool` · `API / Backend service` · `Batch / Data pipeline`.

Do not assume; do not make the user type these out. The runtime always lets them type a custom answer past the options if none fit.

## Step 2: Conduct the Contextual Interview

Based on the explicitly confirmed persona and project size, adapt your strategy:

### Case A: The User is Non-Technical (Non-Tech)
Since the user is non-technical, do not overwhelm them with deep technical or BA questions. Instead:
1. **Auto-Propose**: Spawn a subagent to automatically propose a detailed SPEC and Business Analysis (BA) tailored to the project size and their initial idea.
2. **PM Review**: Once the subagent generates the proposal, spawn the Senior PM Evaluator subagent (via `check-ba-evaluator`) to critically review and refine the proposed SPEC and BA.
3. **Confirm**: Present the finalized, PM-approved SPEC/BA to the non-tech user for a simple confirmation.

### Case B: The User is Technical (Dev / Tech)
If the user is technical, they often know the tech stack but may overlook business edge cases. You must temporarily shift your persona to a **Strict Business Analyst (BA)** and grill them deeply on the SPEC and BA of the project before accepting technical choices.

**Part 1: The BA Grill (MANDATORY)**
Use the **4 Advanced BA Methodologies**:
1. **3-Level Drill-Down**: 
   - *Level 1 (Epic)*: What are the high-level modules?
   - *Level 2 (User Journey)*: What is the step-by-step flow for core features?
   - *Level 3 (Data & Edge Cases)*: What specific data fields are required? What happens in edge cases?
2. **RBAC Matrix**: You MUST ask the user to define roles (e.g., Admin, User, Guest) and establish a clear Role-Based Access Control matrix for actions.
3. **Devil's Advocate**: Proactively invent 2-3 difficult "edge cases" (e.g., network failure, concurrent edits, user abuse) and ask the user how the system should handle them.
4. **Schema-Driven Prompting**: Ensure you have gathered enough information to detail Entities, User Roles, Business Rules, and External Integrations.

**Part 2: Technical Choices**
After the BA is solid, ask for explicit developer choices. **Present each as click-select options** (a few common choices relevant to the app type) plus the implicit free-text escape for a custom answer — do not make the user type from scratch:
1. **Programming Language & Framework**: e.g. `TypeScript / Next.js` · `Node.js / NestJS` · `Python / FastAPI` · `Go` · `Rust / Axum`.
2. **Software Architecture Pattern**: e.g. `MVC` · `DDD / Clean Architecture` · `Layered` · `Hexagonal`.
3. **Database & Persistence**: e.g. `PostgreSQL` · `MySQL` · `MongoDB` · `SQLite` · `Redis (cache)`.
4. **Deployment & Hosting**: e.g. `Docker / docker-compose` · `Vercel` · `AWS` · `Local only`.

Tailor the offered options to the chosen app type and project size; offer 3–4 sensible defaults per question, never an open prompt with no options.

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
