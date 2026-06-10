# Phase 0 — Classify & confirm

Decide which of the 4 cases the incoming prompt is, then confirm with the user before dispatching.

## Signals per case

### Case 1 — New project
- The working directory is empty / greenfield, or has no `.harness/features.json` backlog.
- The prompt describes a product to build from scratch ("build me a …", "I want an app that …").
- → Route 1 (new-project intake).

### Case 2 — Execute a US
- The prompt names a backlog item (`F12`, "the login story") **and** `.harness/features.json` already exists with that US.
- The prompt is "continue", "do the next feature", "implement F12".
- → Route 2 (US execution + task decomposition).

### Case 3 — Add a feature to an existing harness project
- The repo already uses the harness (`.harness/`, `AGENTS.md`, `./harness`) **and** the prompt asks for a *new* capability not yet in the backlog.
- → Route 3 (read source → BA → SPEC → add US → Route 2).

### Case 4 — Legacy onboarding
- The prompt asks to *add the harness itself* to an existing, active project that does **not** yet use harness tooling.
- → Route 4: dispatch [workflow-onboard](../../workflow-onboard/SKILL.md) (survey → docs → safe init → seed backlog).

## Disambiguation
- Existing harness repo + known US id → **Case 2**. Existing harness repo + brand-new capability → **Case 3**.
- Empty repo → **Case 1**. Non-harness repo asking to onboard harness → **Case 4**.
- When two cases are plausible, present both to the user and let them pick.

## Confirm (hard gate)
Present the chosen case and the route it dispatches to via the **ask-user** capability ([agent-tool-mapping](../../../resources/agent-tool-mapping.md)). Do **not** dispatch until the user confirms. On correction, re-classify and re-confirm.
