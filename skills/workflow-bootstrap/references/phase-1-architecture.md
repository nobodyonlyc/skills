# Phase 1 — Requirements Analysis & Tech Discovery

**Skill used:** [plan-architecture-agent](../../plan-architecture-agent/SKILL.md)

## Objective
Evaluate project size and user persona (Dev vs. Non-Tech), then capture the decisions in a single architecture document.

## Steps
1. Invoke the [plan-architecture-agent](../../plan-architecture-agent/SKILL.md) skill to run the contextual interview:
   - **Dev persona** → deep technical questions (language, framework, data store, hosting, scaling, auth).
   - **Non-Tech persona** → friendly, suggestion-driven prompts; offer sensible defaults.
2. Determine languages, databases, hosting, and the overall architecture style (monolith / services / serverless).
3. Resolve open questions with the user before writing anything.

## Output (gate to Phase 2)
- `docs/SYSTEM_ARCHITECTURE.md` exists and contains: tech stack, data model overview, component diagram or list, and a rough roadmap.
- Do not advance to Phase 2 until this file is written and the user has acknowledged it.
