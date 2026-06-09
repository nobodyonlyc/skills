# Phase 1 — Parallel Audit

**Skills used:** [ship-release](../../ship-release/SKILL.md), [ship-commit-msg](../../ship-commit-msg/SKILL.md), [check-security-review](../../check-security-review/SKILL.md)

Run all three agents **IN PARALLEL**.

## Agent 1 — Changelog builder
- **Skill:** [ship-commit-msg](../../ship-commit-msg/SKILL.md) (for consistent categorization)
- **Task:** Read git log since the last tag; categorize commits into Features / Fixes / Breaking Changes / Chores.
- **Output:** a draft CHANGELOG entry.

## Agent 2 — Release health check
- **Skill:** [ship-release](../../ship-release/SKILL.md)
- **Task:** Run tests; check for uncommitted changes; verify no TODO/FIXME/HACK in changed files; confirm version numbers are consistent across all config files (`package.json`, `pyproject.toml`, `Cargo.toml`, etc.).
- **Output:** pass/fail per check with the specific blockers.

## Agent 3 — Dependency audit
- **Skill:** [check-security-review](../../check-security-review/SKILL.md)
- **Task:** Check for outdated dependencies with security advisories.
- **Output:** dependencies that should be updated before release, ranked by severity.

→ Proceed to [Phase 2](phase-2-apply-release.md).
