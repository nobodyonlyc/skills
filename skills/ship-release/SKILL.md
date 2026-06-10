---
name: ship-release
description: Prepare a release, draft release notes, bump versions, and run pre-release validation checks.
---

Prepare a release. Version bump type: $ARGUMENTS (major / minor / patch — defaults to patch)

> This is the single-agent release path. For a multi-agent release workflow (parallel changelog + health check + dependency audit), use [workflow-release-prep](../workflow-release-prep/SKILL.md). That workflow drives this skill.

Gather context:
```bash
git log --oneline $(git describe --tags --abbrev=0 2>/dev/null || echo "")..HEAD 2>/dev/null || git log --oneline -20
git tag --sort=-version:refname | head -5
cat package.json 2>/dev/null | grep '"version"' || cat pyproject.toml 2>/dev/null | grep 'version' || cat Cargo.toml 2>/dev/null | grep 'version'
```

## References
Please follow the guidelines in these references carefully:
- **[SemVer Guide](references/semver-guide.md)**: Rules for bumping Major, Minor, or Patch versions.
- **[Changelog Format](references/changelog-format.md)**: How to convert git logs into structured release notes.
- **[Branching Strategy](references/branching-strategy.md)**: Release vs. Hotfix branch logic.

## Examples
- **[Release Notes Example](examples/release-notes-example.md)**: Sample output of generated release notes.

## Release Workflow

1. **Calculate Version**: Use `references/semver-guide.md` to analyze the commits since the last tag. Determine the appropriate bump (major/minor/patch). Propose the new version to the user.
2. **Determine Branching Strategy**: Review `references/branching-strategy.md`. If this is a hotfix or minor release, check if a dedicated release branch needs to be created or if we are tagging directly on main.
3. **Generate Changelog**: Parse the commits using `references/changelog-format.md`. Draft the new entry for `CHANGELOG.md`.
4. **Update Version**: Do NOT edit version strings manually in files using text generation. You MUST use the native package manager command to bump the version safely:
   * **Node.js**: `npm version <major|minor|patch> --no-git-tag-version`
   * **Rust**: `cargo set-version <new_version>` (requires `cargo-edit`)
   * **Python**: `bump2version <bump>` or `poetry version <bump>`
   * After running the version command, verify the config file was updated. Then, manually append the drafted release notes to `CHANGELOG.md`.
5. **Commit & Tag**:
   ```bash
   git add package.json CHANGELOG.md
   git commit -m "chore: release v<new-version>"
   git tag -a v<new-version> -m "Release v<new-version>"
   ```
6. **Push**: Ask for explicit confirmation before pushing:
   ```bash
   git push origin <branch> --tags
   ```

Stop before each irreversible step (Commit, Tag, Push) and confirm with the user.
