# Semantic Versioning Guide

Versions should follow the format `MAJOR.MINOR.PATCH` (e.g., `1.4.2`).

## Decision Tree for Bumps

Analyze the commits since the last tag to determine the bump type.

### 1. MAJOR Bump (`X.0.0`)
**Condition**: There is at least one `BREAKING CHANGE:` in the commit footers, or a commit type has an exclamation mark (`feat!:`, `refactor!:`).
**Meaning**: Incompatible API changes. Downstream consumers will need to update their code.

### 2. MINOR Bump (`0.X.0`)
**Condition**: There is at least one `feat:` commit, but no breaking changes.
**Meaning**: New functionality added in a backwards-compatible manner.

### 3. PATCH Bump (`0.0.X`)
**Condition**: There are only `fix:`, `refactor:`, `perf:`, or `docs:` commits.
**Meaning**: Backwards-compatible bug fixes or minor internal improvements.

## Pre-releases (Optional)
If the user requests a pre-release, append the pre-release identifier (e.g., `-alpha.1`, `-beta.2`, `-rc.1`).
Example: `1.5.0-rc.1`
