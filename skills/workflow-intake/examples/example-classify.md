# Example — classifying three prompts

## A. "build me a team task tracker with auth and a REST API"
- Signals: greenfield ask, no backlog → **Case 1 (New project)**.
- Confirm with user → approved.
- Dispatch: Route 1 → drives [workflow-bootstrap](../../workflow-bootstrap/SKILL.md) (interview → BA → per-component SPEC → US backlog → common design).

## B. "implement F12"
- Signals: names a backlog US id; `.harness/features.json` has F12 → **Case 2 (Execute a US)**.
- Confirm → approved.
- Dispatch: Route 2 → analyse F12, split into `F12-T1…Tn` ([task-convention](../../../resources/task-convention.md)), send each to [workflow-feature](../../workflow-feature/SKILL.md) (or [workflow-bugfix](../../workflow-bugfix/SKILL.md) if it's a defect).

## C. "add harness to my old PHP site that has no AI tooling"
- Signals: onboarding the harness onto a non-harness legacy repo → **Case 4 (Legacy integration)**.
- Dispatch: Route 4 → tell the user legacy integration is not yet supported, then stop. No changes made.

## D (ambiguous). "add CSV export to the tasks page" on an existing harness repo
- Existing harness repo + new capability not in the backlog → **Case 3 (Add feature)**.
- If it were already a backlog US, it would be **Case 2** instead — when unsure, present both and let the user pick.
