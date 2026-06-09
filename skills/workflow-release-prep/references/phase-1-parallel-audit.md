# Phase 1 — Parallel Audit

**Skills used:** [ship-release](../../ship-release/SKILL.md), [ship-commit-msg](../../ship-commit-msg/SKILL.md), [check-security-review](../../check-security-review/SKILL.md)

Run all three agents **IN PARALLEL**.

## Agent 1 — Changelog builder
- **Skill:** [ship-commit-msg](../../ship-commit-msg/SKILL.md) (for consistent categorization)
- **Task:** Read git log since the last tag. Use Conventional Commits to categorize commits into Features / Fixes / Breaking Changes / Chores.
- **Output:** A draft `CHANGELOG.md` entry.

## Agent 2 — Release health check
- **Skill:** [ship-release](../../ship-release/SKILL.md)
- **Task:** Run tests; check for uncommitted changes; verify no TODO/FIXME/HACK in changed files. 
- **Monorepo Awareness:** Confirm version numbers are consistent across ALL workspace packages (e.g., all `package.json` files in `packages/`, `pyproject.toml`, `Cargo.toml`).
- **Output:** Pass/fail per check with the specific blockers.

## Agent 3 — Dependency audit
- **Skill:** [check-security-review](../../check-security-review/SKILL.md)
- **Task:** Check for outdated dependencies with security advisories using `npm audit`, `cargo audit`, etc.
- **Output:** Dependencies that should be updated before release, ranked by severity. High/Critical advisories are blockers.

→ Proceed to [Phase 2](phase-2-apply-release.md).
