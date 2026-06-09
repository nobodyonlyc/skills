# Phase 2 — Approve & Apply

**Skills used:** [ship-release](../../ship-release/SKILL.md), [ship-deploy](../../ship-deploy/SKILL.md)

Prerequisite: audit results from [Phase 1](phase-1-parallel-audit.md).

## 1. Present & Resolve Blockers
Present the changelog draft, health-check results, and dependency audit.
Do not proceed past an unresolved blocker:
- **Failing Tests**: Must be fixed (route to `workflow-bugfix`).
- **Version Mismatches**: Must be aligned across the monorepo.
- **Critical Advisories**: Must update the dependency or explicitly suppress the warning with justification.

## 2. Get User Approval
Get explicit user approval on the changelog and the calculated semantic version number (Major/Minor/Patch).

## 3. Apply via ship-release
Use [ship-release](../../ship-release/SKILL.md) to:
- Bump the version in config files.
- Write `CHANGELOG.md`.
- Commit and tag.
- **Ask before pushing** the commit and tag to the remote.

## 4. Validate on Staging
Use [ship-deploy](../../ship-deploy/SKILL.md) to deploy the newly tagged code to the staging environment.
- Run smoke tests or health checks.
- If staging validation fails, use the `rollback-runbook.md` from `ship-deploy`, delete the Git tag locally/remotely, and notify the user.

## 5. Announce
If staging passes, prepare an announcement message summarizing the release notes for stakeholders.
