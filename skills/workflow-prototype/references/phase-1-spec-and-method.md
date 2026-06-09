# Phase 1 — FE SPEC & method

Goal: know exactly **what** to mock (every screen + function) and **how** (which method).

## 1. Read the FE SPEC
Read the frontend SPEC at `docs/spec/frontend.md` (produced by the intake router's Route 1). If it does not exist, ask the user for the screens and behaviours, or draft a short screen list and confirm it before proceeding.

## 2. Enumerate full coverage
From the SPEC, build a **coverage checklist** — list **every screen** and, under each, **every function/interaction** the SPEC requires (e.g. Login: email/password fields, validation states, "forgot password" link; Board: columns, cards, drag, filter, empty state). The mock is not done until every item is rendered. Reuse existing design tokens/components via [core-explain](../../core-explain/SKILL.md) if the repo already has a frontend.

## 3. Pick the method (ask-user)
Confirm with the user which method to use ([agent-tool-mapping](../../../resources/agent-tool-mapping.md) for the ask-user capability):
- **A. HTML/CSS** — self-contained static files, served locally and viewed in the browser. Default; no external tools needed.
- **B. Figma via MCP** — build frames in Figma through an available Figma MCP connector (discover it via your MCP connectors/registry). Use when the user wants an editable design file.

## Output (gate to Phase 2)
- The coverage checklist (screens × functions).
- The chosen method.

→ Proceed to [Phase 2](phase-2-generate-mock.md).
