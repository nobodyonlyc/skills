Prepare a release. Version bump type: $ARGUMENTS (major / minor / patch — defaults to patch)

Gather context:

```bash
git log --oneline $(git describe --tags --abbrev=0)..HEAD 2>/dev/null || git log --oneline -20
git tag --sort=-version:refname | head -5
cat package.json 2>/dev/null | grep '"version"' || cat pyproject.toml 2>/dev/null | grep 'version' || cat Cargo.toml 2>/dev/null | grep 'version'
```

Release workflow:

1. **Changelog** — Group commits since last tag into: `### Features`, `### Fixes`, `### Breaking Changes`. Skip chore/style/test commits.

2. **Version bump** — Calculate new version from current tag + bump type. Show the new version and ask for confirmation.

3. **Apply** — Update version in package.json / pyproject.toml / Cargo.toml (whichever exists). Append changelog entry to CHANGELOG.md (create if missing).

4. **Commit & tag**:
```bash
git add -A
git commit -m "chore: release v<new-version>"
git tag v<new-version>
```

5. **Push** — Ask before pushing:
```bash
git push && git push --tags
```

Stop before each irreversible step and confirm with the user.
