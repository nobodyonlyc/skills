# Phase 2 — Approve & Apply

**Skills used:** [ship-release](../../ship-release/SKILL.md), [ship-commit-msg](../../ship-commit-msg/SKILL.md), [ship-deploy](../../ship-deploy/SKILL.md)

Prerequisite: audit results from [Phase 1](phase-1-parallel-audit.md).

## Steps
1. **Present** the changelog draft, health-check results, and dependency audit.
2. **Resolve blockers** — failing tests, version mismatches, critical dependency advisories. Do not proceed past an unresolved blocker.
3. **Get user approval** on the changelog and the version number.
4. **Apply** via [ship-release](../../ship-release/SKILL.md): bump the version, write `CHANGELOG.md`, commit (message via [ship-commit-msg](../../ship-commit-msg/SKILL.md)), and tag.
5. **Validate on staging** via [ship-deploy](../../ship-deploy/SKILL.md) before any production push.

## Hard gate
**Ask before pushing** the commit and tag to the remote.
