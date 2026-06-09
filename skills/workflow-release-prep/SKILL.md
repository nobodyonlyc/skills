---
name: workflow-release-prep
description: Orchestrate a multi-agent workflow to prep release notes, update versions, and execute staging validation.
---

Release preparation workflow. Target version: $ARGUMENTS

Multi-agent release prep: build the changelog, run a health check, and audit dependencies in parallel, then apply the release once the user approves. Each phase has a detailed playbook in [`references/`](references/); see [`examples/`](examples/) for a full worked run.

## Skills this workflow drives
- [ship-release](../ship-release/SKILL.md) — the release procedure: version bump, notes, pre-release validation (Phase 1 & 2).
- [check-security-review](../check-security-review/SKILL.md) — vet dependency advisories flagged in the audit (Phase 1).
- [ship-commit-msg](../ship-commit-msg/SKILL.md) — write the release commit and categorize history (Phase 1 & 2).
- [ship-deploy](../ship-deploy/SKILL.md) — staging validation / deploy once tagged (Phase 2).

## Phases
1. **Parallel Audit** → [references/phase-1-parallel-audit.md](references/phase-1-parallel-audit.md)
   Changelog builder + Release health check + Dependency audit run in parallel; surface blockers.
2. **Approve & Apply** → [references/phase-2-apply-release.md](references/phase-2-apply-release.md)
   Resolve blockers, get user approval, bump version, write CHANGELOG, commit, tag, and validate on staging.

## Hard gates
- All blockers (failing tests, version mismatches, critical dependency advisories) must be resolved before applying.
- Get explicit user approval on the changelog and version number, and **ask before pushing**.
