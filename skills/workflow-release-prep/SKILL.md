---
name: workflow-release-prep
description: Orchestrate a multi-agent workflow to prep release notes, update versions, and execute staging validation.
---

Release preparation workflow. Target version: $ARGUMENTS

Run the following agents IN PARALLEL:

**Agent 1 — Changelog builder**: Read git log since last tag, categorize commits into Features / Fixes / Breaking Changes / Chores. Draft CHANGELOG entry.

**Agent 2 — Release health check**: Run tests, check for uncommitted changes, verify no TODO/FIXME/HACK comments in changed files, check that version numbers are consistent across all config files (package.json, pyproject.toml, Cargo.toml, etc.).

**Agent 3 — Dependency audit**: Check for outdated dependencies with security advisories. Report any that should be updated before release.

After all agents complete:

1. Present: changelog draft, health check results, dependency audit.
2. Resolve any blockers (failing tests, version mismatches, critical deps).
3. Get user approval on the changelog and version number.
4. Apply: update version, write CHANGELOG.md, commit, tag.
5. Ask before pushing.
