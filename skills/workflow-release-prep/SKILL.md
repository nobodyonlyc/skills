---
name: workflow-release-prep
description: Orchestrate a multi-agent workflow to prep release notes, update versions, and execute staging validation.
---

Release preparation workflow. Target version: $ARGUMENTS

Multi-agent release prep: build the changelog, run a health check, and audit dependencies in parallel, then apply the release once the user approves. 

## Skills this workflow drives
- [ship-release](../ship-release/SKILL.md) — the release procedure: version bump, notes, pre-release validation.
- [check-security-review](../check-security-review/SKILL.md) — vet dependency advisories flagged in the audit.
- [ship-commit-msg](../ship-commit-msg/SKILL.md) — write the release commit and categorize history.
- [ship-deploy](../ship-deploy/SKILL.md) — staging validation / deploy once tagged.

## Phases
1. **Parallel Audit** → [references/phase-1-parallel-audit.md](references/phase-1-parallel-audit.md)
   Changelog builder + Release health check + Dependency audit run in parallel; surface blockers.
2. **Approve & Apply** → [references/phase-2-apply-release.md](references/phase-2-apply-release.md)
   Resolve blockers, get user approval, bump version, write CHANGELOG, commit, tag, validate on staging, and announce.

## Examples
- **[Release Prep Scenario](examples/release-prep-scenario.md)**: An end-to-end example of resolving a blocker and validating on staging.

## Hard Gates
- All blockers (failing tests, version mismatches, critical dependency advisories) must be resolved before applying.
- Get explicit user approval on the changelog and version number, and **ask before pushing**.
- Staging validation MUST pass before the process is considered fully complete.
