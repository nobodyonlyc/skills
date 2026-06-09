# Example — Release prep for v1.3.0

Input: `/workflow-release-prep v1.3.0`

## Phase 1 — parallel audit
- **Changelog builder ([ship-commit-msg](../../ship-commit-msg/SKILL.md)):** since `v1.2.4` → 6 Features, 4 Fixes, 1 Breaking (auth token format), 3 Chores. Drafts the entry.
- **Release health check ([ship-release](../../ship-release/SKILL.md)):** tests PASS, working tree clean, but 🔴 `package.json` says `1.2.4` while `Cargo.toml` says `1.3.0` → version mismatch blocker.
- **Dependency audit ([check-security-review](../../check-security-review/SKILL.md)):** 🟡 `axios` has a moderate advisory; safe to bump patch.

## Phase 2 — approve & apply
- Present all three reports. Resolve the version mismatch (align both to `1.3.0`) and bump `axios`.
- User approves changelog + `v1.3.0`.
- Apply ([ship-release](../../ship-release/SKILL.md)): bump versions, write `CHANGELOG.md`, commit (`chore(release): v1.3.0`), tag `v1.3.0`.
- Staging validation ([ship-deploy](../../ship-deploy/SKILL.md)) → green.
- Agent asks before pushing the tag. ✋
